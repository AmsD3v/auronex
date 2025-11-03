"""
Integração com Mercado Pago - PIX e outros métodos brasileiros
"""
import mercadopago
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from django.utils import timezone
from datetime import timedelta


# Configurar Mercado Pago SDK
# Obter token em: https://www.mercadopago.com.br/developers/panel/app
MERCADOPAGO_ACCESS_TOKEN = settings.MERCADOPAGO_ACCESS_TOKEN if hasattr(settings, 'MERCADOPAGO_ACCESS_TOKEN') else ''


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pix_payment(request):
    """
    Criar pagamento via PIX (Mercado Pago)
    """
    plan = request.data.get('plan')
    
    if plan not in ['pro', 'premium']:
        return Response({'error': 'Plano inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Debug: Ver se credenciais estão carregando
    print(f"DEBUG - MERCADOPAGO_ACCESS_TOKEN: {MERCADOPAGO_ACCESS_TOKEN[:20]}..." if MERCADOPAGO_ACCESS_TOKEN else "VAZIO")
    
    # Verificar se Mercado Pago está configurado
    if not MERCADOPAGO_ACCESS_TOKEN:
        return Response({
            'error': 'PIX não configurado',
            'message': 'PIX ainda não está disponível. Use cartão de crédito por enquanto.',
            'setup_required': True
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Valores
    values = {
        'pro': 29.90,     # R$ 29,90
        'premium': 99.99  # R$ 99,99
    }
    
    try:
        print(f"DEBUG - Criando SDK Mercado Pago...")
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        print(f"DEBUG - SDK criado com sucesso")
        
        # Criar preferência de pagamento (SEM auto_return que causa erro!)
        preference_data = {
            "items": [
                {
                    "title": f"RoboTrader {plan.capitalize()}",
                    "description": f"Assinatura mensal do plano {plan.capitalize()}",
                    "category_id": "services",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": float(values[plan])
                }
            ],
            "payer": {
                "name": request.user.first_name or "Cliente",
                "surname": request.user.last_name or "RoboTrader",
                "email": request.user.email,
            },
            "payment_methods": {
                "excluded_payment_types": [{"id": "credit_card"}, {"id": "debit_card"}],
                "installments": 1
            },
            "external_reference": f"{request.user.id}_{plan}",
            "notification_url": f"{settings.SITE_URL}/api/payment/mercadopago-webhook/",
            "statement_descriptor": "ROBOTRADER"
        }
        
        print(f"DEBUG - Criando preferência...")
        preference_response = sdk.preference().create(preference_data)
        print(f"DEBUG - Resposta: {preference_response}")
        
        preference = preference_response["response"]
        
        return Response({
            'checkout_url': preference['init_point'],  # URL do checkout Mercado Pago
            'preference_id': preference['id']
        })
        
    except Exception as e:
        print(f"ERRO MERCADO PAGO: {str(e)}")
        print(f"ERRO COMPLETO: {repr(e)}")
        return Response({
            'error': str(e),
            'message': f'Erro ao criar pagamento PIX: {str(e)[:100]}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def mercadopago_webhook(request):
    """
    Webhook do Mercado Pago para notificações de pagamento
    """
    try:
        # Mercado Pago envia notificação de pagamento
        data = request.data
        
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            if payment_id:
                # Buscar detalhes do pagamento
                sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
                payment_info = sdk.payment().get(payment_id)
                
                if payment_info['status'] == 200:
                    payment = payment_info['response']
                    
                    # Se aprovado, ativar plano
                    if payment['status'] == 'approved':
                        handle_mercadopago_success(payment)
        
        return Response({'status': 'ok'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def handle_mercadopago_success(payment):
    """
    Processar pagamento aprovado do Mercado Pago (PIX)
    """
    try:
        external_ref = payment.get('external_reference', '')
        user_id, plan = external_ref.split('_')
        
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        profile = user.userprofile
        
        # Confirmar pagamento PIX
        profile.plan = plan
        profile.trial_ends_at = None
        profile.save()
        
        print(f"✅ Pagamento PIX confirmado: {user.email} → Plano {plan} → ATIVADO")
        
    except Exception as e:
        print(f"❌ Erro ao processar pagamento PIX: {e}")


def payment_success_pix(request):
    """Página de sucesso para pagamento PIX"""
    return render(request, 'payment_success_pix.html')


def payment_pending(request):
    """Página de pagamento pendente (aguardando PIX)"""
    return render(request, 'payment_pending.html')




