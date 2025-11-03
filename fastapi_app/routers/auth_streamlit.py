"""
Endpoint de autenticação simplificado para Streamlit
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models import User
from ..auth import verify_password, create_access_token

router = APIRouter(prefix="/api/streamlit", tags=["streamlit-auth"])

class StreamlitLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def streamlit_login(credentials: StreamlitLogin, db: Session = Depends(get_db)):
    """Login simplificado para Streamlit"""
    
    print(f"🔍 Tentativa de login: {credentials.email}")
    
    # Buscar usuário
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        print(f"❌ Usuário não encontrado: {credentials.email}")
        raise HTTPException(status_code=401, detail="Email não encontrado")
    
    print(f"✅ Usuário encontrado: {user.first_name} {user.last_name}")
    
    # Verificar senha
    senha_ok = verify_password(credentials.password, user.password)
    print(f"🔑 Senha válida: {senha_ok}")
    
    if not senha_ok:
        print(f"❌ Senha incorreta para {credentials.email}")
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    # Criar token
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    
    print(f"✅ Login bem-sucedido: {user.email}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }




