"""
RoboTrader - Bot de Trading Automatizado
Arquivo principal de execução
"""

import logging
import time
import signal
import sys
from datetime import datetime
from pathlib import Path

# Configurar logging
from config.settings import Settings

settings = Settings()

# Configurar logger
log_file = settings.LOGS_DIR / f'robotrader_{datetime.now().strftime("%Y%m%d")}.log'
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Imports do bot
from bot.exchange import BinanceExchange
from bot.risk_management import RiskManager
from bot.data_manager import DataManager
from bot.notifier import Notifier
from bot.strategies import TrendFollowingStrategy, MeanReversionStrategy
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()


class TradingBot:
    """
    Bot de Trading Principal
    Executa estratégias em tempo real
    """
    
    def __init__(self):
        """Inicializa o bot"""
        self.running = False
        self.settings = Settings()
        
        # Componentes
        self.exchange = None
        self.risk_manager = None
        self.data_manager = None
        self.notifier = None
        self.strategy = None
        
        # Estado
        self.current_position = None
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.highest_price = 0
        self.position_quantity = 0
    
    def initialize(self):
        """Inicializa todos os componentes"""
        try:
            logger.info("="*60)
            logger.info("🤖 ROBOTRADER - Inicializando...")
            logger.info("="*60)
            
            # Validar configurações
            valid, message = self.settings.validate_config()
            if not valid:
                logger.error(f"❌ Configuração inválida: {message}")
                return False
            
            # Mostrar configurações
            self.show_config()
            
            # Inicializar Exchange
            logger.info("📡 Conectando à Binance...")
            self.exchange = BinanceExchange()
            
            # Testar conexão
            success, msg = self.exchange.test_connection()
            if not success:
                logger.error(msg)
                return False
            logger.info(msg)
            
            # Inicializar Data Manager
            logger.info("💾 Inicializando gerenciador de dados...")
            self.data_manager = DataManager(self.exchange)
            
            # Inicializar Risk Manager
            logger.info("🛡️  Inicializando gerenciador de risco...")
            self.risk_manager = RiskManager(self.exchange, self.data_manager)
            self.risk_manager.initialize()
            
            # Inicializar Notifier
            logger.info("📱 Inicializando notificações...")
            self.notifier = Notifier()
            
            # Inicializar Estratégia
            logger.info(f"🎯 Carregando estratégia: {self.settings.STRATEGY}")
            if self.settings.STRATEGY == 'trend_following':
                self.strategy = TrendFollowingStrategy()
            elif self.settings.STRATEGY == 'mean_reversion':
                self.strategy = MeanReversionStrategy()
            else:
                logger.error(f"❌ Estratégia desconhecida: {self.settings.STRATEGY}")
                return False
            
            logger.info(f"✅ Estratégia carregada: {self.strategy.get_name()}")
            
            # Notificar início
            config_summary = self.settings.get_config_summary()
            self.notifier.notify_bot_started(config_summary)
            
            logger.info("="*60)
            logger.info("✅ Bot inicializado com sucesso!")
            logger.info("="*60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na inicialização: {e}", exc_info=True)
            return False
    
    def show_config(self):
        """Mostra configurações do bot"""
        table = Table(title="⚙️  Configurações do Bot")
        table.add_column("Parâmetro", style="cyan")
        table.add_column("Valor", style="green")
        
        config = self.settings.get_config_summary()
        for key, value in config.items():
            table.add_row(key.upper(), str(value))
        
        console.print(table)
        print()
    
    def run(self):
        """Executa o loop principal do bot"""
        try:
            self.running = True
            logger.info("▶️  Bot iniciado! Monitorando mercado...")
            
            if self.settings.PAPER_TRADING:
                logger.warning("📝 MODO PAPER TRADING - Nenhuma ordem real será executada")
            
            while self.running:
                try:
                    # Atualizar balanço e verificar risco
                    self.risk_manager.update_balance()
                    
                    # Verificar se pode tradear
                    can_trade, reason = self.risk_manager.can_trade()
                    if not can_trade:
                        logger.warning(f"⏸️  {reason}")
                        time.sleep(60)
                        continue
                    
                    # Obter dados atualizados
                    df = self.exchange.get_ohlcv(
                        symbol=self.settings.TRADING_SYMBOL,
                        timeframe=self.settings.TIMEFRAME,
                        limit=100
                    )
                    
                    if df.empty:
                        logger.warning("⚠️  Não foi possível obter dados")
                        time.sleep(30)
                        continue
                    
                    # Salvar dados históricos
                    if self.settings.SAVE_HISTORICAL_DATA:
                        self.data_manager.save_ohlcv(df)
                    
                    current_price = df['close'].iloc[-1]
                    
                    # Se tiver posição aberta, gerenciar
                    if self.current_position:
                        self.manage_position(df, current_price)
                    
                    # Se não tiver posição, procurar entrada
                    else:
                        self.look_for_entry(df, current_price)
                    
                    # Aguardar intervalo
                    logger.debug(f"💤 Aguardando {self.settings.UPDATE_INTERVAL}s...")
                    time.sleep(self.settings.UPDATE_INTERVAL)
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"❌ Erro no loop principal: {e}", exc_info=True)
                    self.notifier.notify_error(f"Erro no loop: {str(e)}")
                    time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("\n⏹️  Parando bot...")
            self.stop()
    
    def look_for_entry(self, df, current_price):
        """Procura oportunidade de entrada"""
        # Analisar com estratégia
        signal = self.strategy.analyze(df)
        
        # Se sinal forte, executar
        if signal['signal'] == 'buy' and signal['confidence'] >= 65:
            self.enter_long(current_price, signal)
        
        elif signal['signal'] == 'sell' and signal['confidence'] >= 65:
            # Note: Para spot trading na Binance, não podemos fazer short
            # Este sinal seria ignorado ou usado em futuros
            logger.info("🔴 Sinal de VENDA detectado, mas ignorado (spot trading)")
    
    def enter_long(self, price: float, signal: dict):
        """Entra em posição comprada"""
        try:
            # Calcular tamanho da posição
            position_info = self.risk_manager.calculate_position_size()
            
            if position_info['quantity'] <= 0:
                logger.warning("⚠️  Quantidade inválida para entrada")
                return
            
            # Validar ordem
            valid, msg = self.risk_manager.validate_order(
                'buy',
                self.settings.TRADING_SYMBOL,
                position_info['quantity'],
                price
            )
            
            if not valid:
                logger.warning(f"⚠️  Ordem inválida: {msg}")
                return
            
            # Executar ordem
            logger.info(f"🟢 ENTRANDO LONG @ ${price:.2f}")
            order = self.exchange.create_market_order(
                self.settings.TRADING_SYMBOL,
                'buy',
                position_info['quantity']
            )
            
            if not order:
                logger.error("❌ Falha ao executar ordem de compra")
                return
            
            # Registrar posição
            self.current_position = 'long'
            self.entry_price = price
            self.position_quantity = position_info['quantity']
            self.highest_price = price
            
            # Calcular stop loss e take profit
            self.stop_loss = self.risk_manager.calculate_stop_loss(price, 'buy')
            self.take_profit = self.risk_manager.calculate_take_profit(price, 'buy')
            
            # Registrar trade
            self.risk_manager.record_trade()
            
            # Salvar no banco
            self.data_manager.save_order(order)
            
            # Notificar
            self.notifier.notify_trade_entry(
                self.settings.TRADING_SYMBOL,
                'buy',
                position_info['quantity'],
                price,
                self.strategy.get_name()
            )
            
            logger.info(f"✅ Posição LONG aberta!")
            logger.info(f"   Quantidade: {position_info['quantity']}")
            logger.info(f"   Stop Loss: ${self.stop_loss:.2f}")
            logger.info(f"   Take Profit: ${self.take_profit:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao entrar em posição: {e}", exc_info=True)
            self.notifier.notify_error(f"Erro ao entrar em posição: {str(e)}")
    
    def manage_position(self, df, current_price):
        """Gerencia posição aberta"""
        try:
            # Atualizar preço mais alto
            if current_price > self.highest_price:
                self.highest_price = current_price
                
                # Atualizar trailing stop
                if self.settings.USE_TRAILING_STOP:
                    new_stop = self.risk_manager.calculate_trailing_stop(
                        self.entry_price,
                        current_price,
                        self.highest_price,
                        'buy'
                    )
                    
                    if new_stop and new_stop > self.stop_loss:
                        old_stop = self.stop_loss
                        self.stop_loss = new_stop
                        logger.info(f"📈 Trailing Stop atualizado: ${old_stop:.2f} → ${new_stop:.2f}")
            
            # Calcular P&L atual
            unrealized_pnl = (current_price - self.entry_price) * self.position_quantity
            pnl_percent = ((current_price - self.entry_price) / self.entry_price) * 100
            
            logger.info(f"📊 Posição LONG @ ${self.entry_price:.2f} | "
                       f"Atual: ${current_price:.2f} | "
                       f"P&L: ${unrealized_pnl:+.2f} ({pnl_percent:+.2f}%)")
            
            # Verificar se deve sair
            should_exit, reason = self.risk_manager.should_exit(
                self.entry_price,
                current_price,
                self.stop_loss,
                self.take_profit,
                'buy'
            )
            
            if should_exit:
                self.exit_position(current_price, reason)
                return
            
            # Verificar sinal da estratégia
            should_exit, reason = self.strategy.should_exit_position(df, 'buy')
            if should_exit:
                self.exit_position(current_price, reason)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerenciar posição: {e}", exc_info=True)
    
    def exit_position(self, price: float, reason: str):
        """Sai da posição atual"""
        try:
            if not self.current_position:
                return
            
            logger.info(f"🔴 SAINDO DA POSIÇÃO @ ${price:.2f} - Motivo: {reason}")
            
            # Executar ordem de venda
            order = self.exchange.create_market_order(
                self.settings.TRADING_SYMBOL,
                'sell',
                self.position_quantity
            )
            
            if not order:
                logger.error("❌ Falha ao executar ordem de venda")
                return
            
            # Calcular P&L
            pnl = (price - self.entry_price) * self.position_quantity
            pnl_percent = ((price - self.entry_price) / self.entry_price) * 100
            
            # Notificar
            self.notifier.notify_trade_exit(
                self.settings.TRADING_SYMBOL,
                'buy',
                self.position_quantity,
                self.entry_price,
                price,
                pnl,
                reason
            )
            
            emoji = "💰" if pnl > 0 else "❌"
            logger.info(f"{emoji} Posição fechada!")
            logger.info(f"   P&L: ${pnl:+.2f} ({pnl_percent:+.2f}%)")
            logger.info(f"   Motivo: {reason}")
            
            # Salvar no banco
            self.data_manager.save_order(order)
            
            # Reset
            self.current_position = None
            self.entry_price = 0
            self.position_quantity = 0
            
        except Exception as e:
            logger.error(f"❌ Erro ao sair da posição: {e}", exc_info=True)
            self.notifier.notify_error(f"Erro ao sair da posição: {str(e)}")
    
    def stop(self):
        """Para o bot"""
        self.running = False
        
        # Fechar posição se estiver aberta
        if self.current_position and self.exchange:
            logger.warning("⚠️  Fechando posição aberta...")
            current_price = self.exchange.get_current_price()
            self.exit_position(current_price, "Bot parado")
        
        # Notificar
        if self.notifier:
            self.notifier.notify_bot_stopped("Parado pelo usuário")
        
        logger.info("👋 Bot parado com sucesso!")


def signal_handler(sig, frame):
    """Handler para Ctrl+C"""
    logger.info("\n⚠️  Recebido sinal de parada...")
    if 'bot' in globals():
        bot.stop()
    sys.exit(0)


if __name__ == "__main__":
    # Registrar handler de sinal
    signal.signal(signal.SIGINT, signal_handler)
    
    # Criar e inicializar bot
    bot = TradingBot()
    
    if bot.initialize():
        # Executar
        bot.run()
    else:
        logger.error("❌ Falha na inicialização. Bot não será executado.")
        sys.exit(1)

