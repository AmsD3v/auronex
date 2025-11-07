"""
API de Monitoramento de Bots em Tempo Real
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Trade, BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bot-monitor", tags=["bot-monitor"])

@router.get("/status/{bot_id}")
def get_bot_realtime_status(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Status em tempo real de um bot específico"""
    
    # Verificar se bot pertence ao usuário
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        return {"erro": "Bot não encontrado"}
    
    # Trades hoje
    hoje = datetime.now().date()
    trades_hoje = db.query(Trade).filter(
        Trade.bot_id == bot_id,
        func.date(Trade.entry_time) == hoje
    ).all()
    
    # Calcular métricas
    total_trades = len(trades_hoje)
    trades_ganhos = sum(1 for t in trades_hoje if t.profit_loss and t.profit_loss > 0)
    lucro_hoje = sum(t.profit_loss for t in trades_hoje if t.profit_loss) or 0
    
    win_rate = (trades_ganhos / total_trades * 100) if total_trades > 0 else 0
    
    # Última atividade
    ultimo_trade = db.query(Trade).filter(
        Trade.bot_id == bot_id
    ).order_by(Trade.entry_time.desc()).first()
    
    ultima_atividade = ultimo_trade.entry_time if ultimo_trade else None
    
    return {
        "bot_id": bot_id,
        "nome": bot.name,
        "is_active": bot.is_active,
        "exchange": bot.exchange.upper(),
        "trades_hoje": total_trades,
        "win_rate_hoje": round(win_rate, 2),
        "lucro_hoje": round(lucro_hoje, 2),
        "ultima_atividade": str(ultima_atividade) if ultima_atividade else "Nunca",
        "symbols": bot.symbols
    }

@router.get("/all")
def get_all_bots_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Status de todos os bots do usuário"""
    
    bots = db.query(BotConfiguration).filter(
        BotConfiguration.user_id == current_user.id
    ).all()
    
    resultado = []
    
    for bot in bots:
        # Trades do bot
        trades = db.query(Trade).filter(Trade.bot_config_id == bot.id).all()
        
        total = len(trades)
        ganhos = sum(1 for t in trades if t.profit_loss and t.profit_loss > 0)
        lucro_total = sum(t.profit_loss for t in trades if t.profit_loss) or 0
        
        resultado.append({
            "id": bot.id,
            "nome": bot.name,
            "is_active": bot.is_active,
            "exchange": bot.exchange,
            "total_trades": total,
            "win_rate": round((ganhos / total * 100) if total > 0 else 0, 2),
            "lucro_total": round(lucro_total, 2)
        })
    
    return {"bots": resultado, "total": len(resultado)}


