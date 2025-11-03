"""
API Serializers - RoboTrader SaaS
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile, ExchangeAPIKey
from bots.models import BotConfiguration, Trade
from .utils import validar_cpf


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Registro de novo usuário"""
    password = serializers.CharField(write_only=True, min_length=8)
    cpf = serializers.CharField(write_only=True, min_length=11, max_length=11)
    plan = serializers.CharField(write_only=True, required=False, default='free')
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'cpf', 'plan']
    
    def validate_email(self, value):
        """Valida se email já existe"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já cadastrado. Use o login se já tem conta.")
        return value
    
    def validate_cpf(self, value):
        """Valida CPF"""
        # Validar se CPF é válido (algoritmo brasileiro)
        if not validar_cpf(value):
            raise serializers.ValidationError("CPF inválido. Verifique os números digitados.")
        
        # Validar se CPF já existe
        if UserProfile.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF já cadastrado. Use o login se já tem conta.")
        
        return value
    
    def create(self, validated_data):
        cpf = validated_data.pop('cpf')
        plan = validated_data.pop('plan', 'free')
        
        # Criar usuário ATIVO (para poder fazer login e pagar)
        # Webhook confirmará pagamento e atualizará plano
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=True  # Sempre ativo para poder autenticar
        )
        
        # Criar perfil com CPF
        from django.utils import timezone
        from datetime import timedelta
        
        trial_ends = None
        if plan == 'free':
            trial_ends = timezone.now() + timedelta(days=7)
        
        UserProfile.objects.create(
            user=user,
            cpf=cpf,
            plan=plan,
            trial_ends_at=trial_ends
        )
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Perfil do usuário"""
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['email', 'plan', 'created_at']


class ExchangeAPIKeySerializer(serializers.ModelSerializer):
    """API Keys (não expor chaves reais!)"""
    api_key_masked = serializers.SerializerMethodField()
    
    class Meta:
        model = ExchangeAPIKey
        fields = ['id', 'exchange', 'api_key_masked', 'is_testnet', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at', 'exchange']  # Exchange não pode mudar
    
    def get_api_key_masked(self, obj):
        """Retorna chave mascarada (últimos 4 dígitos)"""
        key = obj.api_key
        return f"***{key[-4:]}"


class ExchangeAPIKeyCreateSerializer(serializers.ModelSerializer):
    """Criar nova API Key (receber chaves completas)"""
    api_key = serializers.CharField(write_only=True)
    secret_key = serializers.CharField(write_only=True)
    passphrase = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = ExchangeAPIKey
        fields = ['exchange', 'api_key', 'secret_key', 'passphrase', 'is_testnet']
    
    def create(self, validated_data):
        api_key = validated_data.pop('api_key')
        secret_key = validated_data.pop('secret_key')
        passphrase = validated_data.pop('passphrase', None)
        
        # Se passphrase está vazia ou é None, não passar para save_keys
        if not passphrase:
            passphrase = None
        
        exchange_key = ExchangeAPIKey.objects.create(**validated_data)
        exchange_key.save_keys(api_key, secret_key, passphrase)
        
        return exchange_key


class BotConfigurationSerializer(serializers.ModelSerializer):
    """Configuração de bot"""
    
    class Meta:
        model = BotConfiguration
        fields = [
            'id', 'name', 'exchange', 'symbols', 'capital',
            'strategy', 'timeframe', 'stop_loss_percent',
            'take_profit_percent', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TradeSerializer(serializers.ModelSerializer):
    """Trade histórico"""
    symbol_display = serializers.CharField(source='symbol', read_only=True)
    
    class Meta:
        model = Trade
        fields = [
            'id', 'symbol_display', 'side', 'entry_price',
            'exit_price', 'quantity', 'profit_loss',
            'profit_loss_percent', 'entry_time', 'exit_time', 'status'
        ]
        read_only_fields = ['id']

