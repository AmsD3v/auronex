#!/bin/bash
# ========================================
# COMANDOS DIRETOS - SEM SCRIPT
# Execute linha por linha no servidor
# ========================================

# COPIE E COLE ESTES COMANDOS NO SERVIDOR (SSH):

echo "Executando comandos diretos..."

# 1. Ir para pasta
cd /home/serverhome/auronex/auronex-dashboard

# 2. Limpar TUDO
rm -rf node_modules .next

# 3. Instalar TODAS dependências (não usar --production!)
npm install

# 4. Build
npm run build

# 5. Iniciar com PM2
pm2 delete auronex-dashboard 2>/dev/null
pm2 start ecosystem.config.js
pm2 save

# 6. Ver status
pm2 status

echo "Pronto!"

