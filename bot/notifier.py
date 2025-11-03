"""
Sistema de Notificações via Telegram
Envia alertas sobre trades, erros e status do bot
"""

import logging
from typing import Optional
from datetime import datetime
from config.settings import Settings

logger = logging.getLogger(__name__)

# Importação condicional do telegram
try:
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.warning("⚠️  Biblioteca python-telegram-bot não instalada. Notificações desabilitadas.")


class Notifier:
    """
    Sistema de notificações via Telegram
    Envia mensagens sobre eventos importantes do bot
    """
    
    def __init__(self):
        """Inicializa o notificador"""
        self.settings = Settings()
        self.bot = None
        self.enabled = False
        
        if self.settings.ENABLE_TELEGRAM and TELEGRAM_AVAILABLE:
            self.initialize()
    
    def initialize(self):
        """Inicializa o bot do Telegram"""
        try:
            if not self.settings.TELEGRAM_BOT_TOKEN:
                logger.warning("⚠️  Token do Telegram não configurado")
                return
            
            if not self.settings.TELEGRAM_CHAT_ID:
                logger.warning("⚠️  Chat ID do Telegram não configurado")
                return
            
            self.bot = Bot(token=self.settings.TELEGRAM_BOT_TOKEN)
            self.enabled = True
            
            # Testar conexão
            self.send_message("🤖 RoboTrader iniciado e conectado!")
            logger.info("✅ Notificações Telegram habilitadas")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Telegram: {e}")
            self.enabled = False
    
    def send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """
        Envia uma mensagem via Telegram
        
        Args:
            message: Texto da mensagem
            parse_mode: Modo de formatação ('HTML' ou 'Markdown')
        
        Returns:
            True se enviou com sucesso
        """
        if not self.enabled or not self.bot:
            logger.debug(f"Notificação (não enviada): {message}")
            return False
        
        try:
            self.bot.send_message(
                chat_id=self.settings.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode=parse_mode
            )
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem Telegram: {e}")
            return False
    
    def notify_trade_entry(self, symbol: str, side: str, quantity: float, 
                          price: float, strategy: str):
        """Notifica entrada em trade"""
        emoji = "🟢" if side == 'buy' else "🔴"
        
        message = f"""
{emoji} <b>ENTRADA EM TRADE</b>

<b>Par:</b> {symbol}
<b>Lado:</b> {side.upper()}
<b>Quantidade:</b> {quantity}
<b>Preço:</b> ${price:.2f}
<b>Estratégia:</b> {strategy}
<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(message.strip())
        logger.info(f"📱 Notificação enviada: Entrada {side.upper()}")
    
    def notify_trade_exit(self, symbol: str, side: str, quantity: float, 
                         entry_price: float, exit_price: float, 
                         profit_loss: float, reason: str):
        """Notifica saída de trade"""
        is_profit = profit_loss > 0
        emoji = "💰" if is_profit else "❌"
        
        profit_percent = ((exit_price - entry_price) / entry_price * 100) if side == 'buy' else ((entry_price - exit_price) / entry_price * 100)
        
        message = f"""
{emoji} <b>SAÍDA DE TRADE</b>

<b>Par:</b> {symbol}
<b>Quantidade:</b> {quantity}
<b>Preço Entrada:</b> ${entry_price:.2f}
<b>Preço Saída:</b> ${exit_price:.2f}
<b>Lucro/Perda:</b> ${profit_loss:.2f} ({profit_percent:+.2f}%)
<b>Motivo:</b> {reason}
<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(message.strip())
        logger.info(f"📱 Notificação enviada: Saída com {profit_loss:.2f} USDT")
    
    def notify_error(self, error_message: str):
        """Notifica erro"""
        message = f"""
⚠️ <b>ERRO</b>

{error_message}

<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(message.strip())
        logger.info("📱 Notificação de erro enviada")
    
    def notify_warning(self, warning_message: str):
        """Notifica aviso"""
        message = f"""
⚠️ <b>AVISO</b>

{warning_message}

<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(message.strip())
    
    def notify_bot_started(self, config: dict):
        """Notifica início do bot"""
        mode = "🧪 TESTNET" if self.settings.USE_TESTNET else "🚨 PRODUÇÃO"
        paper = " (PAPER TRADING)" if self.settings.PAPER_TRADING else ""
        
        message = f"""
🤖 <b>ROBOTRADER INICIADO</b>

<b>Modo:</b> {mode}{paper}
<b>Símbolo:</b> {config.get('symbol', 'N/A')}
<b>Timeframe:</b> {config.get('timeframe', 'N/A')}
<b>Estratégia:</b> {config.get('strategy', 'N/A')}
<b>Stop Loss:</b> {config.get('stop_loss', 'N/A')}
<b>Take Profit:</b> {config.get('take_profit', 'N/A')}

Bot rodando... 🚀
        """
        
        self.send_message(message.strip())
    
    def notify_bot_stopped(self, reason: str = ""):
        """Notifica parada do bot"""
        message = f"""
⏹️ <b>ROBOTRADER PARADO</b>

<b>Motivo:</b> {reason or 'Manual'}
<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(message.strip())
    
    def notify_daily_summary(self, summary: dict):
        """Envia resumo diário"""
        total_trades = summary.get('total_trades', 0)
        winning = summary.get('winning_trades', 0)
        losing = summary.get('losing_trades', 0)
        win_rate = summary.get('win_rate', 0)
        profit_loss = summary.get('profit_loss', 0)
        
        emoji = "💰" if profit_loss > 0 else "❌" if profit_loss < 0 else "➖"
        
        message = f"""
📊 <b>RESUMO DIÁRIO</b>

<b>Total de Trades:</b> {total_trades}
<b>Vitórias:</b> {winning} 🟢
<b>Derrotas:</b> {losing} 🔴
<b>Taxa de Acerto:</b> {win_rate:.1f}%

{emoji} <b>P&L:</b> ${profit_loss:+.2f}

<b>Data:</b> {datetime.now().strftime('%d/%m/%Y')}
        """
        
        self.send_message(message.strip())
    
    def notify_balance_update(self, initial: float, current: float):
        """Notifica atualização de saldo"""
        profit_loss = current - initial
        percent = (profit_loss / initial * 100) if initial > 0 else 0
        
        emoji = "📈" if profit_loss > 0 else "📉" if profit_loss < 0 else "➖"
        
        message = f"""
{emoji} <b>ATUALIZAÇÃO DE SALDO</b>

<b>Saldo Inicial:</b> ${initial:.2f}
<b>Saldo Atual:</b> ${current:.2f}
<b>Variação:</b> ${profit_loss:+.2f} ({percent:+.2f}%)
        """
        
        self.send_message(message.strip())
    
    def notify_risk_alert(self, alert_type: str, message: str):
        """Notifica alertas de risco"""
        emojis = {
            'drawdown': '🚨',
            'max_trades': '⏸️',
            'low_balance': '💸',
            'error': '⚠️'
        }
        
        emoji = emojis.get(alert_type, '⚠️')
        
        notification = f"""
{emoji} <b>ALERTA DE RISCO</b>

<b>Tipo:</b> {alert_type.upper()}
<b>Mensagem:</b> {message}

<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(notification.strip())
        logger.warning(f"🚨 Alerta de risco: {alert_type}")

