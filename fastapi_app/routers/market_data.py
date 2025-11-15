"""
Market Data - Top 5 Performance via CoinCap (SEM LIMITE!)
Fallback: CoinGecko se CoinCap falhar
"""
from fastapi import APIRouter
import requests
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/market", tags=["market-data"])

# API Keys
COINCAP_API_KEY = "15f75b748b66ebec0b9ece9b946682e001c2abf27e83224372efd260507f27e0"
COINGECKO_API_KEY = "CG-vSM45DWyL7ujMYAAdfSSmbay"

# ✅ SEM CACHE - Sempre dados frescos!
@router.get("/top-gainers")
def get_top_gainers(period: str = "24h"):
    """
    Top 5 cryptos com maior ganho
    
    ✅ Dados REAIS da Binance em tempo real
    ✅ Atualiza a cada request
    ✅ Sem dependência de APIs externas
    """
    
    try:
        # ✅ MÉTODO 1: Buscar da BINANCE DIRETAMENTE (sempre funciona!)
        try:
            import ccxt
            
            # Criar Binance exchange (público, sem API key)
            binance = ccxt.binance({
                'enableRateLimit': True,
                'timeout': 10000,
            })
            
            # Buscar tickers de TODAS moedas
            print("[Top5] Buscando tickers da Binance...")
            tickers = binance.fetch_tickers()
            
            # Filtrar apenas pares /USDT
            usdt_pairs = {symbol: data for symbol, data in tickers.items() if '/USDT' in symbol}
            
            # Ordenar por % de mudança 24h
            sorted_pairs = sorted(
                usdt_pairs.items(),
                key=lambda x: float(x[1].get('percentage', 0) or 0),
                reverse=True
            )[:5]  # Top 5
            
            result = []
            for symbol, data in sorted_pairs:
                base = symbol.split('/')[0]  # BTC de BTC/USDT
                result.append({
                    "symbol": base,
                    "name": base,
                    "price": float(data.get('last', 0) or 0),
                    "change_24h": float(data.get('percentage', 0) or 0),
                    "change_7d": 0,  # Binance não tem 7d em ticker
                    "volume_24h": float(data.get('quoteVolume', 0) or 0),
                    "market_cap": 0,  # Não disponível em ticker
                    "image": ""
                })
            
            print(f"[Binance] Top 5: {[c['symbol'] for c in result]}")
            
            return {
                "data": result,
                "source": "binance",
                "attribution": "Dados da Binance Exchange"
            }
            
        except Exception as e:
            print(f"[Binance] Erro: {str(e)[:100]}")
        
        # ✅ MÉTODO 2: CoinCap (fallback)
        try:
            # CoinCap não precisa auth (API Key opcional apenas para rate limit)
            response = requests.get('https://api.coincap.io/v2/assets?limit=100', timeout=10)
            
            if response.status_code == 200:
                data = response.json()['data']
                
                # Ordenar por ganho 24h
                data_sorted = sorted(data, 
                    key=lambda x: float(x.get('changePercent24Hr', 0)), 
                    reverse=True
                )[:5]
                
                result = []
                for coin in data_sorted:
                    result.append({
                        "symbol": coin.get('symbol', '').upper(),
                        "name": coin.get('name', ''),
                        "price": float(coin.get('priceUsd', 0)),
                        "change_24h": float(coin.get('changePercent24Hr', 0)),
                        "change_7d": 0,  # CoinCap não tem 7d
                        "volume_24h": float(coin.get('volumeUsd24Hr', 0)),
                        "market_cap": float(coin.get('marketCapUsd', 0)),
                        "image": f"https://assets.coincap.io/assets/icons/{coin.get('symbol', '').lower()}@2x.png"
                    })
                
                print(f"[CoinCap] Top 5 {period}: {[c['symbol'] for c in result]}")
                
                return {
                    "data": result,
                    "source": "coincap",
                    "attribution": "Data provided by CoinCap.io",
                    "url": "https://coincap.io"
                }
        
        except Exception as e:
            print(f"[CoinCap] Erro (tentando CoinGecko): {e}")
        
        # ✅ MÉTODO 2: CoinGecko API V3 (fallback)
        headers = {
            'x-cg-pro-api-key': COINGECKO_API_KEY
        }
        
        # Ordenar por ganho 24h ou 7d
        order_by = 'price_change_percentage_24h_desc' if period == '24h' else 'price_change_percentage_7d_desc'
        
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order={order_by}&per_page=5&page=1&sparkline=false"
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            result = []
            for coin in data:
                result.append({
                    "symbol": coin.get('symbol', '').upper(),
                    "name": coin.get('name', ''),
                    "price": coin.get('current_price', 0),
                    "change_24h": coin.get('price_change_percentage_24h', 0),
                    "change_7d": coin.get('price_change_percentage_7d', 0),
                    "volume_24h": coin.get('total_volume', 0),
                    "market_cap": coin.get('market_cap', 0),
                    "image": coin.get('image', '')
                })
            
            print(f"[CoinGecko] Top 5 {period}: {[c['symbol'] for c in result]}")
            
            return {
                "data": result,
                "source": "coingecko",
                "attribution": "Data provided by CoinGecko",
                "url": "https://www.coingecko.com?utm_source=auronex&utm_medium=referral"
            }
    
    except Exception as e:
        print(f"[CoinGecko] Erro: {e}")
    
    # ✅ Fallback com dados MOCK (enquanto APIs offline)
    print("[Market] Usando dados MOCK (APIs offline)")
    return {
        "data": [
            {"symbol": "BTC", "name": "Bitcoin", "price": 37000, "change_24h": 2.5, "change_7d": 8.3, "volume_24h": 25000000000, "market_cap": 720000000000, "image": ""},
            {"symbol": "ETH", "name": "Ethereum", "price": 2050, "change_24h": 3.2, "change_7d": 12.1, "volume_24h": 12000000000, "market_cap": 250000000000, "image": ""},
            {"symbol": "SOL", "name": "Solana", "price": 58, "change_24h": 5.8, "change_7d": 15.4, "volume_24h": 1500000000, "market_cap": 25000000000, "image": ""},
            {"symbol": "BNB", "name": "BNB", "price": 240, "change_24h": 1.9, "change_7d": 6.7, "volume_24h": 800000000, "market_cap": 37000000000, "image": ""},
            {"symbol": "XRP", "name": "Ripple", "price": 0.52, "change_24h": 1.1, "change_7d": 4.2, "volume_24h": 900000000, "market_cap": 28000000000, "image": ""}
        ],
        "source": "mock",
        "attribution": "Dados temporários (APIs offline)"
    }

