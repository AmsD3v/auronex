"""
Market Data - Top 5 Performance via CoinCap (SEM LIMITE!)
Fallback: CoinGecko se CoinCap falhar
"""
from fastapi import APIRouter
import requests
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/market", tags=["market-data"])

# CoinGecko API Key (fallback)
COINGECKO_API_KEY = "CG-vSM45DWyL7ujMYAAdfSSmbay"

# Cache (atualiza a cada 1 min)
_cache = {
    'top_gainers_24h': [],
    'top_gainers_7d': [],
    'timestamp': None
}

@router.get("/top-gainers")
def get_top_gainers(period: str = "24h"):
    """
    Top 5 cryptos com maior ganho (CoinGecko API)
    
    ✅ Dados REAIS em tempo real
    ✅ Atualiza a cada 1 min (cache)
    ✅ 10.000 calls/mês (33/dia OK!)
    
    Attribution: Data provided by CoinGecko
    """
    
    global _cache
    
    # Se cache tem menos de 1 min, usar
    if _cache['timestamp'] and (datetime.now() - _cache['timestamp']) < timedelta(minutes=1):
        key = f'top_gainers_{period}'
        if key in _cache and _cache[key]:
            return {
                "data": _cache[key],
                "source": "cache",
                "attribution": "Data provided by CoinGecko"
            }
    
    try:
        # ✅ MÉTODO 1: CoinCap (SEM LIMITE!)
        try:
            response = requests.get('https://api.coincap.io/v2/assets?limit=100', timeout=5)
            
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
                
                # Atualizar cache
                _cache[f'top_gainers_{period}'] = result
                _cache['timestamp'] = datetime.now()
                
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
            
            # Atualizar cache
            _cache[f'top_gainers_{period}'] = result
            _cache['timestamp'] = datetime.now()
            
            print(f"[CoinGecko] Top 5 {period}: {[c['symbol'] for c in result]}")
            
            return {
                "data": result,
                "source": "coingecko",
                "attribution": "Data provided by CoinGecko",
                "url": "https://www.coingecko.com?utm_source=auronex&utm_medium=referral"
            }
    
    except Exception as e:
        print(f"[CoinGecko] Erro: {e}")
    
    # Fallback
    return {
        "data": [],
        "source": "error",
        "error": "Erro ao buscar dados"
    }

