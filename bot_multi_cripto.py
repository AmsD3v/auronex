"""
Bot Multi-Cripto - Opera em várias criptomoedas simultaneamente
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging
log_file = Path('bot_multi_cripto.log')
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

class BotMultiCripto:
    """Bot que opera múltiplas criptomoedas"""
    
    def __init__(self, capital_total: float = None, symbols: List[str] = None):
        """
        Inicializa bot multi-cripto
        
        Args:
            capital_total: Capital total para dividir
            symbols: Lista de símbolos para operar
        """
        self.settings = Settings()
        self.capital_total = capital_total
        self.symbols = symbols or ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
        
        # Componentes
        self.exchange = None
        self.risk_manager = None
        self.data_manager = None
        self.portfolio = None
        self.strategy = MeanReversionStrategy()
        
        self.running = False
    
    def inicializar(self):
        """Inicializa o bot"""
        print("\n" + "="*70)
        print("BOT MULTI-CRIPTO")
        print("="*70)
        print(f"\nCriptomoedas: {', '.join(self.symbols)}")
        print(f"Capital Total: ${self.capital_total or 'Saldo completo'}")
        print(f"Estrategia: {self.strategy.get_name()}")
        print("\n" + "="*70 + "\n")
        
        try:
            self.exchange = BinanceExchange()
            self.data_manager = DataManager(self.exchange)
            self.risk_manager = RiskManager(self.exchange, self.data_manager)
            self.risk_manager.initialize()
            
            # Inicializar portfolio
            self.portfolio = PortfolioManager(self.exchange, self.risk_manager, self.data_manager)
            self.portfolio.symbols = self.symbols
            self.portfolio.initialize(self.capital_total)
            
            logger.info("Bot multi-cripto inicializado!")
            return True
            
        except Exception as e:
            logger.error(f"Erro na inicializacao: {e}")
            return False
    
    def executar(self):
        """Loop principal"""
        self.running = True
        
        print("\nBot iniciado! Monitorando", len(self.symbols), "criptomoedas...")
        print("Pressione Ctrl+C para parar\n")
        
        iteracao = 0
        
        try:
            while self.running:
                iteracao += 1
                print(f"\n[{iteracao}] {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 70)
                
                # Obter preços atuais
                current_prices = {}
                for symbol in self.symbols:
                    try:
                        price = self.exchange.get_current_price(symbol)
                        current_prices[symbol] = price
                    except:
                        pass
                
                # Para cada símbolo
                for symbol in self.symbols:
                    try:
                        self.processar_simbolo(symbol, current_prices.get(symbol, 0))
                    except Exception as e:
                        logger.error(f"Erro ao processar {symbol}: {e}")
                
                # Mostrar resumo do portfolio
                self.mostrar_resumo(current_prices)
                
                # Aguardar
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n\nBot parado pelo usuario!")
            self.parar()
    
    def processar_simbolo(self, symbol: str, current_price: float):
        """Processa um símbolo"""
        # Se já está em posição, gerenciar
        if self.portfolio.has_position(symbol):
            self.gerenciar_posicao(symbol, current_price)
        else:
            # Procurar entrada
            self.procurar_entrada(symbol, current_price)
    
    def procurar_entrada(self, symbol: str, current_price: float):
        """Procura oportunidade de entrada"""
        # Obter dados
        df = self.exchange.get_ohlcv(symbol, self.settings.TIMEFRAME, limit=100)
        
        if df.empty:
            return
        
        # Analisar
        signal = self.strategy.analyze(df)
        
        # Se sinal forte de compra
        if signal['signal'] == 'buy' and signal['confidence'] >= 60:
            logger.info(f"{symbol}: COMPRA detectada ({signal['confidence']:.0f}%)")
            self.comprar(symbol, current_price, signal)
    
    def comprar(self, symbol: str, price: float, signal: Dict):
        """Executa compra"""
        try:
            # Capital disponível para este símbolo
            capital = self.portfolio.get_available_capital(symbol)
            
            if capital <= 10:
                return
            
            # Calcular quantidade
            quantidade = self.exchange.calculate_quantity(symbol, capital * 0.9)  # 90% do alocado
            
            if quantidade <= 0:
                return
            
            # Executar ordem
            ordem = self.exchange.create_market_order(symbol, 'buy', quantidade)
            
            if ordem:
                # Calcular SL e TP
                stop_loss = self.risk_manager.calculate_stop_loss(price, 'buy')
                take_profit = self.risk_manager.calculate_take_profit(price, 'buy')
                
                # Registrar no portfolio
                self.portfolio.open_position(symbol, price, quantidade, stop_loss, take_profit, ordem.get('id'))
                
                print(f"\n  {symbol}: COMPRA @ ${price:,.2f}")
                print(f"    Qtd: {quantidade:.6f}")
                print(f"    SL: ${stop_loss:,.2f} | TP: ${take_profit:,.2f}")
                
        except Exception as e:
            logger.error(f"Erro ao comprar {symbol}: {e}")
    
    def gerenciar_posicao(self, symbol: str, current_price: float):
        """Gerencia posição aberta"""
        position = self.portfolio.get_position(symbol)
        
        if not position:
            return
        
        # Calcular P&L
        pnl = (current_price - position['entry_price']) * position['quantity']
        pnl_percent = ((current_price - position['entry_price']) / position['entry_price']) * 100
        
        print(f"  {symbol}: ${current_price:,.2f} | P&L: ${pnl:+.2f} ({pnl_percent:+.2f}%)")
        
        # Verificar Stop Loss
        if current_price <= position['stop_loss']:
            logger.warning(f"{symbol}: Stop Loss atingido!")
            self.vender(symbol, current_price, "Stop Loss")
            return
        
        # Verificar Take Profit
        if current_price >= position['take_profit']:
            logger.info(f"{symbol}: Take Profit atingido!")
            self.vender(symbol, current_price, "Take Profit")
            return
    
    def vender(self, symbol: str, price: float, reason: str):
        """Executa venda"""
        try:
            position = self.portfolio.get_position(symbol)
            
            if not position:
                return
            
            # Executar ordem
            ordem = self.exchange.create_market_order(symbol, 'sell', position['quantity'])
            
            if ordem:
                # Fechar no portfolio
                trade_result = self.portfolio.close_position(symbol, price, reason)
                
                print(f"\n  {symbol}: VENDA @ ${price:,.2f}")
                print(f"    P&L: ${trade_result['pnl']:+.2f} ({trade_result['pnl_percent']:+.2f}%)")
                print(f"    Motivo: {reason}")
                
        except Exception as e:
            logger.error(f"Erro ao vender {symbol}: {e}")
    
    def mostrar_resumo(self, current_prices: Dict):
        """Mostra resumo do portfolio"""
        portfolio_value = self.portfolio.calculate_portfolio_value(current_prices)
        
        print(f"\nPORTFOLIO: ${portfolio_value['current_value']:.2f} | P&L: ${portfolio_value['total_pnl']:+.2f} ({portfolio_value['total_pnl_percent']:+.2f}%)")
        print(f"Posicoes abertas: {portfolio_value['num_positions']}/{len(self.symbols)}")
    
    def parar(self):
        """Para o bot"""
        self.running = False
        
        # Fechar todas as posições
        current_prices = {}
        for symbol in self.symbols:
            try:
                current_prices[symbol] = self.exchange.get_current_price(symbol)
            except:
                pass
        
        for symbol in list(self.positions.keys()):
            price = current_prices.get(symbol, 0)
            if price > 0:
                self.vender(symbol, price, "Bot parado")
        
        logger.info("Bot parado!")


if __name__ == "__main__":
    from typing import List
    
    # Configuração
    CAPITAL = 10000  # $10,000 USDT do testnet
    SYMBOLS = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
    
    bot = BotMultiCripto(capital_total=CAPITAL, symbols=SYMBOLS)
    
    if bot.inicializar():
        print(f"\nDashboard: http://localhost:8501")
        print("Para monitorar em tempo real!\n")
        bot.executar()







