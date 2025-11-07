#!/bin/bash
# ====================================
# DEPLOY PRODUÇÃO - SEM BOT
# FastAPI + React + Tunnel apenas
# Bot inicia quando usuário clicar Play!
# ====================================

PROJETO="/home/serverhome/auronex"
cd "$PROJETO" || exit 1

echo "============================================================"
echo "  DEPLOY PRODUÇÃO - AURONEX"
echo "============================================================"
echo ""

# 1. Pull GitHub
echo "[1/8] Pull do GitHub..."
git stash
git pull origin main
git checkout stash -- db.sqlite3 2>/dev/null
git stash drop 2>/dev/null
echo "OK"
echo ""

# 2. Atualizar banco
echo "[2/8] Atualizando banco..."
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>/dev/null
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>/dev/null
echo "OK"
echo ""

# 3. Deps Python
echo "[3/8] Deps Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet --upgrade
echo "OK"
echo ""

# 4. Criar .env.production
echo "[4/8] Configurando .env.production..."
cd auronex-dashboard
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
EOF
echo "OK"
echo ""

# 5. Deps React
echo "[5/8] Deps React..."
npm install
echo "OK"
echo ""

# 6. Build React
echo "[6/8] Build React..."
npm run build
if [ $? -ne 0 ]; then
    echo "[ERRO] Build falhou!"
    exit 1
fi
echo "OK"
echo ""

cd ..

# 7. Parar serviços
echo "[7/8] Parando serviços..."
pm2 stop all 2>/dev/null
pm2 delete all 2>/dev/null
sudo systemctl stop cloudflared 2>/dev/null
echo "OK"
echo ""

sleep 3

# 8. Iniciar serviços
echo "[8/8] Iniciando serviços..."

# FastAPI
echo "  - FastAPI (porta 8001)..."
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 3

# React
echo "  - Dashboard React (porta 8501)..."
cd auronex-dashboard
pm2 start ecosystem.config.js
sleep 3
cd ..

# Cloudflare Tunnel
echo "  - Cloudflare Tunnel..."
if systemctl is-active --quiet cloudflared 2>/dev/null; then
    sudo systemctl restart cloudflared
else
    sudo systemctl start cloudflared
fi

sleep 2

# Salvar PM2
pm2 save

echo "OK"
echo ""

# Status final
echo "============================================================"
echo "  DEPLOY CONCLUIDO!"
echo "============================================================"
echo ""

pm2 status

echo ""
echo "Cloudflare Tunnel:"
if systemctl is-active --quiet cloudflared; then
    echo "  Status: ATIVO"
else
    echo "  Status: VERIFICAR"
fi

echo ""
echo "URLs:"
echo "  Landing + API: https://auronex.com.br"
echo "  Dashboard: https://app.auronex.com.br/"
echo ""
echo "Bot Controller:"
echo "  NAO iniciado (usuarios controlam pelo Dashboard)"
echo "  Bots iniciam quando usuario clicar Play"
echo ""
echo "============================================================"
echo ""

