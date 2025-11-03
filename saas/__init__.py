# RoboTrader SaaS

# Importar Celery app para que seja descoberto pelo worker
from .celery_config import app as celery_app

__all__ = ('celery_app',)
