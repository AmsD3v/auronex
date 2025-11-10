#!/bin/bash
# ====================================
# ATUALIZAR PRODUCAO - GARANTIDO
# Simples e direto - FUNCIONA!
# ====================================

echo "============================================================"
echo "  ATUALIZANDO PRODUCAO - GARANTIDO"
echo "============================================================"

cd /home/serverhome/auronex

# 1. PARAR TUDO
echo "[1/7] Parando..."
pm2 stop all
pm2 delete all
sleep 2

# 2. BACKUP BANCO + PULL
echo "[2/7] Backup banco + Pull..."
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null
git fetch --all
git reset --hard origin/main
# ✅ RESTAURAR BANCO (NUNCA sobrescrever!)
if [ -f db.sqlite3.backup.* ]; then
    mv db.sqlite3.backup.* db.sqlite3 2>/dev/null
fi
echo "Versao: $(cat VERSION.txt 2>/dev/null || echo '?')"

# 3. LIMPAR REACT
echo "[3/7] Limpando React..."
cd auronex-dashboard
rm -rf .next
rm -rf node_modules/.cache

# 4. ENV PRODUCTION
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
EOF

# 5. BUILD
echo "[4/7] npm install..."
npm install

echo "[5/7] npm run build..."
npm run build

cd ..

# 6. INICIAR
echo "[6/7] Iniciando..."
source venv/bin/activate

pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app

pm2 start "npm --prefix auronex-dashboard start" --name auronex-dashboard

sleep 3

# 7. TUNNEL
echo "[7/7] Tunnel..."
pkill -f cloudflared
nohup cloudflared tunnel run auronex > logs/tunnel.log 2>&1 &

pm2 save

echo ""
echo "============================================================"
echo "  CONCLUIDO!"
echo "============================================================"

pm2 status

echo ""
echo "URLs: https://app.auronex.com.br/"
echo "Versao: $(cat VERSION.txt)"
echo ""

