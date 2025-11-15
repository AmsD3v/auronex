"""
Rate Limiting para FastAPI
Previne abuse e DDoS
"""

import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Tuple
from fastapi import Request, HTTPException, status
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter simples (em memória)
    
    Para produção com múltiplos workers, use Redis:
    pip install slowapi redis
    """
    
    def __init__(self):
        # {ip: deque([timestamp1, timestamp2, ...])}
        self.requests_by_ip = defaultdict(deque)
        
        # {user_id: deque([timestamp1, timestamp2, ...])}
        self.requests_by_user = defaultdict(deque)
        
        logger.info("✅ Rate Limiter inicializado (em memória)")
    
    def _clean_old_requests(self, queue: deque, window_seconds: int):
        """Remove requests antigas fora da janela de tempo"""
        now = time.time()
        cutoff = now - window_seconds
        
        while queue and queue[0] < cutoff:
            queue.popleft()
    
    def check_rate_limit_ip(
        self,
        ip: str,
        max_requests: int,
        window_seconds: int
    ) -> Tuple[bool, int]:
        """
        Verifica rate limit por IP
        
        Args:
            ip: Endereço IP
            max_requests: Máximo de requests permitidos
            window_seconds: Janela de tempo em segundos
        
        Returns:
            (permitido, requests_restantes)
        """
        queue = self.requests_by_ip[ip]
        
        # Limpar requests antigas
        self._clean_old_requests(queue, window_seconds)
        
        # Verificar limite
        if len(queue) >= max_requests:
            remaining = max_requests - len(queue)
            return False, remaining
        
        # Registrar novo request
        queue.append(time.time())
        
        remaining = max_requests - len(queue)
        return True, remaining
    
    def check_rate_limit_user(
        self,
        user_id: int,
        max_requests: int,
        window_seconds: int
    ) -> Tuple[bool, int]:
        """
        Verifica rate limit por usuário
        
        Args:
            user_id: ID do usuário
            max_requests: Máximo de requests permitidos
            window_seconds: Janela de tempo em segundos
        
        Returns:
            (permitido, requests_restantes)
        """
        queue = self.requests_by_user[user_id]
        
        # Limpar requests antigas
        self._clean_old_requests(queue, window_seconds)
        
        # Verificar limite
        if len(queue) >= max_requests:
            remaining = max_requests - len(queue)
            return False, remaining
        
        # Registrar novo request
        queue.append(time.time())
        
        remaining = max_requests - len(queue)
        return True, remaining

# Instância global
rate_limiter = RateLimiter()

def rate_limit_by_ip(max_requests: int = 60, window_seconds: int = 60):
    """
    Decorator para rate limiting por IP
    
    Uso:
        @rate_limit_by_ip(max_requests=10, window_seconds=60)
        @router.post("/login")
        async def login(...):
            pass
    
    Args:
        max_requests: Máximo de requests na janela
        window_seconds: Janela de tempo (segundos)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extrair request dos kwargs ou args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None:
                for key, value in kwargs.items():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if request:
                # Obter IP
                client_ip = request.client.host
                
                # Verificar rate limit
                allowed, remaining = rate_limiter.check_rate_limit_ip(
                    client_ip,
                    max_requests,
                    window_seconds
                )
                
                if not allowed:
                    logger.warning(f"⚠️  Rate limit excedido: {client_ip}")
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Muitas requisições. Tente novamente em {window_seconds} segundos.",
                        headers={"Retry-After": str(window_seconds)}
                    )
            
            # Executar função
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def rate_limit_by_user(max_requests: int = 100, window_seconds: int = 60):
    """
    Decorator para rate limiting por usuário autenticado
    
    Uso:
        @rate_limit_by_user(max_requests=50, window_seconds=60)
        @router.get("/bots")
        async def list_bots(current_user: User = Depends(get_current_user)):
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Procurar current_user nos kwargs
            current_user = kwargs.get('current_user')
            
            if current_user:
                # Verificar rate limit
                allowed, remaining = rate_limiter.check_rate_limit_user(
                    current_user.id,
                    max_requests,
                    window_seconds
                )
                
                if not allowed:
                    logger.warning(f"⚠️  Rate limit excedido: User {current_user.id}")
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Muitas requisições. Tente novamente em {window_seconds} segundos.",
                        headers={"Retry-After": str(window_seconds)}
                    )
            
            # Executar função
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# ========================================
# ALTERNATIVA: slowapi (Produção Recomendada)
# ========================================
# pip install slowapi redis
#
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
#
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
#
# @router.post("/login")
# @limiter.limit("5/minute")
# async def login(request: Request, ...):
#     pass

