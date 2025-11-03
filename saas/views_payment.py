"""
Views de Pagamento - Integração com Stripe
"""
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from django.utils import timezone
from datetime import timedelta
import stripe

# Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """
    Criar sessão de checkout do Stripe
    """
    # Verificar se Stripe está configurado
    if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY == '':
        return Response({
            'error': 'Pagamentos não configurados',
            'message': 'O sistema de pagamentos está em configuração. Por enquanto, use o plano Free ou aguarde.',
            'setup_required': True
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    plan = request.data.get('plan')
    
    if plan not in ['pro', 'premium']:
        return Response({'error': 'Plano inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Definir preços (IDs do Stripe - você criará esses produtos no painel Stripe)
    # Exemplo: price_1ABC... são IDs reais do Stripe após criar os produtos
    price_ids = {
        'pro': 'price_pro_monthly',  # Substituir pelo ID real do Stripe
        'premium': 'price_premium_monthly'  # Substituir pelo ID real do Stripe
    }
    
    # Valores em centavos (BRL) - TESTE
    prices = {
        'pro': 2990,     # R$ 29,90
        'premium': 9999  # R$ 99,99
    }
    
    try:
        # Criar sessão de checkout
        # Nota: PIX via Stripe precisa ser ativado no painel primeiro
        # Por enquanto, apenas cartão (mais estável)
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],  # Apenas cartão por enquanto
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': f'RoboTrader {plan.capitalize()}',
                            'description': f'Assinatura mensal do plano {plan.capitalize()}',
                        },
                        'unit_amount': prices[plan],
                        'recurring': {
                            'interval': 'month',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=settings.SITE_URL + '/payment/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.SITE_URL + '/payment/cancel/',
            metadata={
                'user_id': request.user.id,
                'plan': plan
            }
        )
        
        return Response({
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def stripe_webhook(request):
    """
    Webhook do Stripe para eventos de pagamento
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Processar eventos
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_success(session)
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancelled(subscription)
    
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_payment_failed(invoice)
    
    return Response(status=status.HTTP_200_OK)


def handle_checkout_success(session):
    """
    Processar pagamento bem-sucedido (Stripe)
    """
    user_id = session['metadata']['user_id']
    plan = session['metadata']['plan']
    
    try:
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        profile = user.userprofile
        
        # Atualizar plano
        profile.plan = plan
        profile.stripe_customer_id = session.get('customer')
        profile.trial_ends_at = None  # Remover trial
        profile.save()
        
        print(f"✅ Pagamento Stripe confirmado: {user.email} → Plano {plan} → ATIVADO")
        
    except Exception as e:
        print(f"❌ Erro ao processar pagamento: {e}")


def handle_subscription_cancelled(subscription):
    """
    Processar cancelamento de assinatura
    """
    customer_id = subscription.get('customer')
    
    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        
        # Downgrade para free
        profile.plan = 'free'
        profile.trial_ends_at = timezone.now() + timedelta(days=7)  # 7 dias de graça
        profile.save()
        
        print(f"⚠️ Assinatura cancelada: {profile.user.email} → Plano free")
        
    except UserProfile.DoesNotExist:
        print(f"❌ Perfil não encontrado para customer {customer_id}")


def handle_payment_failed(invoice):
    """
    Processar falha de pagamento
    """
    customer_id = invoice.get('customer')
    
    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        
        # Enviar notificação (implementar email)
        print(f"⚠️ Falha no pagamento: {profile.user.email}")
        
        # Dar 3 dias de graça antes de desativar
        profile.trial_ends_at = timezone.now() + timedelta(days=3)
        profile.save()
        
    except UserProfile.DoesNotExist:
        pass


# Views de Frontend
def payment_success(request):
    """Página de sucesso após pagamento"""
    return render(request, 'payment_success.html')


def payment_cancel(request):
    """Página de cancelamento"""
    return render(request, 'payment_cancel.html')

