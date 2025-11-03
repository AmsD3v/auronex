"""
API Views - RoboTrader SaaS
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from users.models import UserProfile, ExchangeAPIKey
from bots.models import BotConfiguration, Trade
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    ExchangeAPIKeySerializer,
    ExchangeAPIKeyCreateSerializer,
    BotConfigurationSerializer,
    TradeSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Registro de novo usuário"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuário criado com sucesso!',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login de usuário"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'email': user.email,
                'first_name': user.first_name,
            }
        })
    
    return Response(
        {'error': 'Credenciais inválidas'},
        status=status.HTTP_401_UNAUTHORIZED
    )


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Perfil do usuário"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def limits(self, request):
        """Retorna limites do plano do usuário"""
        try:
            profile = request.user.userprofile
            limits = profile.get_plan_limits()
            
            return Response({
                'plan': profile.plan,
                'limits': limits,
                'trial_expired': profile.is_trial_expired() if profile.plan == 'free' else False,
                'trial_ends_at': profile.trial_ends_at
            })
        except:
            return Response({'error': 'Perfil não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ExchangeAPIKeyViewSet(viewsets.ModelViewSet):
    """Gerenciar API Keys"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ExchangeAPIKey.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ExchangeAPIKeyCreateSerializer
        return ExchangeAPIKeySerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Retorna API Key com chaves descriptografadas (para uso no dashboard)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        data = serializer.data
        
        # Adicionar chaves descriptografadas (APENAS PARA O DONO)
        data['api_key_decrypted'] = instance.api_key
        data['secret_key_decrypted'] = instance.secret_key
        
        if instance.passphrase:
            data['passphrase_decrypted'] = instance.passphrase
        
        return Response(data)
    
    def perform_create(self, serializer):
        # Verificar limites do plano
        user_profile = self.request.user.userprofile
        limits = user_profile.get_plan_limits()
        
        # Verificar se já atingiu limite de corretoras
        current_exchanges = ExchangeAPIKey.objects.filter(
            user=self.request.user,
            is_active=True
        ).values_list('exchange', flat=True).distinct().count()
        
        if current_exchanges >= limits['max_exchanges']:
            return Response(
                {'error': f"Plano {user_profile.plan} permite apenas {limits['max_exchanges']} corretora(s). Faça upgrade!"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar se corretora é permitida no plano
        exchange = serializer.validated_data.get('exchange')
        if exchange not in limits['allowed_exchanges']:
            return Response(
                {'error': f"Corretora {exchange} não disponível no plano {user_profile.plan}. Faça upgrade!"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar se API Key já foi usada por outro usuário (anti-fraude)
        api_key_preview = serializer.validated_data.get('api_key')[:20]  # Primeiros 20 chars
        existing_keys = ExchangeAPIKey.objects.exclude(user=self.request.user).all()
        for key in existing_keys:
            if key.api_key[:20] == api_key_preview:
                return Response(
                    {'error': 'Esta API Key já está sendo usada por outro usuário. Cada API Key só pode ser usada em uma conta.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer.save(user=self.request.user)


class BotConfigurationViewSet(viewsets.ModelViewSet):
    """Gerenciar configurações de bot"""
    serializer_class = BotConfigurationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BotConfiguration.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Verificar limites do plano
        user_profile = self.request.user.userprofile
        
        # Verificar se teste expirou
        if user_profile.is_trial_expired():
            return Response(
                {'error': 'Período de teste expirado! Assine um plano para continuar usando.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        limits = user_profile.get_plan_limits()
        
        # Verificar limite de bots
        current_bots = BotConfiguration.objects.filter(user=self.request.user).count()
        if current_bots >= limits['max_bots']:
            return Response(
                {'error': f"Plano {user_profile.plan} permite apenas {limits['max_bots']} bot(s). Faça upgrade para criar mais!"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar limite de símbolos
        symbols = serializer.validated_data.get('symbols', [])
        if len(symbols) > limits['max_symbols_per_bot']:
            return Response(
                {'error': f"Plano {user_profile.plan} permite apenas {limits['max_symbols_per_bot']} criptomoeda(s) por bot. Reduza a quantidade ou faça upgrade!"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar se corretora é permitida
        exchange = serializer.validated_data.get('exchange')
        if exchange not in limits['allowed_exchanges']:
            return Response(
                {'error': f"Corretora {exchange} não disponível no plano {user_profile.plan}. Apenas Binance está disponível no plano Free. Faça upgrade!"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Iniciar bot"""
        bot_config = self.get_object()
        bot_config.is_active = True
        bot_config.save()
        
        # TODO: Iniciar tarefa Celery
        
        return Response({'message': 'Bot iniciado!'})
    
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Parar bot"""
        bot_config = self.get_object()
        bot_config.is_active = False
        bot_config.save()
        
        # TODO: Parar tarefa Celery
        
        return Response({'message': 'Bot parado!'})


class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    """Histórico de trades"""
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)

