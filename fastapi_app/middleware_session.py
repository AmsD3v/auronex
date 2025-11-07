"""
Middleware de Sessão Única
Garante que usuário só tenha 1 sessão ativa por vez
CRÍTICO para evitar múltiplos bots rodando!
"""
import time
from typing import Dict

# Cache de sessões ativas {user_id: {"token": str, "timestamp": float}}
active_sessions: Dict[int, dict] = {}

def register_session(user_id: int, token: str):
    """
    Registra nova sessão e INVALIDA sessão anterior
    """
    # Se já tem sessão ativa, invalidar
    if user_id in active_sessions:
        old_token = active_sessions[user_id].get('token')
        print(f"[SESSION] Usuário {user_id}: Invalidando sessão anterior")
        print(f"[SESSION] Token antigo: {old_token[:20]}...")
    
    # Registrar nova sessão
    active_sessions[user_id] = {
        'token': token,
        'timestamp': time.time(),
        'active': True
    }
    
    print(f"[SESSION] Usuário {user_id}: Nova sessão registrada")
    print(f"[SESSION] Sessões ativas: {len(active_sessions)}")

def is_session_valid(user_id: int, token: str) -> bool:
    """
    Verifica se sessão é válida (é a mais recente)
    """
    if user_id not in active_sessions:
        return False
    
    session = active_sessions[user_id]
    
    # Verificar se é o token mais recente
    if session['token'] != token:
        print(f"[SESSION] Usuário {user_id}: Token inválido (sessão antiga)")
        return False
    
    # Verificar timeout (6 horas)
    age = time.time() - session['timestamp']
    if age > 21600:  # 6 horas
        print(f"[SESSION] Usuário {user_id}: Sessão expirada")
        del active_sessions[user_id]
        return False
    
    return True

def invalidate_session(user_id: int):
    """
    Invalida sessão do usuário (logout)
    """
    if user_id in active_sessions:
        del active_sessions[user_id]
        print(f"[SESSION] Usuário {user_id}: Sessão invalidada (logout)")

def get_active_sessions_count() -> int:
    """
    Retorna número de sessões ativas
    """
    return len(active_sessions)

