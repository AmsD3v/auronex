#!/bin/bash
# ====================================
# ATUALIZAR SERVIDOR PRODUÇÃO
# FastAPI + React + Tunnel
# SEM Bot Controller (usuario controla!)
# ====================================

PROJETO="/home/serverhome/auronex"
cd "$PROJETO" || exit 1

echo "============================================================"
echo "  ATUALIZAR SERVIDOR - PRODUCAO"
echo "============================================================"
echo ""

# Ver versao atual
VERSAO_ANTES=$(cat VERSION.txt 2>/dev/null || echo "Desconhecida")
echo "Versao atual: $VERSAO_ANTES"
echo ""

# 1. Pull GitHub
echo "[1/9] Pull do GitHub..."
git stash
git pull origin main
git checkout stash -- db.sqlite3 2>/dev/null
git stash drop 2>/dev/null

VERSAO_DEPOIS=$(cat VERSION.txt 2>/dev/null || echo "Desconhecida")
echo "Nova versao: $VERSAO_DEPOIS"
echo ""

# 2. Backup
echo "[2/9] Criando backup..."
mkdir -p ~/backups
BACKUP_NAME="auronex_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf ~/backups/$BACKUP_NAME \
    --exclude='venv' \
    --exclude='node_modules' \
    --exclude='.next' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.log' \
    . 2>/dev/null
echo "Backup: ~/backups/$BACKUP_NAME"
echo ""

# 3. Atualizar banco
echo "[3/9] Atualizando banco..."
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>/dev/null
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>/dev/null
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN is_testnet BOOLEAN DEFAULT 1;" 2>/dev/null
echo "OK"
echo ""

# 4. Deps Python
echo "[4/9] Atualizando deps Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet --upgrade
echo "OK"
echo ""

# 5. Criar .env.production
echo "[5/9] Configurando .env.production..."
cd auronex-dashboard
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
EOF
echo "OK"
echo ""

# 6. Deps React
echo "[6/9] Instalando deps React..."
npm install
echo "OK"
echo ""

# 7. Build React
echo "[7/9] Build React (producao)..."
npm run build
if [ $? -ne 0 ]; then
    echo "[ERRO] Build falhou!"
    exit 1
fi
echo "OK"
echo ""

cd ..

# 8. Reiniciar servicos
echo "[8/9] Reiniciando servicos..."

# Parar tudo
pm2 stop all 2>/dev/null
pm2 delete all 2>/dev/null
sleep 2

# Iniciar FastAPI
echo "  - FastAPI..."
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 3

# Iniciar React
echo "  - React..."
cd auronex-dashboard
pm2 start ecosystem.config.js
sleep 3
cd ..

pm2 save

echo "OK"
echo ""

# 9. Tunnel
echo "[9/9] Cloudflare Tunnel..."

# Parar tunnel antigo
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 2

# Iniciar tunnel
nohup cloudflared tunnel run auronex > logs/tunnel.log 2>&1 &
TUNNEL_PID=$!
sleep 3

if ps -p $TUNNEL_PID > /dev/null 2>&1; then
    echo "  Tunnel iniciado (PID: $TUNNEL_PID)"
else
    echo "  [AVISO] Tunnel pode nao ter iniciado - verifique logs/tunnel.log"
fi

echo ""

# Status final
echo "============================================================"
echo "  DEPLOY CONCLUIDO!"
echo "============================================================"
echo ""
echo "Versao: $VERSAO_ANTES -> $VERSAO_DEPOIS"
echo ""

pm2 status

echo ""
echo "Cloudflare Tunnel:"
if ps aux | grep -q "cloudflared tunnel run"; then
    echo "  Status: ATIVO"
    ps aux | grep "cloudflared tunnel run" | grep -v grep
else
    echo "  Status: VERIFICAR logs/tunnel.log"
fi

echo ""
echo "URLs Publicas:"
echo "  https://auronex.com.br"
echo "  https://app.auronex.com.br/"
echo ""
echo "Bot Controller:"
echo "  NAO iniciado automaticamente"
echo "  Bots iniciam quando usuario clicar Play no Dashboard"
echo ""
echo "Logs:"
echo "  FastAPI:   pm2 logs fastapi-app"
echo "  React:     pm2 logs auronex-dashboard"
echo "  Tunnel:    tail -f logs/tunnel.log"
echo ""
echo "============================================================"
echo ""

