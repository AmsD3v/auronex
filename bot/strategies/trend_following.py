"""
Estratégia: Trend Following (Seguir Tendência)

Lógica:
- Usa médias móveis exponenciais (EMA 9, 21, 50)
- Compra quando todas as EMAs estão alinhadas em alta
- Vende quando todas as EMAs estão alinhadas em baixa
- Usa RSI para confirmar e evitar sobrecompra/sobrevenda
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict
from .base import BaseStrategy
from config.settings import Settings

logger = logging.getLogger(__name__)


class TrendFollowingStrategy(BaseStrategy):
    """
    Estratégia de seguir tendência usando EMAs e RSI
    
    Sinais de Compra:
    - EMA9 > EMA21 > EMA50 (tendência de alta)
    - Preço acima de todas as EMAs
    - RSI entre 40 e 70 (não sobrecomprado)
    
    Sinais de Venda:
    - EMA9 < EMA21 < EMA50 (tendência de baixa)
    - Preço abaixo de todas as EMAs
    - RSI entre 30 e 60 (não sobrevendido)
    """
    
    def __init__(self, config: Dict = None):
        """Inicializa a estratégia"""
        super().__init__(config)
        self.settings = Settings()
        
        # Parâmetros configuráveis
        self.ema_fast = self.config.get('ema_fast', self.settings.EMA_FAST)
        self.ema_medium = self.config.get('ema_medium', self.settings.EMA_MEDIUM)
        self.ema_slow = self.config.get('ema_slow', self.settings.EMA_SLOW)
        self.rsi_period = self.config.get('rsi_period', self.settings.RSI_PERIOD)
    
    def get_name(self) -> str:
        """Retorna o nome da estratégia"""
        return "Trend Following"
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula os indicadores necessários
        
        Args:
            df: DataFrame com dados OHLCV
        
        Returns:
            DataFrame com indicadores adicionados
        """
        df = df.copy()
        
        # Médias Móveis Exponenciais
        df['ema_9'] = df['close'].ewm(span=self.ema_fast, adjust=False).mean()
        df['ema_21'] = df['close'].ewm(span=self.ema_medium, adjust=False).mean()
        df['ema_50'] = df['close'].ewm(span=self.ema_slow, adjust=False).mean()
        
        # RSI (Relative Strength Index)
        df['rsi'] = self.calculate_rsi(df['close'], self.rsi_period)
        
        # Tendência (1 = alta, -1 = baixa, 0 = lateral)
        df['trend'] = 0
        df.loc[(df['ema_9'] > df['ema_21']) & (df['ema_21'] > df['ema_50']), 'trend'] = 1
        df.loc[(df['ema_9'] < df['ema_21']) & (df['ema_21'] < df['ema_50']), 'trend'] = -1
        
        # Força da tendência (distância entre EMAs)
        df['trend_strength'] = abs(df['ema_9'] - df['ema_50']) / df['close'] * 100
        
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
        ema_9 = df['ema_9'].iloc[-1]
        ema_21 = df['ema_21'].iloc[-1]
        ema_50 = df['ema_50'].iloc[-1]
        rsi = df['rsi'].iloc[-1]
        trend = df['trend'].iloc[-1]
        trend_strength = df['trend_strength'].iloc[-1]
        
        # Inicializar resultado
        result = {
            'signal': 'hold',
            'confidence': 0,
            'reason': '',
            'indicators': {
                'price': current_price,
                'ema_9': ema_9,
                'ema_21': ema_21,
                'ema_50': ema_50,
                'rsi': rsi,
                'trend': trend,
                'trend_strength': trend_strength,
            }
        }
        
        # ===== SINAL DE COMPRA =====
        if trend == 1:  # Tendência de alta
            # Verificar se preço está acima das EMAs
            price_above_emas = current_price > ema_9 and current_price > ema_21
            
            # RSI não sobrecomprado
            rsi_ok = 40 < rsi < 70
            
            # Força da tendência boa
            strong_trend = trend_strength > 0.5
            
            if price_above_emas and rsi_ok:
                confidence = 50
                
                # Aumentar confiança com base nos fatores
                if strong_trend:
                    confidence += 20
                if rsi < 60:  # RSI mais baixo = melhor entrada
                    confidence += 15
                if current_price > ema_50:  # Preço bem acima da EMA lenta
                    confidence += 15
                
                result['signal'] = 'buy'
                result['confidence'] = min(confidence, 95)
                result['reason'] = f'Tendência de alta confirmada, RSI em {rsi:.1f}'
        
        # ===== SINAL DE VENDA =====
        elif trend == -1:  # Tendência de baixa
            # Verificar se preço está abaixo das EMAs
            price_below_emas = current_price < ema_9 and current_price < ema_21
            
            # RSI não sobrevendido
            rsi_ok = 30 < rsi < 60
            
            # Força da tendência boa
            strong_trend = trend_strength > 0.5
            
            if price_below_emas and rsi_ok:
                confidence = 50
                
                # Aumentar confiança com base nos fatores
                if strong_trend:
                    confidence += 20
                if rsi > 40:  # RSI mais alto = melhor entrada para venda
                    confidence += 15
                if current_price < ema_50:  # Preço bem abaixo da EMA lenta
                    confidence += 15
                
                result['signal'] = 'sell'
                result['confidence'] = min(confidence, 95)
                result['reason'] = f'Tendência de baixa confirmada, RSI em {rsi:.1f}'
        
        # ===== SINAL DE HOLD (AGUARDAR) =====
        else:
            reasons = []
            
            if trend == 0:
                reasons.append("mercado lateral")
            if rsi > 70:
                reasons.append("RSI sobrecomprado")
            elif rsi < 30:
                reasons.append("RSI sobrevendido")
            if trend_strength < 0.5:
                reasons.append("tendência fraca")
            
            result['signal'] = 'hold'
            result['confidence'] = 0
            result['reason'] = ', '.join(reasons) if reasons else 'Aguardando melhor oportunidade'
        
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
        ema_9 = df['ema_9'].iloc[-1]
        ema_21 = df['ema_21'].iloc[-1]
        trend = df['trend'].iloc[-1]
        rsi = df['rsi'].iloc[-1]
        
        if entry_side == 'buy':
            # Sair de posição comprada se:
            # 1. Tendência virou para baixa
            if trend == -1:
                return True, "Tendência reverteu para baixa"
            
            # 2. Preço cruzou abaixo da EMA rápida
            if current_price < ema_9:
                return True, "Preço cruzou abaixo da EMA9"
            
            # 3. RSI sobrecomprado
            if rsi > 75:
                return True, "RSI sobrecomprado (>75)"
        
        elif entry_side == 'sell':
            # Sair de posição vendida se:
            # 1. Tendência virou para alta
            if trend == 1:
                return True, "Tendência reverteu para alta"
            
            # 2. Preço cruzou acima da EMA rápida
            if current_price > ema_9:
                return True, "Preço cruzou acima da EMA9"
            
            # 3. RSI sobrevendido
            if rsi < 25:
                return True, "RSI sobrevendido (<25)"
        
        return False, ""

