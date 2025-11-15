"""
Criptografia para API Keys - SEGURO com variável de ambiente
"""

from cryptography.fernet import Fernet
import base64
import os
import logging
from dotenv import load_dotenv

# ✅ CARREGAR .env PRIMEIRO!
load_dotenv()

logger = logging.getLogger(__name__)

# ✅ SEGURANÇA: Chave DEVE vir do .env
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# ⚠️ TEMPORÁRIO: Se não tiver no .env, usar a ANTIGA para compatibilidade
if not ENCRYPTION_KEY:
    logger.warning("⚠️ ENCRYPTION_KEY não no .env - usando chave antiga (TEMPORÁRIO)")
    ENCRYPTION_KEY = "dev-encryption-key-change-in-production"  # Chave antiga
else:
    logger.info("✅ ENCRYPTION_KEY carregada do .env")

# Processar chave
try:
    # Tentar formato Fernet nativo (44 chars base64)
    if len(ENCRYPTION_KEY) == 44 and ENCRYPTION_KEY.endswith('='):
        # Formato Fernet nativo (base64 de 32 bytes)
        key = ENCRYPTION_KEY.encode()
        logger.info(f"✅ Usando chave Fernet nativa (44 chars)")
    else:
        # Formato string (converter para base64)
        key = base64.urlsafe_b64encode(ENCRYPTION_KEY.encode().ljust(32)[:32])
        logger.info(f"✅ Usando chave string convertida ({len(ENCRYPTION_KEY)} chars)")
    
    fernet = Fernet(key)
    logger.info("✅ Sistema de criptografia inicializado com sucesso")
    
except Exception as e:
    logger.critical(f"❌ Erro ao inicializar criptografia: {e}")
    raise ValueError(f"ENCRYPTION_KEY inválida: {e}")

def encrypt_data(data: str) -> str:
    """
    Criptografar dados com Fernet (AES-128)
    
    Args:
        data: String para criptografar
    
    Returns:
        String base64 criptografada
    """
    try:
        return fernet.encrypt(data.encode()).decode()
    except Exception as e:
        logger.error(f"Erro ao criptografar: {e}")
        raise

def decrypt_data(encrypted_data: str) -> str:
    """
    Descriptografar dados
    
    Args:
        encrypted_data: String base64 criptografada
    
    Returns:
        String original
    """
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        logger.error(f"Erro ao descriptografar: {e}")
        raise ValueError("Dados corrompidos ou chave incorreta")


