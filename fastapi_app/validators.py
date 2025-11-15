"""
Validadores para FastAPI
Validações de dados e segurança
"""

import re
from typing import Tuple

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validar força da senha
    
    Requisitos:
    - Mínimo 8 caracteres
    - 1 letra maiúscula
    - 1 letra minúscula
    - 1 número
    - 1 caractere especial
    
    Args:
        password: Senha para validar
    
    Returns:
        (is_valid, message)
    """
    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"
    
    if len(password) > 128:
        return False, "Senha deve ter no máximo 128 caracteres"
    
    if not re.search(r"[A-Z]", password):
        return False, "Senha deve ter pelo menos 1 letra maiúscula"
    
    if not re.search(r"[a-z]", password):
        return False, "Senha deve ter pelo menos 1 letra minúscula"
    
    if not re.search(r"[0-9]", password):
        return False, "Senha deve ter pelo menos 1 número"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/;'`~]", password):
        return False, "Senha deve ter pelo menos 1 caractere especial (!@#$%^&* etc)"
    
    # Verificar senhas comuns (top 100 mais usadas)
    common_passwords = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "111111", "iloveyou", "master", "sunshine",
        "ashley", "bailey", "passw0rd", "shadow", "123123",
        "654321", "superman", "qazwsx", "michael", "football"
    ]
    
    if password.lower() in common_passwords:
        return False, "Senha muito comum. Escolha uma senha mais forte e única"
    
    # Verificar sequências simples
    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)", password.lower()):
        return False, "Senha contém sequência simples. Use combinação mais complexa"
    
    return True, "Senha forte"

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validar formato de email
    
    Args:
        email: Email para validar
    
    Returns:
        (is_valid, message)
    """
    if not email or len(email) < 3:
        return False, "Email inválido"
    
    # Regex simples para email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Formato de email inválido"
    
    # Verificar domínios temporários/descartáveis comuns
    temp_domains = [
        "tempmail.com", "guerrillamail.com", "10minutemail.com",
        "throwaway.email", "temp-mail.org", "fakeinbox.com"
    ]
    
    domain = email.split('@')[1].lower()
    if domain in temp_domains:
        return False, "Emails temporários não são permitidos"
    
    return True, "Email válido"

def validate_capital(capital: float, min_value: float = 2.0, max_value: float = 10000.0) -> Tuple[bool, str]:
    """
    Validar capital do bot
    
    Args:
        capital: Valor do capital
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
    
    Returns:
        (is_valid, message)
    """
    if capital < min_value:
        return False, f"Capital mínimo: ${min_value:.2f}"
    
    if capital > max_value:
        return False, f"Capital máximo: ${max_value:.2f}"
    
    return True, "Capital válido"

def sanitize_string(text: str, max_length: int = 255) -> str:
    """
    Sanitizar string para prevenir XSS/injection
    
    Args:
        text: Texto para sanitizar
        max_length: Tamanho máximo
    
    Returns:
        Texto sanitizado
    """
    if not text:
        return ""
    
    # Remover caracteres perigosos
    text = text.strip()
    
    # Limitar tamanho
    text = text[:max_length]
    
    # Remover tags HTML/SQL injection básicos
    dangerous_patterns = [
        r'<script.*?</script>',
        r'<.*?>',
        r'javascript:',
        r'on\w+\s*=',
        r'DROP\s+TABLE',
        r'DELETE\s+FROM',
        r'INSERT\s+INTO',
        r'UPDATE\s+\w+\s+SET'
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return text






