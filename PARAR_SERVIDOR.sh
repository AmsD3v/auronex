#!/bin/bash
# ========================================
# AURONEX - PARAR SERVIDOR
# ========================================

clear

echo "========================================"
echo "  AURONEX - PARANDO SERVIDOR"
echo "========================================"
echo ""

# Ler PIDs salvos
if [ -f /tmp/auronex_pids.txt ]; then
    source /tmp/auronex_pids.txt
    
    echo "Parando serviços salvos..."
    kill $FASTAPI_PID $STREAMLIT_PID $TUNNEL_PID 2>/dev/null
fi

echo "Parando TODOS os processos Auronex..."
echo ""

# Matar processos
sudo pkill -f "uvicorn fastapi_app"
sudo pkill -f "streamlit run dashboard"
sudo pkill -f "cloudflared tunnel run"

sleep 2

echo "✅ Todos os serviços parados!"
echo ""

# Verificar
echo "Verificando portas..."
if netstat -tlnp 2>/dev/null | grep -q 8001; then
    echo "  ⚠️  Porta 8001 ainda em uso"
else
    echo "  ✅ Porta 8001 livre"
fi

if netstat -tlnp 2>/dev/null | grep -q 8501; then
    echo "  ⚠️  Porta 8501 ainda em uso"
else
    echo "  ✅ Porta 8501 livre"
fi

echo ""
echo "========================================"
echo "  Sistema parado!"
echo "========================================"
echo ""

