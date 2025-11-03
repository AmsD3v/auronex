"""
Bot Automatico - Executa trades reais no Testnet
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging
log_file = Path('bot_automatico.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Imports
from config.settings import Settings
from bot.exchange import BinanceExchange
from bot.risk_management import RiskManager
from bot.data_manager import DataManager
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy

class BotAutomatico:
    """Bot que executa trades automaticamente"""
    
    def __init__(self):
        self.settings = Settings()
        self.exchange = None
        self.risk_manager = None
        self.data_manager = None
        self.strategy = None
        self.running = False
        
        # Posição atual
        self.em_posicao = False
        self.preco_entrada = 0
        self.quantidade = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.ordem_compra_id = None
    
    def inicializar(self):
        """Inicializa o bot"""
        print("\n" + "="*70)
        print("ROBOTRADER - BOT AUTOMATICO")
        print("="*70)
        print(f"\nModo: {'TESTNET' if self.settings.USE_TESTNET else 'PRODUCAO'}")
        print(f"Paper Trading: {'SIM' if self.settings.PAPER_TRADING else 'NAO - TRADING REAL!'}")
        print(f"Simbolo: {self.settings.TRADING_SYMBOL}")
        print(f"Estrategia: {self.settings.STRATEGY}")
        print(f"Stop Loss: {self.settings.STOP_LOSS_PERCENT*100}%")
        print(f"Take Profit: {self.settings.TAKE_PROFIT_PERCENT*100}%")
        print("\n" + "="*70 + "\n")
        
        try:
            logger.info("Conectando a Binance...")
            self.exchange = BinanceExchange()
            
            logger.info("Inicializando gerenciadores...")
            self.data_manager = DataManager(self.exchange)
            self.risk_manager = RiskManager(self.exchange, self.data_manager)
            self.risk_manager.initialize()
            
            # Criar estratégia
            if self.settings.STRATEGY == 'mean_reversion':
                self.strategy = MeanReversionStrategy()
            else:
                self.strategy = TrendFollowingStrategy()
            
            logger.info(f"Estrategia carregada: {self.strategy.get_name()}")
            logger.info("Bot inicializado com sucesso!")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na inicializacao: {e}")
            return False
    
    def executar(self):
        """Loop principal do bot"""
        self.running = True
        
        print("\n" + "="*70)
        print("BOT INICIADO - Monitorando mercado...")
        print("Pressione Ctrl+C para parar")
        print("="*70 + "\n")
        
        iteracao = 0
        
        try:
            while self.running:
                iteracao += 1
                logger.info(f"\n[{iteracao}] Analisando mercado...")
                
                # Obter dados
                df = self.exchange.get_ohlcv(
                    self.settings.TRADING_SYMBOL,
                    self.settings.TIMEFRAME,
                    limit=100
                )
                
                if df.empty:
                    logger.warning("Nao foi possivel obter dados")
                    time.sleep(60)
                    continue
                
                preco_atual = df['close'].iloc[-1]
                logger.info(f"Preco atual: ${preco_atual:,.2f}")
                
                # Se não está em posição, procurar entrada
                if not self.em_posicao:
                    self.procurar_entrada(df, preco_atual)
                else:
                    self.gerenciar_posicao(df, preco_atual)
                
                # Aguardar 60 segundos
                logger.info("Aguardando 60 segundos...")
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n\nBot interrompido pelo usuario!")
            self.parar()
        except Exception as e:
            logger.error(f"Erro no loop: {e}")
            import traceback
            traceback.print_exc()
    
    def procurar_entrada(self, df, preco_atual):
        """Procura oportunidade de entrada"""
        # Verificar se pode tradear
        pode_tradear, motivo = self.risk_manager.can_trade()
        if not pode_tradear:
            logger.warning(f"Nao pode tradear: {motivo}")
            return
        
        # Analisar mercado
        sinal = self.strategy.analyze(df)
        
        logger.info(f"Sinal: {sinal['signal'].upper()} (Confianca: {sinal['confidence']:.1f}%)")
        logger.info(f"Motivo: {sinal['reason']}")
        
        # Se sinal forte de COMPRA
        if sinal['signal'] == 'buy' and sinal['confidence'] >= 65:
            logger.info("\n" + "="*70)
            logger.info("OPORTUNIDADE DE COMPRA DETECTADA!")
            logger.info("="*70)
            
            self.comprar(preco_atual, sinal)
    
    def comprar(self, preco, sinal):
        """Executa compra"""
        try:
            # Calcular tamanho da posicao
            posicao = self.risk_manager.calculate_position_size(self.settings.TRADING_SYMBOL)
            
            if posicao['quantity'] <= 0:
                logger.warning("Quantidade invalida")
                return
            
            logger.info(f"Comprando {posicao['quantity']} {self.settings.TRADING_SYMBOL}")
            logger.info(f"Valor: ${posicao['usdt_amount']:.2f} USDT")
            
            # Executar ordem
            ordem = self.exchange.create_market_order(
                self.settings.TRADING_SYMBOL,
                'buy',
                posicao['quantity']
            )
            
            if ordem:
                self.em_posicao = True
                self.preco_entrada = preco
                self.quantidade = posicao['quantity']
                self.ordem_compra_id = ordem.get('id')
                
                # Calcular SL e TP
                self.stop_loss = self.risk_manager.calculate_stop_loss(preco, 'buy')
                self.take_profit = self.risk_manager.calculate_take_profit(preco, 'buy')
                
                self.risk_manager.record_trade()
                self.data_manager.save_order(ordem)
                
                print("\n" + "="*70)
                print("COMPRA EXECUTADA!")
                print("="*70)
                print(f"Preco de Entrada: ${self.preco_entrada:,.2f}")
                print(f"Quantidade: {self.quantidade}")
                print(f"Stop Loss: ${self.stop_loss:,.2f} (-{self.settings.STOP_LOSS_PERCENT*100}%)")
                print(f"Take Profit: ${self.take_profit:,.2f} (+{self.settings.TAKE_PROFIT_PERCENT*100}%)")
                print("="*70 + "\n")
                
                logger.info("Posicao aberta com sucesso!")
            else:
                logger.error("Falha ao executar ordem de compra")
                
        except Exception as e:
            logger.error(f"Erro ao comprar: {e}")
    
    def gerenciar_posicao(self, df, preco_atual):
        """Gerencia posição aberta"""
        # Calcular P&L
        pnl = (preco_atual - self.preco_entrada) * self.quantidade
        pnl_percent = ((preco_atual - self.preco_entrada) / self.preco_entrada) * 100
        
        logger.info(f"EM POSICAO - Entrada: ${self.preco_entrada:,.2f} | Atual: ${preco_atual:,.2f}")
        logger.info(f"P&L: ${pnl:+.2f} ({pnl_percent:+.2f}%)")
        
        # Verificar Stop Loss
        if preco_atual <= self.stop_loss:
            logger.warning("STOP LOSS ATINGIDO!")
            self.vender(preco_atual, "Stop Loss atingido")
            return
        
        # Verificar Take Profit
        if preco_atual >= self.take_profit:
            logger.info("TAKE PROFIT ATINGIDO!")
            self.vender(preco_atual, "Take Profit atingido")
            return
        
        # Verificar sinal da estratégia
        deve_sair, motivo = self.strategy.should_exit_position(df, 'buy')
        if deve_sair:
            logger.info(f"Estrategia sinalizou saida: {motivo}")
            self.vender(preco_atual, motivo)
    
    def vender(self, preco, motivo):
        """Executa venda"""
        try:
            logger.info(f"Vendendo {self.quantidade} {self.settings.TRADING_SYMBOL}")
            
            ordem = self.exchange.create_market_order(
                self.settings.TRADING_SYMBOL,
                'sell',
                self.quantidade
            )
            
            if ordem:
                # Calcular resultado
                pnl = (preco - self.preco_entrada) * self.quantidade
                pnl_percent = ((preco - self.preco_entrada) / self.preco_entrada) * 100
                
                self.data_manager.save_order(ordem)
                
                print("\n" + "="*70)
                print("VENDA EXECUTADA!")
                print("="*70)
                print(f"Preco de Entrada: ${self.preco_entrada:,.2f}")
                print(f"Preco de Saida: ${preco:,.2f}")
                print(f"Quantidade: {self.quantidade}")
                print(f"Motivo: {motivo}")
                print(f"\nRESULTADO: ${pnl:+.2f} ({pnl_percent:+.2f}%)")
                
                if pnl > 0:
                    print("LUCRO! Parabens!")
                else:
                    print("Prejuizo - Mas loss limitado pelo SL!")
                
                print("="*70 + "\n")
                
                # Reset
                self.em_posicao = False
                self.preco_entrada = 0
                self.quantidade = 0
                
                logger.info(f"Posicao fechada: {motivo}")
            else:
                logger.error("Falha ao executar venda")
                
        except Exception as e:
            logger.error(f"Erro ao vender: {e}")
    
    def parar(self):
        """Para o bot"""
        self.running = False
        
        # Se tiver posição aberta, fechar
        if self.em_posicao:
            logger.warning("Fechando posicao aberta...")
            preco_atual = self.exchange.get_current_price(self.settings.TRADING_SYMBOL)
            self.vender(preco_atual, "Bot parado pelo usuario")
        
        logger.info("Bot parado!")


if __name__ == "__main__":
    bot = BotAutomatico()
    
    if bot.inicializar():
        print("\nDeixe o dashboard aberto em: http://localhost:8501")
        print("Para ver lucro/prejuizo em tempo real!\n")
        bot.executar()
    else:
        print("Erro na inicializacao!")







