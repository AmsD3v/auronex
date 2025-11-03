"""
Views para páginas HTML (frontend)
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def home(request):
    """Landing page"""
    return render(request, 'landing.html')

def register_page(request):
    """Página de cadastro"""
    return render(request, 'register.html')

def login_page(request):
    """Página de login"""
    return render(request, 'login.html')

def dashboard_page(request):
    """Dashboard do usuário"""
    return render(request, 'dashboard_user.html')

def api_keys_page(request):
    """Página de gerenciamento de API Keys"""
    return render(request, 'api_keys.html')

def bots_page(request):
    """Página de gerenciamento de Bots"""
    return render(request, 'bots.html')

def trades_page(request):
    """Página de histórico de Trades"""
    return render(request, 'trades.html')

def payment_choice_page(request):
    """Página de escolha de forma de pagamento"""
    return render(request, 'payment_choice.html')

