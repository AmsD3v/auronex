"""
URL Configuration - RoboTrader SaaS
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from . import views_frontend
from . import views_payment
from . import views_system
from . import views_mercadopago

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, basename='profile')
router.register('api-keys', views.ExchangeAPIKeyViewSet, basename='api-keys')
router.register('bots', views.BotConfigurationViewSet, basename='bots')
router.register('trades', views.TradeViewSet, basename='trades')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Frontend Pages (HTML)
    path('', views_frontend.home, name='home'),
    path('register/', views_frontend.register_page, name='register_page'),
    path('login/', views_frontend.login_page, name='login_page'),
    path('dashboard/', views_frontend.dashboard_page, name='dashboard_page'),
    path('api-keys/', views_frontend.api_keys_page, name='api_keys_page'),
    path('bots/', views_frontend.bots_page, name='bots_page'),
    path('trades/', views_frontend.trades_page, name='trades_page'),
    path('system/', views_system.system_control_page, name='system_control'),
    
    # Payment Pages
    path('payment/choice/', views_frontend.payment_choice_page, name='payment_choice'),
    path('payment/success/', views_payment.payment_success, name='payment_success'),
    path('payment/success-pix/', views_mercadopago.payment_success_pix, name='payment_success_pix'),
    path('payment/pending/', views_mercadopago.payment_pending, name='payment_pending'),
    path('payment/cancel/', views_payment.payment_cancel, name='payment_cancel'),
    
    # Auth API
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login, name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Payment API
    path('api/payment/create-checkout/', views_payment.create_checkout_session, name='create_checkout'),
    path('api/payment/webhook/', views_payment.stripe_webhook, name='stripe_webhook'),
    path('api/payment/mercadopago/create/', views_mercadopago.create_pix_payment, name='create_pix'),
    path('api/payment/mercadopago-webhook/', views_mercadopago.mercadopago_webhook, name='mercadopago_webhook'),
    
    # System API
    path('api/system/status/', views_system.check_servers_status, name='system_status'),
    path('api/system/streamlit/start/', views_system.start_streamlit, name='streamlit_start'),
    path('api/system/streamlit/stop/', views_system.stop_streamlit, name='streamlit_stop'),
    path('api/system/streamlit/restart/', views_system.restart_streamlit, name='streamlit_restart'),
    
    # API
    path('api/', include(router.urls)),
]

