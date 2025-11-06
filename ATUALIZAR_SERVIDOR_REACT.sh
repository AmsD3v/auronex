#!/bin/bash

# ========================================
# ATUALIZAR SERVIDOR - DASHBOARD REACT
# Inicia: FastAPI + React + Cloudflare Tunnel
# ========================================

echo ""
echo "============================================================"
echo "  ATUALIZANDO SERVIDOR AURONEX - DASHBOARD REACT"
echo "============================================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está no diretório correto
if [ ! -f "package.json" ]; then
    cd auronex-dashboard 2>/dev/null || {
        echo -e "${RED}❌ Erro: pasta auronex-dashboard não encontrada!${NC}"
        exit 1
    }
fi

# ========================================
# PASSO 1: PARAR SERVIÇOS ANTIGOS
# ========================================

echo -e "${YELLOW}[1/7] Parando serviços antigos...${NC}"

# Parar Streamlit antigo (se estiver rodando)
pm2 stop streamlit 2>/dev/null
pm2 delete streamlit 2>/dev/null

# Parar FastAPI antigo
pm2 stop fastapi-app 2>/dev/null

# Parar React antigo (se existir)
pm2 stop auronex-dashboard 2>/dev/null
pm2 delete auronex-dashboard 2>/dev/null

echo -e "${GREEN}✅ Serviços antigos parados${NC}"
sleep 1

# ========================================
# PASSO 2: ATUALIZAR CÓDIGO (GIT PULL)
# ========================================

echo -e "${YELLOW}[2/7] Atualizando código do GitHub...${NC}"

cd ..
git pull origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Código atualizado${NC}"
else
    echo -e "${RED}❌ Erro ao atualizar código${NC}"
    exit 1
fi

sleep 1

# ========================================
# PASSO 3: INSTALAR DEPENDÊNCIAS REACT
# ========================================

echo -e "${YELLOW}[3/7] Instalando dependências React...${NC}"

cd auronex-dashboard

npm ci --production

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências instaladas${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi

sleep 1

# ========================================
# PASSO 4: BUILD DO REACT
# ========================================

echo -e "${YELLOW}[4/7] Compilando React (build de produção)...${NC}"

npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build compilado${NC}"
else
    echo -e "${RED}❌ Erro no build${NC}"
    exit 1
fi

sleep 1

# ========================================
# PASSO 5: INICIAR FASTAPI
# ========================================

echo -e "${YELLOW}[5/7] Iniciando FastAPI (porta 8001)...${NC}"

cd ..

# Ativar venv Python
source venv/bin/activate

# Iniciar FastAPI com PM2
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload" --name "fastapi-app"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ FastAPI iniciado na porta 8001${NC}"
else
    echo -e "${RED}❌ Erro ao iniciar FastAPI${NC}"
fi

sleep 2

# ========================================
# PASSO 6: INICIAR DASHBOARD REACT
# ========================================

echo -e "${YELLOW}[6/7] Iniciando Dashboard React (porta 8501)...${NC}"

cd auronex-dashboard

# Iniciar React com PM2 usando ecosystem.config.js
pm2 start ecosystem.config.js

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dashboard React iniciado na porta 8501${NC}"
else
    echo -e "${RED}❌ Erro ao iniciar React${NC}"
fi

sleep 2

# ========================================
# PASSO 7: VERIFICAR CLOUDFLARE TUNNEL
# ========================================

echo -e "${YELLOW}[7/7] Verificando Cloudflare Tunnel...${NC}"

# Verificar se cloudflared está rodando
if systemctl is-active --quiet cloudflared; then
    echo -e "${GREEN}✅ Cloudflare Tunnel rodando${NC}"
else
    echo -e "${YELLOW}⚠️  Iniciando Cloudflare Tunnel...${NC}"
    sudo systemctl start cloudflared
    sleep 3
    
    if systemctl is-active --quiet cloudflared; then
        echo -e "${GREEN}✅ Cloudflare Tunnel iniciado${NC}"
    else
        echo -e "${RED}❌ Erro ao iniciar tunnel${NC}"
    fi
fi

# ========================================
# SALVAR CONFIGURAÇÃO PM2
# ========================================

pm2 save

# ========================================
# STATUS FINAL
# ========================================

echo ""
echo "============================================================"
echo "  SERVIDOR ATUALIZADO COM SUCESSO!"
echo "============================================================"
echo ""

pm2 status

echo ""
echo -e "${GREEN}✅ FastAPI:${NC} http://localhost:8001"
echo -e "${GREEN}✅ Dashboard React:${NC} http://localhost:8501"
echo ""
echo -e "${GREEN}URLs Públicas:${NC}"
echo "   Landing + API: https://auronex.com.br"
echo "   Admin: https://admin.auronex.com.br"
echo "   Dashboard: https://app.auronex.com.br"
echo ""
echo -e "${YELLOW}Comandos úteis:${NC}"
echo "   Ver logs: pm2 logs auronex-dashboard"
echo "   Reiniciar: pm2 restart auronex-dashboard"
echo "   Status: pm2 status"
echo ""
echo "============================================================"
echo ""

