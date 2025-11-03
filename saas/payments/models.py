from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    """Assinatura do usuário"""
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro - $29/mês'),
        ('premium', 'Premium - $99/mês'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('canceled', 'Cancelada'),
        ('past_due', 'Pagamento atrasado'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    current_period_start = models.DateTimeField(null=True)
    current_period_end = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'

class Payment(models.Model):
    """Histórico de pagamentos"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    stripe_payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payments'

