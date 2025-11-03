"""
Users Models
"""
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings

class UserProfile(models.Model):
    """Perfil estendido do usuário"""
    
    PLAN_CHOICES = [
        ('free', 'Free (7 dias teste)'),
        ('pro', 'Pro - R$ 29,90/mês'),
        ('premium', 'Premium - R$ 99,99/mês'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='free')
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)  # CPF sem formatação
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    trial_ends_at = models.DateTimeField(null=True, blank=True)  # Data fim do teste
    
    # Sistema de Bots Extras (mínimo 5, com 20% desconto)
    extra_bots = models.IntegerField(default=0, help_text="Bots adicionais (além do plano base)")
    monthly_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Preço mensal atual (calculado automaticamente)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan}"
    
    def is_trial_expired(self):
        """Verifica se o período de teste expirou"""
        if self.plan != 'free' or not self.trial_ends_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.trial_ends_at
    
    def get_plan_limits(self):
        """Retorna limites do plano (incluindo bots extras)"""
        limits = {
            'free': {
                'max_bots': 1,
                'max_exchanges': 1,
                'allowed_exchanges': ['binance'],
                'max_symbols_per_bot': 1,
                'history_days': 7,
                'trial_days': 7,
            },
            'pro': {
                'max_bots': 3,
                'max_exchanges': 999,
                'allowed_exchanges': ['binance', 'bybit', 'okx', 'kraken', 'kucoin'],
                'max_symbols_per_bot': 10,
                'history_days': 90,
                'trial_days': 0,
            },
            'premium': {
                'max_bots': 10,  # Limite base Premium
                'max_exchanges': 999,
                'allowed_exchanges': ['binance', 'bybit', 'okx', 'kraken', 'kucoin'],
                'max_symbols_per_bot': 999,
                'history_days': 9999,
                'trial_days': 0,
            }
        }
        
        plan_limits = limits.get(self.plan, limits['free'])
        
        # Adicionar bots extras ao limite (se houver)
        if hasattr(self, 'extra_bots'):
            plan_limits['max_bots'] += self.extra_bots
        
        return plan_limits
    
    def calculate_monthly_price(self):
        """Calcula preço mensal baseado no plano + bots extras"""
        base_prices = {
            'free': 0,
            'pro': 29.90,
            'premium': 99.99,
        }
        
        # Preço por bot extra: R$ 9,90 (FIXO para ambos os planos)
        price_per_extra_bot = {
            'free': 0,
            'pro': 9.90,
            'premium': 9.90,
        }
        
        base_price = base_prices.get(self.plan, 0)
        
        # Adicionar custo dos bots extras
        if self.extra_bots > 0:
            bot_price = price_per_extra_bot.get(self.plan, 0)
            extra_cost = self.extra_bots * bot_price
            return base_price + extra_cost
        
        return base_price
    
    def save(self, *args, **kwargs):
        """Sobrescrever save para calcular preço automaticamente"""
        self.monthly_price = self.calculate_monthly_price()
        super().save(*args, **kwargs)
    
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
    
    @property
    def passphrase(self):
        """Retorna passphrase descriptografada (se existir)"""
        if self.passphrase_encrypted:
            return self.decrypt_key(self.passphrase_encrypted)
        return None
    
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
