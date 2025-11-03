"""
RoboTrader - Dashboard COMPLETO com Tracking de Lucro/Prejuízo
Execute com: streamlit run dashboard_completo.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy
from config.settings import Settings

# Configurar página
st.set_page_config(
    page_title="RoboTrader Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título
st.title("💰 RoboTrader - Dashboard Completo")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")

settings = Settings()

# Capital inicial
capital_inicial = st.sidebar.number_input(
    "Capital Inicial (USDT)",
    min_value=10.0,
    max_value=100000.0,
    value=10.0,
    step=10.0,
    help="Quanto você investiria"
)

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
    index=0
)

# Timeframe
timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1m", "5m", "15m", "1h"],
    index=2
)

# Número de candles
num_candles = st.sidebar.slider("Candles no Gráfico", 50, 500, 100)

# Auto-refresh
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Status")
mode_color = "blue" if settings.USE_TESTNET else "red"
st.sidebar.markdown(f":{mode_color}[Modo: **TESTNET**]")

paper_status = "Ativo ✅" if settings.PAPER_TRADING else "Desativado ⚠️"
paper_color = "green" if settings.PAPER_TRADING else "orange"
st.sidebar.markdown(f":{paper_color}[Paper Trading: **{paper_status}**]")

# Inicializar
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
        df = exchange.get_ohlcv(symbol, timeframe, limit=num_candles)
        ticker = exchange.get_ticker(symbol)
        saldo_testnet = exchange.get_usdt_balance()
    
    if not df.empty and ticker:
        # Análise
        signal = strategy.analyze(df)
        current_price = ticker['last']
        
        # SIMULAÇÃO DE LUCRO/PREJUÍZO
        # Calcular quantas moedas compraria com capital inicial
        quantidade = capital_inicial / df['close'].iloc[0]
        valor_atual = quantidade * current_price
        lucro_prejuizo = valor_atual - capital_inicial
        lucro_percent = (lucro_prejuizo / capital_inicial) * 100
        
        # MÉTRICAS PRINCIPAIS - DESTAQUE
        st.markdown("## 💰 SIMULAÇÃO DE INVESTIMENTO")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💵 Investimento Inicial",
                f"${capital_inicial:.2f}",
                f"Comprou {quantidade:.6f} {symbol.replace('USDT', '')}"
            )
        
        with col2:
            st.metric(
                "💎 Valor Atual",
                f"${valor_atual:.2f}",
                f"@ ${current_price:,.2f}"
            )
        
        with col3:
            delta_color = "normal" if lucro_prejuizo >= 0 else "inverse"
            st.metric(
                "📊 Lucro/Prejuízo",
                f"${lucro_prejuizo:+.2f}",
                f"{lucro_percent:+.2f}%",
                delta_color=delta_color
            )
        
        with col4:
            if lucro_prejuizo > 0:
                st.success(f"✅ LUCRO de ${lucro_prejuizo:.2f}!")
            elif lucro_prejuizo < 0:
                st.error(f"❌ PREJUÍZO de ${abs(lucro_prejuizo):.2f}")
            else:
                st.info("➖ Empate")
        
        st.markdown("---")
        
        # Informações de mercado
        st.markdown("## 📊 Mercado Atual")
        
        col1, col2, col3, col4 = st.columns(4)
        
        change_24h = ((ticker['last'] - ticker['open']) / ticker['open']) * 100
        
        with col1:
            st.metric(
                "💰 Preço Atual",
                f"${current_price:,.2f}",
                f"{change_24h:+.2f}% (24h)"
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
                "💵 Saldo Testnet",
                f"${saldo_testnet:,.2f}",
                "Virtual"
            )
        
        with col4:
            vol_24h = ticker.get('baseVolume', 0)
            st.metric(
                "📈 Volume 24h",
                f"{vol_24h:,.0f}",
                f"High: ${ticker['high']:,.2f}"
            )
        
        # Detalhes do sinal
        if signal['confidence'] >= 65:
            if signal['signal'] == 'buy':
                st.success(f"🟢 **OPORTUNIDADE DE COMPRA DETECTADA!**\n\n{signal['reason']}")
            elif signal['signal'] == 'sell':
                st.error(f"🔴 **OPORTUNIDADE DE VENDA DETECTADA!**\n\n{signal['reason']}")
        else:
            st.info(f"ℹ️ **Aguardando melhor momento:** {signal['reason']}")
        
        st.markdown("---")
        
        # Gráfico de preços
        st.markdown("## 📈 Gráfico de Preços")
        
        # Calcular indicadores
        df_copy = strategy.calculate_indicators(df)
        
        # Criar gráfico
        fig = go.Figure()
        
        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=symbol,
            increasing_line_color='#00ff00',
            decreasing_line_color='#ff0000'
        ))
        
        # Bandas de Bollinger (se Mean Reversion)
        if 'bb_middle' in df_copy.columns:
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['bb_upper'],
                name='BB Superior',
                line=dict(color='rgba(255, 0, 0, 0.5)', width=1, dash='dash')
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
                line=dict(color='rgba(0, 255, 0, 0.5)', width=1, dash='dash')
            ))
        
        # EMAs (se Trend Following)
        if 'ema_9' in df_copy.columns:
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['ema_9'],
                name='EMA 9',
                line=dict(color='rgba(255, 0, 255, 0.8)', width=1)
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['ema_21'],
                name='EMA 21',
                line=dict(color='rgba(0, 255, 255, 0.8)', width=1)
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index,
                y=df_copy['ema_50'],
                name='EMA 50',
                line=dict(color='rgba(255, 255, 0, 0.8)', width=2)
            ))
        
        fig.update_layout(
            height=500,
            xaxis_title="Data/Hora",
            yaxis_title="Preço (USDT)",
            hovermode='x unified',
            template='plotly_dark',
            xaxis_rangeslider_visible=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Indicadores e análise
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("## 📊 Indicadores Técnicos")
            
            indicators = signal.get('indicators', {})
            
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
            st.markdown("## 🎯 Análise da Estratégia")
            
            st.write(f"**Estratégia:** {strategy.get_name()}")
            st.write(f"**Sinal:** {signal['signal'].upper()}")
            st.write(f"**Confiança:** {signal['confidence']:.1f}%")
            st.write(f"**Motivo:** {signal['reason']}")
            
            # Barra de progresso
            confidence_color = "green" if signal['confidence'] >= 65 else "orange" if signal['confidence'] >= 40 else "red"
            st.progress(signal['confidence'] / 100, text=f"Confiança: {signal['confidence']:.1f}%")
            
            if signal['confidence'] >= 65:
                st.success("✅ SINAL FORTE - Operação válida!")
            elif signal['confidence'] >= 40:
                st.warning("⚠️ SINAL MODERADO")
            else:
                st.info("ℹ️ Sem sinal - Aguardando...")
        
        # Simulação de Trade
        st.markdown("---")
        st.markdown("## 🧮 SIMULAÇÃO: E Se Comprasse Agora?")
        
        col1, col2, col3 = st.columns(3)
        
        # Calcular potencial
        stop_loss_price = current_price * (1 - settings.STOP_LOSS_PERCENT)
        take_profit_price = current_price * (1 + settings.TAKE_PROFIT_PERCENT)
        
        perda_max = capital_inicial * settings.STOP_LOSS_PERCENT
        ganho_esperado = capital_inicial * settings.TAKE_PROFIT_PERCENT
        
        with col1:
            st.info(f"**Se comprar agora @ ${current_price:,.2f}**")
            st.write(f"Quantidade: {quantidade:.6f} {symbol.replace('USDT', '')}")
        
        with col2:
            st.error(f"**Stop Loss @ ${stop_loss_price:,.2f}**")
            st.write(f"Perda máxima: ${perda_max:.2f} (-{settings.STOP_LOSS_PERCENT*100:.1f}%)")
        
        with col3:
            st.success(f"**Take Profit @ ${take_profit_price:,.2f}**")
            st.write(f"Ganho esperado: ${ganho_esperado:.2f} (+{settings.TAKE_PROFIT_PERCENT*100:.1f}%)")
        
        # Informações 24h
        st.markdown("---")
        st.markdown("## 📉 Estatísticas 24h")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Abertura", f"${ticker['open']:,.2f}")
        
        with col2:
            st.metric("Máxima", f"${ticker['high']:,.2f}")
        
        with col3:
            st.metric("Mínima", f"${ticker['low']:,.2f}")
        
        with col4:
            variacao_24h = ticker['high'] - ticker['low']
            st.metric("Variação 24h", f"${variacao_24h:,.2f}")
        
        # Última atualização
        st.markdown("---")
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        st.caption(f"⏰ Última atualização: {now}")
        
        # Auto-refresh
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    else:
        st.error("❌ Erro ao obter dados do mercado")

except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    
    # Botão para retry
    if st.button("🔄 Tentar Novamente"):
        st.rerun()







