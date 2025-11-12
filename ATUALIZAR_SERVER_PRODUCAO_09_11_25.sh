#!/bin/bash
# ====================================
# ATUALIZAR SERVIDOR PRODUCAO
# Data: 09/11/2025
# COMPLETO: cd + pull + para + atualiza + reinicia
# ====================================

echo "============================================================"
echo "  ATUALIZANDO SERVIDOR PRODUCAO - 09/11/2025"
echo "============================================================"
echo ""

# 0. IR PARA PASTA
echo "[0/11] Navegando para pasta..."
cd /home/serverhome/auronex || exit 1
echo "Pasta: $(pwd)"
echo "OK"
echo ""

# 0.5 VERIFICAR GIT
echo "[0.5/11] Verificando Git..."
git status
echo ""

# 1. PULL GITHUB (FORÇADO!)
echo "[1/11] PULL GITHUB FORCADO..."
echo "Branch atual: $(git branch --show-current)"
git fetch --all
git stash push -u -m "backup_$(date +%Y%m%d_%H%M%S)"
git reset --hard origin/main
git pull origin main --rebase

# Ver versao
VERSAO=$(cat VERSION.txt 2>/dev/null || echo "Desconhecida")
echo "Versao NOVA: $VERSAO"
echo "Commits: $(git log --oneline -5)"
echo "OK - CODIGO ATUALIZADO!"
echo ""

# 2. PARAR TUDO
echo "[2/11] Parando servicos..."
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true
sudo lsof -ti:8001 | xargs sudo kill -9 2>/dev/null || true
sudo lsof -ti:8501 | xargs sudo kill -9 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 3
echo "OK"

# 3. BACKUP
echo "[3/11] Backup..."
mkdir -p ~/backups
BACKUP="auronex_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf ~/backups/$BACKUP db.sqlite3 2>/dev/null
echo "Backup: ~/backups/$BACKUP"

# 3. PULL GITHUB (PRESERVANDO BANCO!)
echo "[3/11] Pull do GitHub..."
# ✅ Stash apenas arquivos modificados (não db.sqlite3)
git add -u  # Apenas tracked files
git stash push -m "temp" -- $(git diff --name-only --cached | grep -v "db.sqlite3")
git stash drop 2>/dev/null

git pull origin main

VERSAO_NOVA=$(cat VERSION.txt 2>/dev/null || echo "Desconhecida")
echo "Nova versao: $VERSAO_NOVA"
echo "Banco: LOCAL preservado (usuarios/trades mantidos)"
echo ""

# 4. ATUALIZAR BANCO
echo "[4/11] Atualizando banco..."
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>/dev/null || true
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>/dev/null || true
sqlite3 db.sqlite3 "ALTER TABLE bot_configurations ADD COLUMN is_testnet BOOLEAN DEFAULT 1;" 2>/dev/null || true
echo "OK"

# 5. DEPS PYTHON
echo "[5/11] Deps Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet --upgrade
echo "OK"

# 6. CRIAR .env.production
echo "[6/11] Configurando .env..."
cd auronex-dashboard
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
EOF
echo "OK"

# 7. LIMPAR CACHE
echo "[7/11] Limpando cache React..."
rm -rf .next node_modules/.cache
echo "OK"

# 8. DEPS REACT
echo "[8/11] Deps React..."
npm install --production=false
echo "OK"

# 9. BUILD REACT
echo "[9/11] Build React..."
npm run build
if [ $? -ne 0 ]; then
    echo "[ERRO] Build falhou!"
    exit 1
fi
echo "OK"
cd ..

# 10. INICIAR SERVICOS
echo "[10/11] Iniciando servicos..."

# FastAPI
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 3

# React (1 processo)
pm2 start "npm --prefix auronex-dashboard start" --name auronex-dashboard
sleep 3

# Tunnel
nohup cloudflared tunnel run auronex > logs/tunnel.log 2>&1 &
sleep 2

pm2 save

echo "OK"

# 11. STATUS
echo "[11/11] Verificando status..."
echo ""

pm2 status

echo ""
echo "Tunnel:"
if ps aux | grep -q "cloudflared tunnel run"; then
    echo "  Status: ATIVO"
else
    echo "  [AVISO] Verificar logs/tunnel.log"
fi

echo ""
echo "============================================================"
echo "  DEPLOY CONCLUIDO!"
echo "============================================================"
echo ""
echo "Versao: $VERSAO_ANTES -> $VERSAO_NOVA"
echo ""
echo "URLs:"
echo "  https://auronex.com.br"
echo "  https://app.auronex.com.br/"
echo ""
echo "Testar:"
echo "  1. Login funciona"
echo "  2. Bot capital=0 nao ativa"
echo "  3. admin/#bots carrega"
echo "  4. Saldo Total correto"
echo ""
echo "============================================================"

