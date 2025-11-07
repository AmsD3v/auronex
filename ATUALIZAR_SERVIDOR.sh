#!/bin/bash
# ========================================
# AURONEX - ATUALIZAR SERVIDOR (1 CLIQUE!)
# ========================================
# Baixa código do GitHub e reinicia serviços
# VERSÃO REACT (substitui Streamlit)

clear

echo "========================================"
echo "  AURONEX - ATUALIZAR SERVIDOR"
echo "========================================"
echo ""

# Confirmar usuário
if [ "$(whoami)" != "serverhome" ]; then
    echo "❌ ERRO: Execute como usuário serverhome!"
    exit 1
fi

# Ir para pasta
cd /home/serverhome/auronex || exit 1

echo "📍 Pasta: $(pwd)"
echo ""

# ========================================
# 1. PARAR SERVIÇOS
# ========================================

echo "1️⃣  Parando serviços..."
echo ""

# Parar FastAPI
echo "  - Parando FastAPI..."
sudo pkill -f "uvicorn fastapi_app.main"

# Parar Streamlit ANTIGO (substituir por React)
echo "  - Parando Streamlit antigo..."
sudo pkill -f "streamlit run dashboard"

# Parar React (se estiver rodando)
echo "  - Parando React..."
sudo pkill -f "next start"

# Parar Cloudflare Tunnel
echo "  - Parando Cloudflare Tunnel..."
sudo pkill -f "cloudflared tunnel run"

echo "  ✅ Serviços parados!"
echo ""

# Aguardar processos terminarem
sleep 3

# ========================================
# 2. BACKUP (SEGURANÇA)
# ========================================

echo "2️⃣  Criando backup..."
echo ""

# Criar pasta backup se não existir
mkdir -p ~/backups

# Backup com data/hora
BACKUP_NAME="auronex_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

# Fazer backup (exceto venv e cache)
tar -czf ~/backups/$BACKUP_NAME \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='*.log' \
    --exclude='node_modules' \
    --exclude='.next' \
    .

echo "  ✅ Backup criado: ~/backups/$BACKUP_NAME"
echo ""

# ========================================
# 3. ATUALIZAR CÓDIGO (GIT PULL)
# ========================================

echo "3️⃣  Baixando atualizações do GitHub..."
echo ""

# Ver versão atual
VERSAO_ANTES=$(cat VERSION.txt 2>/dev/null || echo "Desconhecida")
echo "  Versão atual: $VERSAO_ANTES"

# Stash mudanças locais (banco de dados)
git stash -u

# Pull
git pull origin main

# Ver nova versão
VERSAO_DEPOIS=$(cat VERSION.txt 2>/dev/null || echo "Desconhecida")
echo "  Nova versão: $VERSAO_DEPOIS"
echo ""

# Mostrar mudanças
echo "  📊 Arquivos alterados:"
git diff --stat HEAD@{1} HEAD 2>/dev/null | head -20
echo ""

echo "  ✅ Código atualizado!"
echo ""

# ========================================
# 4. ATUALIZAR DEPENDÊNCIAS PYTHON
# ========================================

echo "4️⃣  Verificando dependências Python..."
echo ""

# Ativar venv
source venv/bin/activate

# Atualizar se requirements.txt mudou
if git diff --name-only HEAD@{1} HEAD | grep -q "requirements.txt"; then
    echo "  📦 requirements.txt mudou - atualizando..."
    pip install -r requirements.txt --quiet --upgrade
    echo "  ✅ Dependências atualizadas!"
else
    echo "  ℹ️  Dependências já atualizadas"
fi

echo ""

# ========================================
# 5. ATUALIZAR DEPENDÊNCIAS REACT
# ========================================

echo "5️⃣  Instalando dependências React..."
echo ""

cd auronex-dashboard

if [ ! -d "node_modules" ]; then
    echo "  Primeira instalação..."
    npm install
else
    echo "  Atualizando..."
    npm install
fi

echo "  ✅ Deps React OK!"
echo ""

# ========================================
# 6. BUILD REACT
# ========================================

echo "6️⃣  Compilando React (produção)..."
echo ""

npm run build

if [ $? -eq 0 ]; then
    echo "  ✅ Build React OK!"
else
    echo "  ❌ Build falhou!"
    exit 1
fi

cd ..
echo ""

# ========================================
# 7. REINICIAR SERVIÇOS
# ========================================

echo "7️⃣  Reiniciando serviços..."
echo ""

# Aguardar portas liberarem
sleep 2

# FastAPI em background (nohup)
echo "  - Iniciando FastAPI (porta 8001)..."
nohup python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 > logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
echo "    PID: $FASTAPI_PID"

sleep 5

# ✅ REACT ao invés de Streamlit! (porta 8501)
echo "  - Iniciando Dashboard React (porta 8501)..."
cd auronex-dashboard
nohup npm start > ../logs/react.log 2>&1 &
REACT_PID=$!
echo "    PID: $REACT_PID"
cd ..

sleep 3

# Cloudflare Tunnel em background
echo "  - Iniciando Cloudflare Tunnel..."
nohup cloudflared tunnel run auronex > logs/tunnel.log 2>&1 &
TUNNEL_PID=$!
echo "    PID: $TUNNEL_PID"

echo ""
echo "  ✅ Serviços reiniciados!"
echo ""

sleep 5

# ========================================
# 8. VERIFICAR STATUS
# ========================================

echo "8️⃣  Verificando status dos serviços..."
echo ""

# FastAPI
if netstat -tlnp 2>/dev/null | grep -q 8001; then
    echo "  ✅ FastAPI: RODANDO (porta 8001)"
else
    echo "  ❌ FastAPI: ERRO"
fi

# React (porta 8501 - mesma do Streamlit!)
if netstat -tlnp 2>/dev/null | grep -q 8501; then
    echo "  ✅ Dashboard React: RODANDO (porta 8501)"
else
    echo "  ❌ Dashboard React: ERRO"
fi

# Cloudflare Tunnel
if ps aux | grep -q "cloudflared tunnel run"; then
    echo "  ✅ Cloudflare Tunnel: CONECTADO"
else
    echo "  ❌ Cloudflare Tunnel: ERRO"
fi

echo ""

# ========================================
# 9. INFORMAÇÕES FINAIS
# ========================================

echo "========================================"
echo "  ✅ ATUALIZAÇÃO COMPLETA!"
echo "========================================"
echo ""
echo "Versão: $VERSAO_ANTES → $VERSAO_DEPOIS"
echo ""
echo "🌐 ACESSAR SISTEMA:"
echo ""
echo "  Site: https://auronex.com.br/"
echo "  Dashboard: https://app.auronex.com.br/"
echo ""
echo "📊 MONITORAR LOGS:"
echo ""
echo "  FastAPI:   tail -f logs/fastapi.log"
echo "  React:     tail -f logs/react.log"
echo "  Tunnel:    tail -f logs/tunnel.log"
echo ""
echo "🔄 PARAR SERVIÇOS:"
echo ""
echo "  kill $FASTAPI_PID $REACT_PID $TUNNEL_PID"
echo ""
echo "========================================"
echo "  Sistema operacional!"
echo "========================================"
echo ""

# Salvar PIDs em arquivo
echo "FASTAPI_PID=$FASTAPI_PID" > /tmp/auronex_pids.txt
echo "REACT_PID=$REACT_PID" >> /tmp/auronex_pids.txt
echo "TUNNEL_PID=$TUNNEL_PID" >> /tmp/auronex_pids.txt

echo "PIDs salvos em: /tmp/auronex_pids.txt"
echo ""
