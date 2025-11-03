"""
Criptografia para API Keys - Compatível com Django
"""

from cryptography.fernet import Fernet
import base64

# Mesma chave do Django (ou configure via env)
ENCRYPTION_KEY = "dev-encryption-key-change-in-production"

# Criar Fernet key (32 bytes base64)
key = base64.urlsafe_b64encode(ENCRYPTION_KEY.encode().ljust(32)[:32])
fernet = Fernet(key)

def encrypt_data(data: str) -> str:
    """Criptografar dados"""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Descriptografar dados"""
    return fernet.decrypt(encrypted_data.encode()).decode()


