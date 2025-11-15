"""
Validador de Símbolos em Exchanges
Verifica se símbolos existem antes de criar bot
"""

import ccxt
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ExchangeValidator:
    """Valida símbolos em exchanges usando ccxt"""
    
    def __init__(self):
        self.cache_markets = {}  # Cache de mercados por exchange
        logger.info("✅ Exchange Validator inicializado")
    
    def get_available_symbols(self, exchange_name: str) -> Optional[List[str]]:
        """
        Busca símbolos disponíveis na exchange
        
        Args:
            exchange_name: Nome da exchange (binance, bybit, etc)
        
        Returns:
            Lista de símbolos ou None se erro
        """
        try:
            # Verificar cache
            if exchange_name in self.cache_markets:
                logger.info(f"[Cache] Usando símbolos em cache para {exchange_name}")
                return list(self.cache_markets[exchange_name].keys())
            
            # Mapa de nomes
            ccxt_map = {
                'mercadobitcoin': 'mercado',
                'gateio': 'gate',
                'foxbit': 'foxbit',
                'novadax': 'novadax',
                'brasilbitcoin': None,  # Não suportada pelo ccxt
            }
            
            ccxt_name = ccxt_map.get(exchange_name.lower(), exchange_name.lower())
            
            if ccxt_name is None:
                logger.warning(f"Exchange {exchange_name} não suportada pelo ccxt")
                return None
            
            # Criar instância
            exchange_class = getattr(ccxt, ccxt_name, None)
            
            if not exchange_class:
                logger.error(f"Exchange {ccxt_name} não encontrada no ccxt")
                return None
            
            exchange = exchange_class()
            
            # Carregar mercados (público, não precisa API Key)
            logger.info(f"Carregando mercados de {exchange_name}...")
            markets = exchange.load_markets()
            
            # Cachear
            self.cache_markets[exchange_name] = markets
            
            symbols = list(markets.keys())
            logger.info(f"✅ {len(symbols)} símbolos carregados de {exchange_name}")
            
            return symbols
            
        except Exception as e:
            logger.error(f"Erro ao carregar símbolos de {exchange_name}: {e}")
            return None
    
    def validate_symbols(
        self,
        exchange_name: str,
        symbols_to_validate: List[str]
    ) -> Tuple[bool, str, List[str]]:
        """
        Valida se símbolos existem na exchange
        
        Args:
            exchange_name: Nome da exchange
            symbols_to_validate: Lista de símbolos para validar
        
        Returns:
            (todos_validos, mensagem, simbolos_invalidos)
        """
        if not symbols_to_validate:
            return False, "Lista de símbolos vazia", []
        
        # Buscar símbolos disponíveis
        available_symbols = self.get_available_symbols(exchange_name)
        
        if available_symbols is None:
            # Se não conseguiu carregar, permitir (não bloquear criação)
            logger.warning(f"Não foi possível validar símbolos para {exchange_name} - permitindo")
            return True, "Validação ignorada (exchange offline?)", []
        
        # Converter para set para busca rápida
        available_set = set(available_symbols)
        
        # Verificar quais são inválidos
        invalid_symbols = [s for s in symbols_to_validate if s not in available_set]
        
        if invalid_symbols:
            return False, f"Símbolos inválidos para {exchange_name}: {', '.join(invalid_symbols)}", invalid_symbols
        
        return True, "Todos os símbolos são válidos", []
    
    def suggest_similar_symbols(
        self,
        exchange_name: str,
        invalid_symbol: str,
        max_suggestions: int = 5
    ) -> List[str]:
        """
        Sugere símbolos similares ao inválido
        
        Args:
            exchange_name: Nome da exchange
            invalid_symbol: Símbolo inválido
            max_suggestions: Máximo de sugestões
        
        Returns:
            Lista de símbolos similares
        """
        available_symbols = self.get_available_symbols(exchange_name)
        
        if not available_symbols:
            return []
        
        # Extrair base do símbolo (ex: BTC de BTC/USDT)
        base = invalid_symbol.split('/')[0] if '/' in invalid_symbol else invalid_symbol
        
        # Buscar símbolos que começam com a mesma base
        suggestions = [
            s for s in available_symbols
            if s.startswith(base) or base in s
        ]
        
        return suggestions[:max_suggestions]

# Instância global
exchange_validator = ExchangeValidator()






