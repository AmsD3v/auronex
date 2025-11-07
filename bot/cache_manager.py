"""
Cache Manager - Gerenciador de Cache Inteligente
Reduz requisições para exchanges em 70%
"""
from datetime import datetime
from typing import Dict, Tuple, Optional

class CacheManager:
    """
    Cache com TTL (Time To Live)
    Ideal para dados que mudam rapidamente mas não a cada segundo
    """
    
    def __init__(self, ttl_seconds=30):
        self.cache: Dict[str, Tuple] = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[any]:
        """Buscar do cache"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            
            # Verificar se expirou
            age = (datetime.now() - timestamp).total_seconds()
            if age < self.ttl:
                return data  # ✅ Cache hit!
            else:
                # Expirou
                del self.cache[key]
        
        return None  # Cache miss
    
    def set(self, key: str, data: any):
        """Salvar no cache"""
        self.cache[key] = (data, datetime.now())
    
    def clear_old(self):
        """Limpar itens expirados"""
        now = datetime.now()
        expired = [
            k for k, (_, ts) in self.cache.items()
            if (now - ts).total_seconds() >= self.ttl
        ]
        
        for k in expired:
            del self.cache[k]
        
        return len(expired)
    
    def clear_all(self):
        """Limpar todo cache"""
        count = len(self.cache)
        self.cache.clear()
        return count

