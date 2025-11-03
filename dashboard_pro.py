"""
RoboTrader - Dashboard PROFISSIONAL com Perfis Predefinidos
Execute com: streamlit run dashboard_pro.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy, TrendFollowingStrategy
from config.settings import Settings

# Configurar página
st.set_page_config(
    page_title="RoboTrader Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# PERFIS DE TRADING PREDEFINIDOS
PERFIS = {
    "🏦 Hedge Fund (Conservador)": {
        "timeframe": "1h",
        "stop_loss": 0.02,      # 2%
        "take_profit": 0.04,    # 4%
        "confidence": 70,
        "update_interval": 120,  # 2 minutos
        "position_size": 0.05,   # 5%
        "description": """
        **Perfil Conservador**
        
        - Timeframe: 1 hora (visão macro)
        - Stop Loss: 2% (proteção moderada)
        - Take Profit: 4% (objetivos maiores)
        - Confiança mínima: 70% (muito seletivo)
        - Trades/dia: 1-2
        - Risco: BAIXO
        - Retorno esperado: +5-10% ao mês
        
        ✅ Ideal para: Iniciantes, capital grande, baixo estresse
        ❌ Evitar: Quem quer ganhos rápidos
        """
    },
    "📈 Day Trader (Moderado)": {
        "timeframe": "15m",
        "stop_loss": 0.015,     # 1.5%
        "take_profit": 0.03,    # 3%
        "confidence": 60,
        "update_interval": 60,   # 1 minuto
        "position_size": 0.10,   # 10%
        "description": """
        **Perfil Moderado - ATUAL**
        
        - Timeframe: 15 minutos (balanceado)
        - Stop Loss: 1.5% (proteção boa)
        - Take Profit: 3% (realista)
        - Confiança mínima: 60% (seletivo)
        - Trades/dia: 2-5
        - Risco: MÉDIO
        - Retorno esperado: +10-20% ao mês
        
        ✅ Ideal para: Maioria dos traders, equilíbrio
        ❌ Evitar: Impacientes
        """
    },
    "⚡ Scalper (Agressivo)": {
        "timeframe": "5m",
        "stop_loss": 0.01,      # 1%
        "take_profit": 0.02,    # 2%
        "confidence": 55,
        "update_interval": 30,   # 30 segundos
        "position_size": 0.15,   # 15%
        "description": """
        **Perfil Agressivo - Scalping**
        
        - Timeframe: 5 minutos (rápido)
        - Stop Loss: 1% (proteção apertada)
        - Take Profit: 2% (objetivos rápidos)
        - Confiança mínima: 55% (moderado)
        - Trades/dia: 8-15
        - Risco: ALTO
        - Retorno esperado: +15-30% ao mês
        
        ✅ Ideal para: Traders experientes, quer ação
        ❌ Evitar: Iniciantes, conexão instável
        """
    },
    "🚀 Ultra Scalper (Muito Agressivo)": {
        "timeframe": "1m",
        "stop_loss": 0.005,     # 0.5%
        "take_profit": 0.01,    # 1%
        "confidence": 50,
        "update_interval": 10,   # 10 segundos
        "position_size": 0.20,   # 20%
        "description": """
        **Perfil Muito Agressivo - Ultra Scalping**
        
        - Timeframe: 1 minuto (ultra rápido)
        - Stop Loss: 0.5% (muito apertado)
        - Take Profit: 1% (ganhos pequenos frequentes)
        - Confiança mínima: 50% (aceita mais sinais)
        - Trades/dia: 20-50
        - Risco: MUITO ALTO
        - Retorno esperado: +20-50% ao mês (ou -20%)
        
        ✅ Ideal para: Profissionais, bots 24/7, gosta de risco
        ❌ Evitar: Iniciantes, capital pequeno
        """
    }
}

# Título
st.title("🤖 RoboTrader Pro - Dashboard Avançado")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações de Trading")

# PERFIL PREDEFINIDO
perfil_escolhido = st.sidebar.selectbox(
    "🎯 Perfil de Trading",
    list(PERFIS.keys()),
    index=1,  # Day Trader como padrão
    help="Escolha o perfil que define automaticamente todas as configurações"
)

# Mostrar descrição do perfil
with st.sidebar.expander("ℹ️ Sobre este Perfil", expanded=False):
    st.markdown(PERFIS[perfil_escolhido]["description"])

# Pegar configurações do perfil
config_perfil = PERFIS[perfil_escolhido]

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Configurações Aplicadas")
st.sidebar.info(f"""
**Timeframe:** {config_perfil['timeframe']}  
**Stop Loss:** {config_perfil['stop_loss']*100}%  
**Take Profit:** {config_perfil['take_profit']*100}%  
**Confiança Min:** {config_perfil['confidence']}%  
**Update:** {config_perfil['update_interval']}s  
**Position Size:** {config_perfil['position_size']*100}%
""")

st.sidebar.markdown("---")

# Capital inicial
capital_inicial = st.sidebar.number_input(
    "💵 Capital Inicial (USDT)",
    min_value=10.0,
    max_value=100000.0,
    value=10.0,
    step=10.0,
    help="Quanto você investiria (simulação)"
)

# Símbolo
symbol = st.sidebar.selectbox(
    "💰 Símbolo",
    ["ETHUSDT", "BTCUSDT", "BNBUSDT", "SOLUSDT"],
    help="Par de trading"
)

# Estratégia
strategy_name = st.sidebar.selectbox(
    "🎯 Estratégia",
    ["mean_reversion", "trend_following"],
    help="Mean Reversion = mercados laterais | Trend Following = mercados em tendência"
)

# Auto-refresh
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Status do Sistema")

settings = Settings()
mode = "TESTNET 🧪" if settings.USE_TESTNET else "PRODUCAO ⚠️"
paper = "Ativo (Simulação)" if settings.PAPER_TRADING else "DESATIVADO (Real!)"

st.sidebar.success(f"**Modo:** {mode}")
if settings.PAPER_TRADING:
    st.sidebar.info(f"**Paper Trading:** {paper}")
else:
    st.sidebar.warning(f"**Paper Trading:** {paper}")

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
    
    # Obter dados usando configurações do perfil
    with st.spinner("🔄 Carregando dados do mercado..."):
        df = exchange.get_ohlcv(symbol, config_perfil['timeframe'], limit=200)
        ticker = exchange.get_ticker(symbol)
        saldo_testnet = exchange.get_usdt_balance()
    
    if not df.empty and ticker:
        # Análise
        signal = strategy.analyze(df)
        current_price = ticker['last']
        
        # SIMULAÇÃO DE LUCRO/PREJUÍZO
        preco_inicial = df['close'].iloc[0]
        quantidade = capital_inicial / preco_inicial
        valor_atual = quantidade * current_price
        lucro_prejuizo = valor_atual - capital_inicial
        lucro_percent = (lucro_prejuizo / capital_inicial) * 100
        
        # ========================================
        # SEÇÃO 1: SIMULAÇÃO DE INVESTIMENTO
        # ========================================
        st.markdown("## 💰 SIMULAÇÃO DE INVESTIMENTO")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💵 Investimento",
                f"${capital_inicial:.2f}",
                f"{quantidade:.6f} {symbol.replace('USDT', '')}"
            )
        
        with col2:
            st.metric(
                "💎 Valor Atual",
                f"${valor_atual:.2f}",
                f"@ ${current_price:,.2f}"
            )
        
        with col3:
            st.metric(
                "📊 P&L Total",
                f"${lucro_prejuizo:+.2f}",
                f"{lucro_percent:+.2f}%",
                delta_color="normal" if lucro_prejuizo >= 0 else "inverse"
            )
        
        with col4:
            if lucro_prejuizo > 0:
                st.success(f"✅ LUCRO!\n${lucro_prejuizo:.2f}")
            elif lucro_prejuizo < 0:
                st.error(f"❌ PREJUÍZO\n${abs(lucro_prejuizo):.2f}")
            else:
                st.info("➖ Neutro\n$0.00")
        
        st.markdown("---")
        
        # ========================================
        # SEÇÃO 2: MERCADO E SINAL
        # ========================================
        st.markdown("## 📊 Mercado e Análise")
        
        col1, col2, col3, col4 = st.columns(4)
        
        change_24h = ((ticker['last'] - ticker['open']) / ticker['open']) * 100
        
        with col1:
            st.metric(
                "💰 Preço Atual",
                f"${current_price:,.2f}",
                f"{change_24h:+.2f}% (24h)"
            )
        
        with col2:
            signal_text = {
                'buy': '🟢 COMPRAR',
                'sell': '🔴 VENDER',
                'hold': '⚪ AGUARDAR'
            }.get(signal['signal'], 'HOLD')
            
            st.metric(
                "🎯 Sinal Atual",
                signal_text,
                f"{signal['confidence']:.0f}% confiança"
            )
        
        with col3:
            st.metric(
                "💵 Saldo Testnet",
                f"${saldo_testnet:,.0f}",
                "Dinheiro Virtual"
            )
        
        with col4:
            vol_24h = ticker.get('baseVolume', 0)
            st.metric(
                "📈 Volume 24h",
                f"{vol_24h:,.0f}",
                symbol.replace('USDT', '')
            )
        
        # Alerta de sinal
        if signal['confidence'] >= config_perfil['confidence']:
            if signal['signal'] == 'buy':
                st.success(f"🟢 **OPORTUNIDADE DE COMPRA!** (Confiança: {signal['confidence']:.1f}%)\n\n📝 {signal['reason']}")
            elif signal['signal'] == 'sell':
                st.error(f"🔴 **OPORTUNIDADE DE VENDA!** (Confiança: {signal['confidence']:.1f}%)\n\n📝 {signal['reason']}")
        else:
            st.info(f"ℹ️ **Aguardando melhor momento** (Confiança: {signal['confidence']:.1f}%)\n\n📝 {signal['reason']}")
        
        st.markdown("---")
        
        # ========================================
        # SEÇÃO 3: GRÁFICO
        # ========================================
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
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ))
        
        # Indicadores baseados na estratégia
        if 'bb_middle' in df_copy.columns:
            fig.add_trace(go.Scatter(
                x=df_copy.index, y=df_copy['bb_upper'],
                name='BB Superior', line=dict(color='rgba(255, 82, 82, 0.6)', width=1, dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index, y=df_copy['bb_middle'],
                name='BB Média', line=dict(color='rgba(255, 235, 59, 0.9)', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index, y=df_copy['bb_lower'],
                name='BB Inferior', line=dict(color='rgba(76, 175, 80, 0.6)', width=1, dash='dash')
            ))
        
        if 'ema_9' in df_copy.columns:
            fig.add_trace(go.Scatter(
                x=df_copy.index, y=df_copy['ema_9'],
                name='EMA 9', line=dict(color='rgba(156, 39, 176, 0.8)', width=1)
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index, y=df_copy['ema_21'],
                name='EMA 21', line=dict(color='rgba(3, 169, 244, 0.8)', width=1)
            ))
            fig.add_trace(go.Scatter(
                x=df_copy.index, y=df_copy['ema_50'],
                name='EMA 50', line=dict(color='rgba(255, 193, 7, 0.9)', width=2)
            ))
        
        fig.update_layout(
            height=550,
            xaxis_title="Data/Hora",
            yaxis_title="Preço (USDT)",
            hovermode='x unified',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ========================================
        # SEÇÃO 4: SIMULAÇÃO DE TRADE
        # ========================================
        st.markdown("---")
        st.markdown("## 🧮 SE COMPRASSE AGORA...")
        
        col1, col2, col3 = st.columns(3)
        
        # Calcular com configurações do perfil
        stop_loss_price = current_price * (1 - config_perfil['stop_loss'])
        take_profit_price = current_price * (1 + config_perfil['take_profit'])
        
        valor_compra = capital_inicial * config_perfil['position_size']
        qty_compra = valor_compra / current_price
        
        perda_max = valor_compra * config_perfil['stop_loss']
        ganho_esperado = valor_compra * config_perfil['take_profit']
        
        with col1:
            st.info(f"""
            **💰 Compra**
            
            Preço: ${current_price:,.2f}  
            Valor: ${valor_compra:.2f}  
            Qtd: {qty_compra:.6f} {symbol.replace('USDT', '')}
            """)
        
        with col2:
            st.error(f"""
            **🛑 Stop Loss**
            
            Preço: ${stop_loss_price:,.2f}  
            Perda: ${perda_max:.2f}  
            Percentual: -{config_perfil['stop_loss']*100}%
            """)
        
        with col3:
            st.success(f"""
            **🎯 Take Profit**
            
            Preço: ${take_profit_price:,.2f}  
            Ganho: ${ganho_esperado:.2f}  
            Percentual: +{config_perfil['take_profit']*100}%
            """)
        
        # Relação Risco/Recompensa
        risco_recompensa = config_perfil['take_profit'] / config_perfil['stop_loss']
        
        st.markdown(f"""
        **⚖️ Relação Risco/Recompensa:** 1:{risco_recompensa:.1f}  
        *(Para cada $1 arriscado, pode ganhar ${risco_recompensa:.2f})*
        """)
        
        # ========================================
        # SEÇÃO 5: INDICADORES E ANÁLISE
        # ========================================
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Indicadores Técnicos")
            
            indicators = signal.get('indicators', {})
            
            # Formatar indicadores
            ind_formatted = []
            for key, value in indicators.items():
                if isinstance(value, (int, float)):
                    # Colorir RSI
                    if key == 'rsi':
                        if value < 30:
                            color = "🟢 Sobrevendido"
                        elif value > 70:
                            color = "🔴 Sobrecomprado"
                        else:
                            color = "⚪ Neutro"
                        ind_formatted.append({
                            'Indicador': 'RSI',
                            'Valor': f"{value:.1f}",
                            'Status': color
                        })
                    else:
                        ind_formatted.append({
                            'Indicador': key.replace('_', ' ').title(),
                            'Valor': f"{value:.2f}",
                            'Status': '-'
                        })
            
            if ind_formatted:
                st.dataframe(
                    pd.DataFrame(ind_formatted),
                    hide_index=True,
                    use_container_width=True
                )
        
        with col2:
            st.markdown("### 🎯 Análise Atual")
            
            st.write(f"**Estratégia:** {strategy.get_name()}")
            st.write(f"**Perfil:** {perfil_escolhido}")
            st.write(f"**Timeframe:** {config_perfil['timeframe']}")
            st.write(f"**Sinal:** {signal['signal'].upper()}")
            
            # Barra de confiança
            st.progress(
                signal['confidence'] / 100,
                text=f"Confiança: {signal['confidence']:.1f}%"
            )
            
            st.write(f"**Análise:** {signal['reason']}")
            
            # Status operacional
            if signal['confidence'] >= config_perfil['confidence']:
                st.success("✅ Sinal VÁLIDO para operar!")
            else:
                st.info(f"⏳ Aguardando confiança >= {config_perfil['confidence']}%")
        
        # ========================================
        # SEÇÃO 6: INFO 24H
        # ========================================
        st.markdown("---")
        st.markdown("### 📉 Estatísticas 24 Horas")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Abertura", f"${ticker['open']:,.2f}")
        
        with col2:
            st.metric("Máxima", f"${ticker['high']:,.2f}")
        
        with col3:
            st.metric("Mínima", f"${ticker['low']:,.2f}")
        
        with col4:
            variacao = ticker['high'] - ticker['low']
            st.metric("Amplitude", f"${variacao:,.2f}")
        
        with col5:
            vol_pct = (change_24h / 100) if change_24h != 0 else 0
            st.metric("Variação", f"{change_24h:+.2f}%")
        
        # Footer
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.caption(f"⏰ Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        with col2:
            if st.button("🔄 Atualizar Agora"):
                st.rerun()
        
        # Auto-refresh
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    else:
        st.error("❌ Erro ao obter dados do mercado")
        if st.button("🔄 Tentar Novamente"):
            st.rerun()

except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    st.exception(e)
    if st.button("🔄 Recarregar"):
        st.rerun()







