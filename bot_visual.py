"""
Bot Visual - Feedback Claro de Todas as Ações
Mostra CLARAMENTE o que está fazendo
"""

import sys
import time
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

class BotVisual:
    """Bot com feedback visual completo"""
    
    def __init__(self, symbols: List[str] = None):
        self.settings = Settings()
        self.symbols = symbols or ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
        
        self.exchange = None
        self.risk_manager = None
        self.data_manager = None
        self.portfolio = None
        self.strategy = MeanReversionStrategy()
        
        self.running = False
        self.total_analises = 0
        self.total_compras = 0
        self.total_vendas = 0
        self.cache_dados = {}
        self.cache_time = {}
    
    def inicializar(self):
        """Inicializa"""
        self.limpar_tela()
        self.print_header()
        
        try:
            print("Conectando a Binance...")
            self.exchange = BinanceExchange()
            
            print("Inicializando sistemas...")
            self.data_manager = DataManager(self.exchange)
            self.risk_manager = RiskManager(self.exchange, self.data_manager)
            self.risk_manager.initialize()
            
            self.portfolio = PortfolioManager(self.exchange, self.risk_manager, self.data_manager)
            self.portfolio.symbols = self.symbols
            self.portfolio.initialize()
            
            print("Sistema pronto!\n")
            return True
            
        except Exception as e:
            print(f"ERRO: {e}")
            return False
    
    def executar(self):
        """Loop principal"""
        self.running = True
        
        print("="*70)
        print("CACADOR INICIADO - MODO VISUAL ATIVO!")
        print("="*70)
        print(f"Criptos: {', '.join(self.symbols)}")
        print("Delay: 3 segundos (tempo real)")
        print("Pressione Ctrl+C para parar")
        print("="*70 + "\n")
        
        ultima_info = time.time()
        ultima_limpeza = time.time()
        
        try:
            while self.running:
                self.total_analises += 1
                
                # Limpar tela a cada 2 minutos
                if time.time() - ultima_limpeza >= 120:
                    self.limpar_tela()
                    self.print_header()
                    ultima_limpeza = time.time()
                
                # Obter preços
                precos = self.obter_precos_rapido()
                
                # Caçar em TODAS
                for symbol in self.symbols:
                    self.processar_cripto(symbol, precos.get(symbol, 0))
                
                # Resumo a cada 30s
                if time.time() - ultima_info >= 30:
                    self.mostrar_status(precos)
                    ultima_info = time.time()
                
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("\n\nParando bot...")
            self.parar()
    
    def processar_cripto(self, symbol: str, price: float):
        """Processa uma cripto"""
        
        # Gerenciar posição
        if self.portfolio.has_position(symbol):
            self.gerenciar_posicao(symbol, price)
            return
        
        # Procurar entrada
        pode, _ = self.risk_manager.can_trade()
        if not pode:
            return
        
        df = self.obter_dados_com_cache(symbol)
        if df.empty:
            return
        
        sinal = self.strategy.analyze(df)
        
        # COMPRAR!
        if sinal['signal'] == 'buy' and sinal['confidence'] >= 60:
            self.comprar(symbol, price, sinal)
    
    def comprar(self, symbol: str, price: float, sinal: Dict):
        """COMPRA com feedback visual"""
        try:
            capital = self.portfolio.get_available_capital(symbol)
            if capital < 10:
                return
            
            quantidade = self.exchange.calculate_quantity(symbol, capital * 0.9)
            if quantidade <= 0:
                return
            
            # VISUAL: COMPRANDO
            print("\n" + "="*70)
            print(f"  COMPRANDO {symbol}")
            print("="*70)
            print(f"  Hora: {datetime.now().strftime('%H:%M:%S')}")
            print(f"  Preco: ${price:,.2f}")
            print(f"  Quantidade: {quantidade:.6f}")
            print(f"  Valor: ${capital * 0.9:.2f}")
            print(f"  Confianca: {sinal['confidence']:.0f}%")
            print(f"  Motivo: {sinal['reason']}")
            print("="*70)
            
            ordem = self.exchange.create_market_order(symbol, 'buy', quantidade)
            
            if ordem:
                self.total_compras += 1
                
                sl = self.risk_manager.calculate_stop_loss(price, 'buy')
                tp = self.risk_manager.calculate_take_profit(price, 'buy')
                
                self.portfolio.open_position(symbol, price, quantidade, sl, tp, ordem.get('id'))
                self.risk_manager.record_trade()
                
                print(f"  COMPRA #{self.total_compras} EXECUTADA!")
                print(f"  Stop Loss: ${sl:,.2f} (-{self.settings.STOP_LOSS_PERCENT*100}%)")
                print(f"  Take Profit: ${tp:,.2f} (+{self.settings.TAKE_PROFIT_PERCENT*100}%)")
                print("="*70 + "\n")
                
        except Exception as e:
            print(f"  ERRO ao comprar: {e}\n")
    
    def gerenciar_posicao(self, symbol: str, price: float):
        """Gerencia posição"""
        position = self.portfolio.get_position(symbol)
        if not position:
            return
        
        # Stop Loss
        if price <= position['stop_loss']:
            self.vender(symbol, price, "STOP LOSS ATIVADO")
            return
        
        # Take Profit  
        if price >= position['take_profit']:
            self.vender(symbol, price, "TAKE PROFIT ATINGIDO")
            return
    
    def vender(self, symbol: str, price: float, motivo: str):
        """VENDA com feedback visual"""
        try:
            position = self.portfolio.get_position(symbol)
            if not position:
                return
            
            pnl = (price - position['entry_price']) * position['quantity']
            pnl_pct = ((price - position['entry_price']) / position['entry_price']) * 100
            
            # VISUAL: VENDENDO
            print("\n" + "="*70)
            print(f"  VENDENDO {symbol}")
            print("="*70)
            print(f"  Hora: {datetime.now().strftime('%H:%M:%S')}")
            print(f"  Preco Entrada: ${position['entry_price']:,.2f}")
            print(f"  Preco Saida: ${price:,.2f}")
            print(f"  Quantidade: {position['quantity']:.6f}")
            print(f"  Motivo: {motivo}")
            print("-"*70)
            
            ordem = self.exchange.create_market_order(symbol, 'sell', position['quantity'])
            
            if ordem:
                self.total_vendas += 1
                
                self.portfolio.close_position(symbol, price, motivo)
                
                if pnl > 0:
                    print(f"  LUCRO! +${pnl:.2f} (+{pnl_pct:.2f}%)")
                else:
                    print(f"  Prejuizo: ${pnl:.2f} ({pnl_pct:.2f}%)")
                
                print(f"  VENDA #{self.total_vendas} EXECUTADA!")
                print("="*70 + "\n")
                
        except Exception as e:
            print(f"  ERRO ao vender: {e}\n")
    
    def obter_precos_rapido(self) -> Dict[str, float]:
        """Obtém preços"""
        precos = {}
        for symbol in self.symbols:
            try:
                ticker = self.exchange.get_ticker(symbol)
                if ticker:
                    precos[symbol] = ticker['last']
            except:
                pass
        return precos
    
    def obter_dados_com_cache(self, symbol: str):
        """Obtém dados com cache"""
        agora = time.time()
        
        if symbol in self.cache_time:
            if agora - self.cache_time[symbol] < 30:
                return self.cache_dados.get(symbol, pd.DataFrame())
        
        try:
            df = self.exchange.get_ohlcv(symbol, self.settings.TIMEFRAME, limit=100)
            self.cache_dados[symbol] = df
            self.cache_time[symbol] = agora
            return df
        except:
            return self.cache_dados.get(symbol, pd.DataFrame())
    
    def mostrar_status(self, precos: Dict):
        """Status a cada 30s"""
        portfolio_value = self.portfolio.calculate_portfolio_value(precos)
        
        print("\n" + "-"*70)
        print(f"STATUS - {datetime.now().strftime('%H:%M:%S')}")
        print("-"*70)
        print(f"Analises: {self.total_analises} | Compras: {self.total_compras} | Vendas: {self.total_vendas}")
        print(f"Portfolio: ${portfolio_value['current_value']:.2f}")
        print(f"P&L Total: ${portfolio_value['total_pnl']:+.2f} ({portfolio_value['total_pnl_percent']:+.2f}%)")
        print(f"Posicoes: {portfolio_value['num_positions']}/{len(self.symbols)}")
        
        if portfolio_value['num_positions'] > 0:
            print("\nPosicoes abertas:")
            for symbol, pos in self.portfolio.positions.items():
                preco = precos.get(symbol, 0)
                if preco > 0:
                    pnl = (preco - pos['entry_price']) * pos['quantity']
                    pnl_pct = ((preco - pos['entry_price']) / pos['entry_price']) * 100
                    status = "LUCRO" if pnl > 0 else "Prejuizo"
                    print(f"  {symbol}: ${preco:,.2f} | {status}: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        
        print("-"*70 + "\n")
    
    def parar(self):
        """Para e fecha tudo"""
        self.running = False
        
        print("\nFechando posicoes...")
        precos = self.obter_precos_rapido()
        
        for symbol in list(self.portfolio.positions.keys()):
            price = precos.get(symbol, 0)
            if price > 0:
                self.vender(symbol, price, "Bot parado")
        
        print("\n" + "="*70)
        print("BOT PARADO")
        print("="*70)
        print(f"Total Analises: {self.total_analises}")
        print(f"Total Compras: {self.total_compras}")
        print(f"Total Vendas: {self.total_vendas}")
        print("="*70 + "\n")
    
    def limpar_tela(self):
        """Limpa terminal"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Header visual"""
        print("\n" + "="*70)
        print("  ROBOTRADER - BOT CACADOR VISUAL")
        print("="*70)
        print(f"  Modo: Multi-Cripto Tempo Real")
        print(f"  Criptos: {len(self.symbols)} ({', '.join([s.replace('USDT','') for s in self.symbols])})")
        print(f"  Delay: 3 segundos")
        print(f"  Status: CACANDO OPORTUNIDADES...")
        print("="*70 + "\n")


if __name__ == "__main__":
    
    SYMBOLS = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
    
    bot = BotVisual(symbols=SYMBOLS)
    
    if bot.inicializar():
        time.sleep(1)
        bot.executar()





