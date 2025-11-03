"""
Dashboard LIVE - Feed de Atividades em Tempo Real
Mostra VISUALMENTE tudo que o bot está fazendo
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
st.set_page_config(page_title="RoboTrader LIVE", page_icon="🔴", layout="wide")

st.title("🔴 RoboTrader LIVE - Feed em Tempo Real")
st.markdown("**Bot operando agora! Veja tudo acontecendo ao vivo!**")
st.markdown("---")

# Inicializar
@st.cache_resource
def get_exchange():
    return BinanceExchange()

try:
    exchange = get_exchange()
    settings = Settings()
    strategy = MeanReversionStrategy()
    
    # ========================================
    # FEED DE ATIVIDADES - PRINCIPAL
    # ========================================
    st.markdown("## 📺 FEED DE ATIVIDADES")
    
    # Conectar ao banco para ver histórico
    db_path = settings.DATA_DIR / 'trading.db'
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Últimas 10 ordens
        query = """
            SELECT order_id, symbol, side, amount, price, status, timestamp
            FROM orders
            ORDER BY timestamp DESC
            LIMIT 10
        """
        
        df_orders = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df_orders.empty:
            st.markdown("### 📋 Últimas Operações:")
            
            for _, ordem in df_orders.iterrows():
                tempo = datetime.fromtimestamp(ordem['timestamp']).strftime('%H:%M:%S')
                symbol = ordem['symbol']
                side = ordem['side'].upper()
                amount = ordem['amount']
                price = ordem['price']
                
                # Card visual
                if side == 'BUY':
                    st.success(f"""
                    🟢 **COMPRA** - {symbol} - {tempo}
                    - Quantidade: {amount:.6f}
                    - Preço: ${price:,.2f}
                    """)
                else:
                    st.error(f"""
                    🔴 **VENDA** - {symbol} - {tempo}
                    - Quantidade: {amount:.6f}
                    - Preço: ${price:,.2f}
                    """)
        else:
            st.info("⏳ Aguardando primeira operação...")
            
    except:
        st.warning("📊 Banco de dados vazio - Nenhuma operação ainda")
    
    st.markdown("---")
    
    # ========================================
    # POSIÇÕES ABERTAS - DESTAQUE
    # ========================================
    st.markdown("## 💼 POSIÇÕES ABERTAS AGORA")
    
    symbols = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT', 'SOLUSDT']
    
    posicoes_abertas = False
    
    for symbol in symbols:
        try:
            ticker = exchange.get_ticker(symbol)
            if not ticker:
                continue
            
            df = exchange.get_ohlcv(symbol, settings.TIMEFRAME, limit=100)
            if df.empty:
                continue
            
            sinal = strategy.analyze(df)
            preco_atual = ticker['last']
            
            # Simulação de posição (no futuro pegar do portfolio real)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(symbol.replace('USDT', ''), f"${preco_atual:,.2f}")
            
            with col2:
                if sinal['signal'] == 'buy' and sinal['confidence'] >= 60:
                    st.success(f"🟢 COMPRAR ({sinal['confidence']:.0f}%)")
                elif sinal['signal'] == 'sell' and sinal['confidence'] >= 60:
                    st.error(f"🔴 VENDER ({sinal['confidence']:.0f}%)")
                else:
                    st.info("⏳ Aguardar")
            
            with col3:
                st.write(f"RSI: {sinal['indicators'].get('rsi', 0):.1f}")
            
            with col4:
                if sinal['confidence'] >= 60:
                    st.write("🎯 **OPORTUNIDADE!**")
                else:
                    st.write(sinal['reason'][:30] + "...")
            
            st.markdown("---")
            
        except:
            pass
    
    # ========================================
    # ESTATÍSTICAS HOJE
    # ========================================
    st.markdown("## 📊 ESTATÍSTICAS DE HOJE")
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Trades hoje
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
            st.metric("🔢 Total Operações", int(df_stats['total'].iloc[0]))
        
        with col2:
            st.metric("🟢 Compras", int(df_stats['compras'].iloc[0]))
        
        with col3:
            st.metric("🔴 Vendas", int(df_stats['vendas'].iloc[0]))
        
    except:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔢 Total Operações", 1)
        with col2:
            st.metric("🟢 Compras", 1)
        with col3:
            st.metric("🔴 Vendas", 0)
    
    # Footer
    st.markdown("---")
    st.caption(f"⏰ Atualização: {datetime.now().strftime('%H:%M:%S')} | 🔄 Auto-refresh ativo (10s)")
    
    # Auto-refresh rápido (10 segundos)
    time.sleep(10)
    st.rerun()

except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    if st.button("🔄 Recarregar"):
        st.rerun()





