"""
Endpoint para ativar/desativar bot
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots-toggle"])

@router.patch("/{bot_id}/toggle")
def toggle_bot(
    bot_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ativar ou desativar bot - COM VALIDAÇÃO DE SALDO"""
    
    try:
        from ..models import ExchangeAPIKey
        
        bot = db.query(BotConfiguration).filter(
            BotConfiguration.id == bot_id,
            BotConfiguration.user_id == current_user.id
        ).first()
        
        if not bot:
            raise HTTPException(status_code=404, detail="Bot não encontrado")
        
        # SE QUER ATIVAR, validar saldo SEMPRE!
        if data.get('is_active', False):
            print(f"🔍 Validando ativação do bot {bot.id} ({bot.exchange})...")
            
            # 1. Buscar API Key
            api_key = db.query(ExchangeAPIKey).filter(
                ExchangeAPIKey.user_id == current_user.id,
                ExchangeAPIKey.exchange == bot.exchange,
                ExchangeAPIKey.is_active == True
            ).first()
            
            if not api_key:
                print(f"❌ API Key não encontrada para {bot.exchange}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Configure API Key para {bot.exchange.upper()} antes de ativar!"
                )
            
            # 2. SEMPRE validar saldo (NUNCA permitir sem validar!)
            from ..utils.encryption import decrypt_data
            import ccxt
            
            try:
                api_key_dec = decrypt_data(api_key.api_key_encrypted)
                secret_dec = decrypt_data(api_key.secret_key_encrypted)
                
                # MAPEAMENTO DE NOMES (mesmo que listar bots!)
                ccxt_map = {
                    'mercadobitcoin': 'mercado',
                    'brasilbitcoin': None,
                    'gateio': 'gate'
                }
                
                ccxt_name = ccxt_map.get(bot.exchange, bot.exchange)
                
                if ccxt_name is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{bot.exchange.upper()} não é suportada ainda."
                    )
                
                print(f"🔗 Conectando: {bot.exchange} -> {ccxt_name}")
                
                exchange_class = getattr(ccxt, ccxt_name)
                exchange = exchange_class({
                    'apiKey': api_key_dec,
                    'secret': secret_dec,
                    'enableRateLimit': True,
                    'timeout': 20000
                })
                
                if api_key.is_testnet:
                    exchange.set_sandbox_mode(True)
                
                balance = exchange.fetch_balance()
                
                # Buscar USDT (várias formas) - COM LOGS
                print(f"🔍 Balance keys: {list(balance.keys())[:10]}")
                
                saldo_usdt = 0
                saldo_usdt = balance.get('free', {}).get('USDT', 0) or 0
                print(f"  Tentativa 1 (free.USDT): ${saldo_usdt}")
                
                if saldo_usdt == 0:
                    saldo_usdt = balance.get('USDT', {}).get('free', 0) or 0
                    print(f"  Tentativa 2 (USDT.free): ${saldo_usdt}")
                
                if saldo_usdt == 0:
                    busd = balance.get('free', {}).get('BUSD', 0) or 0
                    usdc = balance.get('free', {}).get('USDC', 0) or 0
                    saldo_usdt = busd + usdc
                    print(f"  Tentativa 3 (stablecoins): ${saldo_usdt}")
                
                # BRL
                if saldo_usdt == 0:
                    brl = balance.get('free', {}).get('BRL', 0) or 0
                    if brl > 0:
                        saldo_usdt = brl / 5.0
                        print(f"  Tentativa 4 (BRL): R$ {brl} = ${saldo_usdt}")
                
                print(f"💰 SALDO FINAL: ${saldo_usdt:.2f} USDT")
                
                # BLOQUEAR se < $2 (R$ 10)
                minimo_usd = 2.0
                
                print(f"🔍 Comparação: ${saldo_usdt:.2f} >= ${minimo_usd}? {saldo_usdt >= minimo_usd}")
                
                if saldo_usdt < minimo_usd:
                    print(f"❌ BLOQUEADO: ${saldo_usdt:.2f} < ${minimo_usd}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Saldo insuficiente! Você tem R$ {saldo_usdt*5:.2f}. Mínimo: R$ 10,00."
                    )
                
                print(f"✅✅✅ SALDO APROVADO: ${saldo_usdt:.2f} >= ${minimo_usd}")
                
            except HTTPException:
                # Sempre propagar erro de validação
                raise
            except Exception as e:
                # NUNCA permitir se validação falhar!
                print(f"❌ BLOQUEADO: Erro ao validar saldo: {str(e)[:100]}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Não foi possível validar saldo da {bot.exchange.upper()}. Verifique API Key e tente novamente."
                )
        
        # Atualizar status
        bot.is_active = data.get('is_active', False)
        bot.updated_at = datetime.utcnow()
        
        db.commit()
        
        status_text = "INICIADO" if bot.is_active else "PAUSADO"
        print(f"✅ Bot {bot.id} ({bot.name}) {status_text}!")
        
        return {
            "success": True,
            "bot_id": bot.id,
            "is_active": bot.is_active
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao toggle bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


