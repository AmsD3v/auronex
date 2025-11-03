"""
Estratégia: Mean Reversion (Reversão à Média)

Lógica:
- Usa Bandas de Bollinger e RSI
- Compra quando preço está muito abaixo da média (sobrevendido)
- Vende quando preço está muito acima da média (sobrecomprado)
- Funciona melhor em mercados laterais
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict
from .base import BaseStrategy
from config.settings import Settings

logger = logging.getLogger(__name__)


class MeanReversionStrategy(BaseStrategy):
    """
    Estratégia de reversão à média usando Bandas de Bollinger e RSI
    
    Sinais de Compra:
    - Preço tocou ou cruzou a banda inferior de Bollinger
    - RSI < 30 (sobrevendido)
    - Volume acima da média (confirmação)
    
    Sinais de Venda:
    - Preço tocou ou cruzou a banda superior de Bollinger
    - RSI > 70 (sobrecomprado)
    - Volume acima da média (confirmação)
    """
    
    def __init__(self, config: Dict = None):
        """Inicializa a estratégia"""
        super().__init__(config)
        self.settings = Settings()
        
        # Parâmetros configuráveis
        self.bb_period = self.config.get('bb_period', self.settings.BOLLINGER_PERIOD)
        self.bb_std = self.config.get('bb_std', self.settings.BOLLINGER_STD)
        self.rsi_period = self.config.get('rsi_period', self.settings.RSI_PERIOD)
        self.rsi_oversold = self.config.get('rsi_oversold', self.settings.RSI_OVERSOLD)
        self.rsi_overbought = self.config.get('rsi_overbought', self.settings.RSI_OVERBOUGHT)
    
    def get_name(self) -> str:
        """Retorna o nome da estratégia"""
        return "Mean Reversion"
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula os indicadores necessários
        
        Args:
            df: DataFrame com dados OHLCV
        
        Returns:
            DataFrame com indicadores adicionados
        """
        df = df.copy()
        
        # Bandas de Bollinger
        df['bb_middle'] = df['close'].rolling(window=self.bb_period).mean()
        bb_std = df['close'].rolling(window=self.bb_period).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * self.bb_std)
        df['bb_lower'] = df['bb_middle'] - (bb_std * self.bb_std)
        
        # Posição do preço nas Bandas (%B)
        # %B = 0 significa preço na banda inferior
        # %B = 1 significa preço na banda superior
        df['bb_percent'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # RSI (Relative Strength Index)
        df['rsi'] = self.calculate_rsi(df['close'], self.rsi_period)
        
        # Volume médio
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # Distância do preço até a média (em %)
        df['distance_from_mean'] = ((df['close'] - df['bb_middle']) / df['bb_middle']) * 100
        
        return df
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calcula o RSI (Relative Strength Index)
        
        Args:
            prices: Serie de preços
            period: Período do RSI
        
        Returns:
            Serie com valores de RSI
        """
        delta = prices.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """
        Analisa os dados e retorna sinal de trading
        
        Args:
            df: DataFrame com dados OHLCV
        
        Returns:
            Dicionário com sinal e detalhes
        """
        # Validar dados
        is_valid, message = self.validate_dataframe(df)
        if not is_valid:
            logger.error(f"Dados inválidos: {message}")
            return {
                'signal': 'hold',
                'confidence': 0,
                'reason': f'Dados inválidos: {message}',
                'indicators': {}
            }
        
        # Calcular indicadores
        df = self.calculate_indicators(df)
        
        # Obter valores mais recentes
        current_price = df['close'].iloc[-1]
        bb_upper = df['bb_upper'].iloc[-1]
        bb_middle = df['bb_middle'].iloc[-1]
        bb_lower = df['bb_lower'].iloc[-1]
        bb_percent = df['bb_percent'].iloc[-1]
        rsi = df['rsi'].iloc[-1]
        volume_ratio = df['volume_ratio'].iloc[-1]
        distance_from_mean = df['distance_from_mean'].iloc[-1]
        
        # Inicializar resultado
        result = {
            'signal': 'hold',
            'confidence': 0,
            'reason': '',
            'indicators': {
                'price': current_price,
                'bb_upper': bb_upper,
                'bb_middle': bb_middle,
                'bb_lower': bb_lower,
                'bb_percent': bb_percent,
                'rsi': rsi,
                'volume_ratio': volume_ratio,
                'distance_from_mean': distance_from_mean,
            }
        }
        
        # ===== SINAL DE COMPRA (Sobrevendido) =====
        # Preço perto ou abaixo da banda inferior
        near_lower_band = bb_percent < 0.2  # Menos de 20% entre bandas
        
        # RSI sobrevendido
        rsi_oversold = rsi < self.rsi_oversold
        
        # Volume confirmando
        volume_ok = volume_ratio > 0.8
        
        if near_lower_band and rsi_oversold:
            confidence = 60
            
            # Ajustar confiança
            if bb_percent < 0:  # Preço abaixo da banda inferior
                confidence += 20
            if rsi < 25:  # Muito sobrevendido
                confidence += 10
            if volume_ratio > 1.2:  # Volume alto
                confidence += 10
            
            result['signal'] = 'buy'
            result['confidence'] = min(confidence, 95)
            result['reason'] = f'Sobrevendido: RSI {rsi:.1f}, preço {distance_from_mean:+.2f}% da média'
        
        # ===== SINAL DE VENDA (Sobrecomprado) =====
        # Preço perto ou acima da banda superior
        near_upper_band = bb_percent > 0.8  # Mais de 80% entre bandas
        
        # RSI sobrecomprado
        rsi_overbought = rsi > self.rsi_overbought
        
        if near_upper_band and rsi_overbought:
            confidence = 60
            
            # Ajustar confiança
            if bb_percent > 1:  # Preço acima da banda superior
                confidence += 20
            if rsi > 75:  # Muito sobrecomprado
                confidence += 10
            if volume_ratio > 1.2:  # Volume alto
                confidence += 10
            
            result['signal'] = 'sell'
            result['confidence'] = min(confidence, 95)
            result['reason'] = f'Sobrecomprado: RSI {rsi:.1f}, preço {distance_from_mean:+.2f}% da média'
        
        # ===== SINAL DE HOLD (AGUARDAR) =====
        if result['signal'] == 'hold':
            reasons = []
            
            if 0.3 < bb_percent < 0.7:
                reasons.append("preço próximo à média")
            if self.rsi_oversold <= rsi <= self.rsi_overbought:
                reasons.append(f"RSI neutro ({rsi:.1f})")
            if volume_ratio < 0.8:
                reasons.append("volume baixo")
            
            result['reason'] = ', '.join(reasons) if reasons else 'Aguardando extremos'
        
        # Log da análise
        self.log_analysis(result)
        
        return result
    
    def should_exit_position(self, df: pd.DataFrame, entry_side: str) -> tuple[bool, str]:
        """
        Verifica se deve sair de uma posição aberta
        
        Args:
            df: DataFrame com dados atualizados
            entry_side: 'buy' ou 'sell' (lado da entrada)
        
        Returns:
            (deve_sair, motivo)
        """
        df = self.calculate_indicators(df)
        
        current_price = df['close'].iloc[-1]
        bb_middle = df['bb_middle'].iloc[-1]
        bb_percent = df['bb_percent'].iloc[-1]
        rsi = df['rsi'].iloc[-1]
        
        if entry_side == 'buy':
            # Sair de posição comprada se:
            # 1. Preço voltou à média ou acima
            if bb_percent > 0.5:
                return True, "Preço voltou à média"
            
            # 2. RSI saiu da zona de sobrevenda
            if rsi > 55:
                return True, "RSI normalizou"
            
            # 3. Preço atingiu banda superior (máximo ganho)
            if bb_percent > 0.9:
                return True, "Atingiu banda superior"
        
        elif entry_side == 'sell':
            # Sair de posição vendida se:
            # 1. Preço voltou à média ou abaixo
            if bb_percent < 0.5:
                return True, "Preço voltou à média"
            
            # 2. RSI saiu da zona de sobrecompra
            if rsi < 45:
                return True, "RSI normalizou"
            
            # 3. Preço atingiu banda inferior (máximo ganho)
            if bb_percent < 0.1:
                return True, "Atingiu banda inferior"
        
        return False, ""
    
    def is_market_suitable(self, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Verifica se o mercado está adequado para estratégia de reversão à média
        
        Args:
            df: DataFrame com dados
        
        Returns:
            (adequado, motivo)
        """
        df = self.calculate_indicators(df)
        
        # Calcular volatilidade (largura das bandas)
        bb_width = ((df['bb_upper'] - df['bb_lower']) / df['bb_middle']).iloc[-20:].mean()
        
        # Calcular se está em tendência forte
        # (preço consistentemente acima ou abaixo da média)
        prices_above_mean = (df['close'] > df['bb_middle']).iloc[-20:].sum()
        
        # Ideal para mean reversion:
        # - Volatilidade moderada (nem muito baixa, nem muito alta)
        # - Mercado lateral (preço cruza a média frequentemente)
        
        if bb_width < 0.02:
            return False, "Volatilidade muito baixa (mercado sem movimento)"
        
        if bb_width > 0.08:
            return False, "Volatilidade muito alta (mercado em tendência forte)"
        
        if prices_above_mean > 17 or prices_above_mean < 3:
            return False, "Mercado em tendência forte (não lateral)"
        
        return True, "Mercado adequado para reversão à média"

