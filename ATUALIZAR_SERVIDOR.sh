#!/bin/bash
# ====================================
# ATUALIZAR SERVIDOR - LIMPO E FUNCIONAL
# Para tudo, atualiza GitHub, rebuild, inicia limpo
# ====================================

PROJETO="/home/serverhome/auronex"
cd "$PROJETO" || exit 1

echo "============================================================"
echo "  ATUALIZANDO SERVIDOR AURONEX"
echo "============================================================"
echo ""

# 1. PARAR E LIMPAR TUDO
echo "[1/9] Parando serviços..."
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true
sudo lsof -ti:8001 | xargs sudo kill -9 2>/dev/null || true
sudo lsof -ti:8501 | xargs sudo kill -9 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 3
echo "OK"

# 2. PULL GITHUB
echo "[2/9] Pull do GitHub..."
git stash
git pull origin main
echo "OK"

# 3. PYTHON DEPS
echo "[3/9] Deps Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet
echo "OK"

# 4. CRIAR .env.production
echo "[4/9] Configurando .env..."
cd auronex-dashboard
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
EOF
echo "OK"

# 5. LIMPAR CACHE REACT
echo "[5/9] Limpando cache..."
rm -rf .next node_modules/.cache
echo "OK"

# 6. DEPS REACT
echo "[6/9] Deps React..."
npm install --production=false
echo "OK"

# 7. BUILD REACT
echo "[7/9] Build React..."
npm run build
if [ $? -ne 0 ]; then
    echo "[ERRO] Build falhou!"
    exit 1
fi
echo "OK"
cd ..

# 8. INICIAR SERVICOS
echo "[8/9] Iniciando serviços..."

# FastAPI
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 3

# React (1 processo apenas)
cd auronex-dashboard
pm2 start "npm start" --name auronex-dashboard --max-restarts 3
sleep 3
cd ..

pm2 save

echo "OK"

# 9. TUNNEL
echo "[9/9] Cloudflare Tunnel..."
nohup cloudflared tunnel run auronex > logs/tunnel.log 2>&1 &
sleep 2

echo ""
echo "============================================================"
echo "  DEPLOY CONCLUIDO!"
echo "============================================================"
echo ""

pm2 status

echo ""
echo "Tunnel:"
ps aux | grep "cloudflared tunnel" | grep -v grep || echo "  [AVISO] Verifique logs/tunnel.log"

echo ""
echo "URLs:"
echo "  https://auronex.com.br"
echo "  https://app.auronex.com.br/"
echo ""
echo "Testar login e sistema!"
echo ""
echo "============================================================"
