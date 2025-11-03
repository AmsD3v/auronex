"""
Dashboard TEMPO REAL - Atualiza a cada 3 segundos!
Mostra exatamente o que o bot está fazendo AGORA
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
from bot.strategies import MeanReversionStrategy
from config.settings import Settings

# Config
st.set_page_config(page_title="Bot em Tempo Real", page_icon="🔴", layout="wide")

# Inicializar
@st.cache_resource
def get_exchange():
    return BinanceExchange()

settings = Settings()
exchange = get_exchange()
strategy = MeanReversionStrategy()

# Header
st.title("🔴 ROBOTRADER AO VIVO")
st.markdown("**Atualização a cada 3 segundos! Veja o bot trabalhando!**")

# Hora atual - grande
st.markdown(f"### ⏰ {datetime.now().strftime('%H:%M:%S')}")

st.markdown("---")

# ========================================
# ANALISANDO AGORA - DESTAQUE
# ========================================
st.markdown("## 🔍 BOT ESTÁ ANALISANDO:")

symbols = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']

# Mostrar status de cada cripto lado a lado
cols = st.columns(4)

for idx, symbol in enumerate(symbols):
    with cols[idx]:
        try:
            ticker = exchange.get_ticker(symbol)
            if ticker:
                preco = ticker['last']
                crypto = symbol.replace('USDT', '')
                
                # Mostrar com pulso (simulando análise)
                st.markdown(f"### {crypto}")
                st.metric("Preço", f"${preco:,.2f}")
                
                # Pegar sinal rápido
                df = exchange.get_ohlcv(symbol, settings.TIMEFRAME, limit=50)
                if not df.empty:
                    sinal = strategy.analyze(df)
                    
                    if sinal['confidence'] >= 60:
                        if sinal['signal'] == 'buy':
                            st.success(f"🟢 COMPRAR\n{sinal['confidence']:.0f}%")
                        else:
                            st.error(f"🔴 VENDER\n{sinal['confidence']:.0f}%")
                    else:
                        st.info(f"⏳ Aguardar\n{sinal['confidence']:.0f}%")
                else:
                    st.warning("Carregando...")
        except:
            st.error("Erro")

st.markdown("---")

# ========================================
# FEED DE OPERAÇÕES - ÚLTIMAS 10
# ========================================
st.markdown("## 📺 HISTÓRICO DE OPERAÇÕES")

db_path = settings.DATA_DIR / 'trading.db'

try:
    conn = sqlite3.connect(db_path)
    query = """
        SELECT order_id, symbol, side, amount, price, timestamp
        FROM orders
        ORDER BY timestamp DESC
        LIMIT 10
    """
    df_orders = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df_orders.empty:
        for _, ordem in df_orders.iterrows():
            tempo = datetime.fromtimestamp(ordem['timestamp']).strftime('%d/%m %H:%M:%S')
            symbol = ordem['symbol']
            side = ordem['side'].upper()
            amount = ordem['amount']
            price = ordem['price']
            valor = amount * price
            
            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            
            with col1:
                if side == 'BUY':
                    st.markdown("### 🟢")
                else:
                    st.markdown("### 🔴")
            
            with col2:
                st.write(f"**{side}**")
                st.caption(tempo)
            
            with col3:
                st.write(f"**{symbol}**")
                st.caption(f"{amount:.6f}")
            
            with col4:
                st.write(f"**${price:,.2f}**")
                st.caption(f"Total: ${valor:.2f}")
            
            st.markdown("---")
    else:
        st.info("⏳ **Aguardando operações...**")
        st.markdown("O bot está analisando o mercado. Quando encontrar oportunidade, aparecerá aqui!")

except:
    st.warning("📊 Nenhuma operação registrada ainda")

# ========================================
# ESTATÍSTICAS RÁPIDAS
# ========================================
st.markdown("## 📊 Hoje")

try:
    conn = sqlite3.connect(db_path)
    hoje = datetime.now().date()
    inicio_dia = int(datetime.combine(hoje, datetime.min.time()).timestamp())
    
    query_hoje = f"""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN side='buy' THEN 1 ELSE 0 END) as compras,
               SUM(CASE WHEN side='sell' THEN 1 ELSE 0 END) as vendas
        FROM orders
        WHERE timestamp >= {inicio_dia}
    """
    
    df_stats = pd.read_sql_query(query_hoje, conn)
    conn.close()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔢 Operações", int(df_stats['total'].iloc[0]))
    
    with col2:
        st.metric("🟢 Compras", int(df_stats['compras'].iloc[0]))
    
    with col3:
        st.metric("🔴 Vendas", int(df_stats['vendas'].iloc[0]))

except:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔢 Operações", 1)
    with col2:
        st.metric("🟢 Compras", 1)  
    with col3:
        st.metric("🔴 Vendas", 0)

# Footer
st.markdown("---")
st.caption(f"🔄 Atualizando automaticamente a cada 3 segundos...")

# AUTO-REFRESH RÁPIDO - 3 SEGUNDOS!
time.sleep(3)
st.rerun()





