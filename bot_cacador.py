"""
Bot Caçador - Multi-Cripto em TEMPO REAL
Verifica constantemente TODAS as criptos e executa IMEDIATAMENTE
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Configurar logging
log_file = Path('bot_cacador.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from bot.exchange import BinanceExchange
from bot.risk_management import RiskManager
from bot.data_manager import DataManager
from bot.portfolio_manager import PortfolioManager
from bot.strategies import MeanReversionStrategy

class BotCacador:
    """
    Bot Caçador - Tempo Real Multi-Cripto
    
    Características:
    - Verifica TODAS as criptos constantemente
    - Delay mínimo (3 segundos)
    - Executa IMEDIATAMENTE quando encontra oportunidade
    - Máxima eficiência
    """
    
    def __init__(self, symbols: List[str] = None):
        """Inicializa o bot caçador"""
        self.settings = Settings()
        
        # Criptos para caçar
        self.symbols = symbols or ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
        
        # Componentes
        self.exchange = None
        self.risk_manager = None
        self.data_manager = None
        self.portfolio = None
        self.strategy = MeanReversionStrategy()
        
        # Controle
        self.running = False
        self.total_analises = 0
        self.oportunidades_encontradas = 0
        
        # Cache de dados (para não baixar toda hora)
        self.cache_dados = {}
        self.cache_time = {}
    
    def inicializar(self):
        """Inicializa o bot"""
        print("\n" + "="*70)
        print("BOT CACADOR - MULTI-CRIPTO TEMPO REAL")
        print("="*70)
        print(f"\nCriptos: {', '.join(self.symbols)}")
        print(f"Delay: 3 segundos (tempo real!)")
        print(f"Estrategia: {self.strategy.get_name()}")
        print("\n" + "="*70 + "\n")
        
        try:
            self.exchange = BinanceExchange()
            self.data_manager = DataManager(self.exchange)
            self.risk_manager = RiskManager(self.exchange, self.data_manager)
            self.risk_manager.initialize()
            
            # Portfolio
            self.portfolio = PortfolioManager(self.exchange, self.risk_manager, self.data_manager)
            self.portfolio.symbols = self.symbols
            self.portfolio.initialize()
            
            logger.info("Bot Cacador inicializado!")
            return True
            
        except Exception as e:
            logger.error(f"Erro na inicializacao: {e}")
            return False
    
    def executar(self):
        """Loop em TEMPO REAL"""
        self.running = True
        
        print("\n" + "="*70)
        print("BOT INICIADO - MODO CACADOR ATIVO!")
        print("Verificando", len(self.symbols), "criptos em TEMPO REAL...")
        print("Pressione Ctrl+C para parar")
        print("="*70 + "\n")
        
        ultima_info = time.time()
        
        try:
            while self.running:
                self.total_analises += 1
                
                # Obter preços atuais rapidamente
                current_prices = self.obter_precos_rapido()
                
                # Caçar oportunidades em TODAS
                for symbol in self.symbols:
                    try:
                        self.cacar_oportunidade(symbol, current_prices.get(symbol, 0))
                    except Exception as e:
                        logger.error(f"Erro em {symbol}: {e}")
                
                # Mostrar resumo a cada 30 segundos
                if time.time() - ultima_info >= 30:
                    self.mostrar_resumo(current_prices)
                    ultima_info = time.time()
                
                # Delay mínimo (TEMPO REAL!)
                time.sleep(3)  # 3 segundos = muito rápido!
                
        except KeyboardInterrupt:
            print("\n\nBot parado pelo usuario!")
            self.parar()
    
    def obter_precos_rapido(self) -> Dict[str, float]:
        """Obtém preços de todas as criptos rapidamente"""
        precos = {}
        
        for symbol in self.symbols:
            try:
                # Usar ticker (mais rápido que OHLCV)
                ticker = self.exchange.get_ticker(symbol)
                if ticker:
                    precos[symbol] = ticker['last']
            except:
                pass
        
        return precos
    
    def cacar_oportunidade(self, symbol: str, current_price: float):
        """Caça oportunidade em um símbolo"""
        
        # Se já está em posição, gerenciar
        if self.portfolio.has_position(symbol):
            self.gerenciar_posicao(symbol, current_price)
            return
        
        # Verificar se pode tradear
        pode, _ = self.risk_manager.can_trade()
        if not pode:
            return
        
        # Obter dados (usa cache se recente)
        df = self.obter_dados_com_cache(symbol)
        
        if df.empty:
            return
        
        # Analisar
        sinal = self.strategy.analyze(df)
        
        # Se OPORTUNIDADE forte, EXECUTAR IMEDIATAMENTE!
        if sinal['signal'] == 'buy' and sinal['confidence'] >= 60:
            self.oportunidades_encontradas += 1
            
            print(f"\n{'='*70}")
            print(f"OPORTUNIDADE ENCONTRADA! #{self.oportunidades_encontradas}")
            print(f"{'='*70}")
            print(f"Cripto: {symbol}")
            print(f"Preco: ${current_price:,.2f}")
            print(f"Sinal: COMPRA")
            print(f"Confianca: {sinal['confidence']:.1f}%")
            print(f"Motivo: {sinal['reason']}")
            print(f"{'='*70}\n")
            
            self.executar_compra(symbol, current_price, sinal)
    
    def obter_dados_com_cache(self, symbol: str):
        """Obtém dados usando cache (atualiza a cada 30s)"""
        agora = time.time()
        
        # Se tem cache recente (< 30s), usa
        if symbol in self.cache_time:
            if agora - self.cache_time[symbol] < 30:
                return self.cache_dados.get(symbol)
        
        # Senão, baixa novos dados
        try:
            df = self.exchange.get_ohlcv(symbol, self.settings.TIMEFRAME, limit=100)
            self.cache_dados[symbol] = df
            self.cache_time[symbol] = agora
            return df
        except:
            return self.cache_dados.get(symbol, pd.DataFrame())
    
    def executar_compra(self, symbol: str, price: float, sinal: Dict):
        """Executa compra IMEDIATAMENTE"""
        try:
            # Capital disponível
            capital = self.portfolio.get_available_capital(symbol)
            
            if capital < 10:
                return
            
            # Calcular quantidade (90% do alocado)
            quantidade = self.exchange.calculate_quantity(symbol, capital * 0.9)
            
            if quantidade <= 0:
                return
            
            # EXECUTAR!
            logger.info(f"EXECUTANDO COMPRA: {symbol}")
            ordem = self.exchange.create_market_order(symbol, 'buy', quantidade)
            
            if ordem:
                # Registrar no portfolio
                stop_loss = self.risk_manager.calculate_stop_loss(price, 'buy')
                take_profit = self.risk_manager.calculate_take_profit(price, 'buy')
                
                self.portfolio.open_position(symbol, price, quantidade, stop_loss, take_profit, ordem.get('id'))
                self.risk_manager.record_trade()
                
                print(f"\nCOMPRA EXECUTADA!")
                print(f"  {symbol}: {quantidade:.6f} @ ${price:,.2f}")
                print(f"  SL: ${stop_loss:,.2f} | TP: ${take_profit:,.2f}\n")
                
        except Exception as e:
            logger.error(f"Erro ao comprar {symbol}: {e}")
    
    def gerenciar_posicao(self, symbol: str, current_price: float):
        """Gerencia posição aberta"""
        position = self.portfolio.get_position(symbol)
        
        if not position:
            return
        
        # Verificar Stop Loss
        if current_price <= position['stop_loss']:
            logger.warning(f"{symbol}: Stop Loss atingido!")
            self.executar_venda(symbol, current_price, "Stop Loss")
            return
        
        # Verificar Take Profit
        if current_price >= position['take_profit']:
            logger.info(f"{symbol}: Take Profit atingido!")
            self.executar_venda(symbol, current_price, "Take Profit")
            return
    
    def executar_venda(self, symbol: str, price: float, motivo: str):
        """Executa venda IMEDIATAMENTE"""
        try:
            position = self.portfolio.get_position(symbol)
            
            if not position:
                return
            
            logger.info(f"EXECUTANDO VENDA: {symbol}")
            ordem = self.exchange.create_market_order(symbol, 'sell', position['quantity'])
            
            if ordem:
                trade_result = self.portfolio.close_position(symbol, price, motivo)
                
                print(f"\nVENDA EXECUTADA!")
                print(f"  {symbol}: {position['quantity']:.6f} @ ${price:,.2f}")
                print(f"  P&L: ${trade_result['pnl']:+.2f} ({trade_result['pnl_percent']:+.2f}%)")
                print(f"  Motivo: {motivo}\n")
                
        except Exception as e:
            logger.error(f"Erro ao vender {symbol}: {e}")
    
    def mostrar_resumo(self, current_prices: Dict):
        """Mostra resumo do portfolio"""
        portfolio_value = self.portfolio.calculate_portfolio_value(current_prices)
        
        print(f"\n[RESUMO] Analises: {self.total_analises} | Oportunidades: {self.oportunidades_encontradas}")
        print(f"Portfolio: ${portfolio_value['current_value']:.2f} | P&L: ${portfolio_value['total_pnl']:+.2f} ({portfolio_value['total_pnl_percent']:+.2f}%)")
        print(f"Posicoes: {portfolio_value['num_positions']}/{len(self.symbols)}")
        
        # Mostrar posições abertas
        if portfolio_value['num_positions'] > 0:
            print("\nPosicoes abertas:")
            for symbol, pos in self.portfolio.positions.items():
                preco_atual = current_prices.get(symbol, 0)
                if preco_atual > 0:
                    pnl = (preco_atual - pos['entry_price']) * pos['quantity']
                    print(f"  {symbol}: ${preco_atual:,.2f} | P&L: ${pnl:+.2f}")
    
    def parar(self):
        """Para o bot e fecha posições"""
        self.running = False
        
        print("\nFechando posicoes abertas...")
        
        # Obter preços atuais
        current_prices = self.obter_precos_rapido()
        
        # Fechar todas
        for symbol in list(self.portfolio.positions.keys()):
            price = current_prices.get(symbol, 0)
            if price > 0:
                self.executar_venda(symbol, price, "Bot parado")
        
        print("\nBot Cacador parado!")
        print(f"Total de analises: {self.total_analises}")
        print(f"Oportunidades encontradas: {self.oportunidades_encontradas}")


if __name__ == "__main__":
    import pandas as pd
    
    # CONFIGURAÇÃO
    SYMBOLS = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
    
    print("\n" + "="*70)
    print("BOT CACADOR - CAÇADOR DE OPORTUNIDADES EM TEMPO REAL")
    print("="*70)
    print("\nEste bot:")
    print("- Verifica", len(SYMBOLS), "criptos CONSTANTEMENTE")
    print("- Delay: 3 segundos (quase tempo real!)")
    print("- Executa IMEDIATAMENTE ao encontrar oportunidade")
    print("- Maximo de trades possivel!")
    print("\nDashboard: http://localhost:8501")
    print("="*70 + "\n")
    
    bot = BotCacador(symbols=SYMBOLS)
    
    if bot.inicializar():
        print("Iniciando cacada...")
        time.sleep(2)
        bot.executar()







