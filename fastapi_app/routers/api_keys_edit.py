"""
Endpoint para editar API Keys
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, ExchangeAPIKey
from ..auth import get_current_user

router = APIRouter(prefix="/api/api-keys", tags=["api-keys-edit"])

@router.patch("/{key_id}/toggle-testnet")
def toggle_testnet(
    key_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Alternar entre testnet e produção"""
    
    # Buscar API Key
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.id == key_id,
        ExchangeAPIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key não encontrada")
    
    # Atualizar
    api_key.is_testnet = data.get("is_testnet", False)
    db.commit()
    
    print(f"✅ API Key {key_id} atualizada: Testnet={api_key.is_testnet}")
    
    return {"success": True, "is_testnet": api_key.is_testnet}


