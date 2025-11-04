#!/bin/bash
# ========================================
# AURONEX - INICIAR SERVIDOR XUBUNTU
# ========================================
# Script para iniciar todos os serviços do Auronex
# Autor: Claude Sonnet 4.5
# Data: 04/11/2025

clear
echo "========================================"
echo "  AURONEX - INICIANDO SERVIDOR"
echo "========================================"
echo ""
echo "Iniciando 3 serviços:"
echo "  1. FastAPI + Bot Controller (porta 8001)"
echo "  2. Streamlit Dashboard (porta 8501)"
echo "  3. Cloudflare Tunnel (HTTPS global)"
echo ""
echo "⚠️  ATENÇÃO: Mantenha esta janela ABERTA!"
echo ""
echo "========================================"
echo ""

# Ir para pasta do projeto
cd /home/serverhome/auronex

# ========================================
# 1. FASTAPI + BOT CONTROLLER
# ========================================

echo "1️⃣  Iniciando FastAPI + Bot Controller..."
echo ""

# Abrir em novo terminal
gnome-terminal --title="FastAPI + Bot Controller" -- bash -c "
cd /home/serverhome/auronex
source venv/bin/activate
echo '========================================';
echo '  FASTAPI + BOT CONTROLLER';
echo '========================================';
echo '';
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001;
exec bash
" &

sleep 5

# ========================================
# 2. STREAMLIT DASHBOARD
# ========================================

echo "2️⃣  Iniciando Streamlit Dashboard..."
echo ""

# Abrir em novo terminal
gnome-terminal --title="Streamlit Dashboard" -- bash -c "
cd /home/serverhome/auronex
source venv/bin/activate
echo '========================================';
echo '  STREAMLIT DASHBOARD';
echo '========================================';
echo '';
streamlit run dashboard_streamlit_fastapi.py --server.port 8501 --server.address 0.0.0.0 --server.headless true;
exec bash
" &

sleep 5

# ========================================
# 3. CLOUDFLARE TUNNEL
# ========================================

echo "3️⃣  Iniciando Cloudflare Tunnel..."
echo ""

# Abrir em novo terminal
gnome-terminal --title="Cloudflare Tunnel" -- bash -c "
echo '========================================';
echo '  CLOUDFLARE TUNNEL';
echo '========================================';
echo '';
cloudflared tunnel run auronex;
exec bash
" &

sleep 3

# ========================================
# FINALIZAÇÃO
# ========================================

echo ""
echo "========================================"
echo "  ✅ TODOS OS SERVIÇOS INICIADOS!"
echo "========================================"
echo ""
echo "3 terminais foram abertos:"
echo "  - FastAPI + Bot Controller"
echo "  - Streamlit Dashboard"
echo "  - Cloudflare Tunnel"
echo ""
echo "⏰ Aguarde 30 segundos para inicialização completa..."
echo ""
echo "🌐 ACESSAR SISTEMA:"
echo ""
echo "  Site Principal:"
echo "    https://auronex.com.br/"
echo ""
echo "  Dashboard Streamlit:"
echo "    https://app.auronex.com.br/"
echo ""
echo "  Documentação API:"
echo "    https://auronex.com.br/api/docs"
echo ""
echo "========================================"
echo "  STATUS DOS SERVIÇOS"
echo "========================================"
echo ""

sleep 10

# Verificar se serviços estão rodando
echo "FastAPI (porta 8001):"
if netstat -tlnp 2>/dev/null | grep -q 8001; then
    echo "  ✅ RODANDO"
else
    echo "  ❌ NÃO RODANDO"
fi

echo ""
echo "Streamlit (porta 8501):"
if netstat -tlnp 2>/dev/null | grep -q 8501; then
    echo "  ✅ RODANDO"
else
    echo "  ❌ NÃO RODANDO"
fi

echo ""
echo "Cloudflare Tunnel:"
if ps aux | grep -q "cloudflared tunnel run"; then
    echo "  ✅ RODANDO"
else
    echo "  ❌ NÃO RODANDO"
fi

echo ""
echo "========================================"
echo "  SISTEMA OPERACIONAL"
echo "========================================"
echo ""
echo "⚠️  NÃO FECHE OS TERMINAIS ABERTOS!"
echo ""
echo "Para parar sistema:"
echo "  Ctrl+C em cada terminal"
echo ""
echo "Para reiniciar:"
echo "  Execute este script novamente:"
echo "  ./INICIAR_SERVIDOR_XUBUNTU.sh"
echo ""
echo "========================================"
echo "  Desenvolvido por Claude Sonnet 4.5"
echo "  22+ horas de trabalho"
echo "========================================"
echo ""

# Manter este terminal aberto
read -p "Pressione ENTER para fechar este terminal..."

