#!/bin/bash
# ====================================
# ATUALIZAR SERVIDOR - LIMPO E COMPLETO
# Para TODOS serviços, limpa, atualiza, reinicia
# ====================================

set -e  # Parar se houver erro

PROJETO="/home/serverhome/auronex"
cd "$PROJETO" || exit 1

echo "============================================================"
echo "  ATUALIZANDO SERVIDOR - PROCESSO COMPLETO"
echo "============================================================"
echo ""

# 1. PARAR TUDO
echo "[1/10] Parando todos serviços..."
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true
sleep 2

# 2. MATAR PROCESSOS TRAVADOS
echo "[2/10] Limpando portas..."
sudo lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sudo lsof -ti:8501 | xargs kill -9 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 2

# 3. PULL GITHUB
echo "[3/10] Pull do GitHub..."
git stash
git pull origin main
echo "OK"
echo ""

# 4. LIMPAR CACHE REACT
echo "[4/10] Limpando cache React..."
cd auronex-dashboard
rm -rf .next node_modules/.cache
echo "OK"
echo ""

# 5. DEPS REACT
echo "[5/10] Instalando deps React..."
npm install
echo "OK"
echo ""

# 6. BUILD REACT
echo "[6/10] Build React (producao)..."
npm run build
if [ $? -ne 0 ]; then
    echo "[ERRO] Build falhou!"
    exit 1
fi
echo "OK"
echo ""

cd ..

# 7. DEPS PYTHON
echo "[7/10] Atualizando deps Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet
echo "OK"
echo ""

# 8. INICIAR FASTAPI
echo "[8/10] Iniciando FastAPI..."
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 3

# 9. INICIAR REACT
echo "[9/10] Iniciando React..."
cd auronex-dashboard
pm2 start npm --name "auronex-dashboard" -- start
sleep 3
cd ..

# 10. TUNNEL
echo "[10/10] Iniciando Cloudflare Tunnel..."
nohup cloudflared tunnel run auronex > logs/tunnel.log 2>&1 &
sleep 2

pm2 save

echo ""
echo "============================================================"
echo "  DEPLOY CONCLUIDO!"
echo "============================================================"
echo ""

pm2 status

echo ""
echo "Tunnel:"
if ps aux | grep -q "cloudflared tunnel run"; then
    echo "  Status: ATIVO"
else
    echo "  Status: VERIFICAR logs/tunnel.log"
fi

echo ""
echo "URLs:"
echo "  https://auronex.com.br"
echo "  https://app.auronex.com.br/"
echo ""
echo "============================================================"

