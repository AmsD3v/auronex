#!/bin/bash
# ====================================
# DEPLOY PRODUÇÃO - 4 TERMINAIS
# FastAPI | Bot | React | Tunnel
# ====================================

PROJETO="/home/serverhome/auronex"

# Verificar se tmux está instalado
if ! command -v tmux &> /dev/null; then
    echo "Instalando tmux..."
    sudo apt-get update && sudo apt-get install -y tmux
fi

echo "============================================================"
echo "  PREPARANDO DEPLOY..."
echo "============================================================"

cd "$PROJETO"

# Atualizar banco
sqlite3 db.sqlite3 "ALTER TABLE bot_configuration ADD COLUMN analysis_interval INTEGER DEFAULT 5;" 2>/dev/null
sqlite3 db.sqlite3 "ALTER TABLE bot_configuration ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;" 2>/dev/null

# Git pull
git stash
git pull origin main
git checkout stash -- db.sqlite3 2>/dev/null
git stash drop 2>/dev/null

# Build React
cd auronex-dashboard
npm install
npm run build
cd ..

# Parar tudo
pm2 stop all 2>/dev/null
pm2 delete all 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
pkill -f "cloudflared" 2>/dev/null

echo ""
echo "============================================================"
echo "  INICIANDO 4 SERVIÇOS EM TERMINAIS SEPARADOS..."
echo "============================================================"
echo ""

# Criar sessão tmux com 4 painéis
tmux new-session -d -s auronex

# Painel 1: FastAPI
tmux send-keys -t auronex "cd $PROJETO" C-m
tmux send-keys -t auronex "source venv/bin/activate" C-m
tmux send-keys -t auronex "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload" C-m

# Dividir horizontal (painel 2: Bot Controller)
tmux split-window -h -t auronex
tmux send-keys -t auronex "cd $PROJETO" C-m
tmux send-keys -t auronex "source venv/bin/activate" C-m
tmux send-keys -t auronex "python -m bot.bot_controller" C-m

# Dividir vertical (painel 3: React)
tmux split-window -v -t auronex
tmux send-keys -t auronex "cd $PROJETO/auronex-dashboard" C-m
tmux send-keys -t auronex "npm start" C-m

# Selecionar painel 1 e dividir (painel 4: Tunnel)
tmux select-pane -t auronex:0.0
tmux split-window -v -t auronex
tmux send-keys -t auronex "sudo cloudflared tunnel run auronex" C-m

echo ""
echo "============================================================"
echo "  ✅ SERVIÇOS INICIADOS!"
echo "============================================================"
echo ""
echo "Terminais:"
echo "  1. FastAPI (porta 8001)"
echo "  2. Bot Controller"
echo "  3. Dashboard React (porta 8501)"
echo "  4. Cloudflare Tunnel"
echo ""
echo "Comandos úteis:"
echo "  Ver terminais: tmux attach -t auronex"
echo "  Sair: Ctrl+B depois D"
echo "  Parar tudo: tmux kill-session -t auronex"
echo ""
echo "URLs:"
echo "  https://auronex.com.br"
echo "  https://app.auronex.com.br/"
echo ""
echo "============================================================"

