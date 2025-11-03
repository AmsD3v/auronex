"""
RoboTrader - Dashboard Web Interativo
Execute com: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy
from config.settings import Settings

# Configurar página
st.set_page_config(
    page_title="RoboTrader Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-positive {
        color: #00ff00;
    }
    .metric-negative {
        color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🤖 RoboTrader - Dashboard ao Vivo")

# Sidebar
st.sidebar.header("⚙️ Configurações")

settings = Settings()

# Seleção de símbolo
symbol = st.sidebar.selectbox(
    "Símbolo",
    ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"],
    index=1 if settings.TRADING_SYMBOL == "ETHUSDT" else 0
)

# Seleção de estratégia
strategy_name = st.sidebar.selectbox(
    "Estratégia",
    ["mean_reversion", "trend_following"],
    index=0 if settings.STRATEGY == "mean_reversion" else 1
)

# Timeframe
timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1m", "5m", "15m", "1h"],
    index=2
)

# Auto-refresh
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Status")
st.sidebar.info(f"Modo: **TESTNET**")
st.sidebar.success(f"Paper Trading: **Ativo**")

# Inicializar conexão
@st.cache_resource
def get_exchange():
    return BinanceExchange()

try:
    exchange = get_exchange()
    
    # Criar estratégia
    if strategy_name == "mean_reversion":
        strategy = MeanReversionStrategy()
    else:
        strategy = TrendFollowingStrategy()
    
    # Obter dados
    with st.spinner("Carregando dados..."):
        df = exchange.get_ohlcv(symbol, timeframe, limit=100)
        ticker = exchange.get_ticker(symbol)
        balance = exchange.get_usdt_balance()
    
    if not df.empty and ticker:
        # Análise
        signal = strategy.analyze(df)
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = ticker['last']
        change_24h = ((ticker['last'] - ticker['open']) / ticker['open']) * 100
        
        with col1:
            st.metric(
                "💰 Preço Atual",
                f"${current_price:,.2f}",
                f"{change_24h:+.2f}%"
            )
        
        with col2:
            signal_emoji = {
                'buy': '🟢 COMPRAR',
                'sell': '🔴 VENDER',
                'hold': '⚪ AGUARDAR'
            }
            st.metric(
                "🎯 Sinal",
                signal_emoji.get(signal['signal'], 'HOLD'),
                f"{signal['confidence']:.1f}% confiança"
            )
        
        with col3:
            st.metric(
                "💵 Saldo USDT",
                f"${balance:,.2f}",
                "Testnet"
            )
        
        with col4:
            vol_24h = ticker.get('baseVolume', 0)
            st.metric(
                "📊 Volume 24h",
                f"${vol_24h:,.0f}",
                f"High: ${ticker['high']:,.2f}"
            )
        
        # Gráfico de preços
        st.markdown("---")
        st.subheader(f"📈 Gráfico de Preços - {symbol}")
        
        # Criar gráfico de candlestick
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=symbol
        )])
        
        # Adicionar médias móveis se disponível
        df_copy = strategy.calculate_indicators(df)
        
        if 'bb_middle' in df_copy.columns:
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['bb_upper'],
                name='BB Superior',
                line=dict(color='rgba(250, 0, 0, 0.5)', width=1, dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['bb_middle'],
                name='BB Média',
                line=dict(color='rgba(255, 255, 0, 0.8)', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['bb_lower'],
                name='BB Inferior',
                line=dict(color='rgba(0, 250, 0, 0.5)', width=1, dash='dash')
            ))
        
        fig.update_layout(
            height=500,
            xaxis_title="Data/Hora",
            yaxis_title="Preço (USDT)",
            hovermode='x unified',
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Indicadores
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Indicadores Técnicos")
            
            indicators = signal.get('indicators', {})
            
            # Criar DataFrame com indicadores
            ind_data = []
            for key, value in indicators.items():
                if isinstance(value, (int, float)):
                    ind_data.append({
                        'Indicador': key.replace('_', ' ').title(),
                        'Valor': f"{value:.2f}"
                    })
            
            if ind_data:
                st.dataframe(pd.DataFrame(ind_data), hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Análise da Estratégia")
            
            st.write(f"**Estratégia:** {strategy.get_name()}")
            st.write(f"**Sinal:** {signal['signal'].upper()}")
            st.write(f"**Confiança:** {signal['confidence']:.1f}%")
            st.write(f"**Motivo:** {signal['reason']}")
            
            # Barra de confiança
            if signal['confidence'] >= 65:
                st.success("✅ Sinal FORTE - Pode operar!")
            elif signal['confidence'] >= 40:
                st.warning("⚠️ Sinal MODERADO - Cuidado")
            else:
                st.info("ℹ️ Sem sinal - Aguardando...")
        
        # Informações de mercado
        st.markdown("---")
        st.subheader("📉 Informações de Mercado 24h")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Abertura", f"${ticker['open']:,.2f}")
        
        with col2:
            st.metric("Máxima", f"${ticker['high']:,.2f}", delta_color="off")
        
        with col3:
            st.metric("Mínima", f"${ticker['low']:,.2f}", delta_color="off")
        
        with col4:
            st.metric("Fechamento", f"${ticker['close']:,.2f}")
        
        # Última atualização
        st.markdown("---")
        st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
        
        # Auto-refresh
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    else:
        st.error("❌ Erro ao obter dados do mercado")

except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    st.exception(e)








