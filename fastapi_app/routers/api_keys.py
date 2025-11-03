"""
Router de API Keys - Gerenciamento de chaves de exchange
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import ExchangeAPIKey, User
from ..schemas import APIKeyCreate, APIKeyResponse
from ..auth import get_current_user
from ..utils.encryption import encrypt_data, decrypt_data

router = APIRouter(prefix="/api/api-keys", tags=["api-keys"])

@router.get("/")
def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar API Keys do usuário - SEM response_model (Streamlit compatível)"""
    
    keys = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id
    ).all()
    
    # Retornar dict manual (evita erro de serialização)
    result = []
    for key in keys:
        result.append({
            "id": key.id,
            "exchange": key.exchange,
            "is_testnet": key.is_testnet,
            "is_active": key.is_active,
            "created_at": key.created_at.isoformat() if key.created_at else None
        })
    
    print(f"✅ Listando {len(result)} API Keys do usuário {current_user.id}")
    
    return result

@router.post("/", response_model=APIKeyResponse)
def create_api_key(
    key_data: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adicionar nova API Key"""
    
    # Verificar se já existe para esta exchange
    existing = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id,
        ExchangeAPIKey.exchange == key_data.exchange
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Você já tem API Key para {key_data.exchange}. Delete a antiga primeiro."
        )
    
    # Criptografar keys
    api_key_encrypted = encrypt_data(key_data.api_key)
    secret_encrypted = encrypt_data(key_data.secret_key)
    
    # VALIDAR API Key na exchange (OPCIONAL - não bloqueia salvar)
    validation_status = "not_validated"
    validation_message = ""
    
    try:
        import ccxt
        
        # Conectar à exchange para validar
        exchange_class = getattr(ccxt, key_data.exchange.lower())
        exchange = exchange_class({
            'apiKey': key_data.api_key,
            'secret': key_data.secret_key,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}  # Forçar SPOT (não futures)
        })
        
        if key_data.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Tentar buscar saldo (valida credenciais)
        try:
            balance = exchange.fetch_balance()
            validation_status = "validated"
            validation_message = "API Key validada com sucesso!"
            print(f"✅ API Key validada: {key_data.exchange}")
        except Exception as e:
            validation_status = "failed"
            validation_message = f"Aviso: Não foi possível validar (pode funcionar mesmo assim). Erro: {str(e)[:150]}"
            print(f"⚠️ Validação falhou (mas salvando): {str(e)[:100]}")
    except Exception as e:
        validation_status = "error"
        validation_message = f"Aviso: Erro na validação. API Key salva mas verifique se funciona."
        print(f"⚠️ Erro ao validar (mas salvando): {str(e)[:100]}")
    
    # Criar registro
    api_key = ExchangeAPIKey(
        user_id=current_user.id,
        exchange=key_data.exchange.lower(),
        api_key_encrypted=api_key_encrypted,
        secret_key_encrypted=secret_encrypted,
        is_testnet=key_data.is_testnet,
        is_active=key_data.is_active
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    print(f"✅ API Key salva: {key_data.exchange} (Testnet: {key_data.is_testnet})")
    print(f"   Status validação: {validation_status}")
    
    # Retornar com info de validação
    response = {
        "id": api_key.id,
        "exchange": api_key.exchange,
        "is_testnet": api_key.is_testnet,
        "is_active": api_key.is_active,
        "created_at": api_key.created_at,
        "validation_status": validation_status,
        "validation_message": validation_message
    }
    
    return response

@router.delete("/{key_id}/")
def delete_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar API Key"""
    
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.id == key_id,
        ExchangeAPIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key não encontrada")
    
    db.delete(api_key)
    db.commit()
    
    return {"message": "API Key deletada com sucesso"}

@router.get("/{key_id}/decrypt/")
def get_decrypted_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter chaves descriptografadas (para usar no bot)"""
    
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.id == key_id,
        ExchangeAPIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key não encontrada")
    
    return {
        "api_key_decrypted": decrypt_data(api_key.api_key_encrypted),
        "secret_key_decrypted": decrypt_data(api_key.secret_key_encrypted)
    }


