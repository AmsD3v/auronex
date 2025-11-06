"""
Router de Bot Configuration - Gerenciamento de bots
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import BotConfiguration, User
from ..schemas import BotConfigCreate, BotConfigUpdate, BotConfigResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots"])

@router.get("/")
def list_bots(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar bots do usuário"""
    
    try:
        from ..models_payment import Subscription
        
        bots = db.query(BotConfiguration).filter(
            BotConfiguration.user_id == current_user.id
        ).all()
        
        # Buscar plano
        subscription = db.query(Subscription).filter(
            Subscription.user_id == current_user.id,
            Subscription.status == "active"
        ).order_by(Subscription.id.desc()).first()
        
        plan = subscription.plan if subscription else "free"
        limits = {"free": 1, "pro": 3, "premium": 5}  # ✅ Atualizado: PRO=3, PREMIUM=5
        max_bots = limits.get(plan, 1)
        
        # Simples e rápido
        result = []
        for bot in bots:
            result.append({
                "id": bot.id,
                "name": bot.name,
                "exchange": bot.exchange,
                "symbols": bot.symbols if isinstance(bot.symbols, list) else [bot.symbols],
                "capital": 0,  # Será validado ao ativar
                "strategy": bot.strategy,
                "timeframe": bot.timeframe,
                "stop_loss_percent": float(bot.stop_loss_percent) if bot.stop_loss_percent else 0,
                "take_profit_percent": float(bot.take_profit_percent) if bot.take_profit_percent else 0,
                "is_active": bot.is_active,
                "user_id": bot.user_id
            })
        
        print(f"✅ Listando {len(result)} bots do usuário {current_user.id} (Plano: {plan}, Limite: {max_bots})")
        
        # Retornar com info de limite
        return {
            "bots": result,
            "total": len(result),
            "limit": max_bots,
            "plan": plan,
            "can_create": len(result) < max_bots
        }
        
    except Exception as e:
        print(f"❌ Erro ao listar bots: {str(e)}")
        return []

