"""
Dashboard COMPLETO FINAL - TUDO EM UM!
Top 5 + Alocação + Portfolio + Feed de Atividades + Gráficos
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

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy
from config.settings import Settings

# Config
st.set_page_config(page_title="RoboTrader Completo", page_icon="💎", layout="wide")

# Perfis
PERFIS = {
    "🏦 Hedge Fund": {"tf": "1h", "sl": 2.0, "tp": 4.0, "conf": 70},
    "📈 Day Trader": {"tf": "15m", "sl": 1.5, "tp": 3.0, "conf": 60},
    "⚡ Scalper": {"tf": "5m", "sl": 1.0, "tp": 2.0, "conf": 55},
    "🚀 Ultra": {"tf": "1m", "sl": 0.5, "tp": 1.0, "conf": 50}
}

st.title("💎 RoboTrader - Dashboard Completo")

# Inicializar
@st.cache_resource
def get_exchange():
    return BinanceExchange()

# Buscar TODAS as criptos disponíveis
@st.cache_resource
def get_all_symbols():
    try:
        exchange = get_exchange()
        markets = exchange.exchange.load_markets()
        usdt_pairs = [s.replace('/', '') for s in markets.keys() if s.endswith('/USDT')]
        return sorted(usdt_pairs)
    except:
        # Fallback para principais
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 
                'DOGEUSDT', 'MATICUSDT', 'DOTUSDT', 'AVAXUSDT', 'LINKUSDT']

settings = Settings()

# ========================================
# FEED AO VIVO - NO TOPO! (DESTAQUE)
# ========================================
st.markdown("## 🔴 AO VIVO - Últimas Operações do Bot")

db_path = settings.DATA_DIR / 'trading.db'

try:
    conn = sqlite3.connect(db_path)
    query = """
        SELECT symbol, side, amount, price, timestamp
        FROM orders
        ORDER BY timestamp DESC
        LIMIT 5
    """
    df_feed = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df_feed.empty:
        cols = st.columns(5)
        
        for idx, (_, op) in enumerate(df_feed.iterrows()):
            with cols[idx]:
                tempo = datetime.fromtimestamp(op['timestamp']).strftime('%H:%M')
                crypto = op['symbol'].replace('USDT', '')
                side = op['side'].upper()
                
                if side == 'BUY':
                    st.success(f"**🟢 COMPRA**\n\n{crypto} - {tempo}\n\n${op['price']:,.0f}")
                else:
                    st.error(f"**🔴 VENDA**\n\n{crypto} - {tempo}\n\n${op['price']:,.0f}")
    else:
        st.info("⏳ Bot procurando oportunidades...")
except:
    st.warning("Aguardando primeira operação")

st.markdown("---")

# ========================================
# TOP 5 RANKINGS
# ========================================
st.markdown("## 🏆 TOP 5 CRIPTOMOEDAS - DESEMPENHO")

tab1, tab2, tab3 = st.tabs(["🔥 Hoje", "📅 Última Semana", "📆 Último Mês"])

exchange_temp = get_exchange()
# Usar top 30 principais para rankings (todas 425 seria lento)
todos_symbols_ranking = get_all_symbols()[:30]

with tab1:
    st.markdown("### 🔥 Melhor Performance HOJE (24 horas)")
    
    ranking_hoje = []
    for symbol in todos_symbols_ranking:
        try:
            df = exchange_temp.get_ohlcv(symbol, '1h', limit=24)
            if not df.empty and len(df) >= 2:
                var = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                vol = df['close'].pct_change().std() * 100
                ranking_hoje.append({
                    'Cripto': symbol.replace('USDT', ''),
                    'Variação': f"{var:+.2f}%",
                    'var_num': var,
                    'Volatilidade': f"{vol:.2f}%",
                    'Preço': f"${df['close'].iloc[-1]:,.2f}"
                })
        except:
            pass
    
    if ranking_hoje:
        df_rank = pd.DataFrame(ranking_hoje)
        df_rank = df_rank.sort_values('var_num', ascending=False).head(5)
        df_rank = df_rank.drop('var_num', axis=1)
        df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
        st.dataframe(df_rank, use_container_width=True)
        
        melhor_hoje = df_rank.iloc[0]
        st.success(f"💡 **Melhor HOJE:** {melhor_hoje['Cripto']} ({melhor_hoje['Variação']}) - Alta volatilidade! Foco aqui!")
    else:
        st.warning("Dados insuficientes")

with tab2:
    st.markdown("### 📅 Melhor Performance (7 dias)")
    ranking_semanal = []
    for symbol in todos_symbols_ranking:
        try:
            df = exchange_temp.get_ohlcv(symbol, '1d', limit=7)
            if not df.empty and len(df) >= 2:
                var = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                vol = df['close'].pct_change().std() * 100
                ranking_semanal.append({
                    'Cripto': symbol.replace('USDT', ''),
                    'Variação': f"{var:+.2f}%",
                    'var_num': var,
                    'Volatilidade': f"{vol:.2f}%",
                    'Preço': f"${df['close'].iloc[-1]:,.2f}"
                })
        except:
            pass
    
    if ranking_semanal:
        df_rank = pd.DataFrame(ranking_semanal)
        df_rank = df_rank.sort_values('var_num', ascending=False).head(5)
        df_rank = df_rank.drop('var_num', axis=1)
        df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
        st.dataframe(df_rank, use_container_width=True)
    else:
        st.warning("Dados insuficientes")

with tab3:
    st.markdown("### 📆 Melhor Performance (30 dias)")
    ranking_mensal = []
    for symbol in todos_symbols_ranking:
        try:
            df = exchange_temp.get_ohlcv(symbol, '1d', limit=30)
            if not df.empty and len(df) >= 10:
                var = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                vol = df['close'].pct_change().std() * 100
                ranking_mensal.append({
                    'Cripto': symbol.replace('USDT', ''),
                    'Variação': f"{var:+.2f}%",
                    'var_num': var,
                    'Volatilidade': f"{vol:.2f}%",
                    'Preço': f"${df['close'].iloc[-1]:,.2f}"
                })
        except:
            pass
    
    if ranking_mensal:
        df_rank = pd.DataFrame(ranking_mensal)
        df_rank = df_rank.sort_values('var_num', ascending=False).head(5)
        df_rank = df_rank.drop('var_num', axis=1)
        df_rank.index = ['🥇', '🥈', '🥉', '4º', '5º']
        st.dataframe(df_rank, use_container_width=True)
    else:
        st.warning("Dados insuficientes")

st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")

perfil = st.sidebar.selectbox("🎯 Perfil", list(PERFIS.keys()), index=1)
config = PERFIS[perfil]

st.sidebar.markdown("---")

capital_total = st.sidebar.number_input("💰 Capital Total", 10.0, 100000.0, 100.0, 10.0)

todos_symbols = get_all_symbols()

# Principais como padrão
principais_default = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
symbols_sel = st.sidebar.multiselect(
    f"📊 Criptos ({len(todos_symbols)} disponíveis)", 
    todos_symbols, 
    default=principais_default,
    help=f"Total de {len(todos_symbols)} criptomoedas disponíveis na Binance!"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Alocação de Capital")

modo_alocacao = st.sidebar.radio("Modo", ["⚖️ Automático", "🎯 Manual"])

alocacao = {}

if modo_alocacao == "🎯 Manual":
    st.sidebar.markdown("**Defina % (0.5% precisão):**")
    
    total_percent = 0
    for symbol in symbols_sel:
        crypto = symbol.replace('USDT', '')
        default_pct = 100 // len(symbols_sel) if len(symbols_sel) > 0 else 0
        
        pct = st.sidebar.slider(f"{crypto}", 0.0, 100.0, float(default_pct), step=0.5)
        alocacao[symbol] = pct
        total_percent += pct
    
    if total_percent == 100:
        st.sidebar.success(f"✅ Total: {total_percent}%")
    elif total_percent < 100:
        st.sidebar.warning(f"⚠️ Total: {total_percent}%")
    else:
        st.sidebar.error(f"❌ Total: {total_percent}%")
else:
    pct_por_cripto = 100 // len(symbols_sel) if len(symbols_sel) > 0 else 0
    for symbol in symbols_sel:
        alocacao[symbol] = pct_por_cripto
    st.sidebar.info(f"Cada: {pct_por_cripto}%")

strategy_name = st.sidebar.selectbox("🎯 Estratégia", ["mean_reversion", "trend_following"])

# Portfolio
st.markdown("## 💼 Portfolio Multi-Cripto")

try:
    exchange = get_exchange()
    
    if strategy_name == "mean_reversion":
        strategy = MeanReversionStrategy()
    else:
        strategy = TrendFollowingStrategy()
    
    portfolio_data = []
    total_atual = 0
    
    for symbol in symbols_sel:
        try:
            df = exchange.get_ohlcv(symbol, config['tf'], limit=100)
            ticker = exchange.get_ticker(symbol)
            
            if df.empty or not ticker:
                continue
            
            signal = strategy.analyze(df)
            
            capital_alocado = capital_total * (alocacao.get(symbol, 0) / 100)
            preco_inicial = df['close'].iloc[0]
            preco_atual = ticker['last']
            qty = capital_alocado / preco_inicial if preco_inicial > 0 else 0
            valor_atual = qty * preco_atual
            pnl = valor_atual - capital_alocado
            pnl_pct = (pnl / capital_alocado * 100) if capital_alocado > 0 else 0
            
            total_atual += valor_atual
            
            portfolio_data.append({
                'Cripto': symbol.replace('USDT', ''),
                'Alocação': f"{alocacao.get(symbol, 0)}%",
                'Capital': f"${capital_alocado:.2f}",
                'Valor': f"${valor_atual:.2f}",
                'P&L': f"${pnl:+.2f}",
                '%': f"{pnl_pct:+.1f}%",
                'Sinal': signal['signal'].upper()[:4],
                'Conf': f"{signal['confidence']:.0f}%"
            })
        except:
            pass
    
    total_pnl = total_atual - capital_total
    total_pnl_pct = (total_pnl / capital_total * 100) if capital_total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💵 Capital Total", f"${capital_total:.2f}")
    
    with col2:
        st.metric("💎 Valor Atual", f"${total_atual:.2f}")
    
    with col3:
        st.metric("📊 P&L", f"${total_pnl:+.2f}", f"{total_pnl_pct:+.2f}%")
    
    if portfolio_data:
        df_port = pd.DataFrame(portfolio_data)
        st.dataframe(df_port, use_container_width=True, hide_index=True)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Alocação (%)")
            fig = px.pie(values=[alocacao.get(s, 0) for s in symbols_sel],
                        names=[s.replace('USDT', '') for s in symbols_sel], hole=0.4)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 Valor (USDT)")
            fig = px.pie(values=[float(v.replace('$', '').replace(',', '')) for v in df_port['Valor']],
                        names=df_port['Cripto'], hole=0.4)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Análise individual
    st.markdown("## 📈 Análise Detalhada")
    
    symbol_analise = st.selectbox("Cripto:", symbols_sel)
    
    if symbol_analise:
        df = exchange.get_ohlcv(symbol_analise, config['tf'], limit=200)
        ticker = exchange.get_ticker(symbol_analise)
        
        if not df.empty and ticker:
            signal = strategy.analyze(df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                change = ((ticker['last'] - ticker['open']) / ticker['open']) * 100
                st.metric("Preço", f"${ticker['last']:,.2f}", f"{change:+.2f}%")
            
            with col2:
                st.metric("Sinal", signal['signal'].upper(), f"{signal['confidence']:.0f}%")
            
            with col3:
                capital_aqui = capital_total * (alocacao.get(symbol_analise, 0) / 100)
                st.metric("Capital Alocado", f"${capital_aqui:.2f}")
            
            with col4:
                st.metric("Volume 24h", f"{ticker.get('baseVolume', 0):,.0f}")
            
            # Gráfico
            df_ind = strategy.calculate_indicators(df)
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'],
                                        low=df['low'], close=df['close'], name=symbol_analise))
            
            if 'bb_middle' in df_ind.columns:
                fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_upper'], name='BB+', 
                                        line=dict(dash='dash', color='red')))
                fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_middle'], name='BB=',
                                        line=dict(width=2, color='yellow')))
                fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_lower'], name='BB-',
                                        line=dict(dash='dash', color='green')))
            
            fig.update_layout(height=400, template='plotly_dark', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            if signal['confidence'] >= config['conf']:
                if signal['signal'] == 'buy':
                    st.success(f"🟢 OPORTUNIDADE DE COMPRA! {signal['reason']}")
                elif signal['signal'] == 'sell':
                    st.error(f"🔴 OPORTUNIDADE DE VENDA! {signal['reason']}")
            else:
                st.info(f"ℹ️ {signal['reason']}")
    
    st.caption(f"⏰ {datetime.now().strftime('%H:%M:%S')} | 🔄 Atualização: 5 segundos")
    
    time.sleep(5)
    st.rerun()

except Exception as e:
    st.error(f"❌ {str(e)}")
    if st.button("🔄 Recarregar"):
        st.rerun()

