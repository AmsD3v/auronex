"""Exchange endpoints - LIMPO E FUNCIONAL"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import User, ExchangeAPIKey
from ..dependencies import get_current_user_optional
from ..utils.encryption import decrypt_data

router = APIRouter(prefix="/api/exchange", tags=["exchange"])

@router.get("/balance")
def get_balance(
    current_user: Optional[User] = Depends(get_current_user_optional),  # ✅ OPCIONAL
    exchange: str = Query(default=None),
    db: Session = Depends(get_db)
):
    """
    Buscar saldo
    - Se autenticado: saldo do usuário
    - Se não autenticado: saldo GERAL (dashboard)
    - Se exchange específica: saldo dela
    - Sem exchange: soma TODAS
    """
    
    # ✅ Se especificou exchange
    if exchange:
        if current_user:
            # Filtrar por usuário
            api_key = db.query(ExchangeAPIKey).filter(
                ExchangeAPIKey.user_id == current_user.id,
                ExchangeAPIKey.exchange == exchange.lower(),
                ExchangeAPIKey.is_active == True
            ).first()
        else:
            # Primeira ativa do sistema (dashboard público)
            api_key = db.query(ExchangeAPIKey).filter(
                ExchangeAPIKey.exchange == exchange.lower(),
                ExchangeAPIKey.is_active == True
            ).first()
    else:
        # ✅ SEM exchange = SOMAR TODAS
        if current_user:
            # Apenas do usuário
            api_keys = db.query(ExchangeAPIKey).filter(
                ExchangeAPIKey.user_id == current_user.id,
                ExchangeAPIKey.is_active == True
            ).all()
        else:
            # Todas do sistema (dashboard público)
            api_keys = db.query(ExchangeAPIKey).filter(
                ExchangeAPIKey.is_active == True
            ).all()
        
        if not api_keys:
            return {
                "usdt": 0,
                "btc": 0,
                "eth": 0,
                "bnb": 0,
                "total_usd": 0,
                "exchange": "none",
                "is_testnet": True
            }
        
        # Somar TODAS as exchanges
        total_usdt = 0
        
        import concurrent.futures
        
        def get_exchange_balance(api_key):
            """Busca saldo de UMA exchange com timeout"""
            try:
                print(f"\n[Balance] Tentando {api_key.exchange.upper()}...")
                import ccxt
                ccxt_map = {
                    'mercadobitcoin': 'mercado',
                    'brasilbitcoin': None,
                    'gateio': 'gate',
                    'coinbase': 'coinbase',
                }
                ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
                
                if ccxt_name is None:
                    print(f"[Balance] {api_key.exchange.upper()}: não suportada pelo ccxt")
                    return 0
                
                api_dec = decrypt_data(api_key.api_key_encrypted)
                secret_dec = decrypt_data(api_key.secret_key_encrypted)
                
                exchange_class = getattr(ccxt, ccxt_name)
                exchange_obj = exchange_class({
                    'apiKey': api_dec,
                    'secret': secret_dec,
                    'enableRateLimit': True,
                    'timeout': 5000,  # ✅ 5s timeout por exchange
                    'options': {
                        'adjustForTimeDifference': True,
                        'recvWindow': 60000,
                        'defaultType': 'spot',
                    }
                })
                
                if api_key.is_testnet:
                    exchange_obj.set_sandbox_mode(True)
                
                balance = exchange_obj.fetch_balance()
                usdt = balance.get('free', {}).get('USDT', 0) or 0
                
                # Se 0, tentar BRL (converter com cotação real)
                if usdt == 0:
                    brl = balance.get('free', {}).get('BRL', 0) or 0
                    if brl > 0:
                        # Buscar cotação real
                        import requests
                        try:
                            cotacao_resp = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL', timeout=2)
                            cotacao = float(cotacao_resp.json()['USDBRL']['bid'])
                        except:
                            cotacao = 5.30  # Fallback
                        
                        usdt = brl / cotacao
                        print(f"[Balance] {api_key.exchange.upper()}: R$ {brl:.2f} (cotação {cotacao:.2f}) = ${usdt:.2f}")
                
                if usdt > 0:
                    print(f"[Balance] {api_key.exchange.upper()}: ${usdt:.2f}")
                
                return usdt
                
            except Exception as e:
                print(f"[Balance] {api_key.exchange.upper()}: ERRO - {str(e)[:50]}")
                return 0
        
        # ✅ Buscar em PARALELO com timeout de 30s total
        print(f"\n[Balance] Buscando saldo de {len(api_keys)} exchange(s) em paralelo...")
        total_usdt = 0
        sucesso = 0
        falhas = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_exchange = {executor.submit(get_exchange_balance, key): key for key in api_keys}
            
            for future in concurrent.futures.as_completed(future_to_exchange, timeout=30):
                try:
                    usdt = future.result(timeout=5)
                    if usdt > 0:
                        total_usdt += usdt
                        sucesso += 1
                    else:
                        falhas += 1
                except Exception as e:
                    print(f"[Balance] Future falhou: {str(e)[:50]}")
                    falhas += 1
        
        print(f"\n[Balance TOTAL] ${total_usdt:.2f} de {len(api_keys)} exchange(s)")
        print(f"[Balance] Sucesso: {sucesso} | Falhas: {falhas}")
        
        return {
            "usdt": round(total_usdt, 2),
            "btc": 0,
            "eth": 0,
            "bnb": 0,
            "total_usd": round(total_usdt, 2),
            "exchange": "consolidated",
            "is_testnet": True
        }
    
    # Exchange específica (já foi buscada acima)
    if not api_key:
        # ✅ Retornar saldo 0 com mensagem clara
        return {
            "usdt": 0,
            "btc": 0,
            "eth": 0,
            "bnb": 0,
            "total_usd": 0,
            "exchange": exchange or "none",
            "is_testnet": True,
            "message": f"Configure API Key para {exchange.upper()} primeiro",
            "action": "Vá em Menu → API Keys → Adicionar"
        }
    
    try:
        import ccxt
        
        ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate', 'foxbit': 'foxbit', 'novadax': 'novadax'}
        ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
        
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True,
            'timeout': 30000,  # 30s timeout
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,  # ✅ Corrige timestamp
                'recvWindow': 60000,  # 60s tolerância
            }
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        balance = exchange.fetch_balance()
        
        usdt = balance.get('free', {}).get('USDT', 0) or 0
        
        # ✅ Se 0, tentar BRL (cotação real)
        if usdt == 0:
            brl = balance.get('free', {}).get('BRL', 0) or 0
            if brl > 0:
                import requests
                try:
                    cotacao_resp = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL', timeout=2)
                    cotacao = float(cotacao_resp.json()['USDBRL']['bid'])
                except:
                    cotacao = 5.30
                usdt = brl / cotacao
        
        btc = balance.get('free', {}).get('BTC', 0) or 0
        eth = balance.get('free', {}).get('ETH', 0) or 0
        bnb = balance.get('free', {}).get('BNB', 0) or 0
        
        return {
            "usdt": round(usdt, 2),
            "btc": round(btc, 8),
            "eth": round(eth, 6),
            "bnb": round(bnb, 4),
            "total_usd": round(usdt, 2),
            "exchange": api_key.exchange.upper(),
            "is_testnet": api_key.is_testnet
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"[Balance] ERRO: {error_msg[:200]}")
        
        # ✅ Mensagens claras baseadas no erro
        user_message = "Erro ao conectar exchange"
        
        if "Invalid API-key" in error_msg or "API-key" in error_msg:
            user_message = "API Key inválida. Verifique suas credenciais"
        elif "Timestamp" in error_msg:
            user_message = "Erro de sincronização de horário. Verifique relógio do PC"
        elif "Signature" in error_msg:
            user_message = "Erro de assinatura. Secret Key pode estar incorreta"
        elif "testnet" in error_msg.lower():
            user_message = "Testnet pode estar offline. Tente novamente em alguns minutos"
        
        # ✅ Retornar saldo 0 com mensagem clara
        return {
            "usdt": 0,
            "btc": 0,
            "eth": 0,
            "bnb": 0,
            "total_usd": 0,
            "exchange": exchange or "unknown",
            "is_testnet": True,
            "message": user_message,
            "error_detail": error_msg[:100]
        }

@router.get("/symbols")
def get_symbols(
    exchange: str = Query(default="binance")
):
    """
    Buscar símbolos PÚBLICOS da exchange (SEM API KEY necessária!)
    
    ✅ Cliente pode ver cryptos ANTES de criar conta
    ✅ Não precisa API Key para listar
    ✅ Tenta: 1. ccxt público 2. API REST 3. Lista fixa
    """
    
    exchange_lower = exchange.lower()
    
    # ✅ MÉTODO 1: Tentar APIs REST PÚBLICAS primeiro (mais confiável)
    try:
        import requests
        
        # Huobi/HTX: API REST pública
        if exchange_lower == 'huobi':
            response = requests.get('https://api.huobi.pro/v1/common/symbols', timeout=5)
            if response.status_code == 200:
                data = response.json()
                symbols = [f"{s['base-currency'].upper()}/{s['quote-currency'].upper()}" 
                          for s in data.get('data', [])]
                usdt_symbols = [s for s in symbols if '/USDT' in s]
                print(f"[Symbols API REST] Huobi /USDT: {len(usdt_symbols)}")
                return sorted(usdt_symbols)
        
        # Coinbase: API V2 pública
        elif exchange_lower == 'coinbase':
            response = requests.get('https://api.exchange.coinbase.com/products', timeout=5)
            if response.status_code == 200:
                data = response.json()
                symbols = [f"{p['base_currency']}/{p['quote_currency']}" 
                          for p in data if p.get('status') == 'online']
                usd_symbols = [s for s in symbols if '/USD' in s and '/USDT' not in s]
                print(f"[Symbols API REST] Coinbase /USD: {len(usd_symbols)}")
                return sorted(usd_symbols)
    
    except Exception as e:
        print(f"[Symbols API REST] Erro {exchange}: {e}")
    
    # ✅ MÉTODO 2: Tentar ccxt público
    try:
        import ccxt
        
        # Map de exchanges (ccxt usa nomes diferentes)
        ccxt_map = {
            'mercadobitcoin': 'mercado',
            'brasilbitcoin': 'brasilbitcoin',  # ✅ Suportada!
            'gateio': 'gate',
            'foxbit': 'foxbit',
            'huobi': 'huobi',
            # Coinbase já tem nome correto
        }
        
        ccxt_name = ccxt_map.get(exchange.lower(), exchange.lower())
        
        if ccxt_name is None:
            return []  # Exchange não suportada
        
        # ✅ Criar exchange em MODO PÚBLICO (sem API Key!)
        exchange_class = getattr(ccxt, ccxt_name)
        exchange_obj = exchange_class({
            'enableRateLimit': True,
            # ✅ SEM apiKey/secret = modo público!
        })
        
        # ✅ Carregar markets PUBLICAMENTE (não precisa auth!)
        markets = exchange_obj.load_markets()
        
        # Pegar symbols
        symbols = list(markets.keys())
        
        print(f"[Symbols PÚBLICO] {exchange.upper()}: {len(symbols)} símbolos")
        
        # ✅ Filtrar por moeda relevante POR EXCHANGE
        exchange_lower = exchange.lower()
        
        # Exchanges brasileiras: apenas BRL
        if exchange_lower in ['mercadobitcoin', 'brasilbitcoin', 'foxbit']:
            symbols_filtered = [s for s in symbols if '/BRL' in s and ':' not in s]
            print(f"[Symbols] {exchange.upper()} /BRL: {len(symbols_filtered)}")
            return sorted(symbols_filtered)
        
        # Exchanges internacionais: USDT (spot) + USD (algumas)
        elif exchange_lower in ['binance', 'bybit', 'okx', 'gateio', 'huobi']:
            # USDT (spot apenas, sem futuros)
            symbols_usdt = [s for s in symbols if '/USDT' in s and ':' not in s]
            print(f"[Symbols] {exchange.upper()} /USDT: {len(symbols_usdt)}")
            return sorted(symbols_usdt)
        
        # Coinbase: USD
        elif exchange_lower == 'coinbase':
            symbols_usd = [s for s in symbols if '/USD' in s and ':' not in s]
            print(f"[Symbols] COINBASE /USD: {len(symbols_usd)}")
            return sorted(symbols_usd)
        
        # Kraken: USD e USDT
        elif exchange_lower == 'kraken':
            symbols_filtered = [s for s in symbols if ('/USD' in s or '/USDT' in s) and ':' not in s]
            print(f"[Symbols] KRAKEN /USD+/USDT: {len(symbols_filtered)}")
            return sorted(symbols_filtered)
        
        # Outras: retornar tudo
        else:
            print(f"[Symbols] {exchange.upper()} TODAS: {len(symbols)}")
            return sorted(symbols)
        
    except Exception as e:
        print(f"[Symbols] Erro {exchange}: {e}")
        
        # ✅ Fallback com listas FIXAS (exchanges sem modo público)
        from ..data.exchange_symbols import (
            COINBASE_SYMBOLS, FOXBIT_SYMBOLS, BRASILBITCOIN_SYMBOLS, HUOBI_SYMBOLS
        )
        
        exchange_lower = exchange.lower()
        
        if exchange_lower == 'coinbase':
            print(f"[Symbols] Usando lista fixa Coinbase: {len(COINBASE_SYMBOLS)}")
            return COINBASE_SYMBOLS
        
        elif exchange_lower == 'foxbit':
            print(f"[Symbols] Usando lista fixa Foxbit: {len(FOXBIT_SYMBOLS)}")
            return FOXBIT_SYMBOLS
        
        elif exchange_lower == 'brasilbitcoin':
            print(f"[Symbols] Usando lista fixa BrasilBitcoin: {len(BRASILBITCOIN_SYMBOLS)}")
            return BRASILBITCOIN_SYMBOLS
        
        elif exchange_lower == 'huobi':
            print(f"[Symbols] Usando lista fixa Huobi: {len(HUOBI_SYMBOLS)}")
            return HUOBI_SYMBOLS
        
        # Fallback genérico
        elif 'brasil' in exchange_lower or 'mercado' in exchange_lower:
            return ['BTC/BRL', 'ETH/BRL', 'XRP/BRL', 'SOL/BRL', 'USDT/BRL']
        else:
            return ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT']


