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
            
            # ✅ 2. Calcular capital alocado NESTA EXCHANGE
            outros_bots_mesma_exchange = db.query(BotConfiguration).filter(
                BotConfiguration.user_id == current_user.id,
                BotConfiguration.exchange == bot.exchange,  # ✅ Mesma exchange!
                BotConfiguration.is_active == True,
                BotConfiguration.id != bot_id
            ).all()
            
            capital_outros_mesma_exchange = sum(float(b.capital or 0) for b in outros_bots_mesma_exchange)
            capital_este_bot = float(bot.capital or 0)
            capital_total_nesta_exchange = capital_outros_mesma_exchange + capital_este_bot
            
            print(f"[{bot.exchange.upper()}] Capital outros bots: ${capital_outros_mesma_exchange:.2f}")
            print(f"[{bot.exchange.upper()}] Este bot: ${capital_este_bot:.2f}")
            print(f"[{bot.exchange.upper()}] TOTAL nesta exchange: ${capital_total_nesta_exchange:.2f}")
            
            # ✅ BLOQUEAR se capital = 0
            if capital_este_bot == 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Bot sem capital definido! Configure um valor de investimento antes de ativar."
                )
            
            # 3. Validar saldo
            from ..utils.encryption import decrypt_data
            import ccxt
            
            try:
                api_key_dec = decrypt_data(api_key.api_key_encrypted)
                secret_dec = decrypt_data(api_key.secret_key_encrypted)
                
                # ✅ MAPEAMENTO COMPLETO
                ccxt_map = {
                    'mercadobitcoin': 'mercado',
                    'brasilbitcoin': None,
                    'gateio': 'gate',
                    'foxbit': 'foxbit',
                    'novadax': 'novadax',
                }
                
                ccxt_name = ccxt_map.get(bot.exchange, bot.exchange)
                
                if ccxt_name is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{bot.exchange.upper()} não suportada pelo ccxt"
                    )
                
                print(f"🔗 Conectando: {bot.exchange} -> {ccxt_name}")
                
                exchange_class = getattr(ccxt, ccxt_name)
                exchange = exchange_class({
                    'apiKey': api_key_dec,
                    'secret': secret_dec,
                    'enableRateLimit': True,
                    'timeout': 30000,
                    'options': {
                        'defaultType': 'spot',
                        'adjustForTimeDifference': True,
                        'recvWindow': 60000,
                    }
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
                
                print(f"💰 SALDO FINAL: ${saldo_usdt:.2f}")
                
                # ✅ CRÍTICO: Capital nesta exchange NÃO pode ultrapassar saldo!
                if capital_total_nesta_exchange > saldo_usdt:
                    cotacao = 5.0
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"IMPOSSÍVEL ATIVAR! "
                            f"Saldo na {bot.exchange.upper()}: R$ {saldo_usdt*cotacao:.2f} "
                            f"Capital já alocado ({bot.exchange.upper()}): R$ {capital_outros_mesma_exchange*cotacao:.2f} "
                            f"Este bot precisa: R$ {capital_este_bot*cotacao:.2f} "
                            f"Total necessário: R$ {capital_total_nesta_exchange*cotacao:.2f} "
                            f"Reduza o capital dos bots na {bot.exchange.upper()}!"
                        )
                    )
                
                print(f"✅ [{bot.exchange.upper()}] OK: ${capital_total_nesta_exchange:.2f} <= ${saldo_usdt:.2f}")
                
            except HTTPException:
                # Sempre propagar erro de validação
                raise
            except Exception as e:
                # ✅ Se exchange não funcionar, BLOQUEAR!
                print(f"❌ BLOQUEADO: Não foi possível validar saldo")
                print(f"❌ Erro: {str(e)[:150]}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Não foi possível validar saldo da {bot.exchange.upper()}. Verifique se a exchange está online e tente novamente."
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


