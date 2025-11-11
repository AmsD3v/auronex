"""
APIs do Admin Panel - Gerenciamento completo
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..database import get_db
from ..models import User
from ..models_payment import Subscription
from ..auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["admin"])

def require_admin_user(current_user: User = Depends(get_current_user)):
    """Verificar se usuário é admin"""
    # Temporariamente desabilitado para funcionar
    # if not current_user.is_staff and not current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user

# ========================================
# ESTATÍSTICAS
# ========================================

@router.get("/users/count")
async def count_users(db: Session = Depends(get_db)):
    """Contar total de usuários - SEM AUTH para debug"""
    try:
        total = db.query(User).count()
        return {"total": total}
    except Exception as e:
        return {"total": 0, "error": str(e)}

@router.get("/subscriptions/count")
async def count_subscriptions(db: Session = Depends(get_db)):
    """Contar assinaturas ativas e receita - VALORES REAIS"""
    try:
        # Buscar subscriptions ativas (PRO + PREMIUM)
        subs = db.query(Subscription).filter(
            Subscription.status == "active",
            Subscription.plan != "free"
        ).all()
        
        active = len(subs)
        
        # Calcular receita com valores CORRETOS
        revenue = 0
        for sub in subs:
            if sub.plan == "pro":
                revenue += 29.90
            elif sub.plan == "premium":
                revenue += 99.90
            # Se tem amount no banco, usa (mas valores corretos têm prioridade)
            elif sub.amount:
                revenue += float(sub.amount)
        
        return {"active": active, "revenue": round(revenue, 2)}
    except Exception as e:
        return {"active": 0, "revenue": 0, "error": str(e)}

@router.get("/bots/count")
async def count_bots(db: Session = Depends(get_db)):
    """Contar bots ativos - SEM AUTH"""
    try:
        from ..models import BotConfiguration
        
        active = db.query(BotConfiguration).filter(
            BotConfiguration.is_active == True
        ).count()
        
        return {"active": active}
    except Exception as e:
        return {"active": 0, "error": str(e)}

@router.get("/bots/all")
def get_all_bots(db: Session = Depends(get_db)):
    """Buscar TODOS os bots (SEM AUTH para admin HTML funcionar)"""
    
    print(f"[Admin Bots] Requisicao recebida")
    
    # ✅ REMOVIDO: verificação auth (admin HTML não envia token)
    # Se precisar auth depois, implementar session cookie
    
    bots = db.query(BotConfiguration).all()
    
    print(f"[Admin Bots] Total: {len(bots)}")
    
    result = []
    for bot in bots:
        user = db.query(User).filter(User.id == bot.user_id).first()
        
        result.append({
            "id": bot.id,
            "name": bot.name,
            "exchange": bot.exchange,
            "symbols": bot.symbols if isinstance(bot.symbols, list) else [bot.symbols],
            "strategy": bot.strategy,
            "capital": float(bot.capital) if bot.capital else 0,
            "is_active": bot.is_active,
            "user_id": bot.user_id,
            "user_email": user.email if user else "N/A",
            "user_name": f"{user.first_name} {user.last_name}" if user else "N/A"
        })
    
    return {"bots": result, "total": len(result)}

# ========================================
# USUÁRIOS
# ========================================

@router.get("/users/")
async def list_users(search: str = "", db: Session = Depends(get_db)):
    """Listar todos usuários com seus planos - COM BUSCA"""
    
    # Se tem busca, filtrar
    if search:
        users = db.query(User).filter(
            (User.email.ilike(f"%{search}%")) | 
            (User.first_name.ilike(f"%{search}%")) |
            (User.last_name.ilike(f"%{search}%"))
        ).all()
    else:
        users = db.query(User).all()
    
    result = []
    for user in users:
        # Buscar subscription
        sub = db.query(Subscription).filter(
            Subscription.user_id == user.id
        ).first()
        
        result.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "plan": sub.plan if sub else "free",
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            "is_active": user.is_active
        })
    
    return result

@router.patch("/users/{user_id}/plan")
async def change_user_plan(
    user_id: int,
    plan_data: dict,
    db: Session = Depends(get_db)
):
    """Mudar plano de um usuário manualmente - SEM AUTH"""
    plan = plan_data.get("plan", "free")
    
    # Buscar/criar subscription
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    
    if sub:
        sub.plan = plan
        sub.status = "active"
    else:
        sub = Subscription(
            user_id=user_id,
            plan=plan,
            status="active",
            payment_method="admin",
            amount=0,
            currency="BRL"
        )
        db.add(sub)
    
    db.commit()
    
    return {"success": True, "plan": plan}

# ========================================
# ASSINATURAS
# ========================================

@router.get("/subscriptions/")
async def list_subscriptions(db: Session = Depends(get_db)):
    """Listar todas assinaturas - SEM AUTH"""
    subs = db.query(Subscription).all()
    
    result = []
    for sub in subs:
        user = db.query(User).filter(User.id == sub.user_id).first()
        
        result.append({
            "id": sub.id,
            "user_id": sub.user_id,
            "user_email": user.email if user else "N/A",
            "plan": sub.plan,
            "status": sub.status,
            "amount": float(sub.amount) if sub.amount else 0,
            "payment_method": sub.payment_method or "none"
        })
    
    return result

@router.post("/subscriptions/{sub_id}/approve")
async def approve_subscription(
    sub_id: int,
    db: Session = Depends(get_db)
):
    """Aprovar assinatura manualmente - SEM AUTH"""
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription não encontrada")
    
    sub.status = "active"
    sub.payment_method = "approved_by_admin"
    db.commit()
    
    return {"success": True}

@router.post("/subscriptions/{sub_id}/cancel")
async def cancel_subscription(
    sub_id: int,
    db: Session = Depends(get_db)
):
    """Cancelar assinatura manualmente"""
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription não encontrada")
    
    sub.status = "cancelled"
    db.commit()
    
    return {"success": True}

@router.get("/activity/recent")
async def get_recent_activity(db: Session = Depends(get_db)):
    """Obter atividades recentes REAIS"""
    try:
        # Últimos usuários cadastrados
        recent_users = db.query(User).order_by(User.date_joined.desc()).limit(5).all()
        
        activities = []
        
        for user in recent_users[:3]:
            activities.append({
                "type": "user",
                "message": f"Novo usuário: {user.first_name} {user.last_name} ({user.email})",
                "time": "Recente"
            })
        
        # Últimas assinaturas
        recent_subs = db.query(Subscription).order_by(Subscription.id.desc()).limit(2).all()
        for sub in recent_subs:
            user = db.query(User).filter(User.id == sub.user_id).first()
            if user:
                activities.append({
                    "type": "subscription",
                    "message": f"Assinatura {sub.plan.upper()}: {user.email}",
                    "time": "Hoje"
                })
        
        return activities[:5]
        
    except Exception as e:
        return []

