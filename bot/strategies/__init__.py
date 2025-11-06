"""
Estratégias de Trading
"""

from .base import BaseStrategy
from .mean_reversion import MeanReversionStrategy
from .trend_following import TrendFollowingStrategy
from .micro_hunter import MicroHunterStrategy, ScalpingStrategy

__all__ = [
    'BaseStrategy',
    'MeanReversionStrategy',
    'TrendFollowingStrategy',
    'MicroHunterStrategy',
    'ScalpingStrategy',
]
