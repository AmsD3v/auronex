"""
Modelos de Usuários - RoboTrader SaaS
"""

from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings

class UserProfile(models.Model):
    """Perfil estendido do usuário"""
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro - $29/mês'),
        ('premium', 'Premium - $99/mês'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='free')
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan}"
    
    class Meta:
        db_table = 'user_profiles'


class ExchangeAPIKey(models.Model):
    """API Keys das corretoras (criptografadas)"""
    
    EXCHANGE_CHOICES = [
        ('binance', 'Binance'),
        ('bybit', 'Bybit'),
        ('okx', 'OKX'),
        ('kraken', 'Kraken'),
        ('kucoin', 'KuCoin'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES)
    api_key_encrypted = models.TextField()
    secret_key_encrypted = models.TextField()
    passphrase_encrypted = models.TextField(blank=True, null=True)
    is_testnet = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def encrypt_key(self, key):
        """Criptografa uma chave"""
        f = Fernet(settings.ENCRYPTION_KEY.encode())
        return f.encrypt(key.encode()).decode()
    
    def decrypt_key(self, encrypted_key):
        """Descriptografa uma chave"""
        f = Fernet(settings.ENCRYPTION_KEY.encode())
        return f.decrypt(encrypted_key.encode()).decode()
    
    @property
    def api_key(self):
        return self.decrypt_key(self.api_key_encrypted)
    
    @property
    def secret_key(self):
        return self.decrypt_key(self.secret_key_encrypted)
    
    def save_keys(self, api_key, secret_key, passphrase=None):
        """Salva chaves criptografadas"""
        self.api_key_encrypted = self.encrypt_key(api_key)
        self.secret_key_encrypted = self.encrypt_key(secret_key)
        if passphrase:
            self.passphrase_encrypted = self.encrypt_key(passphrase)
        self.save()
    
    def __str__(self):
        return f"{self.user.email} - {self.exchange}"
    
    class Meta:
        db_table = 'exchange_api_keys'
        unique_together = ['user', 'exchange']


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
    
    class Meta:
        db_table = 'trades'
        ordering = ['-entry_time']

