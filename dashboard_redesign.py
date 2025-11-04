"""
Dashboard Auronex - Layout Minimalista Profissional
Versão 2.0 - Clean, Intuitivo, Bonito
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# Config
st.set_page_config(
    page_title="Auronex · Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar minimizada por padrão
)

# ========================================
# ESTILO MINIMALISTA PREMIUM
# ========================================

st.markdown("""
<style>
    /* Reset e Base */
    .stApp {
        background: #0a0e1a;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Container Principal */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Header Minimalista */
    .header-container {
        background: linear-gradient(135deg, rgba(15,20,40,0.6), rgba(25,30,50,0.6));
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Cards Flutuantes */
    .floating-card {
        background: linear-gradient(135deg, 
            rgba(20,25,45,0.4) 0%, 
            rgba(30,35,60,0.4) 100%
        );
        backdrop-filter: blur(30px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.05);
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
    
    [data-testid="stMetricDelta"] {
        font-size: 0.95rem !important;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(0,230,118,0.1);
    }
    
    /* Sidebar Minimalista */
    [data-testid="stSidebar"] {
        background: rgba(10,15,30,0.98);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
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
    
    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #cbd5e0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
    }
    
    /* Dividers Sutis */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255,255,255,0.1) 50%, 
            transparent 100%
        );
        margin: 2rem 0;
    }
    
    /* Tabs Ultra Clean */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        padding: 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background: transparent;
        border-radius: 0;
        color: #718096;
        font-weight: 500;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 0 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.03);
        color: #cbd5e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #ffffff !important;
        border-bottom-color: #00d9ff !important;
    }
    
    /* Tabelas Clean */
    [data-testid="stDataFrame"] {
        background: transparent !important;
        border: none !important;
    }
    
    [data-testid="stDataFrame"] table {
        border-collapse: separate;
        border-spacing: 0 4px;
    }
    
    [data-testid="stDataFrame"] thead {
        display: none;
    }
    
    [data-testid="stDataFrame"] tbody tr {
        background: rgba(20,25,45,0.3);
        transition: all 0.2s;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: rgba(30,35,60,0.5);
        transform: scale(1.01);
    }
    
    [data-testid="stDataFrame"] td {
        border: none !important;
        padding: 12px 16px !important;
        color: #e2e8f0 !important;
    }
    
    /* Inputs Minimalistas */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(30,35,60,0.4) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
        transition: all 0.3s;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: rgba(0,217,255,0.5) !important;
        box-shadow: 0 0 0 3px rgba(0,217,255,0.1) !important;
    }
    
    /* Sliders Ultra Clean */
    .stSlider {
        padding: 20px 0;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: rgba(255,255,255,0.05);
    }
    
    .stSlider [data-baseweb="slider-track-fill"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .stSlider [role="slider"] {
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        width: 18px !important;
        height: 18px !important;
    }
    
    /* Botões Minimalistas */
    .stButton button {
        background: rgba(255,255,255,0.06);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(100,150,255,0.3);
        transform: translateY(-1px);
    }
    
    /* Alertas Sutis */
    .stAlert {
        background: rgba(30,35,60,0.4);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    /* Success Verde */
    .stSuccess {
        background: rgba(0,230,118,0.08) !important;
        border-left: 3px solid #00e676;
        color: #81e6d9 !important;
    }
    
    /* Error Vermelho */
    .stError {
        background: rgba(255,23,68,0.08) !important;
        border-left: 3px solid #ff1744;
        color: #fc8181 !important;
    }
    
    /* Warning Amarelo */
    .stWarning {
        background: rgba(255,196,0,0.08) !important;
        border-left: 3px solid #ffc400;
        color: #f6e05e !important;
    }
    
    /* Info Azul */
    .stInfo {
        background: rgba(0,176,255,0.08) !important;
        border-left: 3px solid #00b0ff;
        color: #90cdf4 !important;
    }
    
    /* Gráficos */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
    }
    
    /* Scrollbar Ultra Thin */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.2);
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
    }
    
    /* Animação de Entrada */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: slideUp 0.4s ease-out;
    }
    
    /* Remove elementos Streamlit padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ========================================
# LOGIN (PREVIEW MODE - PULAR PARA VER LAYOUT)
# ========================================

if 'access_token' not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 100px;'>Auronex</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #718096; margin-bottom: 40px;'>Trading Platform · Preview</p>", unsafe_allow_html=True)
        
        # MODO PREVIEW - Pular login
        if st.button("👁️ Ver Preview do Layout", use_container_width=True):
            st.session_state.access_token = "preview_token"
            st.session_state.user_email = "preview@auronex.com"
            st.rerun()
        
        st.markdown("<p style='text-align: center; color: #4a5568; font-size: 0.85rem; margin-top: 20px;'>Modo preview - Sem autenticação</p>", unsafe_allow_html=True)
    
    st.stop()

# ========================================
# HEADER CLEAN
# ========================================

col_logo, col_saldo, col_lucro, col_user = st.columns([2, 2, 2, 1])

with col_logo:
    st.markdown("""
    <div style='padding: 20px 0;'>
        <h1 style='margin: 0; font-size: 1.8rem; font-weight: 600;'>Auronex</h1>
        <p style='color: #718096; margin: 0; font-size: 0.85rem;'>Trading Platform</p>
    </div>
    """, unsafe_allow_html=True)

with col_saldo:
    try:
        # Buscar saldo real
        saldo_total = 100  # Placeholder
        st.metric("Saldo Total", f"R$ {saldo_total:,.2f}", "+5.2%")
    except:
        st.metric("Saldo Total", "R$ 0,00")

with col_lucro:
    st.metric("Lucro Hoje", "R$ +45,30", "+12.5%")

with col_user:
    if st.button("⚙️", help="Configurações"):
        st.session_state.show_settings = True

st.markdown("<hr style='margin: 1rem 0; opacity: 0.1;'>", unsafe_allow_html=True)

# ========================================
# NAVEGAÇÃO POR CARDS (DASHBOARD PRINCIPAL)
# ========================================

st.markdown("## Overview")

# KPIs Principais em Grid
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
    <div class='floating-card' style='text-align: center;'>
        <div style='font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>Bots Ativos</div>
        <div style='font-size: 3rem; font-weight: 300; color: #00e676; margin-bottom: 8px;'>3</div>
        <div style='font-size: 0.85rem; color: #90cdf4;'>de 10 total</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class='floating-card' style='text-align: center;'>
        <div style='font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>Trades Hoje</div>
        <div style='font-size: 3rem; font-weight: 300; color: #00d9ff; margin-bottom: 8px;'>12</div>
        <div style='font-size: 0.85rem; color: #90cdf4;'>↑ 8 vs ontem</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class='floating-card' style='text-align: center;'>
        <div style='font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>Win Rate</div>
        <div style='font-size: 3rem; font-weight: 300; color: #ffc400; margin-bottom: 8px;'>68%</div>
        <div style='font-size: 0.85rem; color: #90cdf4;'>+3% semana</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class='floating-card' style='text-align: center;'>
        <div style='font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>P&L Mês</div>
        <div style='font-size: 3rem; font-weight: 300; color: #00e676; margin-bottom: 8px;'>+18%</div>
        <div style='font-size: 0.85rem; color: #90cdf4;'>R$ 1,234</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========================================
# GRID PRINCIPAL - 2 COLUNAS
# ========================================

col_main, col_side = st.columns([2, 1])

with col_main:
    # Gráfico Principal
    st.markdown("## Performance")
    
    # Placeholder gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[100, 120, 115, 130, 145],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#00d9ff', width=3),
        fillcolor='rgba(0,217,255,0.1)'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # TOP 5 Minimalista
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Top Oportunidades")
    
    top5_data = {
        'Crypto': ['BTC', 'ETH', 'SOL', 'BNB', 'ADA'],
        'Preço': ['R$ 350.234', 'R$ 18.567', 'R$ 912', 'R$ 3.145', 'R$ 2.87'],
        '24h': ['+2.5%', '+5.3%', '+12.1%', '+3.8%', '+8.2%']
    }
    
    df_top5 = pd.DataFrame(top5_data)
    st.dataframe(df_top5, hide_index=True, use_container_width=True)

with col_side:
    # Bots Ativos Card
    st.markdown("## Bots Ativos")
    
    st.markdown("""
    <div class='floating-card'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;'>
            <div>
                <div style='font-size: 0.85rem; color: #718096;'>Bot Binance</div>
                <div style='font-size: 1.1rem; font-weight: 600; color: white;'>Mean Reversion</div>
            </div>
            <div style='width: 40px; height: 40px; background: linear-gradient(135deg, #00e676, #00c853); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>ON</div>
        </div>
        <div style='display: flex; justify-content: space-between; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05);'>
            <div style='text-align: center;'>
                <div style='font-size: 0.75rem; color: #718096;'>Trades</div>
                <div style='font-size: 1.2rem; color: #00d9ff; font-weight: 600;'>8</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 0.75rem; color: #718096;'>P&L</div>
                <div style='font-size: 1.2rem; color: #00e676; font-weight: 600;'>+R$ 87</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## Ações Rápidas")
    
    if st.button("➕ Criar Novo Bot", use_container_width=True):
        st.info("Redirecionando...")
    
    if st.button("📊 Ver Relatório", use_container_width=True):
        st.info("Gerando relatório...")
    
    if st.button("⚙️ Configurações", use_container_width=True):
        st.info("Abrindo configurações...")

# ========================================
# FOOTER CLEAN
# ========================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 40px 0; color: #4a5568; font-size: 0.85rem;'>
    <p>Auronex Trading Platform · v2.0</p>
    <p style='font-size: 0.75rem; margin-top: 8px;'>Sistema operando 24/7 · Última atualização: 3 nov 2025</p>
</div>
""", unsafe_allow_html=True)

