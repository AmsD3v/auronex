"""
Bot Adaptativo - Lê velocidade do Dashboard
Ajusta automaticamente conforme configuração
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from bot.exchange import BinanceExchange
from bot.risk_management import RiskManager
from bot.data_manager import DataManager
from bot.portfolio_manager import PortfolioManager
from bot.strategies import MeanReversionStrategy

class BotAdaptativo:
    """Bot que se adapta à configuração do dashboard"""
    
    def __init__(self, symbols: List[str] = None):
        self.settings = Settings()
        self.symbols = symbols or ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
        
        self.exchange = None
        self.risk_manager = None
        self.portfolio = None
        self.strategy = MeanReversionStrategy()
        
        self.running = False
        self.freq_bot = 3  # Padrão
        
    def ler_config(self):
        """Lê configuração do dashboard"""
        try:
            with open('bot_config.json', 'r') as f:
                config = json.load(f)
                self.freq_bot = config.get('freq_bot', 3)
                return True
        except:
            return False
    
    def inicializar(self):
        """Inicializa"""
        print("\n" + "="*70)
        print("BOT ADAPTATIVO - Controlado pelo Dashboard")
        print("="*70)
        
        try:
            print("Conectando...")
            self.exchange = BinanceExchange()
            
            self.risk_manager = RiskManager(self.exchange, None)
            self.risk_manager.initialize()
            
            self.portfolio = PortfolioManager(self.exchange, self.risk_manager, None)
            self.portfolio.symbols = self.symbols
            self.portfolio.initialize()
            
            print(f"Criptos: {', '.join(self.symbols)}")
            print("Velocidade: Controlada pelo dashboard")
            print("\nSistema pronto!\n")
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
    
    def executar(self):
        """Loop adaptativo"""
        self.running = True
        
        print("="*70)
        print("BOT EM STANDBY!")
        print("="*70)
        print("Aguardando comando INICIAR do dashboard...")
        print("Dashboard: http://localhost:8501")
        print("\nConfigure tudo e clique em 'INICIAR BOT'")
        print("Pressione Ctrl+C para sair")
        print("="*70 + "\n")
        
        ultima_config = time.time()
        bot_ativo = False
        
        try:
            while self.running:
                # Ler config e status a cada 5s
                if time.time() - ultima_config >= 5:
                    if self.ler_config():
                        if self.freq_bot != ultima_freq if 'ultima_freq' in locals() else True:
                            print(f"Config atualizada: Bot analisa a cada {self.freq_bot}s")
                            ultima_freq = self.freq_bot
                    
                    # Ler status do bot (running ou parado)
                    try:
                        with open('bot_status.json', 'r') as f:
                            status = json.load(f)
                            bot_deve_rodar = status.get('running', False)
                            
                            if bot_deve_rodar and not bot_ativo:
                                print("\n" + "="*70)
                                print("🚀 BOT ATIVADO PELO DASHBOARD!")
                                print("="*70)
                                print("Iniciando operações...")
                                print("="*70 + "\n")
                                bot_ativo = True
                            elif not bot_deve_rodar and bot_ativo:
                                print("\n" + "="*70)
                                print("⏸️  BOT PAUSADO PELO DASHBOARD!")
                                print("="*70)
                                print("Operações pausadas")
                                print("="*70 + "\n")
                                bot_ativo = False
                    except:
                        pass
                    
                    ultima_config = time.time()
                
                # SÓ OPERAR SE BOT ESTIVER ATIVO
                if bot_ativo:
                    # Obter preços
                    precos = {}
                    for symbol in self.symbols:
                        try:
                            ticker = self.exchange.get_ticker(symbol)
                            if ticker:
                                precos[symbol] = ticker['last']
                        except:
                            pass
                    
                    # Processar cada cripto
                    for symbol in self.symbols:
                        if symbol in precos:
                            self.processar(symbol, precos[symbol])
                
                # Aguardar conforme configuração
                time.sleep(self.freq_bot)
                
        except KeyboardInterrupt:
            print("\n\nParando...")
            self.parar()
    
    def processar(self, symbol: str, price: float):
        """Processa uma cripto"""
        
        if self.portfolio.has_position(symbol):
            position = self.portfolio.get_position(symbol)
            
            # Stop Loss
            if price <= position['stop_loss']:
                self.vender(symbol, price, "STOP LOSS")
                return
            
            # Take Profit
            if price >= position['take_profit']:
                self.vender(symbol, price, "TAKE PROFIT")
                return
        else:
            # Procurar entrada
            pode, _ = self.risk_manager.can_trade()
            if not pode:
                return
            
            try:
                df = self.exchange.get_ohlcv(symbol, self.settings.TIMEFRAME, limit=100)
                if df.empty:
                    return
                
                sinal = self.strategy.analyze(df)
                
                if sinal['signal'] == 'buy' and sinal['confidence'] >= 60:
                    self.comprar(symbol, price, sinal)
            except:
                pass
    
    def comprar(self, symbol: str, price: float, sinal: Dict):
        """Compra"""
        try:
            capital = self.portfolio.get_available_capital(symbol)
            if capital < 10:
                return
            
            quantidade = self.exchange.calculate_quantity(symbol, capital * 0.9)
            if quantidade <= 0:
                return
            
            print(f"\n{'='*70}")
            print(f"COMPRANDO {symbol}")
            print(f"{'='*70}")
            print(f"Preco: ${price:,.2f}")
            print(f"Qtd: {quantidade:.6f}")
            print(f"Confianca: {sinal['confidence']:.0f}%")
            print(f"{'='*70}\n")
            
            ordem = self.exchange.create_market_order(symbol, 'buy', quantidade)
            
            if ordem:
                sl = self.risk_manager.calculate_stop_loss(price, 'buy')
                tp = self.risk_manager.calculate_take_profit(price, 'buy')
                
                self.portfolio.open_position(symbol, price, quantidade, sl, tp, ordem.get('id'))
                self.risk_manager.record_trade()
                
                print(f"COMPRA EXECUTADA!")
                print(f"SL: ${sl:,.2f} | TP: ${tp:,.2f}\n")
        except Exception as e:
            print(f"Erro: {e}")
    
    def vender(self, symbol: str, price: float, motivo: str):
        """Venda"""
        try:
            position = self.portfolio.get_position(symbol)
            if not position:
                return
            
            pnl = (price - position['entry_price']) * position['quantity']
            pnl_pct = ((price - position['entry_price']) / position['entry_price']) * 100
            
            print(f"\n{'='*70}")
            print(f"VENDENDO {symbol}")
            print(f"{'='*70}")
            print(f"Motivo: {motivo}")
            print(f"P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
            print(f"{'='*70}\n")
            
            ordem = self.exchange.create_market_order(symbol, 'sell', position['quantity'])
            
            if ordem:
                self.portfolio.close_position(symbol, price, motivo)
                print(f"VENDA EXECUTADA!\n")
        except Exception as e:
            print(f"Erro: {e}")
    
    def parar(self):
        """Para"""
        self.running = False
        print("\nBot parado!")

if __name__ == "__main__":
    SYMBOLS = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
    
    bot = BotAdaptativo(symbols=SYMBOLS)
    
    if bot.inicializar():
        print("Configure a velocidade no Dashboard!")
        print("Dashboard: http://localhost:8501\n")
        time.sleep(2)
        bot.executar()


