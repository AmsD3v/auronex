#!/bin/bash

# ========================================
# SETUP NODE.JS NO SERVIDOR
# Instala Node.js 20 LTS + PM2
# ========================================

clear

echo ""
echo "============================================================"
echo "  AURONEX - INSTALAR NODE.JS NO SERVIDOR"
echo "============================================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ========================================
# 1. VERIFICAR SE JÁ TEM NODE.JS
# ========================================

echo -e "${YELLOW}[1/5] Verificando Node.js...${NC}"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js já instalado: $NODE_VERSION${NC}"
    echo ""
    echo "Deseja reinstalar? (S/N)"
    read -r REINSTALL
    
    if [ "$REINSTALL" != "S" ] && [ "$REINSTALL" != "s" ]; then
        echo "Pulando instalação do Node.js"
        exit 0
    fi
fi

echo ""

# ========================================
# 2. INSTALAR NODE.JS 20 LTS
# ========================================

echo -e "${YELLOW}[2/5] Instalando Node.js 20 LTS...${NC}"
echo ""

# Adicionar repositório NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao adicionar repositório NodeSource${NC}"
    exit 1
fi

# Instalar Node.js
sudo apt-get install -y nodejs

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Node.js instalado${NC}"
else
    echo -e "${RED}❌ Erro ao instalar Node.js${NC}"
    exit 1
fi

echo ""

# ========================================
# 3. VERIFICAR INSTALAÇÃO
# ========================================

echo -e "${YELLOW}[3/5] Verificando instalação...${NC}"

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)

echo -e "${GREEN}✅ Node.js: $NODE_VERSION${NC}"
echo -e "${GREEN}✅ npm: $NPM_VERSION${NC}"

echo ""

# ========================================
# 4. INSTALAR PM2 GLOBALMENTE
# ========================================

echo -e "${YELLOW}[4/5] Instalando PM2...${NC}"

sudo npm install -g pm2

if [ $? -eq 0 ]; then
    PM2_VERSION=$(pm2 --version)
    echo -e "${GREEN}✅ PM2 instalado: v$PM2_VERSION${NC}"
else
    echo -e "${RED}❌ Erro ao instalar PM2${NC}"
    exit 1
fi

echo ""

# ========================================
# 5. CONFIGURAR PM2 STARTUP
# ========================================

echo -e "${YELLOW}[5/5] Configurando PM2 para iniciar no boot...${NC}"
echo ""

# Gerar comando de startup
pm2 startup

echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE: Copie e execute o comando acima!${NC}"
echo -e "   Exemplo: sudo env PATH=\$PATH:/usr/bin pm2 startup systemd -u serverhome --hp /home/serverhome"
echo ""
echo "Pressione ENTER após executar o comando..."
read

# ========================================
# STATUS FINAL
# ========================================

echo ""
echo "============================================================"
echo "  ✅ NODE.JS CONFIGURADO COM SUCESSO!"
echo "============================================================"
echo ""
echo "Versões instaladas:"
echo "  Node.js: $(node --version)"
echo "  npm: $(npm --version)"
echo "  PM2: v$(pm2 --version)"
echo ""
echo "Próximos passos:"
echo "  1. Executar: ./ATUALIZAR_SERVIDOR_REACT.sh"
echo "  2. Aguardar build (~3 min)"
echo "  3. Acessar: https://app.auronex.com.br"
echo ""
echo "============================================================"
echo ""

