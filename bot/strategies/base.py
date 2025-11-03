"""
Classe base para estratégias de trading
Todas as estratégias devem herdar desta classe
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict
import pandas as pd

logger = logging.getLogger(__name__)


class BaseStrategy(ABC):
    """
    Classe abstrata base para estratégias de trading
    
    Todas as estratégias devem implementar:
    - analyze(): Analisa os dados e retorna sinal
    - get_name(): Retorna o nome da estratégia
    """
    
    def __init__(self, config: Dict = None):
        """
        Inicializa a estratégia
        
        Args:
            config: Dicionário com configurações específicas
        """
        self.config = config or {}
        self.last_signal = None
        self.last_analysis_time = None
    
    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> Dict:
        """
        Analisa os dados e retorna um sinal de trading
        
        Args:
            df: DataFrame com dados OHLCV
                Colunas esperadas: timestamp, open, high, low, close, volume
        
        Returns:
            {
                'signal': 'buy', 'sell' ou 'hold',
                'confidence': float (0-100),
                'reason': str,
                'indicators': dict com valores dos indicadores
            }
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome da estratégia"""
        pass
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula indicadores técnicos
        Pode ser sobrescrito por estratégias específicas
        
        Args:
            df: DataFrame com dados OHLCV
        
        Returns:
            DataFrame com indicadores adicionados
        """
        return df
    
    def validate_dataframe(self, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Valida se o DataFrame tem os dados necessários
        
        Args:
            df: DataFrame para validar
        
        Returns:
            (válido, mensagem)
        """
        if df is None or df.empty:
            return False, "DataFrame vazio"
        
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            return False, f"Colunas faltando: {', '.join(missing)}"
        
        if len(df) < 50:
            return False, f"Dados insuficientes: {len(df)} candles (mínimo: 50)"
        
        return True, "OK"
    
    def get_latest_values(self, df: pd.DataFrame, column: str, periods: int = 1):
        """
        Obtém os últimos N valores de uma coluna
        
        Args:
            df: DataFrame
            column: Nome da coluna
            periods: Número de períodos
        
        Returns:
            Valor único ou lista de valores
        """
        if column not in df.columns:
            logger.error(f"Coluna {column} não encontrada")
            return None
        
        if periods == 1:
            return df[column].iloc[-1]
        else:
            return df[column].iloc[-periods:].tolist()
    
    def is_bullish_trend(self, df: pd.DataFrame) -> bool:
        """
        Verifica se está em tendência de alta
        Implementação simples: preço acima da média móvel de 50
        
        Args:
            df: DataFrame com dados
        
        Returns:
            True se tendência de alta
        """
        if 'close' not in df.columns:
            return False
        
        # Calcular média móvel de 50 se não existir
        if 'sma_50' not in df.columns:
            df['sma_50'] = df['close'].rolling(window=50).mean()
        
        current_price = df['close'].iloc[-1]
        sma_50 = df['sma_50'].iloc[-1]
        
        return current_price > sma_50
    
    def is_bearish_trend(self, df: pd.DataFrame) -> bool:
        """
        Verifica se está em tendência de baixa
        
        Args:
            df: DataFrame com dados
        
        Returns:
            True se tendência de baixa
        """
        return not self.is_bullish_trend(df)
    
    def get_signal_summary(self, signal: Dict) -> str:
        """
        Retorna um resumo textual do sinal
        
        Args:
            signal: Dicionário com informações do sinal
        
        Returns:
            String formatada
        """
        signal_type = signal.get('signal', 'hold').upper()
        confidence = signal.get('confidence', 0)
        reason = signal.get('reason', 'N/A')
        
        emoji = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '⚪'
        }.get(signal_type, '⚪')
        
        return f"{emoji} {signal_type} (Confiança: {confidence:.1f}%) - {reason}"
    
    def log_analysis(self, signal: Dict):
        """
        Registra análise no log
        
        Args:
            signal: Dicionário com resultado da análise
        """
        summary = self.get_signal_summary(signal)
        logger.info(f"[{self.get_name()}] {summary}")
        
        # Log de indicadores (debug)
        if signal.get('indicators'):
            indicators_str = ", ".join([f"{k}: {v:.2f}" for k, v in signal['indicators'].items() if isinstance(v, (int, float))])
            logger.debug(f"Indicadores: {indicators_str}")

