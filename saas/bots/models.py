"""
Bots Models
"""
from django.db import models
from django.contrib.auth.models import User

class BotConfiguration(models.Model):
    """Configuração de bot do usuário"""
    
    STRATEGY_CHOICES = [
        ('mean_reversion', 'Mean Reversion'),
        ('trend_following', 'Trend Following'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_configs')
    name = models.CharField(max_length=100)  # "Meu Setup Agressivo"
    exchange = models.CharField(max_length=20)
    symbols = models.JSONField(default=list)  # ['BTCUSDT', 'ETHUSDT']
    capital = models.DecimalField(max_digits=12, decimal_places=2)
    strategy = models.CharField(max_length=20, choices=STRATEGY_CHOICES)
    timeframe = models.CharField(max_length=5, default='15m')
    stop_loss_percent = models.DecimalField(max_digits=5, decimal_places=3, default=1.5)
    take_profit_percent = models.DecimalField(max_digits=5, decimal_places=3, default=3.0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"
    
    class Meta:
        db_table = 'bot_configurations'


class Trade(models.Model):
    """Histórico de trades"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    bot_config = models.ForeignKey(BotConfiguration, on_delete=models.SET_NULL, null=True)
    exchange = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)
    side = models.CharField(max_length=4)  # buy/sell
    entry_price = models.DecimalField(max_digits=20, decimal_places=8)
    exit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    profit_loss = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    profit_loss_percent = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, default='open')  # open/closed
    
    # ✅ TRAILING STOP - Rastrear preço mais alto alcançado
    highest_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True,
                                       help_text="Preço mais alto alcançado (para trailing stop)")
    
    class Meta:
        db_table = 'trades'
        ordering = ['-entry_time']
