#!/bin/bash

# ========================================
# ATUALIZAR SERVIDOR - DASHBOARD REACT
# Inicia: FastAPI + React + Cloudflare Tunnel
# ========================================

clear

echo ""
echo "============================================================"
echo "  AURONEX - ATUALIZAR SERVIDOR (REACT)"
echo "  Repositorio: https://github.com/AmsD3v/auronex.git"
echo "============================================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ========================================
# 0. DETECTAR PASTA DO PROJETO
# ========================================

# Tentar encontrar pasta do projeto
if [ -d "/home/serverhome/robo" ]; then
    PROJETO_DIR="/home/serverhome/robo"
elif [ -d "/home/serverhome/auronex" ]; then
    PROJETO_DIR="/home/serverhome/auronex"
elif [ -d "/home/usuario/robo" ]; then
    PROJETO_DIR="/home/usuario/robo"
elif [ -d "$(pwd)" ] && [ -f "fastapi_app/main.py" ]; then
    PROJETO_DIR="$(pwd)"
else
    echo -e "${RED}❌ Erro: Pasta do projeto não encontrada!${NC}"
    echo -e "   Execute este script da pasta raiz do projeto"
    exit 1
fi

echo -e "${BLUE}📍 Pasta do projeto: $PROJETO_DIR${NC}"
cd "$PROJETO_DIR"
echo ""

# ========================================
# 1. PARAR SERVIÇOS ANTIGOS
# ========================================

echo -e "${YELLOW}[1/9] Parando serviços antigos...${NC}"

# Parar PM2 (se estiver usando)
pm2 stop streamlit 2>/dev/null
pm2 delete streamlit 2>/dev/null
pm2 stop auronex-dashboard 2>/dev/null
pm2 delete auronex-dashboard 2>/dev/null
pm2 stop fastapi-app 2>/dev/null

# Parar processos diretos (fallback)
pkill -f "streamlit" 2>/dev/null
pkill -f "next dev" 2>/dev/null
pkill -f "next start" 2>/dev/null
pkill -f "node.*8501" 2>/dev/null

echo -e "${GREEN}✅ Serviços antigos parados${NC}"
sleep 2

# ========================================
# 2. ATUALIZAR CÓDIGO (GIT PULL)
# ========================================

echo -e "${YELLOW}[2/9] Baixando código do GitHub...${NC}"
echo -e "${BLUE}   Repositório: https://github.com/AmsD3v/auronex.git${NC}"

# Stash mudanças locais (preserva db.sqlite3)
git stash -u 2>/dev/null

# Pull
git pull origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Código atualizado${NC}"
else
    echo -e "${RED}❌ Erro ao atualizar código${NC}"
    echo -e "   Verifique conexão com GitHub"
    exit 1
fi

sleep 1

# ========================================
# 3. VERIFICAR PASTA REACT
# ========================================

echo -e "${YELLOW}[3/9] Verificando pasta auronex-dashboard...${NC}"

if [ ! -d "auronex-dashboard" ]; then
    echo -e "${RED}❌ Pasta auronex-dashboard não encontrada!${NC}"
    echo -e "   Certifique-se de que fez git push com a pasta auronex-dashboard"
    echo ""
    echo -e "${YELLOW}Pastas disponíveis:${NC}"
    ls -la
    exit 1
fi

echo -e "${GREEN}✅ Pasta auronex-dashboard encontrada${NC}"
sleep 1

# ========================================
# 4. INSTALAR DEPENDÊNCIAS PYTHON
# ========================================

echo -e "${YELLOW}[4/9] Verificando dependências Python...${NC}"

# Ativar venv
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ venv ativado${NC}"
else
    echo -e "${YELLOW}⚠️  venv não encontrado, criando...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Atualizar se necessário
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet --upgrade
    echo -e "${GREEN}✅ Dependências Python atualizadas${NC}"
fi

sleep 1

# ========================================
# 5. INSTALAR DEPENDÊNCIAS REACT
# ========================================

echo -e "${YELLOW}[5/9] Instalando dependências React...${NC}"

cd auronex-dashboard

# Instalar node_modules
npm ci --production

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências React instaladas${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi

sleep 1

# ========================================
# 6. BUILD DO REACT
# ========================================

echo -e "${YELLOW}[6/9] Compilando React (build otimizado)...${NC}"

npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build React compilado${NC}"
else
    echo -e "${RED}❌ Erro no build React${NC}"
    exit 1
fi

sleep 1

# Voltar para raiz
cd ..

# ========================================
# 7. INICIAR FASTAPI (PM2)
# ========================================

echo -e "${YELLOW}[7/9] Iniciando FastAPI (porta 8001)...${NC}"

# Iniciar com PM2
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" \
    --name "fastapi-app" \
    --interpreter python3

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ FastAPI iniciado (PM2)${NC}"
else
    echo -e "${YELLOW}⚠️  PM2 falhou, iniciando direto...${NC}"
    nohup python3 -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 > logs/fastapi.log 2>&1 &
fi

sleep 3

# ========================================
# 8. INICIAR REACT (PM2)
# ========================================

echo -e "${YELLOW}[8/9] Iniciando Dashboard React (porta 8501)...${NC}"

cd auronex-dashboard

# Criar pasta de logs se não existir
mkdir -p logs

# Iniciar com PM2 usando ecosystem.config.js
pm2 start ecosystem.config.js

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dashboard React iniciado (PM2 - porta 8501)${NC}"
else
    echo -e "${RED}❌ Erro ao iniciar React${NC}"
    exit 1
fi

sleep 3

cd ..

# ========================================
# 9. VERIFICAR CLOUDFLARE TUNNEL
# ========================================

echo -e "${YELLOW}[9/9] Verificando Cloudflare Tunnel...${NC}"

if systemctl is-active --quiet cloudflared 2>/dev/null; then
    echo -e "${GREEN}✅ Cloudflare Tunnel rodando${NC}"
elif ps aux | grep -q "cloudflared tunnel run"; then
    echo -e "${GREEN}✅ Cloudflare Tunnel rodando (processo direto)${NC}"
else
    echo -e "${YELLOW}⚠️  Iniciando Cloudflare Tunnel...${NC}"
    
    # Tentar com systemctl
    sudo systemctl start cloudflared 2>/dev/null
    
    sleep 3
    
    if systemctl is-active --quiet cloudflared 2>/dev/null; then
        echo -e "${GREEN}✅ Cloudflare Tunnel iniciado${NC}"
    else
        echo -e "${YELLOW}⚠️  Execute manualmente: sudo systemctl start cloudflared${NC}"
    fi
fi

# ========================================
# SALVAR CONFIGURAÇÃO PM2
# ========================================

pm2 save 2>/dev/null

# ========================================
# STATUS FINAL
# ========================================

echo ""
echo "============================================================"
echo "  ✅ SERVIDOR ATUALIZADO COM SUCESSO!"
echo "============================================================"
echo ""

# Status PM2
pm2 status 2>/dev/null || ps aux | grep -E "uvicorn|node"

echo ""
echo -e "${GREEN}URLs Locais (servidor):${NC}"
echo "   FastAPI: http://localhost:8001"
echo "   Dashboard React: http://localhost:8501"
echo ""
echo -e "${GREEN}URLs Públicas:${NC}"
echo "   Landing + API: https://auronex.com.br"
echo "   Admin: https://admin.auronex.com.br"
echo "   Dashboard: https://app.auronex.com.br"
echo ""
echo -e "${YELLOW}Verificar se está funcionando:${NC}"
echo "   curl http://localhost:8001/health"
echo "   curl http://localhost:8501"
echo ""
echo -e "${BLUE}Comandos úteis:${NC}"
echo "   Ver logs: pm2 logs auronex-dashboard"
echo "   Reiniciar: pm2 restart auronex-dashboard"
echo "   Status: pm2 status"
echo "   Parar: pm2 stop all"
echo ""
echo "============================================================"
echo ""

# Testar portas
echo -e "${BLUE}Testando portas...${NC}"

if netstat -tlnp 2>/dev/null | grep -q ":8001"; then
    echo -e "${GREEN}✅ Porta 8001 (FastAPI): ABERTA${NC}"
else
    echo -e "${RED}❌ Porta 8001 (FastAPI): FECHADA${NC}"
fi

if netstat -tlnp 2>/dev/null | grep -q ":8501"; then
    echo -e "${GREEN}✅ Porta 8501 (React): ABERTA${NC}"
else
    echo -e "${RED}❌ Porta 8501 (React): FECHADA${NC}"
fi

echo ""
echo -e "${GREEN}Deploy concluído! Acesse: https://app.auronex.com.br${NC}"
echo ""
