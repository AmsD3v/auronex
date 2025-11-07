#!/bin/bash
# ====================================
# DEPLOY PRODUÇÃO COMPLETO
# Git pull + Build + Inicia serviços + Tunnel
# ====================================

PROJETO="/home/serverhome/auronex"
TUNNEL_NAME="auronex"  # ✅ Nome do seu tunnel

cd "$PROJETO"

echo "============================================================"
echo "  DEPLOY PRODUÇÃO - AURONEX"
echo "============================================================"
echo ""

# 1. Atualizar banco
echo "[1/9] Atualizando banco..."
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>/dev/null
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>/dev/null
echo "✅ Banco OK"

# 2. Git pull
echo "[2/9] Pull do GitHub..."
git stash
git pull origin main
git checkout stash -- db.sqlite3 2>/dev/null
git stash drop 2>/dev/null
echo "✅ Código atualizado"

# 3. Deps Python
echo "[3/9] Deps Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet --upgrade
echo "✅ Python OK"

# 4. Deps React
echo "[4/9] Deps React..."
cd auronex-dashboard
npm install
echo "✅ React deps OK"

# 5. Build React
echo "[5/9] Build React..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Build falhou!"
    exit 1
fi
echo "✅ Build OK"

cd ..

# 6. Parar serviços
echo "[6/9] Parando serviços..."
pm2 stop all 2>/dev/null
pm2 delete all 2>/dev/null
# Parar tunnel também
sudo systemctl stop cloudflared 2>/dev/null
sudo pkill -f "cloudflared tunnel" 2>/dev/null
echo "✅ Serviços parados"

sleep 3

# 7. Iniciar FastAPI
echo "[7/9] FastAPI (porta 8001)..."
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 3
echo "✅ FastAPI iniciado"

# 8. Iniciar React
echo "[8/9] React (porta 8501)..."
cd auronex-dashboard
pm2 start ecosystem.config.js
sleep 3
cd ..
echo "✅ React iniciado"

# 9. INICIAR CLOUDFLARE TUNNEL - CRÍTICO!
echo "[9/9] Cloudflare Tunnel..."

# Método 1: Tentar com systemd
if command -v systemctl &> /dev/null; then
    echo "   Tentando systemd..."
    sudo systemctl start cloudflared
    sleep 3
    
    if systemctl is-active --quiet cloudflared 2>/dev/null; then
        echo "✅ Tunnel iniciado (systemd)"
    else
        # Método 2: Processo direto
        echo "   Tentando processo direto..."
        nohup sudo cloudflared tunnel run $TUNNEL_NAME > /tmp/tunnel.log 2>&1 &
        TUNNEL_PID=$!
        sleep 3
        
        if ps -p $TUNNEL_PID > /dev/null 2>&1; then
            echo "✅ Tunnel iniciado (PID: $TUNNEL_PID)"
        else
            echo "❌ FALHA ao iniciar tunnel!"
            echo "   Execute manualmente:"
            echo "   sudo systemctl start cloudflared"
            echo "   OU"
            echo "   sudo cloudflared tunnel run $TUNNEL_NAME"
        fi
    fi
else
    # Sem systemd - iniciar direto
    echo "   Iniciando processo direto..."
    nohup sudo cloudflared tunnel run $TUNNEL_NAME > /tmp/tunnel.log 2>&1 &
    TUNNEL_PID=$!
    sleep 3
    
    if ps -p $TUNNEL_PID > /dev/null 2>&1; then
        echo "✅ Tunnel iniciado (PID: $TUNNEL_PID)"
    else
        echo "❌ Tunnel não iniciou!"
    fi
fi

# Salvar PM2
pm2 save

echo ""
echo "============================================================"
echo "  ✅ DEPLOY CONCLUÍDO!"
echo "============================================================"
echo ""

# Status
pm2 status

echo ""
echo "Cloudflare Tunnel:"
if systemctl is-active --quiet cloudflared 2>/dev/null; then
    sudo systemctl status cloudflared | grep "Active:"
elif ps aux | grep -q "cloudflared tunnel run"; then
    echo "✅ Rodando (processo direto)"
    ps aux | grep "cloudflared tunnel" | grep -v grep
else
    echo "⚠️ Não detectado"
fi

echo ""
echo "URLs Públicas:"
echo "  Landing + API: https://auronex.com.br"
echo "  Dashboard: https://app.auronex.com.br/"
echo ""
echo "Portas Locais:"
netstat -tulnp 2>/dev/null | grep -E ":(8001|8501)" || echo "  (use sudo para ver portas)"
echo ""
echo "============================================================"
