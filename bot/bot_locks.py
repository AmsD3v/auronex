"""
Sistema de Locks para Bot Controller
Garante que APENAS 1 INSTÂNCIA de cada bot rode por vez
CRÍTICO: Evita trades duplicados!
"""
import time
from typing import Dict, Optional

# Locks ativos {bot_id: {"pid": int, "timestamp": float, "active": bool}}
bot_locks: Dict[int, dict] = {}

def acquire_bot_lock(bot_id: int) -> bool:
    """
    Tenta adquirir lock para iniciar bot
    
    Returns:
        True se conseguiu lock (pode iniciar)
        False se já tem outra instância rodando
    """
    import os
    
    # Se não tem lock, adquirir
    if bot_id not in bot_locks:
        bot_locks[bot_id] = {
            'pid': os.getpid(),
            'timestamp': time.time(),
            'active': True
        }
        print(f"[LOCK] Bot {bot_id}: Lock adquirido (PID: {os.getpid()})")
        return True
    
    # Se já tem lock, verificar se ainda está ativo
    existing = bot_locks[bot_id]
    age = time.time() - existing['timestamp']
    
    # Se lock tem mais de 60s sem renovar = considerar morto
    if age > 60:
        print(f"[LOCK] Bot {bot_id}: Lock expirado (renovado há {age:.0f}s)")
        bot_locks[bot_id] = {
            'pid': os.getpid(),
            'timestamp': time.time(),
            'active': True
        }
        return True
    
    # Lock ainda ativo
    print(f"[LOCK] Bot {bot_id}: JÁ RODANDO (PID: {existing['pid']}) - BLOQUEADO!")
    return False

def renew_bot_lock(bot_id: int):
    """
    Renova lock (chamar a cada 20-30s)
    Mantém lock ativo
    """
    if bot_id in bot_locks:
        bot_locks[bot_id]['timestamp'] = time.time()

def release_bot_lock(bot_id: int):
    """
    Libera lock (ao parar bot)
    """
    if bot_id in bot_locks:
        del bot_locks[bot_id]
        print(f"[LOCK] Bot {bot_id}: Lock liberado")

def get_locked_bots() -> list:
    """
    Retorna lista de bots com lock ativo
    """
    return list(bot_locks.keys())

def force_clear_expired_locks():
    """
    Limpa locks expirados (sem renovação há 60s+)
    """
    now = time.time()
    expired = [
        bot_id for bot_id, lock in bot_locks.items()
        if (now - lock['timestamp']) > 60
    ]
    
    for bot_id in expired:
        print(f"[LOCK] Bot {bot_id}: Lock expirado - removendo")
        del bot_locks[bot_id]
    
    return len(expired)

