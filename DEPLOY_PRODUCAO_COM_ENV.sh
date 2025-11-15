#!/bin/bash
# ========================================
# DEPLOY PARA PRODUÇÃO COM .ENV
# ========================================
# Execute no SERVIDOR de produção
# ssh usuario@auronex.com.br
# cd /home/serverhome/auronex
# ./DEPLOY_PRODUCAO_COM_ENV.sh

set -e

PROJETO="/home/serverhome/auronex"
cd "$PROJETO" || exit 1

echo "======================================================================"
echo "  DEPLOY AURONEX - PRODUÇÃO COM .ENV SEGURO"
echo "======================================================================"
echo ""

# 1. Backup do .env antigo (se existir)
if [ -f ".env" ]; then
    echo "[1/10] Fazendo backup do .env antigo..."
    cp .env ".env.backup.$(date +%Y%m%d_%H%M%S)"
    echo "OK"
else
    echo "[1/10] Nenhum .env existente (primeira vez)"
fi
echo ""

# 2. Gerar chaves de criptografia (se não existirem)
echo "[2/10] Verificando chaves de segurança..."

if ! grep -q "ENCRYPTION_KEY=" .env 2>/dev/null || grep -q "GERAR_NO_SERVIDOR" .env 2>/dev/null; then
    echo "Gerando ENCRYPTION_KEY..."
    ENCRYPTION_KEY=$(python3 scripts/generate_encryption_key.py | grep "ENCRYPTION_KEY=" | cut -d= -f2)
    echo "OK: $ENCRYPTION_KEY"
else
    echo "ENCRYPTION_KEY já configurada"
fi

if ! grep -q "SECRET_KEY=" .env 2>/dev/null || grep -q "GERAR_NO_SERVIDOR" .env 2>/dev/null; then
    echo "Gerando SECRET_KEY..."
    SECRET_KEY=$(python3 scripts/generate_secret_key.py | grep "SECRET_KEY=" | cut -d= -f2)
    echo "OK: $SECRET_KEY"
else
    echo "SECRET_KEY já configurada"
fi
echo ""

# 3. Copiar .env.production para .env (se não existir)
if [ ! -f ".env" ]; then
    echo "[3/10] Criando .env a partir de .env.production..."
    cp .env.production .env
    
    # Substituir placeholders
    sed -i "s/GERAR_NO_SERVIDOR_44_CHARS/$ENCRYPTION_KEY/g" .env
    sed -i "s/GERAR_NO_SERVIDOR_64_CHARS_HEX/$SECRET_KEY/g" .env
    
    echo "OK - Revise o .env e configure PostgreSQL/API Keys!"
    echo ""
    echo "======================================================================"
    echo "  [ATENÇÃO] CONFIGURE MANUALMENTE:"
    echo "======================================================================"
    echo "1. DATABASE_URL (PostgreSQL)"
    echo "2. API Keys das exchanges"
    echo "3. Telegram/Slack webhooks"
    echo "4. Sentry DSN"
    echo ""
    echo "Edite: nano .env"
    echo ""
    read -p "Pressione ENTER após configurar o .env..."
fi
echo ""

# 4. Parar serviços
echo "[4/10] Parando serviços..."
pm2 stop all || true
echo "OK"
echo ""

# 5. Git pull
echo "[5/10] Atualizando código..."
git stash
git pull origin main
git checkout stash -- db.sqlite3 2>/dev/null || true
git stash drop 2>/dev/null || true
echo "OK"
echo ""

# 6. Deps Python
echo "[6/10] Atualizando dependências Python..."
source venv/bin/activate
pip install -r requirements.txt --quiet --upgrade
echo "OK"
echo ""

# 7. Migrations (se usar Alembic)
if [ -d "alembic" ]; then
    echo "[7/10] Executando migrations..."
    alembic upgrade head
    echo "OK"
else
    echo "[7/10] Alembic não configurado (pulando migrations)"
fi
echo ""

# 8. Re-criptografar API Keys (se necessário)
echo "[8/10] Verificando API Keys..."
read -p "Tem API Keys antigas para re-criptografar? (s/n): " RECRYPT

if [ "$RECRYPT" = "s" ] || [ "$RECRYPT" = "S" ]; then
    echo "Executando migração..."
    python3 scripts/migrate_encryption.py
    echo "OK"
else
    echo "Pulando re-criptografia"
fi
echo ""

# 9. Build frontend
echo "[9/10] Build do frontend..."
cd auronex-dashboard
npm install --production
npm run build
cd ..
echo "OK"
echo ""

# 10. Iniciar serviços
echo "[10/10] Iniciando serviços..."

# FastAPI
pm2 start fastapi_app/main.py --name fastapi-app \
    --interpreter python3 \
    --log logs/fastapi.log

# Frontend
pm2 start npm --name auronex-dashboard \
    -- start \
    --log logs/react.log

# Bot Controller
pm2 start bot/bot_controller.py --name bot-controller \
    --interpreter python3 \
    --log logs/bot_controller.log \
    --restart-delay 3000 \
    --max-restarts 10

# Cloudflare Tunnel
pm2 start cloudflared --name cloudflare-tunnel \
    -- tunnel run auronex \
    --log logs/tunnel.log

# Salvar configuração PM2
pm2 save

echo "OK"
echo ""

# Status
echo "======================================================================"
echo "  DEPLOY CONCLUÍDO!"
echo "======================================================================"
echo ""
pm2 status
echo ""
echo "Logs em tempo real:"
echo "  pm2 logs fastapi-app"
echo "  pm2 logs bot-controller"
echo ""
echo "URLs:"
echo "  https://auronex.com.br (Backend)"
echo "  https://app.auronex.com.br (Frontend)"
echo ""
echo "======================================================================"
echo "  [SEGURANÇA] AÇÕES CRÍTICAS:"
echo "======================================================================"
echo "1. Verifique .env está correto"
echo "2. .env NÃO deve estar no Git"
echo "3. Faça backup do .env em local seguro"
echo "4. Teste login: curl https://auronex.com.br/api/health"
echo ""






