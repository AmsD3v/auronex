"""
API para editar usuários no Admin
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User

router = APIRouter(prefix="/api/admin", tags=["admin-edit-user"])

@router.patch("/users/{user_id}/edit")
async def edit_user(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    """Editar informações do usuário (nome, email)"""
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Atualizar campos
        if 'first_name' in data:
            user.first_name = data['first_name']
        
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        if 'email' in data:
            # Verificar se email já existe
            existing = db.query(User).filter(
                User.email == data['email'],
                User.id != user_id
            ).first()
            
            if existing:
                raise HTTPException(status_code=400, detail="Email já cadastrado por outro usuário")
            
            user.email = data['email']
        
        if 'password' in data and data['password']:
            # Redefinir senha
            from ..auth import get_password_hash
            user.password = get_password_hash(data['password'])
            print(f"🔑 Senha do usuário {user_id} redefinida!")
        
        db.commit()
        
        print(f"✅ Usuário {user_id} atualizado: {user.first_name} {user.last_name} ({user.email})")
        
        return {"success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao editar usuário: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




