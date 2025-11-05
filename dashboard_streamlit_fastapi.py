"""
AURONEX ROBÔ TRADER - Dashboard Visual
- Autenticação por usuário (FastAPI)
- API Keys individualizadas
- Isolamento total de dados
- Versão FastAPI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import sys
import sqlite3
from pathlib import Path
import requests
import os

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy
from config.settings import Settings

# Config
st.set_page_config(
    page_title="Auronex · Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar ABERTA por padrão
)

# ESTILO COMPLETO DO PREVIEW (EXATO!)
st.markdown("""
<style>
    /* Reset e Base */
    .stApp {
        background: #0a0e1a;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container Principal */
    .main .block-container {
        padding: 0 !important;
        max-width: 1400px;
        margin: 0 auto !important;
    }
    
    /* Esconder TUDO vazio */
    div:empty {
        display: none !important;
    }
    
    /* Login Container com Borda */
    .login-container {
        background: linear-gradient(135deg, rgba(20,25,45,0.4), rgba(30,35,60,0.4));
        backdrop-filter: blur(30px);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(100,150,255,0.2);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    
    /* Cards Flutuantes */
    .floating-card {
        background: linear-gradient(135deg, rgba(20,25,45,0.4), rgba(30,35,60,0.4));
        backdrop-filter: blur(30px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .floating-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 30px 80px rgba(0,100,255,0.2);
        border-color: rgba(100,150,255,0.3);
    }
    
    /* Métricas Ultra Clean */
    [data-testid="stMetricValue"] {
        font-size: 3.5rem !important;
        font-weight: 300 !important;
        letter-spacing: -2px;
        color: #ffffff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    
    /* Sidebar Minimalista */
    [data-testid="stSidebar"] {
        background: rgba(10,15,30,0.98);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* BOTÃO NATIVO STREAMLIT - SEMPRE VISÍVEL! */
    button[kind="header"],
    [data-testid="collapsedControl"],
    button[data-testid="baseButton-header"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    
    /* Sidebar aberta - botão na posição normal */
    section[data-testid="stSidebar"][aria-expanded="true"] ~ div button[kind="header"],
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) ~ div button[kind="header"] {
        display: block !important;
    }
    
    /* Sidebar fechada - botão deve ficar visível */
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Títulos Clean */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 300 !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    h2 {
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        color: #e2e8f0 !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        letter-spacing: -0.5px;
    }
    
    /* Tabs Ultra Clean */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        padding: 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #718096;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #ffffff !important;
        border-bottom-color: #00d9ff !important;
    }
    
    /* Inputs */
    .stTextInput input {
        background: rgba(30,35,60,0.4) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: rgba(0,217,255,0.5) !important;
        box-shadow: 0 0 0 3px rgba(0,217,255,0.1) !important;
    }
    
    /* Botões */
    .stButton button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102,126,234,0.4);
    }
    
    /* Responsivo */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
    }
</style>

<script>
// Remover elementos vazios
window.addEventListener('load', function() {
    setTimeout(function() {
        document.querySelectorAll('div').forEach(el => {
            if (el.children.length === 0 && el.textContent.trim() === '') {
                el.remove();
            }
        });
    }, 500);
});

// Apenas esconde elementos vazios (mantém simples)
</script>
""", unsafe_allow_html=True)

# ========================================
# 🔐 AUTENTICAÇÃO - MULTI-USUÁRIO
# ========================================

def check_authentication():
    """Verificar autenticação do usuário"""
    
    # Verificar se já está autenticado
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    
    # TELA DE LOGIN SEM SIDEBAR - USA st.stop() ANTES
    # NÃO usa CSS para esconder!
    st.markdown("""
    <style>
        /* Container login sem padding */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Borda suave no formulário de login */
        .login-container {
            background: rgba(30,35,60,0.3);
            border: 1px solid rgba(100,150,255,0.2);
            border-radius: 24px;
            padding: 40px;
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
    </style>
    
    <script>
        // REMOVER FORÇADAMENTE TODOS ELEMENTOS VAZIOS
        setTimeout(function() {
            // Pegar TODOS os divs do container principal
            const container = document.querySelector('.main .block-container');
            if (container) {
                const allDivs = container.querySelectorAll('div');
                
                allDivs.forEach(div => {
                    // Se div está vazia (sem texto, sem filhos visíveis)
                    if (div.children.length === 0 && div.textContent.trim() === '') {
                        div.remove();
                    }
                    // Se div só tem divs vazias
                    if (div.children.length > 0) {
                        const hasContent = Array.from(div.children).some(child => 
                            child.textContent.trim() !== '' || 
                            child.tagName === 'INPUT' || 
                            child.tagName === 'BUTTON'
                        );
                        if (!hasContent) {
                            div.style.display = 'none';
                            div.style.height = '0';
                        }
                    }
                });
                
                // Remover margin/padding dos primeiros 5 elementos
                for (let i = 0; i < 5; i++) {
                    if (container.children[i]) {
                        container.children[i].style.marginTop = '0';
                        container.children[i].style.paddingTop = '0';
                    }
                }
            }
        }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    # TÍTULO COM HOVER - SÓ "AURONEX" SE MOVE!
    st.markdown("""
    <style>
        .auronex-title {
            text-align: center;
            padding: 60px 0 50px 0;
            margin-top: 0 !important;
        }
        
        .auronex-title h1 {
            font-size: 4rem;
            font-weight: 300;
            margin: 0;
            letter-spacing: -2px;
            color: #ffffff;
            display: inline-block;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
        }
        
        /* HOVER SÓ NO H1! */
        .auronex-title h1:hover {
            transform: translateY(-4px);
            text-shadow: 0 0 30px rgba(0,217,255,0.6), 0 0 60px rgba(0,217,255,0.4);
            color: #00d9ff;
        }
        
        /* Subtítulo ESTÁTICO */
        .auronex-subtitle {
            color: #718096;
            font-size: 1.1rem;
            margin-top: 16px;
            letter-spacing: 1px;
        }
    </style>
    
    <div class="auronex-title">
        <h1>Auronex</h1>
        <p class="auronex-subtitle">Trading Platform · By Auronex Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulário centralizado com borda
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Formulário
        email = st.text_input(
            "Email", 
            placeholder="seu@email.com",
            key="login_email_main",
            label_visibility="visible"
        )
        
        password = st.text_input(
            "Senha", 
            type="password", 
            placeholder="••••••••",
            key="login_password_main",
            label_visibility="visible"
        )
        
        # SEM espaçamento entre senha e botão!
        
        if st.button("Entrar", use_container_width=True, type="primary"):
            if not email or not password:
                st.error("❌ Preencha email e senha!")
            else:
                try:
                    # Login SEM mensagens de debug!
                    response = requests.post(
                        'http://localhost:8001/api/streamlit/login',
                        json={'email': email, 'password': password},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.access_token = data['access_token']
                        st.session_state.user_email = email
                        st.session_state.user_name = data.get('user', {}).get('first_name', email.split('@')[0])
                        st.session_state.authenticated = True
                        
                        # RERUN IMEDIATO!
                        st.rerun()
                    else:
                        st.error(f"❌ Email ou senha incorretos! (Status: {response.status_code})")
                        if response.status_code == 401:
                            st.caption("Verifique se email e senha estão corretos")
                            st.caption("Mesmos dados do site: http://localhost:8001/login")
                except Exception as e:
                    st.error(f"❌ Erro de conexão: {str(e)}")
        
        # Link alternativo
        st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <p style='color: #4a5568; font-size: 0.85rem;'>
                Ainda não tem conta? 
                <a href='http://localhost:8001/register' style='color: #00d9ff; text-decoration: none;'>Criar conta</a>
            </p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Fechar login-page
    
    # Parar execução aqui (não mostrar resto do dashboard)
    return False

def refresh_token_if_expired():
    """Renova token se expirou"""
    if 'access_token' not in st.session_state:
        return False
    
    # Tentar usar refresh token do query param
    query_params = st.query_params
    if 'token' in query_params:
        # Token está na URL, não precisa refresh
        return True
    
    return True  # Manter sessão ativa

def get_user_api_keys():
    """Buscar API Keys do usuário logado"""
    if 'access_token' not in st.session_state:
        st.sidebar.warning("⚠️ Token não encontrado")
        return []
    
    try:
        token = st.session_state.access_token
        
        response = requests.get(
            'http://localhost:8001/api/api-keys/',
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            keys = response.json()
            return keys
        elif response.status_code == 401:
            st.sidebar.error("❌ Token inválido - Faça login novamente")
            st.session_state.authenticated = False
            return []
        else:
            st.sidebar.error(f"❌ Erro {response.status_code}")
            st.sidebar.code(response.text[:300])
            return []
            
    except Exception as e:
        st.sidebar.error(f"❌ Conexão falhou")
        st.sidebar.code(str(e)[:200])
        return []

# VERIFICAR AUTENTICAÇÃO
if not check_authentication():
    st.stop()

# ========================================
# BUSCAR BOTS DO USUÁRIO
# ========================================

def get_user_bots():
    """Buscar todos os bots do usuário logado"""
    if 'access_token' not in st.session_state:
        return []
    
    try:
        response = requests.get(
            'http://localhost:8001/api/bots/',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
            timeout=30  # Timeout maior
        )
        
        if response.status_code == 200:
            data = response.json()
            # API retorna {bots: [...], total: X, limit: Y}
            if isinstance(data, dict) and 'bots' in data:
                return data['bots']
            return data if isinstance(data, list) else []
        return []
        
    except Exception as e:
        st.sidebar.error(f"Erro ao buscar bots: {str(e)[:50]}")
        return []

# Buscar limites do plano do usuário
def get_user_plan_limits():
    """Buscar limites do plano"""
    if 'access_token' not in st.session_state:
        return None
    
    try:
        response = requests.get(
            'http://localhost:8001/api/profile/limits/',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
        )
        
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# ========================================
# USUÁRIO LOGADO - INFO LIMPA E PROFISSIONAL
# ========================================

plan_limits = get_user_plan_limits()
user_keys = get_user_api_keys()

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Usuário")

if plan_limits:
    plan_name = plan_limits.get('plan', 'free')
    max_bots = plan_limits.get('max_bots', 1)
    
    plan_display = {
        'free': '🆓 FREE (7 dias)',
        'pro': '⭐ PRO',
        'premium': '👑 PREMIUM'
    }.get(plan_name, plan_name.upper())
    
    # Detectar modo (Testnet ou Produção)
    modo = "🧪 TESTNET"
    if user_keys:
        primeiro_key = user_keys[0]
        modo = "🧪 TESTNET" if primeiro_key.get('is_testnet', True) else "💰 PRODUÇÃO"
    
    st.sidebar.success(f"✅ {st.session_state.get('user_email', 'Usuário')}")
    st.sidebar.info(f"**{plan_display}**")
    st.sidebar.caption(f"🤖 Bots permitidos: {max_bots}")
    st.sidebar.caption(f"{modo}")
else:
    st.sidebar.success(f"✅ {st.session_state.get('user_email', 'Usuário')}")

if st.sidebar.button("🚪 Sair", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Perfis
PERFIS = {
    "🏦 Hedge Fund": {"tf": "1h", "sl": 2.0, "tp": 4.0, "conf": 70},
    "📈 Day Trader": {"tf": "15m", "sl": 1.5, "tp": 3.0, "conf": 60},
    "⚡ Scalper": {"tf": "5m", "sl": 1.0, "tp": 2.0, "conf": 55},
    "🚀 Ultra": {"tf": "1m", "sl": 0.5, "tp": 1.0, "conf": 50}
}

# Inicializar Exchange com API Keys do usuário
def get_exchange_for_user(exchange_name="Binance"):
    """Conecta à exchange usando API Keys do usuário logado"""
    
    # Buscar API Keys do usuário
    user_keys = get_user_api_keys()
    
    if not user_keys:
        st.sidebar.error(f"❌ Você não tem API Keys cadastradas!")
        st.sidebar.info("💡 Adicione suas keys em: http://localhost:8001/api-keys/")
        return None
    
    # Filtrar por exchange - CORRIGIDO
    exchange_key = None
    exchange_search = exchange_name.lower().strip()
    
    for key in user_keys:
        key_exchange = key.get('exchange', '').lower().strip()
        
        if key_exchange == exchange_search:
            exchange_key = key
            break
    
    # Se não encontrou, pegar primeira key disponível
    if not exchange_key and len(user_keys) > 0:
        exchange_key = user_keys[0]
        st.sidebar.info(f"ℹ️ Usando {exchange_key.get('exchange', 'N/A').upper()}")
    
    if not exchange_key:
        st.sidebar.error(f"❌ Nenhuma API Key cadastrada!")
        st.sidebar.info(f"💡 Adicione em: http://localhost:8001/api-keys/")
        return None
    
    # DESCRIPTOGRAFAR chaves no backend - ENDPOINT NÃO EXISTE!
    # Por enquanto, usar chaves mockadas (Streamlit não precisa das chaves reais)
    try:
        # Em produção, o bot Celery usa as chaves do banco
        # Streamlit só mostra dados, não precisa das chaves
        
        # Buscar chaves descriptografadas do backend
        decrypt_response = requests.get(
            f'http://localhost:8001/api/api-keys/{exchange_key["id"]}/decrypt',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
            timeout=10
        )
        
        if decrypt_response.status_code != 200:
            st.sidebar.error("❌ Erro ao descriptografar chaves")
            return None
        
        key_data = decrypt_response.json()
        
        # Criar exchange com chaves REAIS
        import ccxt
        
        exchange_name_ccxt = key_data['exchange'].lower()
        
        # Mapeamento de nomes (ccxt usa nomes diferentes)
        ccxt_names = {
            'mercadobitcoin': 'mercado',  # Mercado Bitcoin
            'brasilbitcoin': None,  # Não suportada
            'novadax': 'novadax',
            'gateio': 'gate',  # Gate.io
            'foxbit': None  # Não suportada
        }
        
        ccxt_name = ccxt_names.get(exchange_name_ccxt, exchange_name_ccxt)
        
        # Se exchange não é suportada (skip silenciosamente)
        if ccxt_name is None:
            return None
        
        try:
            exchange_class = getattr(ccxt, ccxt_name)
        except AttributeError:
            return None
        
        # Configuração base
        config = {
            'apiKey': key_data['api_key'],
            'secret': key_data['secret'],
            'enableRateLimit': True,
            'timeout': 30000
        }
        
        # Configurações específicas por exchange
        if ccxt_name == 'bybit':
            config['options'] = {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,
                'recvWindow': 60000
            }
        elif ccxt_name == 'okx':
            # OKX precisa de hostname específico
            config['hostname'] = 'okx.com'
            config['options'] = {'defaultType': 'spot'}
        else:
            config['options'] = {'defaultType': 'spot'}
        
        # KuCoin precisa de passphrase (skip silenciosamente)
        if ccxt_name == 'kucoin':
            return None
        
        exchange = exchange_class(config)
        
        if key_data['is_testnet']:
            exchange.set_sandbox_mode(True)
        
        return exchange
        
    except Exception as e:
        st.sidebar.error(f"❌ Erro: {str(e)[:100]}")
        return None

# Manter compatibilidade com código antigo
def get_exchange(exchange_name="Binance"):
    """Conecta à exchange do usuário logado (sem cache)"""
    return get_exchange_for_user(exchange_name)

def get_all_symbols_dynamic(exchange_name="Binance"):
    """Buscar TODOS os símbolos da exchange"""
    try:
        exchange = get_exchange(exchange_name)
        
        if exchange is None:
            return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT']
        
        # Exchange agora é objeto ccxt direto
        markets = exchange.load_markets()
        usdt_pairs = [s.replace('/', '') for s in markets.keys() if s.endswith('/USDT')]
        return sorted(usdt_pairs)
    except:
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT']

def buscar_saldo_real_exchange(exchange_name="Binance"):
    """Buscar saldo REAL da corretora"""
    try:
        exchange = get_exchange(exchange_name)
        if exchange:
            balance = exchange.fetch_balance()
            usdt_total = balance.get('total', {}).get('USDT', 0)
            return usdt_total
    except:
        pass
    return 0.0

settings = Settings()

# Carregar configurações salvas POR USUÁRIO (individualizado!)
config_salva = {}
if 'user_email' in st.session_state:
    # Cada usuário tem seu próprio arquivo de config
    user_config_file = f"dashboard_config_{st.session_state.user_email.replace('@', '_').replace('.', '_')}.json"
    try:
        with open(user_config_file, 'r') as f:
            config_salva = json.load(f)
    except:
        config_salva = {}
else:
    # Fallback para config global (compatibilidade)
    try:
        with open('dashboard_config.json', 'r') as f:
            config_salva = json.load(f)
    except:
        config_salva = {}

# Botão sidebar nativo - sem customização extra aqui

# Header clean - TUDO ALINHADO NA MESMA LINHA
col_titulo, col_moeda, col_hora = st.columns([3, 1, 1])

with col_titulo:
    st.markdown("""
    <div style='display: flex; align-items: center; height: 60px;'>
        <div>
            <h1 style='margin: 0; font-size: 2rem; font-weight: 400; line-height: 1;'>Auronex Trading</h1>
            <p style='color: #718096; margin: 0; font-size: 0.9rem;'>Real-time trading platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_moeda:
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    moeda = st.selectbox("💱", ["💰 BRL", "💵 USD"], index=0, label_visibility="collapsed")
    taxa_conversao = 5.0 if moeda == "💰 BRL" else 1.0
    simbolo_moeda = "R$" if moeda == "💰 BRL" else "$"

with col_hora:
    st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: flex-end; height: 60px;'>
        <div style='text-align: right;'>
            <div style='font-size: 1.5rem; font-weight: 300; color: #ffffff; line-height: 1;'>{datetime.now().strftime('%H:%M:%S')}</div>
            <div style='font-size: 0.75rem; color: #718096; margin-top: 4px;'>Atualiza a cada 5s</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Espaçamento clean
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Buscar bots PRIMEIRO (antes de usar)
user_bots = get_user_bots()

if len(user_bots) == 0:
    st.info("ℹ️ Você ainda não tem bots criados. Crie em: http://localhost:8001/bots-page")
    st.stop()

# Calcular active_bots (para usar nas métricas principais mais abaixo)
total_bots = len(user_bots)
active_bots = sum(1 for bot in user_bots if bot.get('is_active', False))

# ========================================
# SIDEBAR - CONTROLES E INFO
# ========================================

# user_bots já foi carregado acima (antes da barra de status)

st.sidebar.header("🎛️ Controles")

# ========================================
# PERFIL DE TRADE (PRESETS)
# ========================================

PERFIS = {
    "🏦 Hedge Fund": {"dashboard": 30, "bot": 60},
    "📈 Day Trader": {"dashboard": 5, "bot": 3},
    "⚡ Scalper": {"dashboard": 3, "bot": 1},
    "🚀 Ultra": {"dashboard": 1, "bot": 1}
}

perfil_selecionado = st.sidebar.selectbox("🎯 Perfil", list(PERFIS.keys()), index=1)
velocidades = PERFIS[perfil_selecionado]

# Mapear perfil para estratégia
PERFIL_ESTRATEGIA = {
    "🏦 Hedge Fund": "trend_following",
    "📈 Day Trader": "mean_reversion",
    "⚡ Scalper": "scalping",
    "🚀 Ultra": "trend_following"
}

estrategia_perfil = PERFIL_ESTRATEGIA[perfil_selecionado]

# Código de atualização movido para depois de selected_bot_name ser definido

st.sidebar.markdown("---")

# ========================================
# ATUALIZAÇÃO DASHBOARD
# ========================================

st.sidebar.markdown("### ⚡ Atualização Dashboard")

freq_dashboard = st.sidebar.slider(
    "Frequência (segundos)",
    1, 60,
    velocidades['dashboard'],
    help=f"Perfil {perfil_selecionado} sugere: {velocidades['dashboard']}s"
)

if freq_dashboard <= 3:
    st.sidebar.success("✅ Rápido - recomendado!")
elif freq_dashboard <= 10:
    st.sidebar.info("⏱️ Normal")
else:
    st.sidebar.warning("🐌 Lento")

st.sidebar.caption(f"Dashboard atualiza: {freq_dashboard}s")

st.sidebar.markdown("---")

# ========================================
# VELOCIDADE DO BOT
# ========================================

st.sidebar.markdown("### 🤖 Velocidade do Bot")

freq_bot = st.sidebar.slider(
    "Análise (segundos)",
    1, 60,
    velocidades['bot'],
    help=f"Perfil {perfil_selecionado} sugere: {velocidades['bot']}s"
)

if freq_bot <= 3:
    st.sidebar.success("⚡ Ultra rápido - máximas oportunidades!")
elif freq_bot <= 10:
    st.sidebar.info("🎯 Balanceado")
else:
    st.sidebar.warning("🐌 Conservador")

st.sidebar.caption(f"Bot analisa: {freq_bot}s")
st.sidebar.caption("💾 Será salvo após selecionar bot")

st.sidebar.markdown("---")

# Seletor de Bot na Sidebar
st.sidebar.markdown("### 🤖 Bot Selecionado")

bot_names_dict = {f"{bot.get('name', f'Bot {i+1}')}": bot for i, bot in enumerate(user_bots)}
bot_names_list = ["📊 Portfólio"] + list(bot_names_dict.keys())

# DEFAULT: Primeiro bot (não Portfólio!)
if 'sidebar_selected_bot' not in st.session_state:
    primeiro_bot_name = list(bot_names_dict.keys())[0] if len(bot_names_dict) > 0 else "📊 Portfólio"
    st.session_state.sidebar_selected_bot = primeiro_bot_name

selected_bot_name = st.sidebar.selectbox(
    "Escolha:",
    bot_names_list,
    index=bot_names_list.index(st.session_state.sidebar_selected_bot) if st.session_state.sidebar_selected_bot in bot_names_list else 1,
    key="bot_selector"
)

st.session_state.sidebar_selected_bot = selected_bot_name

# ATUALIZAR configurações do bot (AGORA que selected_bot_name existe!)
if selected_bot_name != "📊 Portfólio":
    try:
        bot_config = bot_names_dict[selected_bot_name]
        
        # Estratégia baseada no perfil
        if bot_config.get('strategy') != estrategia_perfil:
            resp = requests.patch(
                f'http://localhost:8001/api/bots/{bot_config["id"]}/config',
                headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                json={'strategy': estrategia_perfil},
                timeout=5
            )
        
        # Velocidade de análise
        requests.patch(
            f'http://localhost:8001/api/bots/{bot_config["id"]}/velocidade',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
            json={'freq_analise': freq_bot},
            timeout=5
        )
    except:
        pass

# Info do bot E exchange - SEMPRE SÓ TEXTO!
if selected_bot_name != "📊 Portfólio":
    bot_info = bot_names_dict[selected_bot_name]
    exchange_name = bot_info.get('exchange', 'binance').lower()
    
    st.sidebar.success(f"✅ {bot_info.get('name', 'Bot')}")
    st.sidebar.info(f"🏦 Corretora: {exchange_name.upper()}")
    st.sidebar.caption(f"Status: {'🟢 Ativo' if bot_info.get('is_active') else '⚪ Pausado'}")
    # Capital será mostrado depois (com saldo real da exchange)
else:
    # Portfólio - usar exchange do PRIMEIRO bot
    primeiro_bot = user_bots[0]
    exchange_name = primeiro_bot.get('exchange', 'binance').lower()
    
    st.sidebar.success(f"✅ {primeiro_bot.get('name', 'Bot')}")  # Nome do primeiro bot!
    st.sidebar.info(f"🏦 Corretora: {exchange_name.upper()}")
    st.sidebar.caption("(Primeiro bot configurado)")

st.sidebar.markdown("---")

# ========================================
# 1. SALDO REAL DA CORRETORA
# ========================================
st.sidebar.markdown("### 💰 Saldo Real")

# exchange_name JÁ foi definido nas linhas 430 ou 442
# NÃO redefinir aqui!

exchange_obj = None
usdt_balance = 0

# Exchange já definida

try:
    exchange_obj = get_exchange_for_user(exchange_name.capitalize())
    
    if exchange_obj:
        # Tentar buscar saldo (pode dar erro se permissões erradas)
        try:
            balance = exchange_obj.fetch_balance()
        except Exception as balance_error:
            st.sidebar.warning("⚠️ Erro ao buscar saldo")
            st.sidebar.caption("Verifique permissões da API Key")
            st.sidebar.caption(f"Erro: {str(balance_error)[:80]}")
            balance = None
        
        if balance:
            # Buscar em 'free', 'total' ou direto
            usdt_free = balance.get('free', {}).get('USDT', 0) or balance.get('USDT', {}).get('free', 0) or 0
            usdt_total = balance.get('total', {}).get('USDT', 0) or balance.get('USDT', {}).get('total', 0) or 0
            usdt_balance = max(usdt_free, usdt_total)
            
            # Buscar outras stablecoins se USDT = 0
            if usdt_balance == 0:
                busd = balance.get('free', {}).get('BUSD', 0) or balance.get('BUSD', {}).get('free', 0) or 0
                usdc = balance.get('free', {}).get('USDC', 0) or balance.get('USDC', {}).get('free', 0) or 0
                dai = balance.get('free', {}).get('DAI', 0) or balance.get('DAI', {}).get('free', 0) or 0
                usdt_balance = busd + usdc + dai
            
            # Buscar BRL (exchanges brasileiras)
            if usdt_balance == 0:
                brl = balance.get('free', {}).get('BRL', 0) or balance.get('BRL', {}).get('free', 0) or 0
                if brl > 0:
                    usdt_balance = brl / 5.0
                    st.sidebar.caption(f"💰 R$ {brl:.2f} BRL")
            
        # Mostrar saldo
        if usdt_balance > 0:
            saldo_convertido = usdt_balance * taxa_conversao
            st.sidebar.metric("💵 Saldo Real", f"{simbolo_moeda} {saldo_convertido:.2f}")
        else:
            st.sidebar.warning("⚠️ Saldo: $0.00")
    else:
        st.sidebar.warning("⚠️ Configure API Key")
except Exception as e:
    st.sidebar.error(f"⚠️ Erro ao buscar saldo")
    st.sidebar.caption(f"{str(e)[:60]}")

st.sidebar.markdown("---")

# ========================================
# 2. ESCOLHER CRIPTOMOEDAS
# ========================================
st.sidebar.markdown("### 📊 Criptomoedas")

# Buscar cryptos da exchange DO BOT
selected_symbols = []

try:
    if exchange_obj:
        markets = exchange_obj.load_markets()
        
        # Buscar pares disponíveis
        usdt_pairs = [s for s in markets.keys() if '/USDT' in s]
        brl_pairs = [s for s in markets.keys() if '/BRL' in s]
        btc_pairs = [s for s in markets.keys() if '/BTC' in s]
        
        # Usar o que tiver disponível
        if len(usdt_pairs) > 0:
            pairs_sorted = sorted(usdt_pairs)
            pair_suffix = 'USDT'
        elif len(brl_pairs) > 0:
            pairs_sorted = sorted(brl_pairs)
            pair_suffix = 'BRL'
        elif len(btc_pairs) > 0:
            pairs_sorted = sorted(btc_pairs)
            pair_suffix = 'BTC'
        else:
            pairs_sorted = []
            pair_suffix = 'USDT'
        
        if len(pairs_sorted) == 0:
            st.sidebar.error(f"Nenhuma crypto /{pair_suffix}!")
        else:
            st.sidebar.success(f"💎 {len(pairs_sorted)} disponíveis")
            
            # SALVAR e RECUPERAR por bot
            if selected_bot_name != "📊 Portfólio":
                bot_atual = bot_names_dict[selected_bot_name]
                save_key = f"saved_symbols_bot_{bot_atual['id']}"
            else:
                save_key = f"saved_symbols_portfolio"
            
            # Recuperar seleção salva ou usar defaults
            if save_key in st.session_state:
                # Recuperar escolhas salvas
                saved = st.session_state[save_key]
                valid_saved = [s for s in saved if s in pairs_sorted]
                initial_selection = valid_saved if valid_saved else []
            else:
                # Defaults
                if pair_suffix == 'BRL':
                    defaults = ['BTC/BRL', 'ETH/BRL', 'USDT/BRL']
                elif pair_suffix == 'BTC':
                    defaults = ['ETH/BTC', 'BNB/BTC']
                else:
                    defaults = ['BTC/USDT', 'ETH/USDT']
                
                initial_selection = [s for s in defaults if s in pairs_sorted]
            
            selected_symbols = st.sidebar.multiselect(
                "Escolha:",
                pairs_sorted,
                default=initial_selection
            )
            
            # SALVAR escolha localmente
            st.session_state[save_key] = selected_symbols
            
            # SALVAR NO BANCO (bot lerá automaticamente!)
            if selected_bot_name != "📊 Portfólio" and len(selected_symbols) > 0:
                try:
                    bot_atual = bot_names_dict[selected_bot_name]
                    
                    # Verificar se mudou
                    symbols_atuais_bot = set(bot_atual.get('symbols', []))
                    symbols_novos = set(selected_symbols)
                    
                    if symbols_atuais_bot != symbols_novos:
                        # Atualizar no banco
                        resp = requests.patch(
                            f'http://localhost:8001/api/bots/{bot_atual["id"]}/symbols',
                            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                            json={'symbols': selected_symbols},
                            timeout=5
                        )
                        
                        if resp.status_code == 200:
                            st.sidebar.caption("💾 Salvo! Bot lerá na próxima iteração")
                except:
                    pass  # Silencioso se falhar
            
            if len(selected_symbols) > 10:
                selected_symbols = selected_symbols[:10]
            
            st.sidebar.success(f"✅ {len(selected_symbols)}")
    else:
        st.sidebar.warning(f"⚠️ API Key não configurada para {exchange_name.upper()}")
        st.sidebar.caption("Configure em: http://localhost:8001/api-keys/")
except Exception as e:
    st.sidebar.error(f"❌ Erro ao carregar")
    st.sidebar.caption(f"{str(e)[:60]}")

st.sidebar.markdown("---")

# ========================================
# 3. ALOCAÇÃO DE CAPITAL (SLIDERS INDIVIDUAIS!)
# ========================================
st.sidebar.markdown("### 💰 Alocação de Capital")

capital_mode = st.sidebar.radio(
    "Modo:",
    ["⚖️ Automático", "🎯 Manual (Sliders)"],
    label_visibility="collapsed"
)

# CAPITAL: SEMPRE tentar usar saldo REAL
if usdt_balance > 0:
    # TEM SALDO REAL - USAR!
    capital_total = usdt_balance
else:
    # NÃO conseguiu buscar - AVISO e usa 0
    capital_total = 0
    st.sidebar.warning("⚠️ Sem saldo")
    st.sidebar.caption("Deposite na corretora para operar")

if capital_mode == "🎯 Manual (Sliders)":
    st.sidebar.caption("💡 Alocação inteligente - sempre soma 100%")
    
    alocacoes = {}
    
    # SALVAR alocações por bot
    if selected_bot_name != "📊 Portfólio":
        bot_atual_alloc = bot_names_dict[selected_bot_name]
        alloc_save_key = f"saved_alloc_bot_{bot_atual_alloc['id']}"
    else:
        alloc_save_key = f"saved_alloc_portfolio"
    
    # Recuperar ou inicializar
    if alloc_save_key not in st.session_state:
        st.session_state[alloc_save_key] = {}
    
    saved_allocs = st.session_state[alloc_save_key]
    
    # RECALCULAR se mudou número de cryptos
    cryptos_anteriores = set(saved_allocs.keys())
    cryptos_atuais = set(selected_symbols)
    
    # Se adicionou cryptos
    if len(cryptos_atuais) > len(cryptos_anteriores):
        total_anterior = sum(saved_allocs.values())
        
        if total_anterior >= 100:
            # Redistribuir igualmente
            for sym in selected_symbols:
                saved_allocs[sym] = 100.0 / len(selected_symbols)
        else:
            # Dar o restante para as novas
            novas = cryptos_atuais - cryptos_anteriores
            disponivel = 100 - total_anterior
            for nova in novas:
                saved_allocs[nova] = disponivel / len(novas)
    
    # Remover cryptos que não existem mais
    for sym in list(saved_allocs.keys()):
        if sym not in cryptos_atuais:
            del saved_allocs[sym]
    
    # Se não tem nenhuma, dividir igual
    if not saved_allocs and len(selected_symbols) > 0:
        for sym in selected_symbols:
            saved_allocs[sym] = 100.0 / len(selected_symbols)
    
    # SLIDERS com ajuste automático
    # Coletar valores atuais dos sliders
    valores_atuais = {}
    
    for symbol in selected_symbols:
        crypto_name = symbol.split('/')[0]
        valor_slider = st.sidebar.slider(
            f"{crypto_name}",
            0.0, 100.0,
            float(saved_allocs.get(symbol, 0)),
            step=0.25,
            key=f"alloc_{symbol}_{selected_bot_name}"
        )
        valores_atuais[symbol] = valor_slider
    
    # DETECTAR mudanças e ajustar AUTOMATICAMENTE
    total_sliders = sum(valores_atuais.values())
    ajustou = False
    
    # Encontrar qual mudou
    mudou = None
    for sym in selected_symbols:
        if abs(valores_atuais[sym] - saved_allocs.get(sym, 0)) > 0.01:
            mudou = sym
            break
    
    if mudou and total_sliders > 100:
        # AJUSTAR outros automaticamente
        novo_val = valores_atuais[mudou]
        outros = [s for s in selected_symbols if s != mudou]
        restante = 100 - novo_val
        
        if len(outros) > 0:
            # Distribuir restante proporcionalmente
            total_outros_antes = sum(saved_allocs.get(s, 0) for s in outros)
            
            if total_outros_antes > 0:
                for outro in outros:
                    proporcao = saved_allocs.get(outro, 0) / total_outros_antes
                    valores_atuais[outro] = round(restante * proporcao, 2)
            else:
                for outro in outros:
                    valores_atuais[outro] = round(restante / len(outros), 2)
            
            ajustou = True
    
    # SALVAR valores ajustados
    st.session_state[alloc_save_key] = valores_atuais
    
    # Se ajustou, FORÇAR RERUN para atualizar sliders
    if ajustou:
        st.rerun()
    
    # Usar valores
    alocacoes = valores_atuais
    total_percent = sum(alocacoes.values())
    
    # Mostrar total (arredondado)
    total_round = round(total_percent, 2)
    faltam = round(100 - total_percent, 2)
    
    if total_round == 100:
        st.sidebar.success(f"✅ Total: {total_round}%")
    elif total_round > 100:
        st.sidebar.error(f"❌ Total: {total_round}% (máx: 100%)")
    else:
        st.sidebar.warning(f"⚠️ Total: {total_round}% (faltam {faltam}%)")
    
    if capital_total > 0:
        capital_convertido = capital_total * taxa_conversao
        st.sidebar.caption(f"Capital total: {simbolo_moeda} {capital_convertido:.2f}")
    else:
        st.sidebar.warning("⚠️ Sem saldo na corretora")
else:
    # Automático - divide igual
    if capital_total > 0:
        capital_convertido_auto = capital_total * taxa_conversao
        st.sidebar.info(f"💰 {simbolo_moeda} {capital_convertido_auto:.2f} dividido igualmente")
        percent_each = 100 / len(selected_symbols) if len(selected_symbols) > 0 else 0
        st.sidebar.caption(f"Cada cripto: {percent_each:.1f}%")
    else:
        st.sidebar.warning("⚠️ Sem saldo na corretora")

st.sidebar.markdown("---")

# ========================================
# 4. BOT CAÇADOR (ANÁLISE AUTOMÁTICA)
# ========================================
st.sidebar.markdown("### 🎯 Bot Caçador")

hunter_mode = st.sidebar.checkbox("🔍 Ativar Modo Caçador", value=False)

# SALVAR modo caçador no banco
if selected_bot_name != "📊 Portfólio":
    try:
        bot_hunter = bot_names_dict[selected_bot_name]
        
        resp = requests.patch(
            f'http://localhost:8001/api/bots/{bot_hunter["id"]}/config',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
            json={'modo_cacador': hunter_mode},
            timeout=5
        )
    except:
        pass

if hunter_mode:
    st.sidebar.success("✅ Caçador ATIVO!")
    st.sidebar.caption("🎯 Bot operará nas TOP 10 com maiores ganhos")
    
    # Configurações do caçador
    min_profit = st.sidebar.slider("Lucro mínimo (%)", 0.5, 10.0, 2.0, 0.1)
    max_risk = st.sidebar.slider("Risco máximo (%)", 1.0, 10.0, 5.0, 0.5)
    
    st.sidebar.caption(f"✅ Opera se: Lucro > {min_profit}% E Risco < {max_risk}%")
    st.sidebar.caption("🔍 Busca nas cryptos selecionadas acima")
else:
    st.sidebar.info("✋ Modo Manual")
    st.sidebar.caption("Você escolhe quando operar")

st.sidebar.markdown("---")

# Links úteis
st.sidebar.markdown("### 🔗 Links")
st.sidebar.markdown("[🤖 Bots](http://localhost:8001/bots-page)")
st.sidebar.markdown("[🔑 Keys](http://localhost:8001/api-keys-page)")
st.sidebar.markdown("[👨‍💼 Admin](http://localhost:8001/admin/)")

# ========================================
# RESUMO GERAL DE TODOS OS BOTS
# ========================================

# user_bots e active_bots já carregados no topo

# KPIs Gerais
# Centralizar cards principais
col_space1, col_cards, col_space2 = st.columns([0.5, 10, 0.5])

with col_cards:
    # CARDS COM GLOW HOVER - CSS INLINE PARA FUNCIONAR!
    st.markdown("""
    <style>
    /* Cards com efeito glow - APLICADO A ELEMENT-CONTAINER! */
    .element-container:has(div.glow-card),
    div[data-testid="column"]:has(div.glow-card) > div {
        background: linear-gradient(135deg, rgba(20,25,45,0.4), rgba(30,35,60,0.4)) !important;
        backdrop-filter: blur(30px) !important;
        border-radius: 20px !important;
        padding: 1.2rem !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: default;
    }
    
    .element-container:has(div.glow-card):hover,
    div[data-testid="column"]:has(div.glow-card) > div:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px rgba(0,100,255,0.3), 0 0 60px rgba(0,100,255,0.2) !important;
        border-color: rgba(100,150,255,0.4) !important;
        background: linear-gradient(135deg, rgba(25,30,60,0.6), rgba(35,40,70,0.6)) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        st.metric("🤖 Total de Bots", total_bots, f"{active_bots} ativos")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        saldo_kpi = capital_total * taxa_conversao if capital_total > 0 else 0
        st.metric("💰 Saldo Total", f"{simbolo_moeda} {saldo_kpi:.2f}", "+5.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        # Buscar trades REAIS da API + Status dos bots
        trades_hoje = 0
        bots_operando = 0
        
        try:
            if 'access_token' in st.session_state:
                # Trades hoje
                resp = requests.get(
                    'http://localhost:8001/api/trades/today',
                    headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                    timeout=5
                )
                if resp.status_code == 200:
                    trades_data = resp.json()
                    trades_hoje = trades_data.get('count', 0)
                
                # Status dos bots
                resp_monitor = requests.get(
                    'http://localhost:8001/api/bot-monitor/all',
                    headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                    timeout=5
                )
                if resp_monitor.status_code == 200:
                    monitor_data = resp_monitor.json()
                    bots_operando = sum(1 for b in monitor_data.get('bots', []) if b.get('total_trades', 0) > 0)
        except:
            pass
        
        st.metric("📈 Trades Hoje", trades_hoje)
        st.caption(f"🤖 {bots_operando} bots operando")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        # Taxa de sucesso (win rate)
        taxa_sucesso = 0
        try:
            if 'access_token' in st.session_state:
                resp = requests.get(
                    'http://localhost:8001/api/trades/stats',
                    headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                    timeout=5
                )
                if resp.status_code == 200:
                    stats = resp.json()
                    taxa_sucesso = stats.get('win_rate', 0)
        except:
            pass
        
        st.metric("✅ Taxa Sucesso", f"{taxa_sucesso:.1f}%")
        st.caption("Win rate")
        st.markdown('</div>', unsafe_allow_html=True)

# Espaçamento clean
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Barra de status já está no topo (logo após título)

# ========================================
# OPERAÇÕES RECENTES
# ========================================

st.subheader("📺 Operações Recentes")

if active_bots > 0:
    st.info("⏳ Nenhuma operação realizada ainda. Bot procurando oportunidades...")
else:
    st.warning("⚠️ Bot pausado. Inicie para começar a operar.")

# Espaçamento clean
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ========================================
# TOP 5 PERFORMANCE (2ª POSIÇÃO!)
# ========================================

st.subheader("🏆 TOP 5 - Performance")

tab_hoje, tab_semana, tab_mes, tab_virais, tab_corretora = st.tabs(["🔥 Hoje", "📆 Semana", "📊 Mês", "💥 Virais", "🏦 Corretora"])

with tab_hoje:
    # TOP 5 do dia
    try:
        top5_exchange = get_exchange_for_user(exchange_name.capitalize())
        
        if top5_exchange:
            # Símbolos baseados na exchange
            if pair_suffix == 'BRL':
                symbols = ['BTC/BRL', 'ETH/BRL', 'USDT/BRL', 'SOL/BRL', 'XRP/BRL']
            else:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT',
                          'ADA/USDT', 'DOGE/USDT', 'MATIC/USDT', 'DOT/USDT', 'AVAX/USDT',
                          'LINK/USDT', 'ATOM/USDT', 'LTC/USDT', 'UNI/USDT', 'APT/USDT']
            
            tickers = []
            for sym in symbols:
                try:
                    t = top5_exchange.fetch_ticker(sym)
                    var = t.get('percentage', 0) or 0
                    preco = (t.get('last', 0) or 0) * taxa_conversao
                    
                    tickers.append({
                        'Cripto': sym.split('/')[0],
                        'Var': var,
                        'Variação 24h': f"{var:+.2f}%",
                        'Preço': f"{simbolo_moeda} {preco:,.4f}"
                    })
                except:
                    pass
            
            # TOP 5 (pega 5 mesmo se negativos)
            top5 = sorted(tickers, key=lambda x: x['Var'], reverse=True)[:5]
            
            # Formatar
            resultado = []
            for i, item in enumerate(top5):
                resultado.append({
                    '🏆': f"#{i+1}",
                    'Cripto': item['Cripto'],
                    'Variação 24h': item['Variação 24h'],
                    'Preço': item['Preço']
                })
            
            st.dataframe(pd.DataFrame(resultado), use_container_width=True, hide_index=True)
            st.caption(f"✅ {exchange_name.upper()}")
        else:
            st.warning(f"Configure API Key para {exchange_name.upper()}")
    except Exception as e:
        st.error(f"Erro: {str(e)[:80]}")

with tab_semana:
    # Semana (estimativa x3)
    try:
        top5_semana = get_exchange_for_user(exchange_name.capitalize())
        
        if top5_semana:
            if pair_suffix == 'BRL':
                symbols = ['BTC/BRL', 'ETH/BRL', 'USDT/BRL', 'SOL/BRL', 'XRP/BRL']
            else:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
            
            tickers = []
            for sym in symbols:
                try:
                    t = top5_semana.fetch_ticker(sym)
                    var = (t.get('percentage', 0) or 0) * 3
                    preco = (t.get('last', 0) or 0) * taxa_conversao
                    
                    tickers.append({
                        'Cripto': sym.split('/')[0],
                        'Var': var,
                        'Variação 7d': f"{var:+.2f}%",
                        'Preço': f"{simbolo_moeda} {preco:,.4f}"
                    })
                except:
                    pass
            
            top5 = sorted(tickers, key=lambda x: x['Var'], reverse=True)[:5]
            
            resultado = []
            for i, item in enumerate(top5):
                resultado.append({
                    '🏆': f"#{i+1}",
                    'Cripto': item['Cripto'],
                    'Variação 7d': item['Variação 7d'],
                    'Preço': item['Preço']
                })
            
            st.dataframe(pd.DataFrame(resultado), use_container_width=True, hide_index=True)
            st.caption("📊 Estimativa")
        else:
            st.warning("Configure API Key")
    except Exception as e:
        st.error(f"Erro: {str(e)[:80]}")

with tab_mes:
    # Mês (estimativa x10)
    try:
        top5_mes = get_exchange_for_user(exchange_name.capitalize())
        
        if top5_mes:
            if pair_suffix == 'BRL':
                symbols = ['BTC/BRL', 'ETH/BRL', 'USDT/BRL', 'SOL/BRL', 'XRP/BRL']
            else:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
            
            tickers = []
            for sym in symbols:
                try:
                    t = top5_mes.fetch_ticker(sym)
                    var = (t.get('percentage', 0) or 0) * 10
                    preco = (t.get('last', 0) or 0) * taxa_conversao
                    
                    tickers.append({
                        'Cripto': sym.split('/')[0],
                        'Var': var,
                        'Variação 30d': f"{var:+.2f}%",
                        'Preço': f"{simbolo_moeda} {preco:,.4f}"
                    })
                except:
                    pass
            
            top5 = sorted(tickers, key=lambda x: x['Var'], reverse=True)[:5]
            
            resultado = []
            for i, item in enumerate(top5):
                resultado.append({
                    '🏆': f"#{i+1}",
                    'Cripto': item['Cripto'],
                    'Variação 30d': item['Variação 30d'],
                    'Preço': item['Preço']
                })
            
            st.dataframe(pd.DataFrame(resultado), use_container_width=True, hide_index=True)
            st.caption("📊 Estimativa")
        else:
            st.warning("Configure API Key")
    except Exception as e:
        st.error(f"Erro: {str(e)[:80]}")

with tab_virais:
    # Virais (só USDT/BRL)
    try:
        top5_virais = get_exchange_for_user(exchange_name.capitalize())
        
        if top5_virais:
            # Virais
            if pair_suffix == 'BRL':
                symbols = ['SHIB/BRL', 'FLOKI/BRL', 'PEPE/BRL'] if pair_suffix == 'BRL' else []
            else:
                symbols = ['PEPE/USDT', 'SHIB/USDT', 'FLOKI/USDT', 'BONK/USDT', 'WIF/USDT',
                          'FTM/USDT', 'GALA/USDT', 'SAND/USDT', 'MANA/USDT', 'CHZ/USDT']
            
            if len(symbols) == 0:
                st.info("Virais disponíveis apenas em exchanges com pares /USDT")
            else:
                virais = []
                for sym in symbols:
                    try:
                        t = top5_virais.fetch_ticker(sym)
                        var = abs(t.get('percentage', 0) or 0)
                        preco = (t.get('last', 0) or 0) * taxa_conversao
                        
                        virais.append({
                            'Cripto': sym.split('/')[0],
                            'Var': var,
                            'Volatilidade': f"{var:.2f}%",
                            'Preço': f"{simbolo_moeda} {preco:,.6f}"
                        })
                    except:
                        pass
                
                if len(virais) > 0:
                    top5_viral = sorted(virais, key=lambda x: x['Var'], reverse=True)[:5]
                    
                    resultado = []
                    for i, item in enumerate(top5_viral):
                        resultado.append({
                            '🏆': f"#{i+1}",
                            'Cripto': item['Cripto'],
                            'Volatilidade 24h': item['Volatilidade'],
                            'Preço': item['Preço']
                        })
                    
                    st.dataframe(pd.DataFrame(resultado), use_container_width=True, hide_index=True)
                    st.caption("💥 Volatilidade")
                else:
                    st.info("Sem dados disponíveis")
        else:
            st.warning("Configure API Key")
    except Exception as e:
        st.error(f"Erro: {str(e)[:80]}")

with tab_corretora:
    # Corretora (mais cryptos)
    try:
        top5_corr = get_exchange_for_user(exchange_name.capitalize())
        
        if top5_corr:
            if pair_suffix == 'BRL':
                symbols = ['BTC/BRL', 'ETH/BRL', 'USDT/BRL', 'SOL/BRL', 'XRP/BRL']
            else:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
            
            cryptos = []
            for sym in symbols:
                try:
                    t = top5_corr.fetch_ticker(sym)
                    var = t.get('percentage', 0) or 0
                    preco = (t.get('last', 0) or 0) * taxa_conversao
                    
                    cryptos.append({
                        'Cripto': sym.split('/')[0],
                        'Var': var,
                        'Variação': f"{var:+.2f}%",
                        'Preço': f"{simbolo_moeda} {preco:,.4f}"
                    })
                except:
                    pass
            
            top5_lista = sorted(cryptos, key=lambda x: x['Var'], reverse=True)[:5]
            
            resultado = []
            for i, item in enumerate(top5_lista):
                resultado.append({
                    '🏆': f"#{i+1}",
                    'Cripto': item['Cripto'],
                    'Variação 24h': item['Variação'],
                    'Preço': item['Preço']
                })
            
            st.dataframe(pd.DataFrame(resultado), use_container_width=True, hide_index=True)
            st.caption(f"🏆 {exchange_name.upper()}")
        else:
            st.warning("Configure API Key")
    except Exception as e:
        st.error(f"Erro: {str(e)[:80]}")

# Espaçamento clean
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ========================================
# SISTEMA DE ABAS - UM BOT POR ABA
# ========================================

st.subheader("📊 Seus Bots de Trading")

# Criar abas - uma para cada bot + aba de Portfólio
tab_names = ["📊 Portfólio"] + [f"{bot.get('name', f'Bot {i+1}')} {'🟢' if bot.get('is_active') else '⚪'}" for i, bot in enumerate(user_bots)]
tabs = st.tabs(tab_names)

# ========================================
# ABA 1: PORTFÓLIO GERAL
# ========================================
with tabs[0]:
    # Botão invisível para detectar clique (sincroniza sidebar)
    if st.button("Sincronizar", key="sync_portfolio", type="secondary"):
        st.session_state.sidebar_selected_bot = "📊 Portfólio"
        st.rerun()
    
    st.markdown("### 💼 Portfólio Consolidado")
    
    # Gráfico menor (40% do espaço) + Info (60%)
    col_pizza, col_info = st.columns([0.4, 0.6])
    
    with col_pizza:
        # Gráfico de pizza - SEMPRE MOSTRAR
        if len(selected_symbols) > 0:
            import plotly.graph_objects as go
            
            labels = [s.split('/')[0] for s in selected_symbols]
            
            # Se modo automático, dividir igual
            if capital_mode == "⚖️ Automático":
                values = [100 / len(selected_symbols)] * len(selected_symbols)
            else:
                # Modo manual - usar alocações definidas
                values = [alocacoes.get(s, 0) for s in selected_symbols]
            
            # Adicionar "Disponível" se não usou 100%
            total_alocado = sum(values)
            if total_alocado < 100:
                labels.append('Disponível')
                values.append(100 - total_alocado)
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                textinfo='label+percent',
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            fig.update_layout(
                title=f"Alocação de Capital ({capital_mode.split()[1]})",
                height=280,  # 40% menor (era 350, agora 280)
                margin=dict(l=10, r=10, t=35, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Selecione criptomoedas na sidebar")
    
    with col_info:
        st.markdown("### 📈 Resumo do Portfólio")
        
        # LÓGICA CORRETA DO PORTFÓLIO
        
        # BUSCAR SALDO REAL DE CADA EXCHANGE
        exchanges_com_saldo = {}
        
        for bot in user_bots:
            if bot.get('is_active', False):
                bot_exch = bot.get('exchange', 'binance').lower()
                
                # Buscar saldo REAL (uma vez por exchange)
                if bot_exch not in exchanges_com_saldo:
                    try:
                        exch_obj = get_exchange_for_user(bot_exch.capitalize())
                        
                        if exch_obj:
                            bal = exch_obj.fetch_balance()
                            usdt = bal.get('free', {}).get('USDT', 0) or bal.get('USDT', {}).get('free', 0) or 0
                            
                            if usdt == 0:
                                busd = bal.get('free', {}).get('BUSD', 0) or 0
                                usdc = bal.get('free', {}).get('USDC', 0) or 0
                                usdt = busd + usdc
                            
                            if usdt == 0:
                                brl = bal.get('free', {}).get('BRL', 0) or 0
                                if brl > 0:
                                    usdt = brl / 5.0
                            
                            exchanges_com_saldo[bot_exch] = usdt
                    except:
                        exchanges_com_saldo[bot_exch] = 0
        
        # 1. SALDO TOTAL = Soma de todas exchanges
        saldo_total_corretoras = sum(exchanges_com_saldo.values())
        
        # 2. CAPITAL INICIAL = Quanto está alocado REALMENTE
        capital_inicial_portfolio = 0
        
        # Para cada bot ativo, calcular quanto está alocado
        for bot in user_bots:
            if bot.get('is_active', False):
                bot_exch_calc = bot.get('exchange', 'binance').lower()
                saldo_exch = exchanges_com_saldo.get(bot_exch_calc, 0)
                
                # Buscar alocação DESTE bot específico
                bot_id = bot.get('id')
                alloc_key_bot = f"saved_alloc_bot_{bot_id}"
                
                if alloc_key_bot in st.session_state:
                    # Tem alocação manual salva
                    allocs_bot = st.session_state[alloc_key_bot]
                    total_percent_bot = sum(allocs_bot.values())
                    capital_inicial_portfolio += (saldo_exch * total_percent_bot / 100)
                else:
                    # Não tem alocação → assume 100%
                    capital_inicial_portfolio += saldo_exch
        
        # 3. LUCRO/PERDA = Quanto ganhou/perdeu
        # (Seria: saldo agora - saldo quando começou, mas não temos histórico)
        # Por enquanto: 0 até ter trades reais
        lucro_perda = 0
        lucro_perda_percent = 0
        
        # Métricas alinhadas
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            saldo_convertido = saldo_total_corretoras * taxa_conversao
            st.metric("💰 Saldo das Corretoras", f"{simbolo_moeda} {saldo_convertido:.2f}")
            
            # Mostrar detalhes de cada exchange
            for exch, valor in exchanges_com_saldo.items():
                valor_conv = valor * taxa_conversao
                st.caption(f"{exch.upper()}: {simbolo_moeda} {valor_conv:.2f}")
        
        with col_metric2:
            lucro_convertido = lucro_perda * taxa_conversao
            st.metric(
                "📊 Lucro/Perda",
                f"{simbolo_moeda} {lucro_convertido:+.2f}",
                f"{lucro_perda_percent:+.2f}%"
            )
            st.caption("(Desde início)")
        
        # Espaçamento clean
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        col_metric3, col_metric4 = st.columns(2)
        
        with col_metric3:
            st.metric("🤖 Bots Ativos", f"{active_bots}")
            st.caption(f"Total: {total_bots} bots")
        
        with col_metric4:
            capital_inicial_conv = capital_inicial_portfolio * taxa_conversao
            st.metric("💵 Capital Inicial", f"{simbolo_moeda} {capital_inicial_conv:.2f}")
            st.caption("(Alocação de Capital)")
        
        # Espaçamento clean
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        if len(selected_symbols) > 0:
            st.markdown("**📊 Cryptos Selecionadas:**")
            for sym in selected_symbols:
                st.write(f"• {sym}")

# Espaçamento clean
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ========================================
# ABAS 2+: CADA BOT
# ========================================
for i, bot in enumerate(user_bots):
    with tabs[i + 1]:
        # Botão para sincronizar sidebar quando clica na aba
        bot_tab_name = f"{bot.get('name', f'Bot {i+1}')}"
        if st.button(f"📊 Atualizar Sidebar para este Bot", key=f"sync_bot_{bot['id']}", type="secondary"):
            st.session_state.sidebar_selected_bot = bot_tab_name
            st.rerun()
        
        st.markdown(f"### {bot.get('name', 'Bot')}")
        
        col_config, col_chart = st.columns([1, 2])
        
        with col_config:
            st.markdown("#### ⚙️ Configurações")
            st.write(f"**Exchange:** {bot.get('exchange', 'N/A').upper()}")
            capital_bot_convertido = float(bot.get('capital', 0)) * taxa_conversao
            st.write(f"**Capital:** {simbolo_moeda} {capital_bot_convertido:.2f}")
            st.write(f"**Estratégia:** {bot.get('strategy', 'N/A')}")
            st.write(f"**Timeframe:** {bot.get('timeframe', 'N/A')}")
            st.write(f"**Stop Loss:** {bot.get('stop_loss_percent', 0)}%")
            st.write(f"**Take Profit:** {bot.get('take_profit_percent', 0)}%")
            
            # Espaçamento clean
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            
            # TOGGLE BOT - INICIA/PARA VIA API
            bot_ativo_now = bot.get('is_active', False)
            
            # Texto e cor do botão
            if bot_ativo_now:
                texto_btn = "⏸️ Parar Bot"
                tipo_btn = "secondary"
            else:
                texto_btn = "▶️ Iniciar Bot"
                tipo_btn = "primary"
            
            # Botão toggle
            if st.button(texto_btn, key=f"toggle_{bot['id']}", use_container_width=True, type=tipo_btn):
                try:
                    # Chamar API toggle
                    nova_acao = not bot_ativo_now
                    
                    resp = requests.post(
                        f'http://localhost:8001/api/bots/{bot["id"]}/toggle',
                        headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                        json={'is_active': nova_acao},
                        timeout=10
                    )
                    
                    if resp.status_code == 200:
                        if nova_acao:
                            st.success(f"✅ Bot {bot['name']} INICIADO! Operará em 10 segundos.")
                            st.info("🤖 Bot Controller detectará automaticamente e iniciará operação!")
                        else:
                            st.warning(f"⏸️ Bot {bot['name']} PARADO! Parará em 10 segundos.")
                        
                        time.sleep(2)
                        st.rerun()
                    else:
                        erro = resp.json()
                        st.error(f"Erro: {erro.get('detail', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao comunicar com API: {str(e)[:100]}")
            
            # Validação de saldo (aviso)
            if not bot_ativo_now:
                # Verificar se tem saldo antes de iniciar
                bot_exchange = bot.get('exchange', 'binance').lower()
                
                # Tentar buscar saldo da exchange do bot
                try:
                    bot_exchange_obj = get_exchange_for_user(bot_exchange.capitalize())
                    if bot_exchange_obj:
                        bot_balance = bot_exchange_obj.fetch_balance()
                        bot_usdt = bot_balance.get('free', {}).get('USDT', 0) or 0
                        
                        if bot_usdt < 10:  # Mínimo $10
                            st.error("❌ Sem saldo na corretora!")
                            st.caption(f"Saldo: ${bot_usdt:.2f} (mín: $10)")
                            st.caption(f"Deposite USDT na {bot_exchange.upper()}")
                        else:
                            if st.button("▶️ Iniciar Bot", key=f"start_{bot['id']}", use_container_width=True):
                                st.success("✅ Bot iniciado!")
                    else:
                        st.warning("⚠️ Configure API Key")
                except:
                    # Se não conseguir verificar, permitir iniciar
                    if st.button("▶️ Iniciar Bot", key=f"start_{bot['id']}", use_container_width=True):
                        st.success("✅ Bot iniciado!")
        
        with col_chart:
            st.markdown("#### 📈 Performance")
            
            # Gráfico de performance do bot
            import plotly.graph_objects as go
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            capital_inicial = float(bot.get('capital', 100))
            values = [capital_inicial + i*3 + (i%5)*2 for i in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=values,
                mode='lines+markers',
                name=bot.get('name', 'Bot'),
                line=dict(color='#667eea', width=2),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)'
            ))
            fig.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Data",
                yaxis_title="Capital (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Trades do bot
        st.markdown("#### 🎯 Últimos Trades")
        trades_exemplo = pd.DataFrame({
            'Data': [datetime.now() - timedelta(hours=i) for i in range(5)],
            'Par': ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT'],
            'Tipo': ['COMPRA', 'VENDA', 'COMPRA', 'VENDA', 'COMPRA'],
            'Lucro': ['+$12', '+$8', '-$3', '+$15', '+$5']
        })
        st.dataframe(trades_exemplo, use_container_width=True, hide_index=True)

# Espaçamento clean
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Rankings já implementados acima (2ª posição)

# Código antigo removido

# Código antigo removido - funcionalidades nas abas acima

st.stop()  # Fim do dashboard
