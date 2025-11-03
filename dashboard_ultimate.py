"""
RoboTrader ULTIMATE - Dashboard Completo Multi-Cripto
Execute com: streamlit run dashboard_ultimate.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy

# Configurar página
st.set_page_config(
    page_title="RoboTrader Ultimate",
    page_icon="💎",
    layout="wide"
)

# PERFIS
PERFIS = {
    "🏦 Hedge Fund": {"tf": "1h", "sl": 0.02, "tp": 0.04, "conf": 70, "desc": "Conservador - 1-2 trades/dia - Baixo risco"},
    "📈 Day Trader": {"tf": "15m", "sl": 0.015, "tp": 0.03, "conf": 60, "desc": "Moderado - 2-5 trades/dia - Médio risco"},
    "⚡ Scalper": {"tf": "5m", "sl": 0.01, "tp": 0.02, "conf": 55, "desc": "Agressivo - 8-15 trades/dia - Alto risco"},
    "🚀 Ultra": {"tf": "1m", "sl": 0.005, "tp": 0.01, "conf": 50, "desc": "Muito Agressivo - 20-50 trades/dia"}
}

# Título
st.title("💎 RoboTrader Ultimate - Multi-Cripto")

# Sidebar
st.sidebar.header("⚙️ Configurações")

perfil = st.sidebar.selectbox("🎯 Perfil", list(PERFIS.keys()), index=1)
config = PERFIS[perfil]

st.sidebar.caption(config["desc"])
st.sidebar.markdown("---")

capital_total = st.sidebar.number_input("💰 Capital Total", 10.0, 100000.0, 100.0, 10.0)

# Criptos para monitorar
todos_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT']
symbols_selecionados = st.sidebar.multiselect(
    "📊 Criptos para Monitorar",
    todos_symbols,
    default=['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
)

strategy_name = st.sidebar.selectbox("🎯 Estratégia", ["mean_reversion", "trend_following"])

auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh", True)

# Inicializar
@st.cache_resource
def get_exchange():
    return BinanceExchange()

try:
    exchange = get_exchange()
    
    if strategy_name == "mean_reversion":
        strategy = MeanReversionStrategy()
    else:
        strategy = TrendFollowingStrategy()
    
    # ========================================
    # TOP 5 RANKING
    # ========================================
    st.markdown("## 🏆 TOP 5 CRIPTOMOEDAS - DESEMPENHO")
    
    tab1, tab2 = st.tabs(["📅 Última Semana", "📆 Último Mês"])
    
    with tab1:
        st.markdown("### Melhor Performance (7 dias)")
        
        ranking_semanal = []
        for symbol in todos_symbols:
            try:
                df = exchange.get_ohlcv(symbol, '1d', limit=7)
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
    
    with tab2:
        st.markdown("### Melhor Performance (30 dias)")
        
        ranking_mensal = []
        for symbol in todos_symbols:
            try:
                df = exchange.get_ohlcv(symbol, '1d', limit=30)
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
    
    st.markdown("---")
    
    # ========================================
    # PORTFOLIO GERAL
    # ========================================
    st.markdown("## 💼 PORTFOLIO MULTI-CRIPTO")
    
    # Calcular alocação
    num_cryptos = len(symbols_selecionados)
    capital_por_cripto = capital_total / num_cryptos if num_cryptos > 0 else 0
    
    # Coletar dados de todas
    portfolio_data = []
    total_atual = 0
    
    for symbol in symbols_selecionados:
        try:
            df = exchange.get_ohlcv(symbol, config['tf'], limit=100)
            ticker = exchange.get_ticker(symbol)
            
            if not df.empty and ticker:
                signal = strategy.analyze(df)
                
                preco_inicial = df['close'].iloc[0]
                preco_atual = ticker['last']
                qty = capital_por_cripto / preco_inicial
                valor_atual = qty * preco_atual
                pnl = valor_atual - capital_por_cripto
                pnl_pct = (pnl / capital_por_cripto) * 100
                
                total_atual += valor_atual
                
                portfolio_data.append({
                    'Cripto': symbol.replace('USDT', ''),
                    'Alocado': f"${capital_por_cripto:.2f}",
                    'Valor Atual': f"${valor_atual:.2f}",
                    'P&L': f"${pnl:+.2f}",
                    'P&L %': f"{pnl_pct:+.2f}%",
                    'Sinal': signal['signal'].upper(),
                    'Conf': f"{signal['confidence']:.0f}%",
                    'pnl_num': pnl
                })
        except:
            pass
    
    # Métricas gerais
    total_pnl = total_atual - capital_total
    total_pnl_pct = (total_pnl / capital_total * 100) if capital_total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💵 Capital Total", f"${capital_total:.2f}", f"{num_cryptos} criptos")
    
    with col2:
        st.metric("💎 Valor Atual", f"${total_atual:.2f}")
    
    with col3:
        st.metric("📊 P&L Total", f"${total_pnl:+.2f}", f"{total_pnl_pct:+.2f}%")
    
    with col4:
        if total_pnl > 0:
            st.success(f"✅ LUCRO\n${total_pnl:.2f}")
        elif total_pnl < 0:
            st.error(f"❌ PREJUÍZO\n${abs(total_pnl):.2f}")
        else:
            st.info("➖ Neutro")
    
    # Tabela do portfolio
    if portfolio_data:
        df_port = pd.DataFrame(portfolio_data)
        
        # Colorir P&L
        def color_pnl(val):
            if '+' in str(val):
                return 'background-color: rgba(0, 255, 0, 0.2)'
            elif '-' in str(val):
                return 'background-color: rgba(255, 0, 0, 0.2)'
            return ''
        
        st.dataframe(
            df_port.style.applymap(color_pnl, subset=['P&L', 'P&L %']),
            use_container_width=True
        )
        
        # Gráfico de alocação
        st.markdown("### 📊 Distribuição do Portfolio")
        
        fig_pie = px.pie(
            df_port,
            values=[float(v.replace('$', '').replace(',', '')) for v in df_port['Valor Atual']],
            names=df_port['Cripto'],
            title="Alocação Atual",
            hole=0.4
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================
    # ANÁLISE INDIVIDUAL
    # ========================================
    st.markdown("## 📈 Análise Individual")
    
    symbol_analise = st.selectbox("Cripto para Analisar", symbols_selecionados)
    
    if symbol_analise:
        df = exchange.get_ohlcv(symbol_analise, config['tf'], limit=200)
        ticker = exchange.get_ticker(symbol_analise)
        
        if not df.empty and ticker:
            signal = strategy.analyze(df)
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                change = ((ticker['last'] - ticker['open']) / ticker['open']) * 100
                st.metric("Preço", f"${ticker['last']:,.2f}", f"{change:+.2f}%")
            
            with col2:
                st.metric("Sinal", signal['signal'].upper(), f"{signal['confidence']:.0f}%")
            
            with col3:
                st.metric("Volume 24h", f"{ticker.get('baseVolume', 0):,.0f}")
            
            with col4:
                var_24h = ticker['high'] - ticker['low']
                st.metric("Amplitude", f"${var_24h:,.2f}")
            
            # Gráfico
            df_ind = strategy.calculate_indicators(df)
            
            fig = go.Figure()
            
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name=symbol_analise
            ))
            
            if 'bb_middle' in df_ind.columns:
                fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_upper'], name='BB+', line=dict(dash='dash')))
                fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_middle'], name='BB=', line=dict(width=2)))
                fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind['bb_lower'], name='BB-', line=dict(dash='dash')))
            
            fig.update_layout(height=400, template='plotly_dark', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Análise
            if signal['confidence'] >= config['conf']:
                if signal['signal'] == 'buy':
                    st.success(f"🟢 OPORTUNIDADE DE COMPRA! ({signal['confidence']:.0f}%) - {signal['reason']}")
                elif signal['signal'] == 'sell':
                    st.error(f"🔴 OPORTUNIDADE DE VENDA! ({signal['confidence']:.0f}%) - {signal['reason']}")
            else:
                st.info(f"ℹ️ {signal['reason']}")
    
    # Footer
    st.caption(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if auto_refresh:
        time.sleep(30)
        st.rerun()

except Exception as e:
    st.error(f"❌ {str(e)}")







