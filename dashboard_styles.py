"""
Estilos CSS Profissionais para Dashboard Auronex
Inspirado em: Binance, TradingView, Bloomberg Terminal
"""

PROFESSIONAL_DARK_THEME = """
<style>
    /* ========================================
       TEMA DARK PROFISSIONAL
    ======================================== */
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 50%, #0f1628 100%);
    }
    
    /* ========================================
       CARDS GLASSMORPHISM
    ======================================== */
    
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(25,30,60,0.7) 0%, 
            rgba(35,40,70,0.7) 100%
        );
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(100,150,255,0.2);
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0,100,255,0.3);
        border-color: rgba(100,150,255,0.5);
    }
    
    /* ========================================
       MÉTRICAS (KPIs)
    ======================================== */
    
    [data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00f5ff 0%, #00a8ff 50%, #0080ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0,245,255,0.3);
        letter-spacing: -1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0aec0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* ========================================
       SIDEBAR PROFISSIONAL
    ======================================== */
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(20,25,45,0.95) 0%, 
            rgba(15,20,40,0.95) 100%
        );
        border-right: 2px solid rgba(100,150,255,0.15);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00d9ff !important;
        font-weight: 700;
        padding: 10px 0;
        border-bottom: 2px solid rgba(0,217,255,0.2);
        margin-bottom: 15px;
    }
    
    /* ========================================
       TÍTULOS E HEADERS
    ======================================== */
    
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
    }
    
    h2 {
        color: #00d9ff !important;
        font-weight: 700 !important;
        border-left: 5px solid #00d9ff;
        padding-left: 15px;
        margin: 30px 0 20px 0;
    }
    
    h3 {
        color: #64b5f6 !important;
        font-weight: 600 !important;
    }
    
    /* ========================================
       TABELAS E DATAFRAMES
    ======================================== */
    
    [data-testid="stDataFrame"] {
        background: rgba(20,25,45,0.6) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(100,150,255,0.2) !important;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] thead tr {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    [data-testid="stDataFrame"] thead th {
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: rgba(100,150,255,0.1) !important;
        transition: all 0.2s;
    }
    
    /* ========================================
       TABS MODERNAS
    ======================================== */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(20,25,45,0.4);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: rgba(40,45,70,0.6);
        border-radius: 10px;
        color: #a0aec0;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(60,65,90,0.8);
        border-color: rgba(100,150,255,0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: rgba(100,150,255,0.5) !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    
    /* ========================================
       INPUTS E SELECTS
    ======================================== */
    
    .stSelectbox, .stMultiselect {
        background: rgba(30,35,60,0.6);
        border-radius: 10px;
    }
    
    .stTextInput input, .stNumberInput input {
        background: rgba(30,35,60,0.8) !important;
        color: white !important;
        border: 1px solid rgba(100,150,255,0.3) !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #00d9ff !important;
        box-shadow: 0 0 15px rgba(0,217,255,0.3) !important;
    }
    
    /* ========================================
       SLIDERS MODERNOS
    ======================================== */
    
    .stSlider {
        padding: 15px 0;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: rgba(100,150,255,0.2);
        border-radius: 10px;
    }
    
    .stSlider [role="slider"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102,126,234,0.5);
        width: 20px !important;
        height: 20px !important;
    }
    
    /* ========================================
       BADGES E ALERTAS
    ======================================== */
    
    .stAlert {
        background: rgba(30,35,60,0.8);
        border-radius: 12px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        border-left-color: #00e676 !important;
        background: rgba(0,230,118,0.1) !important;
    }
    
    .stError {
        border-left-color: #ff1744 !important;
        background: rgba(255,23,68,0.1) !important;
    }
    
    .stWarning {
        border-left-color: #ffc400 !important;
        background: rgba(255,196,0,0.1) !important;
    }
    
    .stInfo {
        border-left-color: #00b0ff !important;
        background: rgba(0,176,255,0.1) !important;
    }
    
    /* ========================================
       GRÁFICOS (PLOTLY)
    ======================================== */
    
    .js-plotly-plot {
        border-radius: 15px;
        background: rgba(20,25,45,0.6);
        padding: 15px;
        border: 1px solid rgba(100,150,255,0.2);
    }
    
    /* ========================================
       RESPONSIVIDADE MOBILE/TABLET
    ======================================== */
    
    /* Tablets (768px - 1024px) */
    @media (max-width: 1024px) {
        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
        }
        
        h1 {
            font-size: 2.5rem !important;
        }
        
        .metric-card {
            padding: 18px;
        }
    }
    
    /* Mobile Landscape (576px - 768px) */
    @media (max-width: 768px) {
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .metric-card {
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* Tabelas scrolláveis em mobile */
        [data-testid="stDataFrame"] {
            overflow-x: auto;
            font-size: 0.85rem !important;
        }
        
        /* Sidebar fecha automático em mobile */
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    
    /* Mobile Portrait (< 576px) */
    @media (max-width: 576px) {
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.2rem !important;
        }
        
        .metric-card {
            padding: 12px;
        }
        
        /* Botões full-width em mobile */
        .stButton button {
            width: 100%;
            padding: 15px !important;
        }
        
        /* Sliders maiores para touch */
        .stSlider [role="slider"] {
            width: 25px !important;
            height: 25px !important;
        }
    }
    
    /* ========================================
       SCROLLBAR CUSTOMIZADA
    ======================================== */
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20,25,45,0.4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* ========================================
       ANIMAÇÕES SUTIS
    ======================================== */
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* ========================================
       STATUS INDICATORS
    ======================================== */
    
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00e676;
        border-radius: 50%;
        box-shadow: 0 0 10px #00e676;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
"""

