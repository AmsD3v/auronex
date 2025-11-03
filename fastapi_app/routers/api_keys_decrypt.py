"""
Endpoint para descriptografar API Keys (apenas para Streamlit)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, ExchangeAPIKey
from ..auth import get_current_user
from ..utils.encryption import decrypt_data

router = APIRouter(prefix="/api/api-keys", tags=["api-keys-decrypt"])

@router.get("/{key_id}/decrypt")
def decrypt_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Descriptografar API Key para uso no Streamlit"""
    
    # Buscar API Key
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.id == key_id,
        ExchangeAPIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key não encontrada")
    
    # Descriptografar
    try:
        api_key_decrypted = decrypt_data(api_key.api_key_encrypted)
        secret_decrypted = decrypt_data(api_key.secret_key_encrypted)
        
        return {
            "id": api_key.id,
            "exchange": api_key.exchange,
            "api_key": api_key_decrypted,
            "secret": secret_decrypted,
            "is_testnet": api_key.is_testnet,
            "is_active": api_key.is_active
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao descriptografar: {str(e)}")


