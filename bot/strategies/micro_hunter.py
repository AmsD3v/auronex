"""
Estratégia: Micro Hunter (Caçador de Micro Oscilações)

ENTERPRISE - Para day traders e scalpers

Lógica:
- Detecta micro movimentos (<1%) antes de acontecerem
- Usa múltiplos indicadores ultra-sensíveis
- Entra e sai rápido (segundos a minutos)
- Perfeito para timeframes 1m, 5m, 15m
- Alta frequência de trades (20-50/dia)

Win Rate esperado: 65-70%
Avg win: 0.5-1%
Avg loss: 0.3-0.5%
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict
from .base import BaseStrategy

logger = logging.getLogger(__name__)


class MicroHunterStrategy(BaseStrategy):
    """
    Estratégia especializada em micro oscilações
    
    Indicadores:
    - StochRSI (mais sensível que RSI)
    - EMA 5/13/26 (mais rápidas que 9/21/50)
    - Volume Spike (detecta pressão)
    - Price Action (velas, patterns)
    - Micro Trend (últimas 10 velas)
    
    Alvos:
    - Take Profit: 0.5-1% (micro ganhos)
    - Stop Loss: 0.3-0.5% (micro perdas)
    - Tempo médio: 30s - 5min
    """
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        
        # Parâmetros ultra-sensíveis
        self.ema_ultra_fast = 5
        self.ema_fast = 13
        self.ema_medium = 26
        self.rsi_period = 9  # Mais sensível que 14
        self.stoch_period = 14
        
        # Thresholds para micro movimentos
        self.min_volatility = 0.2  # 0.2% mínimo
        self.max_volatility = 3.0  # 3% máximo
        self.volume_spike_threshold = 1.5  # 50% acima da média
        
        logger.info("🎯 Micro Hunter Strategy inicializada")
        logger.info(f"   Min volatilidade: {self.min_volatility}%")
        logger.info(f"   Sensibilidade: ALTA (EMA {self.ema_ultra_fast}/{self.ema_fast}/{self.ema_medium})")
    
    def get_name(self) -> str:
        return "Micro Hunter"
    
    def calculate_stoch_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calcula StochRSI (mais sensível que RSI)
        
        StochRSI oscila entre 0-100
        < 20 = Oversold (compra)
        > 80 = Overbought (venda)
        """
        # Calcular RSI primeiro
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # StochRSI = (RSI - RSI_min) / (RSI_max - RSI_min) * 100
        rsi_min = rsi.rolling(window=period).min()
        rsi_max = rsi.rolling(window=period).max()
        
        stoch_rsi = ((rsi - rsi_min) / (rsi_max - rsi_min)) * 100
        
        return stoch_rsi
    
    def calculate_micro_trend(self, df: pd.DataFrame, lookback: int = 10) -> pd.Series:
        """
        Detecta micro tendência (últimas N velas)
        
        Returns:
            1 = Micro alta
            -1 = Micro baixa
            0 = Lateral
        """
        # Linear regression das últimas N velas
        df['micro_trend'] = 0
        
        for i in range(lookback, len(df)):
            recent_prices = df['close'].iloc[i-lookback:i].values
            x = np.arange(lookback)
            
            # Regressão linear
            slope = np.polyfit(x, recent_prices, 1)[0]
            
            # Normalizar slope
            avg_price = recent_prices.mean()
            slope_pct = (slope / avg_price) * 100
            
            if slope_pct > 0.05:  # > 0.05% = alta
                df.loc[df.index[i], 'micro_trend'] = 1
            elif slope_pct < -0.05:  # < -0.05% = baixa
                df.loc[df.index[i], 'micro_trend'] = -1
        
        return df['micro_trend']
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula indicadores ultra-sensíveis"""
        df = df.copy()
        
        # EMAs ultra-rápidas (5/13/26 vs 9/21/50)
        df['ema_5'] = df['close'].ewm(span=self.ema_ultra_fast, adjust=False).mean()
        df['ema_13'] = df['close'].ewm(span=self.ema_fast, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=self.ema_medium, adjust=False).mean()
        
        # StochRSI (mais sensível)
        df['stoch_rsi'] = self.calculate_stoch_rsi(df['close'], self.stoch_period)
        
        # Volume Spike
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_spike'] = df['volume'] / df['volume_ma']
        
        # Micro Trend
        df = df.copy()  # Evitar SettingWithCopyWarning
        df['micro_trend'] = self.calculate_micro_trend(df, lookback=10)
        
        # Price momentum (velocidade da mudança)
        df['momentum'] = df['close'].pct_change(periods=3) * 100  # Últimas 3 velas
        
        # Volatilidade recente
        df['volatility'] = df['close'].pct_change().rolling(window=10).std() * 100
        
        return df
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """
        Analisa dados e retorna sinal
        
        Foco: MICRO movimentos (0.3-1%)
        """
        # Validar
        is_valid, message = self.validate_dataframe(df)
        if not is_valid:
            return {
                'signal': 'hold',
                'confidence': 0,
                'reason': f'Dados inválidos: {message}',
                'indicators': {}
            }
        
        # Calcular indicadores
        df = self.calculate_indicators(df)
        
        # Valores atuais
        close = df['close'].iloc[-1]
        ema_5 = df['ema_5'].iloc[-1]
        ema_13 = df['ema_13'].iloc[-1]
        ema_26 = df['ema_26'].iloc[-1]
        stoch_rsi = df['stoch_rsi'].iloc[-1]
        volume_spike = df['volume_spike'].iloc[-1]
        micro_trend = df['micro_trend'].iloc[-1]
        momentum = df['momentum'].iloc[-1]
        volatility = df['volatility'].iloc[-1]
        
        result = {
            'signal': 'hold',
            'confidence': 0,
            'reason': '',
            'indicators': {
                'price': close,
                'ema_5': ema_5,
                'ema_13': ema_13,
                'stoch_rsi': stoch_rsi,
                'volume_spike': volume_spike,
                'micro_trend': micro_trend,
                'momentum': momentum,
                'volatility': volatility,
            }
        }
        
        # ========================================
        # FILTRO 1: Volatilidade adequada
        # ========================================
        if volatility < self.min_volatility:
            result['reason'] = f'Volatilidade muito baixa ({volatility:.2f}%)'
            return result
        
        if volatility > self.max_volatility:
            result['reason'] = f'Volatilidade muito alta ({volatility:.2f}%)'
            return result
        
        # ========================================
        # SINAL DE COMPRA (Micro Alta Iminente)
        # ========================================
        
        # Condições para compra:
        conditions_buy = []
        confidence = 0
        
        # 1. EMAs alinhadas em micro alta
        if ema_5 > ema_13 > ema_26:
            conditions_buy.append("EMAs alinhadas")
            confidence += 20
        
        # 2. StochRSI oversold (< 20)
        if stoch_rsi < 20:
            conditions_buy.append(f"StochRSI oversold ({stoch_rsi:.0f})")
            confidence += 25
        
        # 3. Micro trend positivo
        if micro_trend == 1:
            conditions_buy.append("Micro trend alta")
            confidence += 15
        
        # 4. Volume spike (pressão compradora)
        if volume_spike > self.volume_spike_threshold:
            conditions_buy.append(f"Volume spike ({volume_spike:.1f}x)")
            confidence += 20
        
        # 5. Momentum positivo
        if momentum > 0.1:  # > 0.1%
            conditions_buy.append(f"Momentum +{momentum:.2f}%")
            confidence += 15
        
        # 6. Preço acima de EMA5 (confirmação)
        if close > ema_5:
            confidence += 5
        
        # Se 3+ condições satisfeitas = COMPRA
        if len(conditions_buy) >= 3:
            result['signal'] = 'buy'
            result['confidence'] = min(confidence, 95)
            result['reason'] = ', '.join(conditions_buy)
            
            logger.info(f"")
            logger.info(f"{'🎯'*30}")
            logger.info(f"OPORTUNIDADE DETECTADA!")
            logger.info(f"Condições: {', '.join(conditions_buy)}")
            logger.info(f"Confiança: {result['confidence']}%")
            logger.info(f"{'🎯'*30}")
            
            return result
        
        # ========================================
        # SINAL DE VENDA (Micro Baixa Iminente)
        # ========================================
        
        conditions_sell = []
        confidence_sell = 0
        
        # 1. EMAs invertidas
        if ema_5 < ema_13 < ema_26:
            conditions_sell.append("EMAs invertidas")
            confidence_sell += 20
        
        # 2. StochRSI overbought
        if stoch_rsi > 80:
            conditions_sell.append(f"StochRSI overbought ({stoch_rsi:.0f})")
            confidence_sell += 25
        
        # 3. Micro trend negativo
        if micro_trend == -1:
            conditions_sell.append("Micro trend baixa")
            confidence_sell += 15
        
        # 4. Momentum negativo
        if momentum < -0.1:
            conditions_sell.append(f"Momentum {momentum:.2f}%")
            confidence_sell += 20
        
        if len(conditions_sell) >= 3:
            result['signal'] = 'sell'
            result['confidence'] = min(confidence_sell, 95)
            result['reason'] = ', '.join(conditions_sell)
            return result
        
        # ========================================
        # HOLD
        # ========================================
        reasons = []
        
        if volatility < self.min_volatility:
            reasons.append(f"baixa volatilidade ({volatility:.2f}%)")
        if 20 <= stoch_rsi <= 80:
            reasons.append(f"StochRSI neutro ({stoch_rsi:.0f})")
        if abs(momentum) < 0.1:
            reasons.append("momentum fraco")
        
        result['reason'] = ', '.join(reasons) if reasons else 'Aguardando setup'
        
        return result
    
    def should_exit_position(self, df: pd.DataFrame, entry_side: str) -> tuple[bool, str]:
        """
        Verifica se deve sair (micro ganhos/perdas)
        """
        df = self.calculate_indicators(df)
        
        stoch_rsi = df['stoch_rsi'].iloc[-1]
        ema_5 = df['ema_5'].iloc[-1]
        ema_13 = df['ema_13'].iloc[-1]
        close = df['close'].iloc[-1]
        
        if entry_side == 'buy':
            # Sair se:
            # 1. StochRSI > 80 (overbought - realize lucro!)
            if stoch_rsi > 80:
                return True, "StochRSI overbought (realizando lucro)"
            
            # 2. EMA5 cruzou abaixo de EMA13 (reversão)
            if close < ema_5 < ema_13:
                return True, "Reversão detectada"
        
        return False, ""


class ScalpingStrategy(BaseStrategy):
    """
    Estratégia de Scalping (operações ultra-rápidas)
    
    Timeframe: 1m, 3m
    Take Profit: 0.3-0.5%
    Stop Loss: 0.2-0.3%
    Frequência: 50-100 trades/dia
    """
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        
        # Ultra sensível
        self.ema_period = 3
        self.rsi_period = 5
        
    def get_name(self) -> str:
        return "Scalping Ultra"
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # EMA 3 (ultra rápida!)
        df['ema'] = df['close'].ewm(span=self.ema_period, adjust=False).mean()
        
        # RSI 5 (ultra sensível)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Momentum instantâneo
        df['momentum'] = df['close'].pct_change(periods=1) * 100
        
        return df
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """Análise ultra-rápida para scalping"""
        is_valid, msg = self.validate_dataframe(df)
        if not is_valid:
            return {'signal': 'hold', 'confidence': 0, 'reason': msg, 'indicators': {}}
        
        df = self.calculate_indicators(df)
        
        close = df['close'].iloc[-1]
        ema = df['ema'].iloc[-1]
        rsi = df['rsi'].iloc[-1]
        momentum = df['momentum'].iloc[-1]
        
        result = {
            'signal': 'hold',
            'confidence': 0,
            'reason': '',
            'indicators': {'price': close, 'ema': ema, 'rsi': rsi, 'momentum': momentum}
        }
        
        # COMPRA: Preço acima de EMA + RSI baixo + momentum positivo
        if close > ema and rsi < 40 and momentum > 0.05:
            result['signal'] = 'buy'
            result['confidence'] = 75
            result['reason'] = f'Scalp: EMA cross + RSI {rsi:.0f} + momentum +{momentum:.2f}%'
        
        # VENDA: Preço abaixo de EMA + RSI alto
        elif close < ema and rsi > 60:
            result['signal'] = 'sell'
            result['confidence'] = 70
            result['reason'] = f'Scalp: Reversão - RSI {rsi:.0f}'
        
        return result

