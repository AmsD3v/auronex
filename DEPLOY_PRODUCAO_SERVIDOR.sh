#!/bin/bash
# ====================================
# DEPLOY PRODUÇÃO - 4 Terminais
# FastAPI + React + Bot + Tunnel
# ====================================

PROJETO="/home/serverhome/auronex"
cd "$PROJETO"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================================"
echo "  DEPLOY PRODUÇÃO - AURONEX"
echo "============================================================"
echo ""

# 1. Atualizar banco
echo -e "${YELLOW}[1/8] Atualizando banco...${NC}"
sqlite3 db.sqlite3 "ALTER TABLE bot_configuration ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>/dev/null
sqlite3 db.sqlite3 "ALTER TABLE bot_configuration ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>/dev/null
echo -e "${GREEN}✅ Banco atualizado${NC}"

# 2. Git pull
echo -e "${YELLOW}[2/8] Pull do GitHub...${NC}"
git stash
git pull origin main
git checkout stash -- db.sqlite3 2>/dev/null
git stash drop 2>/dev/null
echo -e "${GREEN}✅ Código atualizado${NC}"

# 3. npm install
echo -e "${YELLOW}[3/8] Instalando deps React...${NC}"
cd auronex-dashboard
npm install
echo -e "${GREEN}✅ Deps instaladas${NC}"

# 4. Build
echo -e "${YELLOW}[4/8] Build React...${NC}"
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build falhou!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build OK${NC}"

cd ..

# 5. Parar serviços
echo -e "${YELLOW}[5/8] Parando serviços...${NC}"
pm2 stop all
pm2 delete all
echo -e "${GREEN}✅ Serviços parados${NC}"

# 6. Iniciar FastAPI
echo -e "${YELLOW}[6/8] FastAPI (porta 8001)...${NC}"
source venv/bin/activate
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
sleep 2

# 7. Iniciar React
echo -e "${YELLOW}[7/8] React (porta 8501)...${NC}"
cd auronex-dashboard
pm2 start ecosystem.config.js
sleep 2
cd ..

# 8. Iniciar Tunnel
echo -e "${YELLOW}[8/8] Cloudflare Tunnel...${NC}"
if systemctl is-active --quiet cloudflared 2>/dev/null; then
    sudo systemctl restart cloudflared
else
    sudo systemctl start cloudflared
fi

pm2 save

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  ✅ DEPLOY CONCLUÍDO!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""

pm2 status

echo ""
echo "Acesse: https://app.auronex.com.br/"
echo ""

