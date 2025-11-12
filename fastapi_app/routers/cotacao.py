"""
Cotação Dólar em Tempo Real
"""
from fastapi import APIRouter
import requests
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/cotacao", tags=["cotacao"])

# Cache simples (atualiza a cada 5 min)
_cache = {
    'valor': 5.0,
    'timestamp': None
}

@router.get("/usd-brl")
def get_cotacao_usd_brl():
    """Cotação USD/BRL em tempo real (AwesomeAPI)"""
    
    global _cache
    
    # Se cache tem menos de 5 min, usar
    if _cache['timestamp'] and (datetime.now() - _cache['timestamp']) < timedelta(minutes=5):
        return {
            "valor": _cache['valor'],
            "fonte": "cache",
            "atualizado": _cache['timestamp'].isoformat()
        }
    
    try:
        # ✅ API pública e gratuita do Banco Central via AwesomeAPI
        response = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL', timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            valor = float(data['USDBRL']['bid'])  # Cotação de compra
            
            # Atualizar cache
            _cache['valor'] = valor
            _cache['timestamp'] = datetime.now()
            
            print(f"[Cotação] USD/BRL: R$ {valor:.2f}")
            
            return {
                "valor": valor,
                "fonte": "awesomeapi",
                "atualizado": datetime.now().isoformat()
            }
    except Exception as e:
        print(f"[Cotação] Erro ao buscar: {e}")
    
    # Fallback: usar cache ou 5.0
    return {
        "valor": _cache['valor'],
        "fonte": "fallback",
        "atualizado": _cache['timestamp'].isoformat() if _cache['timestamp'] else None
    }

