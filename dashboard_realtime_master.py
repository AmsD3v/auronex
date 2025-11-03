"""
🚀 DASHBOARD TEMPO REAL - SEM OPACITY!

Características:
- ✅ Atualização em tempo real (SEM st.rerun())
- ✅ Relógio fluido (nunca para!)
- ✅ ZERO opacity
- ✅ Auto-save configurações
- ✅ Multi-usuário autenticado
- ✅ Experiência profissional
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
import json
import ccxt

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy
from config.settings import Settings

# Config
st.set_page_config(page_title="🚀 RoboTrader RealTime", page_icon="⚡", layout="wide")

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def check_authentication():
    """Verificar autenticação"""
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    
    st.sidebar.title("🔐 Login")
    
    email = st.sidebar.text_input("Email:", key="login_email")
    password = st.sidebar.text_input("Senha:", type="password", key="login_password")
    
    if st.sidebar.button("🔓 Entrar", use_container_width=True):
        with st.spinner("Conectando..."):
            try:
                response = requests.post(
                    'http://localhost:8001/api/auth/login/',
                    json={'email': email, 'password': password},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.access_token = data['access']
                    st.session_state.user_email = email
                    st.session_state.user_name = data['user'].get('first_name', 'Usuário')
                    st.session_state.authenticated = True
                    st.sidebar.success("✅ Login OK!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.sidebar.error("❌ Email ou senha incorretos!")
            except Exception as e:
                st.sidebar.error("❌ Erro de conexão!")
                st.sidebar.caption("Verifique se Django está em: http://localhost:8001")
    
    st.title("🔒 Login Necessário")
    st.info("👈 Faça login na sidebar")
    return False

def get_user_api_keys():
    """Buscar API Keys do usuário"""
    if 'access_token' not in st.session_state:
        return []
    
    try:
        response = requests.get(
            'http://localhost:8001/api/api-keys/',
            headers={'Authorization': f'Bearer {st.session_state.access_token}'},
            timeout=5
        )
        return response.json() if response.status_code == 200 else []
    except:
        return []

def get_exchange_for_user(exchange_name="binance"):
    """Conectar exchange do usuário"""
    user_keys = get_user_api_keys()
    
    if not user_keys:
        return None
    
    for key in user_keys:
        if key.get('exchange', '').lower() == exchange_name.lower():
            try:
                response = requests.get(
                    f'http://localhost:8001/api/api-keys/{key["id"]}/',
                    headers={'Authorization': f'Bearer {st.session_state.access_token}'},
                    timeout=5
                )
                
                if response.status_code == 200:
                    key_data = response.json()
                    
                    exchange_class = getattr(ccxt, exchange_name.lower())
                    exchange = exchange_class({
                        'apiKey': key_data.get('api_key_decrypted', ''),
                        'secret': key_data.get('secret_key_decrypted', ''),
                        'enableRateLimit': True,
                        'options': {'defaultType': 'spot'}
                    })
                    
                    if key_data.get('is_testnet', False):
                        exchange.set_sandbox_mode(True)
                    
                    return exchange
            except:
                return None
    return None

def load_config():
    """Carregar configuração do usuário"""
    if 'user_email' not in st.session_state:
        return {}
    
    config_file = f"config_{st.session_state.user_email.replace('@', '_').replace('.', '_')}.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """Salvar configuração automaticamente"""
    if 'user_email' not in st.session_state:
        return False
    
    config_file = f"config_{st.session_state.user_email.replace('@', '_').replace('.', '_')}.json"
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False

def auto_save_config(config_atual):
    """Auto-save detectando mudanças"""
    if config_atual != st.session_state.get('config_anterior', {}):
        if save_config(config_atual):
            st.session_state.config_anterior = config_atual
            return True
    return False

# ========================================
# VERIFICAR AUTENTICAÇÃO
# ========================================

if not check_authentication():
    st.stop()

# ========================================
# SIDEBAR - CONTROLES (ESTÁTICOS)
# ========================================

# Debug auth
with st.sidebar.expander("🔍 Debug Auth"):
    st.write(f"Auth: {st.session_state.get('authenticated', False)}")
    st.write(f"User: {st.session_state.get('user_email', 'N/A')}")
    st.write(f"Name: {st.session_state.get('user_name', 'N/A')}")

st.sidebar.success(f"✅ {st.session_state.get('user_name', 'Usuário')}")

if st.sidebar.button("🚪 Sair"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Configurações")

# Carregar config salva
config_salva = load_config()

# Perfis
PERFIS = {
    "🏦 Hedge Fund": {"tf": "1h", "sl": 2.0, "tp": 4.0},
    "📈 Day Trader": {"tf": "15m", "sl": 1.5, "tp": 3.0},
    "⚡ Scalper": {"tf": "5m", "sl": 1.0, "tp": 2.0},
}

perfil_index = 1

# Aplicar perfil carregado se existir
if 'perfil_load' in st.session_state:
    try:
        perfil_index = list(PERFIS.keys()).index(st.session_state.perfil_load)
        del st.session_state.perfil_load
    except:
        pass
elif config_salva.get('perfil'):
    try:
        perfil_index = list(PERFIS.keys()).index(config_salva['perfil'])
    except:
        pass

perfil = st.sidebar.selectbox("🎯 Perfil", list(PERFIS.keys()), index=perfil_index)
config = PERFIS[perfil]

# Frequência atualização
if 'freq_load' in st.session_state:
    value_freq = st.session_state.freq_load
    del st.session_state.freq_load
else:
    value_freq = config_salva.get('freq_update', 3)

freq_update = st.sidebar.slider(
    "⚡ Frequência (segundos)",
    min_value=1,
    max_value=10,
    value=value_freq,
    help="Velocidade de atualização do dashboard"
)

if freq_update <= 3:
    st.sidebar.success("⚡ Tempo real!")
else:
    st.sidebar.info(f"↻ Atualiza a cada {freq_update}s")

st.sidebar.markdown("---")

# Capital
if 'capital_load' in st.session_state:
    value_capital = st.session_state.capital_load
    del st.session_state.capital_load
else:
    value_capital = config_salva.get('capital', 1000.0)

capital_input = st.sidebar.number_input(
    "💵 Capital Total (R$)",
    min_value=10.0,
    max_value=1000000.0,
    value=value_capital,
    step=100.0
)

# Moeda
if 'moeda_load' in st.session_state:
    moeda_val = st.session_state.moeda_load
    del st.session_state.moeda_load
else:
    moeda_val = config_salva.get('moeda', 'BRL')

moeda = st.sidebar.selectbox(
    "💰 Moeda",
    ["BRL", "USD"],
    index=0 if moeda_val == 'BRL' else 1
)

simbolo_moeda = "R$" if moeda == "BRL" else "$"
taxa_conversao = 1.0 if moeda == "BRL" else 0.20

st.sidebar.markdown("---")

# ✅ SELETOR DE CORRETORA (melhorado!)
st.sidebar.markdown("### 🏦 Corretora")
corretora_options = ["Binance", "Bybit", "OKX", "Kraken", "KuCoin"]

# Verificar qual exchange usuário tem API Keys
user_keys = get_user_api_keys()
exchanges_disponiveis = [k.get('exchange', 'Binance') for k in user_keys] if user_keys else ['Binance']

if exchanges_disponiveis:
    default_index = 0
    if config_salva.get('corretora') and config_salva.get('corretora') in corretora_options:
        try:
            default_index = corretora_options.index(config_salva.get('corretora'))
        except:
            pass
    
    corretora = st.sidebar.selectbox(
        "Selecione:",
        corretora_options,
        index=default_index,
        help="Apenas corretoras com API Keys configuradas funcionarão"
    )
    
    # Mostrar quais estão configuradas
    if corretora.lower() in [e.lower() for e in exchanges_disponiveis]:
        st.sidebar.success(f"✅ {corretora} configurada!")
    else:
        st.sidebar.warning(f"⚠️ {corretora} não tem API Keys")
        st.sidebar.caption("Configure em: http://localhost:8001/api-keys/")
else:
    corretora = "Binance"
    st.sidebar.warning("⚠️ Nenhuma API Key configurada")
    st.sidebar.caption("Adicione em: http://localhost:8001/api-keys/")

# ✅ Símbolos DINÂMICOS baseado na corretora (DROPDOWN como era!)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Criptomoedas")

# Buscar símbolos da corretora
exchange_temp = get_exchange_for_user(corretora)

if exchange_temp:
    try:
        # Buscar TODOS os pares da exchange
        markets = exchange_temp.load_markets()
        all_symbols = sorted([s.replace('/', '') for s in markets.keys() if s.endswith('/USDT')])
        
        st.sidebar.success(f"✅ {len(all_symbols)} pares disponíveis em {corretora}")
    except:
        all_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT']
        st.sidebar.warning(f"⚠️ Usando lista padrão")
else:
    all_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT']
    st.sidebar.info("Configure API Keys para carregar lista completa")

# Valor padrão
if 'symbols_load' in st.session_state:
    default_symbols = st.session_state.symbols_load
    del st.session_state.symbols_load
else:
    default_symbols = config_salva.get('symbols', ['BTCUSDT', 'ETHUSDT', 'SOLUSDT'])

# ✅ MULTISELECT como era antes (melhor para pesquisar!)
symbols_sel = st.sidebar.multiselect(
    "Selecione (digite para pesquisar):",
    all_symbols,
    default=default_symbols,
    help=f"Total: {len(all_symbols)} pares disponíveis em {corretora}"
)

# Estratégia
if 'strategy_load' in st.session_state:
    strategy_val = st.session_state.strategy_load
    del st.session_state.strategy_load
else:
    strategy_val = config_salva.get('strategy', 'mean_reversion')

strategy_name = st.sidebar.selectbox(
    "🎯 Estratégia",
    ["mean_reversion", "trend_following"],
    index=0 if strategy_val == 'mean_reversion' else 1
)

st.sidebar.markdown("---")

# ========================================
# SALVAR/CARREGAR PERFIS NOMEADOS
# ========================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Perfis")

# Criar pasta perfis se não existir
if not os.path.exists('perfis'):
    os.makedirs('perfis')

# Listar perfis salvos
perfis_salvos = [f.replace('.json', '') for f in os.listdir('perfis') if f.endswith('.json')]

# Nome do perfil
nome_perfil = st.sidebar.text_input("📝 Nome do Perfil", "Meu_Setup", help="Nome para salvar/carregar")

col_save, col_load = st.sidebar.columns(2)

with col_save:
    if st.button("💾 Salvar", use_container_width=True):
        config_completa = {
            'perfil': perfil,
            'freq_update': freq_update,
            'capital': capital_input,
            'moeda': moeda,
            'symbols': symbols_sel,
            'strategy': strategy_name
        }
        with open(f'perfis/{nome_perfil}.json', 'w') as f:
            json.dump(config_completa, f, indent=2)
        
        # Auto-save do usuário também
        if save_config(config_completa):
            st.sidebar.success(f"✅ '{nome_perfil}' salvo!")

with col_load:
    perfil_sel = st.selectbox("Carregar:", [""] + perfis_salvos, label_visibility="collapsed", key="load_sel")
    
    if perfil_sel and st.button("📂 Carregar", use_container_width=True):
        try:
            with open(f'perfis/{perfil_sel}.json', 'r') as f:
                config_load = json.load(f)
            
            # Salvar no session_state para aplicar após rerun
            st.session_state.perfil_load = config_load.get('perfil', '📈 Day Trader')
            st.session_state.freq_load = config_load.get('freq_update', 3)
            st.session_state.capital_load = config_load.get('capital', 1000.0)
            st.session_state.moeda_load = config_load.get('moeda', 'BRL')
            st.session_state.symbols_load = config_load.get('symbols', ['BTCUSDT'])
            st.session_state.strategy_load = config_load.get('strategy', 'mean_reversion')
            
            st.sidebar.success(f"✅ '{perfil_sel}' carregado!")
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Erro: {e}")

# Auto-save config atual
config_atual = {
    'perfil': perfil,
    'freq_update': freq_update,
    'capital': capital_input,
    'moeda': moeda,
    'symbols': symbols_sel,
    'strategy': strategy_name
}

if auto_save_config(config_atual):
    st.sidebar.caption("💾 Auto-salvo!")

# ========================================
# CONECTAR EXCHANGE
# ========================================

exchange = get_exchange_for_user(corretora.lower())

if exchange is None:
    st.sidebar.warning(f"⚠️ API Keys {corretora} não configuradas")
    st.warning(f"⚠️ Configure suas API Keys para {corretora}")
    st.info("💡 Acesse: http://localhost:8001/api-keys/")
    st.info("💡 Ou continue para ver o dashboard (sem dados de mercado)")
    
    # Não parar - mostrar dashboard vazio
    exchange_disponivel = False
else:
    exchange_disponivel = True

# Estratégia
if strategy_name == "mean_reversion":
    strategy = MeanReversionStrategy()
else:
    strategy = TrendFollowingStrategy()

# Settings
settings = Settings()

# ========================================
# CONTEÚDO PRINCIPAL
# ========================================
        
# ========================================
# HEADER COM RELÓGIO E CONTROLE BOT
# ========================================

# Ler estado do bot
try:
    with open('bot_status.json', 'r') as f:
        bot_status = json.load(f)
        bot_running = bot_status.get('running', False)
except:
    bot_running = False

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    st.markdown(f"### ⏰ {datetime.now().strftime('%H:%M:%S')}")

with col2:
    if bot_running:
        st.success("🟢 **BOT ATIVO**")
    else:
        st.error("🔴 **PARADO**")

with col3:
    st.metric("💵 Capital", f"{simbolo_moeda} {capital_input:.0f}")

with col4:
    # Botão START/STOP
    if bot_running:
        if st.button("⏸️ PARAR BOT", type="primary", use_container_width=True):
            with open('bot_status.json', 'w') as f:
                json.dump({'running': False}, f)
            st.success("Bot pausado!")
            time.sleep(0.5)
            st.rerun()
    else:
        if st.button("▶️ INICIAR BOT", type="primary", use_container_width=True):
            with open('bot_status.json', 'w') as f:
                json.dump({'running': True}, f)
            st.success("🚀 Bot iniciado!")
            time.sleep(0.5)
            st.rerun()

st.markdown("---")

# ========================================
# SALDO REAL DA CORRETORA
# ========================================

if exchange_disponivel:
    st.markdown("## 💰 Saldo Real na Corretora")
    
    try:
        balance = exchange.fetch_balance()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            usdt_free = balance.get('free', {}).get('USDT', 0)
            st.metric("💵 USDT Disponível", f"${usdt_free:,.2f}")
        
        with col2:
            usdt_used = balance.get('used', {}).get('USDT', 0)
            st.metric("📊 USDT em Uso", f"${usdt_used:,.2f}")
        
        with col3:
            usdt_total = balance.get('total', {}).get('USDT', 0)
            st.metric("💎 USDT Total", f"${usdt_total:,.2f}")
        
        # Mostrar outras criptos se tiver
        with st.expander("📊 Ver todas moedas"):
            outras_moedas = []
            for moeda, valor in balance.get('total', {}).items():
                if valor > 0 and moeda != 'USDT':
                    outras_moedas.append({
                        'Moeda': moeda,
                        'Quantidade': f"{valor:.8f}",
                        'Valor (USDT)': f"${balance['total'][moeda] * (exchange.fetch_ticker(f'{moeda}/USDT')['last'] if f'{moeda}/USDT' in exchange.markets else 0):,.2f}"
                    })
            
            if outras_moedas:
                st.dataframe(pd.DataFrame(outras_moedas), use_container_width=True)
            else:
                st.info("Apenas USDT na carteira")
    
    except Exception as e:
        st.warning(f"⚠️ Erro ao buscar saldo: {str(e)}")
        st.caption("Verifique se API Keys têm permissão de leitura")

st.markdown("---")

# ========================================
# TOP 5 RANKINGS
# ========================================

st.markdown("## 🏆 TOP 5 - Performance")

if not exchange_disponivel:
    st.info("⚠️ Configure API Keys para ver rankings")
else:
    tab1, tab2, tab3 = st.tabs(["🔥 Hoje", "📅 Semana", "📆 Mês"])
    
    with tab1:
        st.markdown("**Últimas 24h**")
        ranking = []
        
        for symbol in all_symbols[:10]:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=24)
                if ohlcv and len(ohlcv) >= 2:
                    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    var = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                    ranking.append({
                        'Cripto': symbol.replace('USDT', ''),
                        'Var': f"{var:+.2f}%",
                        'var_num': var,
                        'Preço': f"{simbolo_moeda} {df['close'].iloc[-1]*taxa_conversao:,.2f}"
                    })
            except:
                pass
        
        if ranking:
            df_rank = pd.DataFrame(ranking).sort_values('var_num', ascending=False).head(5)
            df_rank = df_rank.drop('var_num', axis=1)
            df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_rank, use_container_width=True)
        else:
            st.info("Carregando...")
    
    with tab2:
        st.markdown("**7 dias**")
        ranking_s = []
        for symbol in all_symbols[:10]:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=7)
                if ohlcv and len(ohlcv) >= 2:
                    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    var = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                    ranking_s.append({
                        'Cripto': symbol.replace('USDT', ''),
                        'Var': f"{var:+.2f}%",
                        'var_num': var
                    })
            except:
                pass
        
        if ranking_s:
            df_rank = pd.DataFrame(ranking_s).sort_values('var_num', ascending=False).head(5)
            df_rank = df_rank.drop('var_num', axis=1)
            df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_rank, use_container_width=True)
        else:
            st.info("Carregando...")
    
    with tab3:
        st.markdown("**30 dias**")
        ranking_m = []
        for symbol in all_symbols[:10]:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=30)
                if ohlcv and len(ohlcv) >= 2:
                    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    var = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                    ranking_m.append({
                        'Cripto': symbol.replace('USDT', ''),
                        'Var': f"{var:+.2f}%",
                        'var_num': var
                    })
            except:
                pass
        
        if ranking_m:
            df_rank = pd.DataFrame(ranking_m).sort_values('var_num', ascending=False).head(5)
            df_rank = df_rank.drop('var_num', axis=1)
            df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
            st.dataframe(df_rank, use_container_width=True)
        else:
            st.info("Carregando...")

st.markdown("---")

# ========================================
# PORTFOLIO
# ========================================

st.markdown("## 💼 Portfolio")

if not exchange_disponivel:
    st.info("⚠️ Configure API Keys para ver portfolio")
elif not symbols_sel:
    st.warning("⚠️ Selecione criptomoedas na sidebar!")
else:
    portfolio_data = []
    total_atual = 0
    capital_por_cripto = capital_input / len(symbols_sel)
    
    for symbol in symbols_sel:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, config['tf'], limit=50)
            ticker = exchange.fetch_ticker(symbol)
            
            if ohlcv and ticker:
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                preco_atual = ticker.get('last', 0)
                
                if preco_atual > 0 and not df.empty:
                    signal = strategy.analyze(df)
                    
                    preco_inicial = df['close'].iloc[0]
                    valor_atual = (capital_por_cripto / preco_inicial) * preco_atual
                    pnl = valor_atual - capital_por_cripto
                    
                    total_atual += valor_atual
                    
                    portfolio_data.append({
                        'Cripto': symbol.replace('USDT', ''),
                        'Capital': f"{simbolo_moeda} {capital_por_cripto*taxa_conversao:.0f}",
                        'capital_num': capital_por_cripto*taxa_conversao,
                        'Valor': f"{simbolo_moeda} {valor_atual*taxa_conversao:.0f}",
                        'P&L': f"{simbolo_moeda} {pnl*taxa_conversao:+.0f}",
                        'Sinal': signal['signal'].upper()[:4]
                    })
        except:
            pass
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Capital", f"{simbolo_moeda} {capital_input:.2f}")
    with col2:
        st.metric("💎 Valor Atual", f"{simbolo_moeda} {total_atual*taxa_conversao:.2f}")
    with col3:
        pnl_total = total_atual - capital_input
        pnl_percent = (pnl_total/capital_input*100) if capital_input > 0 else 0
        st.metric("📊 P&L", f"{simbolo_moeda} {pnl_total*taxa_conversao:+.2f}", f"{pnl_percent:+.1f}%")
    
    # Tabela + Gráfico
    if portfolio_data:
        col_table, col_chart = st.columns([2, 1])
        
        with col_table:
            df_port = pd.DataFrame(portfolio_data)
            df_port_display = df_port.drop('capital_num', axis=1) if 'capital_num' in df_port.columns else df_port
            st.dataframe(df_port_display, use_container_width=True, hide_index=True)
        
        with col_chart:
            st.markdown("**📊 Distribuição**")
            
            crypto_names = [d['Cripto'] for d in portfolio_data]
            capital_values = [d.get('capital_num', 0) for d in portfolio_data]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=crypto_names,
                values=capital_values,
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=150,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_chart_{int(time.time())}")
    else:
        st.info("Carregando portfolio...")

st.markdown("---")

# ========================================
# GRÁFICO PRINCIPAL
# ========================================

if symbols_sel and exchange_disponivel:
    st.markdown("## 📈 Análise Gráfica")
    
    symbol_analise = st.selectbox("Cripto:", symbols_sel, key="symbol_select")
    
    try:
        ohlcv = exchange.fetch_ohlcv(symbol_analise, config['tf'], limit=100)
        
        if ohlcv:
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            signal = strategy.analyze(df)
            
            # Candlestick
            fig = go.Figure(data=[go.Candlestick(
                x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name=symbol_analise
            )])
            
            fig.update_layout(
                title=f"{symbol_analise} - {config['tf']}",
                height=400,
                xaxis_title="Tempo",
                yaxis_title="Preço (USDT)"
            )
            
            st.plotly_chart(fig, use_container_width=True, key=f"candlestick_{symbol_analise}_{int(time.time())}")
            
            # Sinal
            if signal['confidence'] >= 60:
                if signal['signal'] == 'buy':
                    st.success(f"🟢 **COMPRAR!** ({signal['confidence']:.0f}%) - {signal.get('reason', '')}")
                else:
                    st.error(f"🔴 **VENDER!** ({signal['confidence']:.0f}%) - {signal.get('reason', '')}")
            else:
                st.info(f"ℹ️ {signal.get('reason', 'Aguardar')}")
    except Exception as e:
        st.warning(f"Erro ao carregar gráfico: {str(e)}")
        
# Footer
st.caption(f"⚡ Atualização automática a cada {freq_update}s | Última: {datetime.now().strftime('%H:%M:%S')}")

# ========================================
# AUTO-REFRESH
# ========================================

# Aguardar e recarregar
time.sleep(freq_update)
st.rerun()

