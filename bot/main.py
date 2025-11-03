"""
BOT PRINCIPAL - Sistema de Trading Automatizado
Executa trades reais baseado nas estratégias configuradas
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from bot.exchange import BinanceExchange
from bot.data_manager import DataManager
from bot.risk_management import RiskManager
from bot.portfolio_manager import PortfolioManager
from bot.strategies import TrendFollowingStrategy, MeanReversionStrategy
from bot.notifier import Notifier

from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, Trade

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_trading.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TradingBot:
    """Bot principal de trading"""
    
    def __init__(self, bot_config_id: int):
        """
        Inicializa o bot
        
        Args:
            bot_config_id: ID da configuração do bot no banco
        """
        self.bot_config_id = bot_config_id
        self.is_running = False
        self.config = None
        
        # Componentes
        self.exchange = None
        self.data_manager = None
        self.risk_manager = None
        self.portfolio_manager = None
        self.strategy = None
        self.notifier = Notifier()
        
        logger.info(f"Bot {bot_config_id} inicializado")
    
    def load_config(self):
        """Carrega configuração do banco de dados"""
        try:
            db = SessionLocal()
            bot_config = db.query(BotConfiguration).filter(
                BotConfiguration.id == self.bot_config_id
            ).first()
            
            if not bot_config:
                logger.error(f"[ERRO] Bot {self.bot_config_id} nao encontrado!")
                return False
            
            self.config = {
                'name': bot_config.name,
                'exchange': bot_config.exchange,
                'symbols': bot_config.symbols if isinstance(bot_config.symbols, list) else [bot_config.symbols],
                'strategy': bot_config.strategy,
                'timeframe': bot_config.timeframe,
                'stop_loss': float(bot_config.stop_loss_percent) / 100,
                'take_profit': float(bot_config.take_profit_percent) / 100,
                'is_active': bot_config.is_active,
                'user_id': bot_config.user_id
            }
            
            db.close()
            
            logger.info(f"[OK] Configuração carregada: {self.config['name']}")
            return True
            
        except Exception as e:
            logger.error(f"[OK] Erro ao carregar config: {e}")
            return False
    
    def initialize_components(self):
        """Inicializa componentes do bot"""
        try:
            # Exchange usando API Key DO USUÁRIO
            from fastapi_app.models import ExchangeAPIKey
            from fastapi_app.utils.encryption import decrypt_data
            import ccxt
            
            db = SessionLocal()
            
            # Buscar API Key do usuário
            api_key = db.query(ExchangeAPIKey).filter(
                ExchangeAPIKey.user_id == self.config['user_id'],
                ExchangeAPIKey.exchange == self.config['exchange'],
                ExchangeAPIKey.is_active == True
            ).first()
            
            db.close()
            
            if not api_key:
                logger.error(f"API Key nao encontrada para {self.config['exchange']}")
                return False
            
            # Descriptografar
            api_dec = decrypt_data(api_key.api_key_encrypted)
            secret_dec = decrypt_data(api_key.secret_key_encrypted)
            
            # Mapeamento
            ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
            ccxt_name = ccxt_map.get(self.config['exchange'], self.config['exchange'])
            
            # Criar exchange
            exchange_class = getattr(ccxt, ccxt_name)
            self.exchange = exchange_class({
                'apiKey': api_dec,
                'secret': secret_dec,
                'enableRateLimit': True
            })
            
            if api_key.is_testnet:
                self.exchange.set_sandbox_mode(True)
            
            logger.info(f"[OK] Exchange {self.config['exchange']} conectada")
            
            # Criar wrapper (compatibilidade com BinanceExchange)
            class ExchangeWrapper:
                def __init__(self, ccxt_exchange):
                    self.exchange = ccxt_exchange
                
                def get_usdt_balance(self):
                    bal = self.exchange.fetch_balance()
                    usdt = bal.get('free', {}).get('USDT', 0) or bal.get('USDT', {}).get('free', 0) or 0
                    if usdt == 0:
                        brl = bal.get('free', {}).get('BRL', 0) or 0
                        usdt = brl / 5.0 if brl > 0 else 0
                    return usdt
                
                def get_current_price(self, symbol):
                    ticker = self.exchange.fetch_ticker(symbol)
                    return ticker['last']
                
                def place_order(self, symbol, side, order_type, quantity):
                    return self.exchange.create_order(symbol, order_type, side, quantity)
                
                def calculate_quantity(self, symbol, usdt_amount):
                    price = self.get_current_price(symbol)
                    return usdt_amount / price
            
            self.exchange = ExchangeWrapper(self.exchange)
            
            # Data Manager
            self.data_manager = DataManager(self.exchange)
            
            # Risk Manager
            self.risk_manager = RiskManager(self.exchange, self.data_manager)
            self.risk_manager.initialize()
            
            # Portfolio Manager
            self.portfolio_manager = PortfolioManager(
                self.exchange,
                self.risk_manager,
                self.data_manager
            )
            self.portfolio_manager.symbols = self.config['symbols']
            self.portfolio_manager.initialize()
            
            # Estratégia
            if self.config['strategy'] == 'trend_following':
                self.strategy = TrendFollowingStrategy()
            else:
                self.strategy = MeanReversionStrategy()
            
            logger.info(f"[OK] Componentes inicializados para {self.config['name']}")
            return True
            
        except Exception as e:
            logger.error(f"[OK] Erro ao inicializar componentes: {e}")
            return False
    
    def check_and_execute_trade(self, symbol: str):
        """
        Verifica sinal e executa trade se necessário
        
        Args:
            symbol: Par de trading (ex: BTCUSDT)
        """
        try:
            # Verificar se pode tradear
            can_trade, reason = self.risk_manager.can_trade()
            if not can_trade:
                logger.warning(f"[OK][OK] Não pode tradear: {reason}")
                return
            
            # Buscar dados de mercado
            try:
                # Usar exchange diretamente (DataManager não tem get_ohlcv)
                ohlcv = self.exchange.exchange.fetch_ohlcv(
                    symbol,
                    timeframe=self.config['timeframe'],
                    limit=100
                )
                
                if not ohlcv or len(ohlcv) < 50:
                    logger.warning(f"Dados insuficientes para {symbol}")
                    return
                
                # Converter para DataFrame
                import pandas as pd
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                
            except Exception as e:
                logger.error(f"Erro ao buscar dados de {symbol}: {e}")
                return
            
            # Agora df existe
            if df is None or len(df) < 50:
                return
            
            if df is None or len(df) < 50:
                logger.warning(f"[OK][OK] Dados insuficientes para {symbol}")
                return
            
            # Analisar com estratégia
            signal = self.strategy.analyze(df)
            
            logger.info(f"[OK][OK] {symbol}: Sinal={signal['signal']}, Confiança={signal['confidence']:.1f}%")
            
            # Se já tem posição aberta, verificar saída
            if symbol in self.portfolio_manager.positions:
                position = self.portfolio_manager.positions[symbol]
                current_price = df['close'].iloc[-1]
                
                should_exit, exit_reason = self.risk_manager.should_exit(
                    position['entry_price'],
                    current_price,
                    position['stop_loss'],
                    position['take_profit'],
                    'buy'
                )
                
                if should_exit:
                    self.close_position(symbol, current_price, exit_reason)
                    return
            
            # Se não tem posição e sinal é COMPRA
            if symbol not in self.portfolio_manager.positions and signal['signal'] == 'buy':
                if signal['confidence'] >= 70:  # Mínimo 70% confiança
                    self.open_position(symbol, signal)
            
        except Exception as e:
            logger.error(f"[OK] Erro ao processar {symbol}: {e}")
    
    def open_position(self, symbol: str, signal: dict):
        """Abre uma posição (COMPRA)"""
        try:
            # Calcular tamanho da posição
            position_data = self.risk_manager.calculate_position_size(symbol)
            
            if position_data['quantity'] == 0:
                logger.warning(f"[OK][OK] Quantidade calculada = 0 para {symbol}")
                return
            
            # Preço atual
            current_price = self.exchange.get_current_price(symbol)
            
            # Calcular stop loss e take profit
            stop_loss = self.risk_manager.calculate_stop_loss(current_price, 'buy')
            take_profit = self.risk_manager.calculate_take_profit(current_price, 'buy')
            
            # Validar ordem
            is_valid, msg = self.risk_manager.validate_order(
                'buy', symbol, position_data['quantity'], current_price
            )
            
            if not is_valid:
                logger.error(f"[OK] Ordem inválida: {msg}")
                return
            
            # EXECUTAR ORDEM REAL
            logger.info(f"[OK][OK] COMPRANDO {symbol}: {position_data['quantity']} @ ${current_price:.2f}")
            
            order = self.exchange.place_order(
                symbol=symbol,
                side='buy',
                order_type='market',
                quantity=position_data['quantity']
            )
            
            if order and order.get('status') in ['filled', 'closed']:
                # Registrar posição
                self.portfolio_manager.open_position(
                    symbol,
                    float(order['price']),
                    position_data['quantity'],
                    stop_loss,
                    take_profit,
                    order['id']
                )
                
                # Salvar no banco
                self.save_trade_to_db(symbol, 'buy', order, signal)
                
                # Notificar
                self.notifier.send_notification(
                    f"[OK] COMPRA: {symbol}",
                    f"Preço: ${current_price:.2f}\nQuantidade: {position_data['quantity']}\nMotivo: {signal['reason']}"
                )
                
                logger.info(f"[OK] Posição aberta em {symbol}")
            else:
                logger.error(f"[OK] Ordem não executada: {order}")
                
        except Exception as e:
            logger.error(f"[OK] Erro ao abrir posição em {symbol}: {e}")
    
    def close_position(self, symbol: str, exit_price: float, reason: str):
        """Fecha uma posição (VENDE)"""
        try:
            position = self.portfolio_manager.positions.get(symbol)
            
            if not position:
                return
            
            # EXECUTAR VENDA REAL
            logger.info(f"[OK][OK] VENDENDO {symbol}: {position['quantity']} @ ${exit_price:.2f}")
            
            order = self.exchange.place_order(
                symbol=symbol,
                side='sell',
                order_type='market',
                quantity=position['quantity']
            )
            
            if order and order.get('status') in ['filled', 'closed']:
                # Calcular lucro/perda
                trade_result = self.portfolio_manager.close_position(
                    symbol,
                    float(order['price']),
                    reason
                )
                
                # Salvar no banco
                self.save_trade_close_to_db(symbol, order, trade_result)
                
                # Notificar
                lucro_texto = f"+${trade_result['profit_loss']:.2f}" if trade_result['profit_loss'] > 0 else f"-${abs(trade_result['profit_loss']):.2f}"
                
                self.notifier.send_notification(
                    f"[OK] VENDA: {symbol}",
                    f"Preço: ${exit_price:.2f}\nLucro/Perda: {lucro_texto}\nMotivo: {reason}"
                )
                
                logger.info(f"[OK] Posição fechada em {symbol}: {lucro_texto}")
            
        except Exception as e:
            logger.error(f"[OK] Erro ao fechar posição em {symbol}: {e}")
    
    def save_trade_to_db(self, symbol: str, side: str, order: dict, signal: dict):
        """Salva trade no banco de dados"""
        try:
            db = SessionLocal()
            
            trade = Trade(
                user_id=self.config['user_id'],
                bot_id=self.bot_config_id,
                symbol=symbol,
                side=side,
                entry_price=float(order['price']),
                quantity=float(order['filled']),
                entry_time=datetime.now(),
                signal_confidence=signal['confidence'],
                signal_reason=signal['reason']
            )
            
            db.add(trade)
            db.commit()
            db.close()
            
            logger.info(f"[OK][OK] Trade salvo no banco")
            
        except Exception as e:
            logger.error(f"[OK] Erro ao salvar trade: {e}")
    
    def save_trade_close_to_db(self, symbol: str, order: dict, trade_result: dict):
        """Atualiza trade no banco com dados de fechamento"""
        try:
            db = SessionLocal()
            
            # Buscar trade aberto mais recente
            trade = db.query(Trade).filter(
                Trade.user_id == self.config['user_id'],
                Trade.symbol == symbol,
                Trade.exit_time == None
            ).order_by(Trade.id.desc()).first()
            
            if trade:
                trade.exit_price = float(order['price'])
                trade.exit_time = datetime.now()
                trade.profit_loss = trade_result['profit_loss']
                trade.profit_loss_percent = trade_result['profit_percent']
                
                db.commit()
            
            db.close()
            
        except Exception as e:
            logger.error(f"[OK] Erro ao atualizar trade: {e}")
    
    def run(self):
        """Loop principal do bot"""
        logger.info(f"[OK][OK] Iniciando bot {self.config['name']}...")
        self.is_running = True
        
        iteration = 0
        
        try:
            while self.is_running:
                iteration += 1
                logger.info(f"[OK][OK] Iteração #{iteration}")
                
                # Recarregar config (verificar se foi pausado)
                if iteration % 10 == 0:  # A cada 10 iterações
                    if not self.load_config():
                        break
                    
                    if not self.config['is_active']:
                        logger.info("[OK][OK] Bot pausado pelo usuário")
                        break
                
                # Atualizar saldo e verificar drawdown
                self.risk_manager.update_balance()
                
                # Para cada símbolo
                for symbol in self.config['symbols']:
                    self.check_and_execute_trade(symbol)
                
                # Aguardar (baseado no perfil - por enquanto 60s)
                logger.info("[OK] Aguardando próxima análise...")
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("[OK][OK] Bot interrompido pelo usuário")
        except Exception as e:
            logger.error(f"[OK] Erro fatal no bot: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Para o bot"""
        self.is_running = False
        logger.info(f"[OK][OK] Bot {self.config['name']} parado")
    
    def run_backtest(self, start_date: str, end_date: str, initial_capital: float = 1000):
        """
        Executa backtest (teste com dados históricos)
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            initial_capital: Capital inicial em USDT
        """
        from bot.backtesting.engine import BacktestEngine
        
        logger.info(f"[OK][OK] Iniciando backtest de {start_date} a {end_date}")
        
        engine = BacktestEngine(
            strategy=self.strategy,
            initial_capital=initial_capital
        )
        
        results = {}
        
        for symbol in self.config['symbols']:
            logger.info(f"[OK]� Testando {symbol}...")
            
            # Buscar dados históricos
            df = self.data_manager.get_ohlcv(
                symbol,
                self.config['timeframe'],
                limit=1000  # 1000 candlesticks
            )
            
            if df is not None and len(df) > 50:
                result = engine.run(df, symbol)
                results[symbol] = result
                
                logger.info(f"[OK] {symbol}: {result['total_trades']} trades, "
                          f"Lucro: ${result['total_profit']:.2f} ({result['win_rate']:.1f}% win rate)")
        
        # Resumo geral
        total_trades = sum(r['total_trades'] for r in results.values())
        total_profit = sum(r['total_profit'] for r in results.values())
        avg_win_rate = sum(r['win_rate'] for r in results.values()) / len(results) if results else 0
        
        logger.info("=" * 50)
        logger.info(f"[OK][OK] BACKTEST COMPLETO")
        logger.info(f"Total de Trades: {total_trades}")
        logger.info(f"Lucro Total: ${total_profit:.2f}")
        logger.info(f"Win Rate Médio: {avg_win_rate:.1f}%")
        logger.info(f"Capital Final: ${initial_capital + total_profit:.2f}")
        logger.info("=" * 50)
        
        return results


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auronex Trading Bot')
    parser.add_argument('bot_id', type=int, help='ID do bot no banco de dados')
    parser.add_argument('--backtest', action='store_true', help='Executar backtest ao invés de trading real')
    parser.add_argument('--start-date', type=str, default='2024-01-01', help='Data inicial backtest')
    parser.add_argument('--end-date', type=str, default='2024-12-31', help='Data final backtest')
    parser.add_argument('--capital', type=float, default=1000, help='Capital inicial')
    
    args = parser.parse_args()
    
    # Criar bot
    bot = TradingBot(args.bot_id)
    
    # Carregar configuração
    if not bot.load_config():
        logger.error("[OK] Falha ao carregar configuração")
        return
    
    # Inicializar componentes
    if not bot.initialize_components():
        logger.error("[OK] Falha ao inicializar componentes")
        return
    
    # Executar
    if args.backtest:
        # BACKTEST
        logger.info("[OK][OK] Modo: BACKTEST (dados históricos)")
        bot.run_backtest(args.start_date, args.end_date, args.capital)
    else:
        # TRADING REAL
        logger.info("[OK][OK] Modo: TRADING REAL (produção)")
        logger.warning("[OK][OK] ATENÇÃO: Bot fará trades REAIS com dinheiro real!")
        
        # Aguardar 5 segundos (tempo para cancelar)
        for i in range(5, 0, -1):
            logger.info(f"⏰ Iniciando em {i}...")
            time.sleep(1)
        
        bot.run()


if __name__ == "__main__":
    main()