@router.post("/", response_model=BotConfigResponse)
def create_bot(
    bot_data: BotConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar novo bot - COM VALIDAÇÃO DE CAPITAL"""
    
    try:
        from datetime import datetime
        from ..models_payment import Subscription
        from ..models import ExchangeAPIKey
        
        # 1. VERIFICAR LIMITE DE BOTS (plano)
        subscription = db.query(Subscription).filter(
            Subscription.user_id == current_user.id,
            Subscription.status == "active"
        ).order_by(Subscription.id.desc()).first()
        
        plan = subscription.plan if subscription else "free"
        limits = {"free": 1, "pro": 3, "premium": 5}  # ✅ Atualizado: PRO=3, PREMIUM=5
        max_bots = limits.get(plan, 1)
        
        existing_bots_query = db.query(BotConfiguration).filter(
            BotConfiguration.user_id == current_user.id
        )
        
        if existing_bots_query.count() >= max_bots:
            raise HTTPException(
                status_code=403,
                detail=f"Limite de bots atingido! Plano {plan.upper()}: {max_bots} bot(s)."
            )
        
        # 2. VALIDAR CAPITAL DISPONÍVEL
        api_key = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == current_user.id,
            ExchangeAPIKey.exchange == bot_data.exchange.lower(),
            ExchangeAPIKey.is_active == True
        ).first()
        
        if api_key:
            try:
                from ..utils.encryption import decrypt_data
                import ccxt
                
                api_key_dec = decrypt_data(api_key.api_key_encrypted)
                secret_dec = decrypt_data(api_key.secret_key_encrypted)
                
                exchange_class = getattr(ccxt, bot_data.exchange.lower())
                exchange = exchange_class({
                    'apiKey': api_key_dec,
                    'secret': secret_dec,
                    'enableRateLimit': True
                })
                
                if api_key.is_testnet:
                    exchange.set_sandbox_mode(True)
                
                balance = exchange.fetch_balance()
                saldo_usdt = balance.get('free', {}).get('USDT', 0) or balance.get('USDT', {}).get('free', 0) or 0
                
                # Capital já alocado em outros bots DESTA exchange
                capital_alocado = sum(
                    float(b.capital) for b in existing_bots_query.all() 
                    if b.exchange == bot_data.exchange.lower()
                )
                
                capital_disponivel = saldo_usdt - capital_alocado
                
                # BLOQUEAR se capital solicitado > disponível
                if bot_data.capital > capital_disponivel:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Capital insuficiente! Disponível: ${capital_disponivel:.2f} (Saldo: ${saldo_usdt:.2f} - Já alocado: ${capital_alocado:.2f})"
                    )
                
                print(f"✅ Validação: ${bot_data.capital} <= ${capital_disponivel:.2f}")
                
            except HTTPException:
                raise
            except Exception as e:
                print(f"⚠️ Validação falhou (permitindo criar): {str(e)[:80]}")
        
        # symbols deve ser lista
        symbols_list = bot_data.symbols if isinstance(bot_data.symbols, list) else [bot_data.symbols]
        
        now = datetime.utcnow()
        
        # Capital = 0 (usaremos saldo real da exchange)
        bot = BotConfiguration(
            user_id=current_user.id,
            name=bot_data.name,
            exchange=bot_data.exchange.lower(),
            symbols=symbols_list,
            capital=0,  # Não usado mais - saldo real da exchange
            strategy=bot_data.strategy,
            timeframe=bot_data.timeframe,
            stop_loss_percent=bot_data.stop_loss_percent,
            take_profit_percent=bot_data.take_profit_percent,
            is_active=bot_data.is_active if hasattr(bot_data, 'is_active') else False,
            created_at=now,  # Obrigatório
            updated_at=now   # Obrigatório também!
        )
        
        db.add(bot)
        db.commit()
        db.refresh(bot)
        
        print(f"✅ Bot criado: {bot.name} (ID: {bot.id})")
        
        return bot
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar bot: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar bot: {str(e)[:200]}"
        )

@router.put("/{bot_id}/")
def update_bot(
    bot_id: int,
    bot_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar bot - ACEITA DICT DIRETO"""
    
    try:
        from datetime import datetime
        
        bot = db.query(BotConfiguration).filter(
            BotConfiguration.id == bot_id,
            BotConfiguration.user_id == current_user.id
        ).first()
        
        if not bot:
            raise HTTPException(status_code=404, detail="Bot não encontrado")
        
        # Atualizar TODOS os campos
        if 'name' in bot_data:
            bot.name = bot_data['name']
        if 'capital' in bot_data:
            bot.capital = bot_data['capital']
        if 'strategy' in bot_data:
            bot.strategy = bot_data['strategy']
        if 'timeframe' in bot_data:
            bot.timeframe = bot_data['timeframe']
        if 'stop_loss_percent' in bot_data:
            bot.stop_loss_percent = bot_data['stop_loss_percent']
        if 'take_profit_percent' in bot_data:
            bot.take_profit_percent = bot_data['take_profit_percent']
        if 'is_active' in bot_data:
            bot.is_active = bot_data['is_active']
        
        # Atualizar timestamp
        bot.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(bot)
        
        print(f"✅ Bot {bot.id} atualizado!")
        
        # Retornar dict
        return {
            "id": bot.id,
            "name": bot.name,
            "capital": float(bot.capital),
            "strategy": bot.strategy,
            "timeframe": bot.timeframe,
            "stop_loss_percent": float(bot.stop_loss_percent),
            "take_profit_percent": float(bot.take_profit_percent),
            "is_active": bot.is_active
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao atualizar bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{bot_id}/")
def delete_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar bot"""
    
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    db.delete(bot)
    db.commit()
    
    return {"message": "Bot deletado com sucesso"}

@router.post("/{bot_id}/start/")
def start_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Iniciar bot"""
    
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    bot.is_active = True
    db.commit()
    
    return {"message": "Bot iniciado!", "bot_id": bot_id}

@router.post("/{bot_id}/stop/")
def stop_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Parar bot"""
    
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    bot.is_active = False
    db.commit()
    
    return {"message": "Bot parado!", "bot_id": bot_id}


