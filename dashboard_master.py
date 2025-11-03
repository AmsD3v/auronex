"""
Dashboard MASTER - Controle Total (Multi-Usuário)
- Autenticação por usuário
- API Keys individualizadas
- Isolamento de dados
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
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
st.set_page_config(page_title="RoboTrader Master", page_icon="👑", layout="wide")

# ========================================
# 🔐 AUTENTICAÇÃO - MULTI-USUÁRIO
# ========================================

def check_authentication():
    """Verificar autenticação do usuário"""
    
    # Carregar token da sessão do navegador (cookies) - SEM mostrar na URL!
    # Streamlit não suporta cookies nativos, então usamos session_state persistente
    
    # Verificar se já está autenticado na sessão
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    
    # Pedir token na sidebar
    st.sidebar.title("🔐 Login Necessário")
    st.sidebar.warning("⚠️ Para sua segurança, faça login primeiro!")
    
    # Opção 1: Login com email/senha
    with st.sidebar.expander("📧 Login com Email", expanded=True):
        email = st.text_input("Email:", key="login_email")
        password = st.text_input("Senha:", type="password", key="login_password")
        
        if st.button("🔓 Entrar"):
            try:
                response = requests.post(
                    'http://localhost:8001/api/auth/login/',
                    json={'email': email, 'password': password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    token = data['access_token']
                    st.session_state.access_token = token
                    st.session_state.user_email = email
                    
                    # Buscar informações do usuário
                    try:
                        user_response = requests.get(
                            'http://localhost:8001/api/auth/me/',
                            headers={'Authorization': f'Bearer {token}'}
                        )
                        if user_response.status_code == 200:
                            user_data = user_response.json()
                            st.session_state.user_name = user_data.get('first_name', 'Usuário')
                    except:
                        st.session_state.user_name = email.split('@')[0]
                    
                    st.session_state.authenticated = True
                    
                    st.success("✅ Login bem-sucedido! Aguarde...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos!")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    # Opção 2: Colar token diretamente
    with st.sidebar.expander("🔑 Ou cole seu Token"):
        token_input = st.text_area("Token JWT:", height=100)
        
        if st.button("🔓 Usar Token"):
            if token_input and len(token_input) > 50:
                token = token_input.strip()
                st.session_state.access_token = token
                st.session_state.authenticated = True
                
                st.success("✅ Token salvo! Aguarde...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Token inválido!")
    
    st.sidebar.info("💡 Faça login pelo site: http://localhost:8001/login")
    st.sidebar.info("📖 Depois clique em 'Abrir Dashboard Completo'")
    
    # Tela de login simplificada (NUNCA DEVE APARECER QUANDO LOGADO!)
    st.title("🔒 Dashboard Protegido - Login Necessário")
    st.warning("⚠️ **IMPORTANTE:** Este dashboard está protegido e individualizado por usuário.")
    st.info("👈 Faça login na barra lateral para acessar seus dados.")
    st.caption(f"🐛 Debug: authenticated={st.session_state.get('authenticated', False)}")
    
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
    """Buscar API Keys do usuário logado (com cache)"""
    if 'access_token' not in st.session_state:
        return []
    
    # Cache de API Keys (evita buscar a cada segundo)
    cache_key = 'api_keys_cache'
    cache_time_key = 'api_keys_cache_time'
    
    # Se tem cache válido (< 30s), retornar
    if cache_key in st.session_state and cache_time_key in st.session_state:
        if time.time() - st.session_state[cache_time_key] < 30:
            return st.session_state[cache_key]
    
    try:
        response = requests.get(
            'http://localhost:8001/api/api-keys/',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
        )
        
        if response.status_code == 200:
            keys = response.json()
            # Salvar no cache
            st.session_state[cache_key] = keys
            st.session_state[cache_time_key] = time.time()
            return keys
        else:
            if response.status_code == 401:
                st.sidebar.error("❌ Sessão expirada!")
                st.sidebar.info("💡 Faça login novamente na sidebar")
                st.session_state.authenticated = False
            return []
    except Exception as e:
        st.sidebar.error(f"❌ Erro de conexão: {str(e)[:50]}")
        return []

# VERIFICAR AUTENTICAÇÃO ANTES DE CONTINUAR
if not check_authentication():
    st.stop()

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
    
    # Filtrar por exchange selecionada (case-insensitive)
    exchange_key = None
    for key in user_keys:
        key_exchange = key.get('exchange', '').lower()
        if key_exchange == exchange_name.lower():
            exchange_key = key
            break
    
    if not exchange_key:
        st.sidebar.error(f"❌ Você não tem API Keys para {exchange_name}!")
        available_exchanges = [k.get('exchange', 'N/A') for k in user_keys]
        st.sidebar.info(f"💡 Suas exchanges disponíveis: {', '.join(available_exchanges)}")
        st.sidebar.info(f"💡 Procurando por: '{exchange_name}' (case-insensitive)")
        return None
    
    # Buscar chaves completas (descriptografadas) do servidor
    try:
        response = requests.get(
            f'http://localhost:8001/api/api-keys/{exchange_key["id"]}/',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'}
        )
        
        if response.status_code != 200:
            st.error("❌ Erro ao buscar chaves da API")
            return None
        
        key_data = response.json()
        
        # Criar exchange customizado com as keys do usuário
        import ccxt
        
        exchange_class = getattr(ccxt, exchange_name.lower())
        exchange = exchange_class({
            'apiKey': key_data.get('api_key_decrypted', ''),  # Backend precisa retornar descriptografado
            'secret': key_data.get('secret_key_decrypted', ''),
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,
                'recvWindow': 60000
            }
        })
        
        if key_data.get('is_testnet', False):
            exchange.set_sandbox_mode(True)
        
        # Sincronizar timestamp
        try:
            exchange.load_time_difference()
        except:
            pass
        
        return exchange
        
    except Exception as e:
        st.error(f"❌ Erro ao conectar exchange: {str(e)}")
        return None

# Manter compatibilidade com código antigo (SEM CACHE para multi-usuário!)
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

# Header com seletor de moeda
col_titulo, col_moeda = st.columns([4, 1])

with col_titulo:
    st.title("👑 RoboTrader Master")

with col_moeda:
    moeda_default = config_salva.get('moeda', "💵 USD")
    moedas = ["💵 USD", "💰 BRL", "€ EUR", "£ GBP"]
    index_moeda = moedas.index(moeda_default) if moeda_default in moedas else 0
    
    moeda = st.selectbox(
        "💱 Moeda",
        moedas,
        index=index_moeda,
        label_visibility="collapsed"
    )

# Taxas de conversão (aproximadas)
TAXAS = {
    "💵 USD": 1.0,
    "💰 BRL": 5.0,
    "€ EUR": 0.92,
    "£ GBP": 0.79
}

taxa_conversao = TAXAS[moeda]
simbolo_moeda = moeda.split()[1]

# ========================================
# SIDEBAR - CONTROLES
# ========================================
st.sidebar.header("🎛️ Controles")

# Perfil PRIMEIRO (define velocidades sugeridas)
# Usar valor carregado se existir
if 'perfil_carregado' in st.session_state:
    try:
        index_perfil = list(PERFIS.keys()).index(st.session_state.perfil_carregado)
        del st.session_state.perfil_carregado  # Limpar após usar
    except:
        index_perfil = 1
else:
    index_perfil = 1

perfil = st.sidebar.selectbox("🎯 Perfil", list(PERFIS.keys()), index=index_perfil)
config = PERFIS[perfil]

# Velocidades sugeridas por perfil
VELOCIDADES_PERFIL = {
    "🏦 Hedge Fund": {"dashboard": 30, "bot": 60},
    "📈 Day Trader": {"dashboard": 5, "bot": 3},
    "⚡ Scalper": {"dashboard": 3, "bot": 1},
    "🚀 Ultra": {"dashboard": 1, "bot": 1}
}

velocidades_sugeridas = VELOCIDADES_PERFIL[perfil]

st.sidebar.markdown("---")

# FREQUÊNCIA DE ATUALIZAÇÃO DO DASHBOARD
st.sidebar.markdown("### ⚡ Atualização Dashboard")

# Usar valor carregado se existir
if 'freq_dashboard_carregado' in st.session_state:
    value_dash = st.session_state.freq_dashboard_carregado
    del st.session_state.freq_dashboard_carregado
else:
    value_dash = velocidades_sugeridas['dashboard']

freq_dashboard = st.sidebar.slider(
    "Frequência (segundos)",
    min_value=1,
    max_value=60,
    value=value_dash,
    step=1,
    help=f"Perfil {perfil} sugere: {velocidades_sugeridas['dashboard']}s",
    key="slider_dash"
)

if freq_dashboard <= 3:
    st.sidebar.warning("⚡ Muito rápido - pode ficar pesado!")
elif freq_dashboard <= 10:
    st.sidebar.success("✅ Rápido - recomendado!")
else:
    st.sidebar.info("⏱️ Normal")

st.sidebar.caption(f"Dashboard atualiza: {freq_dashboard}s")

st.sidebar.markdown("---")

# VELOCIDADE DO BOT
st.sidebar.markdown("### 🤖 Velocidade do Bot")

# Usar valor carregado se existir
if 'freq_bot_carregado' in st.session_state:
    value_bot = st.session_state.freq_bot_carregado
    del st.session_state.freq_bot_carregado
else:
    value_bot = velocidades_sugeridas['bot']

freq_bot = st.sidebar.slider(
    "Análise (segundos)",
    min_value=1,
    max_value=60,
    value=value_bot,
    step=1,
    help=f"Perfil {perfil} sugere: {velocidades_sugeridas['bot']}s (você pode ajustar!)",
    key="slider_bot"
)

if freq_bot <= 3:
    st.sidebar.success("⚡ Ultra rápido - máximas oportunidades!")
elif freq_bot <= 10:
    st.sidebar.info("✅ Rápido - bom equilíbrio")
else:
    st.sidebar.warning("⏱️ Lento - poucas oportunidades")

st.sidebar.caption(f"Bot analisa: {freq_bot}s")

# Salvar config para o bot ler
import json
config_bot = {'freq_bot': freq_bot, 'freq_dashboard': freq_dashboard}
with open('bot_config.json', 'w') as f:
    json.dump(config_bot, f)

st.sidebar.caption("✅ Config salva - bot lerá automaticamente")

st.sidebar.markdown("---")

# SELETOR DE CORRETORA (ANTES DE USAR!)
st.sidebar.markdown("### 🏦 Corretora")

CORRETORAS = {
    "Binance": {"testnet": "https://testnet.binance.vision/", "prod": "https://api.binance.com/"},
    "Bybit": {"testnet": "https://testnet.bybit.com/", "prod": "https://api.bybit.com/"},
}

# Aplicar limite de plano FREE (apenas Binance)
if plan_limits:
    allowed_exchanges = plan_limits['limits'].get('allowed_exchanges', ['binance'])
    available_corretoras = [c for c in CORRETORAS.keys() if c.lower() in allowed_exchanges]
    
    if len(available_corretoras) == 1:
        st.sidebar.info(f"📌 Plano {plan_limits['plan'].upper()}: Apenas {available_corretoras[0]}")
        corretora_sel = available_corretoras[0]
    else:
        corretora_sel = st.sidebar.selectbox(
            "Selecione",
            available_corretoras,
            help="Corretoras disponíveis no seu plano"
        )
else:
    corretora_sel = st.sidebar.selectbox(
        "Selecione",
        list(CORRETORAS.keys()),
        help="Binance e Bybit totalmente funcionais!"
    )

if corretora_sel == "Binance":
    st.sidebar.success("✅ Binance - 425 criptos")
elif corretora_sel == "Bybit":
    st.sidebar.success("✅ Bybit - 300+ criptos")

st.sidebar.markdown("---")

# ========================================
# 🤖 MODO PILOTO AUTOMÁTICO (NOVA FUNCIONALIDADE!)
# ========================================
st.sidebar.markdown("### 🤖 Modo de Operação")

modo_piloto = st.sidebar.checkbox(
    "🚀 **PILOTO AUTOMÁTICO**",
    value=False,
    help="Bot escolhe automaticamente as melhores criptos baseado em análise de mercado!"
)

if modo_piloto:
    st.sidebar.success("✅ MODO: Caçador de Oportunidades")
    st.sidebar.info("🎯 Bot analisará o mercado e escolherá as melhores criptos automaticamente!")
    st.sidebar.caption("⚠️ Seleção de criptos desabilitada (automática)")
else:
    st.sidebar.info("✋ MODO: Manual (você escolhe)")
    st.sidebar.caption("💡 Ative o Piloto Automático para o bot escolher por você")

st.sidebar.markdown("---")

# Opção de buscar saldo real
modo_capital = st.sidebar.radio(
    "💰 Capital",
    ["📊 Buscar Saldo Real", "✏️ Informar Manualmente"],
    help="Saldo Real: busca da corretora | Manual: você informa"
)

capital_total_input = 0

if modo_capital == "📊 Buscar Saldo Real":
    # Tentar buscar saldo real da corretora
    try:
        exchange_temp = get_exchange(corretora_sel)
        
        if exchange_temp is None:
            st.sidebar.error(f"❌ Você não tem API Keys para {corretora_sel}!")
            st.sidebar.info("💡 Adicione em: http://localhost:8001/api-keys/")
            capital_total_input = 0
            capital_total = 0
        else:
            # Usar método correto do ccxt (fetch_balance ao invés de get_balance)
            balance = exchange_temp.fetch_balance()
            
            # Buscar saldo total em USDT (incluindo todas as moedas)
            total_usdt = balance.get('total', {}).get('USDT', 0) or 0
            
            # Se não tem USDT total, buscar outras moedas principais e converter
            if total_usdt == 0:
                # Tentar BRL
                brl_balance = balance.get('total', {}).get('BRL', 0) or 0
                if brl_balance > 0:
                    # Converter BRL para USDT (aproximado: 1 USDT = 5 BRL)
                    total_usdt = brl_balance / 5.0
                
                # Tentar outras stablecoins
                if total_usdt == 0:
                    busd_balance = balance.get('total', {}).get('BUSD', 0) or 0
                    usdc_balance = balance.get('total', {}).get('USDC', 0) or 0
                    total_usdt = busd_balance + usdc_balance
            
            # Se ainda zero, buscar QUALQUER saldo e mostrar
            if total_usdt == 0:
                all_balances = []
                for currency, amounts in balance.get('total', {}).items():
                    if amounts and amounts > 0.0001:  # Ignorar valores muito pequenos
                        all_balances.append(f"{currency}: {amounts:.4f}")
                
                if all_balances:
                    st.sidebar.info(f"💰 Saldos encontrados:\n" + "\n".join(all_balances[:5]))
                    st.sidebar.warning("⚠️ Deposite USDT, BRL ou stablecoins para operar")
                    capital_total_input = 0
                else:
                    capital_total_input = 0
                    st.sidebar.warning(f"⚠️ Saldo: {simbolo_moeda} 0.00 (conta vazia)")
            else:
                capital_total_input = total_usdt * taxa_conversao
                st.sidebar.success(f"✅ Saldo Total: {simbolo_moeda} {capital_total_input:.2f} (≈ ${total_usdt:.2f} USDT)")
            
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao buscar saldo: {str(e)[:50]}")
        st.sidebar.info("💡 Verifique suas API Keys em http://localhost:8001/api-keys/")
        capital_total_input = 0
else:
    # Modo manual (antigo)
    capital_total_input = st.sidebar.number_input(
        f"Capital ({simbolo_moeda})", 
        0.0, 100000.0, 
        float(config_salva.get('capital_total', 100.0)), 
        10.0
    )

# Converter capital para USD para cálculos internos
capital_total = capital_total_input / taxa_conversao if capital_total_input > 0 else 0

# ========================================
# 🤖 SELEÇÃO DE CRIPTOS: MANUAL OU AUTOMÁTICO
# ========================================

if modo_piloto:
    # MODO PILOTO AUTOMÁTICO - BOT ESCOLHE
    st.sidebar.markdown("### 🎯 Criptos (Automático)")
    st.sidebar.info("🤖 Bot escolhendo as melhores...")
    
    # Função para escolher as melhores criptos automaticamente
    def escolher_melhores_criptos(exchange_name, num_criptos=10):
        """Bot escolhe automaticamente as melhores criptos"""
        cache_key = f'autopilot_symbols_{exchange_name}'
        cache_time_key = f'{cache_key}_time'
        
        # Cache de 5 minutos (mais longo que rankings)
        if cache_key in st.session_state and cache_time_key in st.session_state:
            if time.time() - st.session_state[cache_time_key] < 300:
                return st.session_state[cache_key]
        
        try:
            # Buscar top performers da exchange
            exchange_temp = get_exchange(exchange_name)
            if exchange_temp is None:
                return ['BTCUSDT', 'ETHUSDT']  # Fallback
            
            all_symbols = get_all_symbols_dynamic(exchange_name)
            
            # Analisar e pontuar cada cripto
            scores = []
            for symbol in all_symbols[:50]:  # Analisa as primeiras 50
                try:
                    ticker = exchange_temp.fetch_ticker(symbol)
                    var_24h = ticker.get('percentage', 0) or 0
                    volume = ticker.get('quoteVolume', 0) or 0
                    
                    # Score = volatilidade + volume
                    # Quanto maior o volume e volatilidade positiva, melhor
                    score = abs(var_24h) * 0.7 + (volume / 10_000_000) * 0.3
                    
                    if volume > 100000:  # Filtro mínimo
                        scores.append({
                            'symbol': symbol,
                            'score': score,
                            'var': var_24h,
                            'volume': volume
                        })
                except:
                    continue
            
            # Ordenar por score e pegar top N
            scores_sorted = sorted(scores, key=lambda x: x['score'], reverse=True)
            top_symbols = [s['symbol'] for s in scores_sorted[:num_criptos]]
            
            # Se não encontrou suficientes, adicionar BTC e ETH
            if len(top_symbols) < 2:
                top_symbols = ['BTCUSDT', 'ETHUSDT']
            
            # Salvar no cache
            st.session_state[cache_key] = top_symbols
            st.session_state[cache_time_key] = time.time()
            
            return top_symbols
        except:
            return ['BTCUSDT', 'ETHUSDT']  # Fallback seguro
    
    # Aplicar limite de plano
    max_symbols = 999
    if plan_limits:
        max_symbols = plan_limits['limits'].get('max_symbols_per_bot', 1)
    
    num_autopilot = min(10, max_symbols)  # Máximo 10 ou limite do plano
    
    symbols_sel = escolher_melhores_criptos(corretora_sel, num_autopilot)
    
    st.sidebar.success(f"✅ {len(symbols_sel)} criptos selecionadas automaticamente:")
    for idx, sym in enumerate(symbols_sel[:5], 1):  # Mostrar apenas primeiras 5
        st.sidebar.caption(f"{idx}. {sym.replace('USDT', '')}")
    
    if len(symbols_sel) > 5:
        st.sidebar.caption(f"... e mais {len(symbols_sel)-5}")
    
    st.sidebar.caption("🔄 Atualiza a cada 5 minutos")

else:
    # MODO MANUAL - USUÁRIO ESCOLHE
    st.sidebar.markdown("### 📊 Criptos (Manual)")
    
    todos_symbols = get_all_symbols_dynamic(corretora_sel)
    principais_default = config_salva.get('symbols', ['BTCUSDT'])

    # Aplicar limite de plano
    max_symbols = 999  # Padrão ilimitado
    if plan_limits:
        max_symbols = plan_limits['limits'].get('max_symbols_per_bot', 1)
        if max_symbols == 1:
            st.sidebar.warning(f"📌 Plano {plan_limits['plan'].upper()}: Máximo {max_symbols} cripto")

    symbols_sel = st.sidebar.multiselect(
        f"Selecione (Máx: {max_symbols if max_symbols < 999 else '∞'})", 
        todos_symbols, 
        default=principais_default[:max_symbols],
        help="Digite para pesquisar. Use Piloto Automático para seleção automática!"
    )

    # Validar se ultrapassou limite
    if len(symbols_sel) > max_symbols:
        st.sidebar.error(f"❌ Limite: {max_symbols} cripto(s)!")
        st.sidebar.info("💡 Faça upgrade do plano para adicionar mais")
        symbols_sel = symbols_sel[:max_symbols]  # Forçar limite

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Alocação")

modo_alocacao = st.sidebar.radio("Modo", ["⚖️ Automático", "🎯 Manual"])

alocacao = {}

if modo_alocacao == "🎯 Manual":
    total_percent = 0
    for symbol in symbols_sel:
        crypto = symbol.replace('USDT', '')
        default_pct = 100 // len(symbols_sel) if len(symbols_sel) > 0 else 0
        pct = st.sidebar.slider(f"{crypto}", 0.0, 100.0, float(default_pct), step=0.5)
        alocacao[symbol] = pct
        total_percent += pct
    
    if total_percent == 100:
        st.sidebar.success(f"✅ {total_percent}%")
    elif total_percent < 100:
        st.sidebar.warning(f"⚠️ {total_percent}%")
    else:
        st.sidebar.error(f"❌ {total_percent}%")
else:
    pct_por_cripto = 100 // len(symbols_sel) if len(symbols_sel) > 0 else 0
    for symbol in symbols_sel:
        alocacao[symbol] = pct_por_cripto

strategy_name = st.sidebar.selectbox("🎯 Estratégia", ["mean_reversion", "trend_following"])

st.sidebar.markdown("---")

# ========================================
# ✅ SISTEMA DE PERFIS SIMPLIFICADO (1 CAMPO APENAS!)
# ========================================
st.sidebar.markdown("### 💾 Perfis")

# Listar perfis existentes
import os
import glob
if not os.path.exists('perfis'):
    os.makedirs('perfis')

perfis_salvos = [os.path.basename(f).replace('.json', '') for f in glob.glob('perfis/*.json')]

# DROPDOWN com opção de criar novo
opcoes_perfil = ["➕ Criar Novo Perfil"] + perfis_salvos

perfil_selecionado = st.sidebar.selectbox(
    "Selecione ou crie:",
    opcoes_perfil,
    help="Escolha um perfil salvo ou crie um novo"
)

# MODO: Criar novo perfil
if perfil_selecionado == "➕ Criar Novo Perfil":
    nome_perfil_novo = st.sidebar.text_input(
        "Nome do novo perfil:",
        "Meu_Perfil",
        help="Digite um nome para salvar suas configurações atuais"
    )
    
    if st.sidebar.button("💾 Salvar Novo Perfil", use_container_width=True):
        if nome_perfil_novo and nome_perfil_novo.strip():
            config_completa = {
                'perfil': perfil,
                'freq_dashboard': freq_dashboard,
                'freq_bot': freq_bot,
                'capital_total': capital_total_input,
                'moeda': moeda,
                'symbols': symbols_sel,
                'modo_alocacao': modo_alocacao,
                'alocacao': alocacao,
                'strategy': strategy_name,
                'corretora': corretora_sel
            }
            
            with open(f'perfis/{nome_perfil_novo}.json', 'w') as f:
                json.dump(config_completa, f, indent=2)
            
            # TAMBÉM salvar como config padrão do usuário
            if 'user_email' in st.session_state:
                user_cfg = f"dashboard_config_{st.session_state.user_email.replace('@', '_').replace('.', '_')}.json"
                with open(user_cfg, 'w') as f:
                    json.dump(config_completa, f, indent=2)
            
            st.sidebar.success(f"✅ '{nome_perfil_novo}' salvo!")
            st.sidebar.info("↻ Recarregando...")
            time.sleep(1)
            st.rerun()
        else:
            st.sidebar.error("❌ Digite um nome válido!")

# MODO: Carregar perfil existente
else:
    st.sidebar.info(f"📂 Perfil: **{perfil_selecionado}**")
    
    col_load, col_del = st.sidebar.columns(2)
    
    with col_load:
        if st.button("📥 Carregar", use_container_width=True):
            try:
                with open(f'perfis/{perfil_selecionado}.json', 'r') as f:
                    config_carregada = json.load(f)
                
                # ✅ APLICAR configurações carregadas
                st.session_state.perfil_carregado = config_carregada.get('perfil', '📈 Day Trader')
                st.session_state.freq_dashboard_carregado = config_carregada.get('freq_dashboard', 5)
                st.session_state.freq_bot_carregado = config_carregada.get('freq_bot', 3)
                st.session_state.capital_input = config_carregada.get('capital_total', 100.0)
                st.session_state.moeda_sel = config_carregada.get('moeda', '💰 BRL')
                st.session_state.symbols_sel = config_carregada.get('symbols', ['BTCUSDT'])
                st.session_state.corretora_sel = config_carregada.get('corretora', 'Binance')
                
                st.sidebar.success(f"✅ Carregado!")
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ Erro: {str(e)[:30]}")
    
    with col_del:
        if st.button("🗑️ Excluir", use_container_width=True):
            try:
                os.remove(f'perfis/{perfil_selecionado}.json')
                st.sidebar.success("✅ Excluído!")
                time.sleep(0.5)
                st.rerun()
            except:
                st.sidebar.error("❌ Erro ao excluir")

# ========================================
# CONTEÚDO PRINCIPAL - COM PLACEHOLDER
# ========================================

# Criar container que não pisca
placeholder = st.empty()

with placeholder.container():
    
    # ========================================
    # CONTROLE START/STOP DO BOT
    # ========================================
    
    # Ler estado atual do bot
    try:
        with open('bot_status.json', 'r') as f:
            bot_status = json.load(f)
            bot_running = bot_status.get('running', False)
    except:
        bot_running = False
    
    # Status bar no topo
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"### ⏰ {datetime.now().strftime('%H:%M:%S')}")
    with col2:
        if bot_running:
            st.success("🟢 **BOT ATIVO**")
        else:
            st.error("🔴 **BOT PARADO**")
    with col3:
        st.metric("🔄 Refresh", f"{freq_dashboard}s")
    with col4:
        # Botão START/STOP
        if bot_running:
            if st.button("⏸️ PARAR BOT", type="primary", use_container_width=True):
                with open('bot_status.json', 'w') as f:
                    json.dump({'running': False}, f)
                st.success("Bot pausado!")
                time.sleep(1)
                st.rerun()
        else:
            # Validações antes de permitir start
            pode_iniciar = True
            avisos = []
            
            if capital_total <= 0:
                pode_iniciar = False
                avisos.append("⚠️ Capital não definido")
            
            if len(symbols_sel) == 0:
                pode_iniciar = False
                avisos.append("⚠️ Nenhuma cripto selecionada")
            
            if modo_alocacao == "🎯 Manual":
                total_alloc = sum(alocacao.values())
                if abs(total_alloc - 100) > 0.1:
                    pode_iniciar = False
                    avisos.append(f"⚠️ Alocação = {total_alloc}% (precisa ser 100%)")
            
            if pode_iniciar:
                if st.button("🚀 INICIAR BOT", type="primary", use_container_width=True):
                    with open('bot_status.json', 'w') as f:
                        json.dump({'running': True}, f)
                    st.success("🚀 Bot iniciado!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.button("⚠️ CONFIGURE ANTES", disabled=True, use_container_width=True)
                for aviso in avisos:
                    st.caption(aviso)
    
    st.markdown("---")
    
    # ========================================
    # 📺 OPERAÇÕES RECENTES - CONECTADO AO DJANGO API
    # ========================================
    st.markdown("## 📺 Operações Recentes")
    
    try:
        # Buscar trades do usuário logado via Django API
        response = requests.get(
            'http://localhost:8001/api/trades/',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
            params={'limit': 5, 'ordering': '-exit_time'},
            timeout=5
        )
        
        if response.status_code == 200:
            trades = response.json()
            
            if trades and len(trades) > 0:
                # Mostrar últimas 5 operações
                cols = st.columns(min(len(trades), 5))
                
                for idx, trade in enumerate(trades[:5]):
                    with cols[idx]:
                        # Extrair dados do trade
                        symbol = trade.get('symbol', 'N/A').replace('USDT', '').replace('/USDT', '')
                        status = trade.get('status', 'open')
                        entry_price = float(trade.get('entry_price', 0))
                        exit_price = float(trade.get('exit_price', 0)) if trade.get('exit_price') else entry_price
                        pnl = float(trade.get('pnl', 0)) if trade.get('pnl') else 0
                        
                        # Timestamp
                        exit_time = trade.get('exit_time')
                        entry_time = trade.get('entry_time')
                        
                        if exit_time:
                            # Parse ISO format
                            try:
                                dt = datetime.fromisoformat(exit_time.replace('Z', '+00:00'))
                                tempo = dt.strftime('%H:%M')
                            except:
                                tempo = exit_time[:5] if exit_time else "N/A"
                        elif entry_time:
                            try:
                                dt = datetime.fromisoformat(entry_time.replace('Z', '+00:00'))
                                tempo = dt.strftime('%H:%M')
                            except:
                                tempo = entry_time[:5] if entry_time else "N/A"
                        else:
                            tempo = "N/A"
                        
                        # Status e cor
                        if status == 'closed':
                            if pnl > 0:
                                st.success(f"**🟢 LUCRO**\n\n{symbol}\n{tempo}\n{simbolo_moeda} {pnl*taxa_conversao:+,.2f}")
                            else:
                                st.error(f"**🔴 PERDA**\n\n{symbol}\n{tempo}\n{simbolo_moeda} {pnl*taxa_conversao:+,.2f}")
                        else:
                            st.info(f"**🔵 ABERTO**\n\n{symbol}\n{tempo}\n{simbolo_moeda} {entry_price*taxa_conversao:,.2f}")
            else:
                st.info("⏳ Nenhuma operação realizada ainda. Bot procurando oportunidades...")
        else:
            st.warning("⚠️ Não foi possível carregar operações recentes")
    except requests.exceptions.ConnectionError:
        st.error("❌ Django não está rodando! Inicie com INICIAR_SISTEMA_FINAL.bat")
    except requests.exceptions.Timeout:
        st.warning("⏳ Timeout ao buscar operações. Django pode estar sobrecarregado.")
    except Exception as e:
        st.info(f"⏳ Aguardando primeira operação... ({str(e)[:50]})")
    
    st.markdown("---")
    
    # ========================================
    # 🏆 TOP 5 - PERFORMANCE (COM CACHE PARA EVITAR RATE LIMIT)
    # ========================================
    st.markdown("## 🏆 TOP 5 - Performance")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 Hoje", "📅 Semana", "📆 Mês", "🚀 Virais", "🏦 Corretora"])
    
    def buscar_top_coingecko_cached(periodo='24h'):
        """Buscar top performers do CoinGecko COM CACHE (60s)"""
        # Cache key
        cache_key = f'coingecko_top_{periodo}'
        cache_time_key = f'{cache_key}_time'
        
        # Verificar cache (válido por 60s)
        if cache_key in st.session_state and cache_time_key in st.session_state:
            if time.time() - st.session_state[cache_time_key] < 60:
                return st.session_state[cache_key]
        
        try:
            # CoinGecko API v3 (gratuita, sem API key)
            url = 'https://api.coingecko.com/api/v3/coins/markets'
            params = {
                'vs_currency': 'usd',
                'order': f'price_change_percentage_{periodo}_desc',
                'per_page': 100,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': periodo
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Filtrar apenas criptos com volume significativo (>$10M)
                filtered = [
                    coin for coin in data 
                    if coin.get('total_volume', 0) > 10_000_000
                ]
                
                # Top 5
                top5 = []
                for coin in filtered[:5]:
                    symbol = coin.get('symbol', '').upper()
                    nome = coin.get('name', symbol)
                    preco = coin.get('current_price', 0)
                    
                    # Variação no período correto
                    if periodo == '24h':
                        var = coin.get('price_change_percentage_24h', 0)
                    elif periodo == '7d':
                        var = coin.get('price_change_percentage_7d_in_currency', 0)
                    elif periodo == '30d':
                        var = coin.get('price_change_percentage_30d_in_currency', 0)
                    else:
                        var = 0
                    
                    top5.append({
                        'Cripto': f"{symbol} ({nome[:15]})",
                        'Var': f"{var:+.2f}%",
                        'var_num': var,
                        'Preço': f"{simbolo_moeda} {preco*taxa_conversao:,.2f}"
                    })
                
                # Salvar no cache
                st.session_state[cache_key] = top5
                st.session_state[cache_time_key] = time.time()
                
                return top5
            else:
                # Retornar cache antigo se houver
                return st.session_state.get(cache_key, None)
        except:
            # Retornar cache antigo se houver
            return st.session_state.get(cache_key, None)
    
    def buscar_virais_coingecko():
        """Buscar criptos virais/recentes com alta volatilidade"""
        cache_key = 'coingecko_virais'
        cache_time_key = f'{cache_key}_time'
        
        if cache_key in st.session_state and cache_time_key in st.session_state:
            if time.time() - st.session_state[cache_time_key] < 60:
                return st.session_state[cache_key]
        
        try:
            # Buscar trending coins (criptos em alta)
            url = 'https://api.coingecko.com/api/v3/search/trending'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                coins = data.get('coins', [])
                
                virais = []
                for item in coins[:5]:
                    coin = item.get('item', {})
                    symbol = coin.get('symbol', '').upper()
                    nome = coin.get('name', symbol)
                    rank = coin.get('market_cap_rank', 'N/A')
                    price_btc = coin.get('price_btc', 0)
                    
                    # Buscar preço atual em USD
                    coin_id = coin.get('id', '')
                    preco_usd = 0
                    var_24h = 0
                    
                    try:
                        # Segunda chamada para pegar preço em USD
                        price_url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true'
                        price_resp = requests.get(price_url, timeout=5)
                        if price_resp.status_code == 200:
                            price_data = price_resp.json()
                            if coin_id in price_data:
                                preco_usd = price_data[coin_id].get('usd', 0)
                                var_24h = price_data[coin_id].get('usd_24h_change', 0)
                    except:
                        pass
                    
                    virais.append({
                        'Cripto': f"{symbol} ({nome[:15]})",
                        'Preço': f"{simbolo_moeda} {preco_usd*taxa_conversao:,.4f}" if preco_usd > 0 else "N/A",
                        'Var 24h': f"{var_24h:+.1f}%" if var_24h != 0 else "N/A",
                        'Rank': f"#{rank}" if rank != 'N/A' else 'Novo',
                        'Score': f"{coin.get('score', 0)}"
                    })
                
                st.session_state[cache_key] = virais
                st.session_state[cache_time_key] = time.time()
                
                return virais
            else:
                return st.session_state.get(cache_key, None)
        except:
            return st.session_state.get(cache_key, None)
    
    def buscar_top_exchange(exchange_name):
        """Buscar Top 5 da CORRETORA selecionada (dados confiáveis)"""
        cache_key = f'exchange_top_{exchange_name}'
        cache_time_key = f'{cache_key}_time'
        
        if cache_key in st.session_state and cache_time_key in st.session_state:
            if time.time() - st.session_state[cache_time_key] < 30:
                return st.session_state[cache_key]
        
        try:
            exchange_temp = get_exchange(exchange_name)
            
            if exchange_temp is None:
                return None
            
            # Buscar símbolos disponíveis
            all_symbols = get_all_symbols_dynamic(exchange_name)
            
            # Analisar variação 24h de cada símbolo
            ranking = []
            for symbol in all_symbols[:50]:  # Primeiros 50 para não demorar
                try:
                    ticker = exchange_temp.fetch_ticker(symbol)
                    var_24h = ticker.get('percentage', 0) or 0
                    preco = ticker.get('last', 0) or 0
                    volume = ticker.get('quoteVolume', 0) or 0
                    
                    if volume > 100000:  # Filtrar por volume mínimo
                        ranking.append({
                            'Cripto': symbol.replace('USDT', '').replace('/USDT', ''),
                            'Var': f"{var_24h:+.2f}%",
                            'var_num': var_24h,
                            'Preço': f"{simbolo_moeda} {preco*taxa_conversao:,.2f}",
                            'Volume': f"${volume:,.0f}"
                        })
                except:
                    continue
            
            # Ordenar por variação
            ranking_sorted = sorted(ranking, key=lambda x: x['var_num'], reverse=True)[:5]
            
            # Remover campo temporário
            for item in ranking_sorted:
                item.pop('var_num', None)
            
            st.session_state[cache_key] = ranking_sorted
            st.session_state[cache_time_key] = time.time()
            
            return ranking_sorted
        except:
            return st.session_state.get(cache_key, None)
    
    with tab1:
        st.markdown("**Últimas 24h** (Mercado Global - CoinGecko)")
        
        ranking = buscar_top_coingecko_cached('24h')
        
        if ranking:
            df_rank = pd.DataFrame(ranking)
            df_rank = df_rank.drop('var_num', axis=1)
            df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_rank, use_container_width=True)
            st.success(f"💡 Foco: {ranking[0]['Cripto'].split('(')[0].strip()}")
            st.caption("📊 Cache: 60s | Fonte: CoinGecko")
        else:
            st.warning("⚠️ Carregando dados... Aguarde alguns segundos.")
    
    with tab2:
        st.markdown("**7 dias** (Mercado Global - CoinGecko)")
        
        ranking_semanal = buscar_top_coingecko_cached('7d')
        
        if ranking_semanal:
            df_rank = pd.DataFrame(ranking_semanal)
            df_rank = df_rank.drop('var_num', axis=1)
            df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_rank, use_container_width=True)
            st.success(f"💡 Foco: {ranking_semanal[0]['Cripto'].split('(')[0].strip()}")
            st.caption("📊 Cache: 60s | Fonte: CoinGecko")
        else:
            st.warning("⚠️ Carregando dados... Aguarde alguns segundos.")
    
    with tab3:
        st.markdown("**30 dias** (Mercado Global - CoinGecko)")
        
        ranking_mensal = buscar_top_coingecko_cached('30d')
        
        if ranking_mensal:
            df_rank = pd.DataFrame(ranking_mensal)
            df_rank = df_rank.drop('var_num', axis=1)
            df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_rank, use_container_width=True)
            st.success(f"💡 Foco: {ranking_mensal[0]['Cripto'].split('(')[0].strip()}")
            st.caption("📊 Cache: 60s | Fonte: CoinGecko")
        else:
            st.warning("⚠️ Carregando dados... Aguarde alguns segundos.")
    
    with tab4:
        st.markdown("**🚀 Criptos Virais** (Trending - CoinGecko)")
        st.caption("Criptos em alta com bastante volatilidade e buzz nas redes sociais")
        
        virais = buscar_virais_coingecko()
        
        if virais:
            df_virais = pd.DataFrame(virais)
            df_virais.index = ['🚀', '💎', '⭐', '🔥', '✨']
            st.dataframe(df_virais, use_container_width=True)
            st.warning("⚠️ **ALTO RISCO!** Criptos virais têm volatilidade extrema")
            st.caption("📊 Cache: 60s | Fonte: CoinGecko Trending")
        else:
            st.warning("⚠️ Carregando dados virais... Aguarde alguns segundos.")
    
    with tab5:
        st.markdown(f"**🏦 Top 5 - {corretora_sel}** (Dados diretos da exchange)")
        st.caption(f"Rankings REAIS da {corretora_sel} - Dados 100% confiáveis!")
        
        ranking_exchange = buscar_top_exchange(corretora_sel)
        
        if ranking_exchange:
            df_exch = pd.DataFrame(ranking_exchange)
            df_exch.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_exch, use_container_width=True)
            st.success(f"✅ Dados REAIS da {corretora_sel}")
            st.caption(f"📊 Cache: 30s | Fonte: {corretora_sel} API")
        else:
            st.warning(f"⚠️ Não foi possível buscar dados da {corretora_sel}")
            st.info("💡 Verifique suas API Keys em http://localhost:8001/api-keys/")
    
    st.markdown("---")
    
    # PORTFOLIO
    st.markdown("## 💼 Portfolio")
    
    portfolio_data = []
    total_atual = 0
    
    # Verificar conexão
    if exchange_temp is None:
        st.warning("⚠️ Conecte suas API Keys para ver o portfólio!")
        st.stop()
    
    for symbol in symbols_sel[:10]:  # Limitar a 10 para não ficar lento
        try:
            ohlcv = exchange_temp.fetch_ohlcv(symbol, config['tf'], limit=50)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            ticker = exchange_temp.fetch_ticker(symbol)
            
            if df.empty or not ticker:
                continue
            
            # Validar se ticker tem dados válidos
            preco_atual = ticker.get('last', 0) or 0
            volume = ticker.get('baseVolume', 0) or 0
            
            # Skip de pares inválidos (como AAVEDOWN que pode ter volume 0)
            if preco_atual <= 0 or volume == 0:
                continue
            
            signal = (MeanReversionStrategy() if strategy_name == "mean_reversion" else TrendFollowingStrategy()).analyze(df)
            
            capital_alocado = capital_total * (alocacao.get(symbol, 0) / 100)
            preco_inicial = df['close'].iloc[0] if not df.empty else 0
            
            # Validar preço inicial
            if preco_inicial is None or preco_inicial <= 0:
                continue
            
            valor_atual = (capital_alocado / preco_inicial) * preco_atual if preco_inicial > 0 else 0
            pnl = valor_atual - capital_alocado
            
            total_atual += valor_atual
            
            portfolio_data.append({
                'Cripto': symbol.replace('USDT', ''),
                'Capital': f"{simbolo_moeda} {capital_alocado*taxa_conversao:.0f}",
                'capital_num': capital_alocado*taxa_conversao,  # Para gráfico de pizza
                'Valor': f"{simbolo_moeda} {valor_atual*taxa_conversao:.0f}",
                'P&L': f"{simbolo_moeda} {pnl*taxa_conversao:+.0f}",
                'Sinal': signal['signal'].upper()[:4]
            })
        except Exception as e:
            # Ignorar criptos problemáticas silenciosamente
            pass
    
    # Mostrar métricas sempre
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Capital", f"{simbolo_moeda} {capital_total_input:.2f}")
    with col2:
        st.metric("💎 Valor Atual", f"{simbolo_moeda} {total_atual*taxa_conversao:.2f}")
    with col3:
        pnl_total = total_atual - capital_total
        pnl_percent = (pnl_total/capital_total*100) if capital_total > 0 else 0
        st.metric("📊 P&L", f"{simbolo_moeda} {pnl_total*taxa_conversao:+.2f}", f"{pnl_percent:+.1f}%")
    
    # Mostrar tabela do portfólio E gráfico de pizza
    if portfolio_data:
        col_table, col_chart = st.columns([2, 1])
        
        with col_table:
            # Remover campo 'capital_num' antes de mostrar
            df_port = pd.DataFrame(portfolio_data)
            if 'capital_num' in df_port.columns:
                df_port_display = df_port.drop('capital_num', axis=1)
            else:
                df_port_display = df_port
            st.dataframe(df_port_display, width='stretch', hide_index=True)
        
        with col_chart:
            # Gráfico de Pizza - Distribuição do Capital
            st.markdown("**📊 Distribuição**")
            
            # Usar valores numéricos salvos
            crypto_names = [d['Cripto'] for d in portfolio_data]
            capital_values = [d.get('capital_num', 0) for d in portfolio_data]
            
            # Criar gráfico de pizza
            fig_pie = go.Figure(data=[go.Pie(
                labels=crypto_names,
                values=capital_values,
                hole=0.4,  # Donut chart
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=150,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        # Mostrar mensagem se não houver dados
        if capital_total == 0:
            st.info("💡 **Capital zerado!** Selecione 'Buscar Saldo Real' ou informe um capital manualmente para começar.")
        elif not symbols_sel:
            st.info("💡 **Selecione criptomoedas** na barra lateral para montar seu portfólio.")
        else:
            st.info("💡 **Carregando dados...** Algumas criptomoedas podem demorar mais. Aguarde ou tente outras.")
    
    st.markdown("---")
    
    # ========================================
    # ANÁLISE INDIVIDUAL COM GRÁFICO
    # ========================================
    st.markdown("## 📈 Análise Detalhada")
    
    # Verificar conexão
    if exchange_temp is None:
        st.warning("⚠️ Conecte suas API Keys para ver análises!")
        st.stop()
    
    symbol_analise = st.selectbox("Selecione a cripto para analisar:", symbols_sel)
    
    if symbol_analise:
        try:
            ohlcv_analise = exchange_temp.fetch_ohlcv(symbol_analise, config['tf'], limit=200)
            df_analise = pd.DataFrame(ohlcv_analise, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            ticker_analise = exchange_temp.fetch_ticker(symbol_analise)
            
            if not df_analise.empty and ticker_analise:
                signal_analise = (MeanReversionStrategy() if strategy_name == "mean_reversion" else TrendFollowingStrategy()).analyze(df_analise)
                
                # Métricas
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    # Validar se valores não são None antes de calcular
                    last_price = ticker_analise.get('last', 0) or 0
                    open_price = ticker_analise.get('open', 0) or 0
                    
                    if open_price > 0 and last_price > 0:
                        change = ((last_price - open_price) / open_price) * 100
                    else:
                        change = 0
                    
                    st.metric("Preço", f"{simbolo_moeda} {last_price*taxa_conversao:,.2f}", f"{change:+.2f}%")
                
                with col2:
                    st.metric("Sinal", signal_analise['signal'].upper(), f"{signal_analise['confidence']:.0f}%")
                
                with col3:
                    capital_aqui = capital_total * (alocacao.get(symbol_analise, 0) / 100)
                    st.metric("Capital Alocado", f"{simbolo_moeda} {capital_aqui*taxa_conversao:.0f}", f"{alocacao.get(symbol_analise, 0)}%")
                
                with col4:
                    st.metric("Volume 24h", f"{ticker_analise.get('baseVolume', 0):,.0f}")
                
                # GRÁFICO
                df_ind = (MeanReversionStrategy() if strategy_name == "mean_reversion" else TrendFollowingStrategy()).calculate_indicators(df_analise)
                
                fig = go.Figure()
                
                # Candlestick
                fig.add_trace(go.Candlestick(
                    x=df_analise.index,
                    open=df_analise['open'],
                    high=df_analise['high'],
                    low=df_analise['low'],
                    close=df_analise['close'],
                    name=symbol_analise,
                    increasing_line_color='#26a69a',
                    decreasing_line_color='#ef5350'
                ))
                
                # Indicadores
                if 'bb_middle' in df_ind.columns:
                    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_upper'], name='BB Superior', 
                                            line=dict(dash='dash', color='red', width=1)))
                    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_middle'], name='BB Média',
                                            line=dict(width=2, color='yellow')))
                    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_lower'], name='BB Inferior',
                                            line=dict(dash='dash', color='green', width=1)))
                
                fig.update_layout(
                    height=500,
                    template='plotly_dark',
                    xaxis_rangeslider_visible=False,
                    title=f"{symbol_analise} - {config['tf']}"
                )
                
                st.plotly_chart(fig)
                
                # Sinal em destaque
                if signal_analise['confidence'] >= config['conf']:
                    if signal_analise['signal'] == 'buy':
                        st.success(f"🟢 **OPORTUNIDADE DE COMPRA!** ({signal_analise['confidence']:.0f}%) - {signal_analise['reason']}")
                    elif signal_analise['signal'] == 'sell':
                        st.error(f"🔴 **OPORTUNIDADE DE VENDA!** ({signal_analise['confidence']:.0f}%) - {signal_analise['reason']}")
                else:
                    st.info(f"ℹ️ {signal_analise['reason']}")
        except Exception as e:
            st.warning(f"Erro ao carregar gráfico: {str(e)}")
    
    # ========================================
    # FOOTER - INFORMAÇÕES FINAIS
    # ========================================
    st.markdown("---")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.caption(f"✅ **Logado:** {st.session_state.get('user_email', 'N/A')}")
    
    with col_f2:
        st.caption(f"🔄 Próxima atualização: {freq_dashboard}s")
    
    with col_f3:
        st.caption(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ========================================
# AUTO-REFRESH (SEM OPACITY!)
# ========================================

# Opção para desabilitar auto-refresh
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Auto-Refresh")
auto_refresh_enabled = st.sidebar.checkbox(
    "Ativar atualização automática",
    value=True,
    help="Se desabilitado, use F5 para atualizar manualmente"
)

if auto_refresh_enabled:
    st.sidebar.caption(f"↻ Atualizando a cada {freq_dashboard}s")
    # Auto-refresh COM delay
    time.sleep(freq_dashboard)
    st.rerun()
else:
    st.sidebar.info("✋ Auto-refresh desabilitado")
    st.sidebar.caption("💡 Pressione F5 para atualizar")
    # Mostrar botão manual
    if st.sidebar.button("🔄 Atualizar Agora", use_container_width=True):
        st.rerun()

