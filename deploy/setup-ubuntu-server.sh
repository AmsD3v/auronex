#!/bin/bash

# ========================================
# ROBOTRADER - SETUP AUTOMÁTICO UBUNTU
# ========================================

set -e

echo "🚀 ROBOTRADER - Setup Ubuntu Server 22.04"
echo "=========================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se é root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${RED}❌ Execute como root: sudo ./setup-ubuntu-server.sh${NC}"
   exit 1
fi

echo -e "${GREEN}✅ Executando como root${NC}"
echo ""

# 1. ATUALIZAR SISTEMA
echo -e "${YELLOW}[1/10] Atualizando sistema...${NC}"
apt update && apt upgrade -y

# 2. INSTALAR DEPENDÊNCIAS
echo -e "${YELLOW}[2/10] Instalando dependências...${NC}"
apt install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    htop \
    tmux \
    net-tools \
    ufw \
    fail2ban \
    nginx \
    postgresql \
    postgresql-contrib \
    redis-server \
    python3.10 \
    python3.10-venv \
    python3-pip \
    certbot \
    python3-certbot-nginx

# 3. CRIAR USUÁRIO
echo -e "${YELLOW}[3/10] Criar usuário bottrader...${NC}"
if id "bottrader" &>/dev/null; then
    echo "Usuário bottrader já existe"
else
    adduser --disabled-password --gecos "" bottrader
    usermod -aG sudo bottrader
    echo "bottrader:TROCAR_SENHA_AQUI" | chpasswd
    echo -e "${GREEN}✅ Usuário criado. TROQUE A SENHA!${NC}"
fi

# 4. CONFIGURAR FIREWALL
echo -e "${YELLOW}[4/10] Configurando firewall...${NC}"
ufw default deny incoming
ufw default allow outgoing
ufw allow 2222/tcp  # SSH customizado
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
echo "y" | ufw enable
echo -e "${GREEN}✅ Firewall configurado${NC}"

# 5. CRIAR SWAP
echo -e "${YELLOW}[5/10] Criando swap de 4GB...${NC}"
if [ ! -f /swapfile ]; then
    fallocate -l 4G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    sysctl vm.swappiness=10
    echo 'vm.swappiness=10' >> /etc/sysctl.conf
    echo -e "${GREEN}✅ Swap criado${NC}"
else
    echo "Swap já existe"
fi

# 6. OTIMIZAR LIMITES
echo -e "${YELLOW}[6/10] Otimizando limites do sistema...${NC}"
cat >> /etc/security/limits.conf << EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
EOF
sysctl -p

# 7. POSTGRESQL
echo -e "${YELLOW}[7/10] Configurando PostgreSQL...${NC}"
sudo -u postgres psql -c "CREATE DATABASE robotrader;" 2>/dev/null || echo "DB já existe"
sudo -u postgres psql -c "CREATE USER botuser WITH PASSWORD 'TROCAR_SENHA_DB';" 2>/dev/null || echo "User já existe"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE robotrader TO botuser;"
echo -e "${GREEN}✅ PostgreSQL configurado. TROQUE A SENHA!${NC}"

# 8. REDIS
echo -e "${YELLOW}[8/10] Configurando Redis...${NC}"
sed -i 's/^# maxmemory <bytes>/maxmemory 512mb/' /etc/redis/redis.conf
sed -i 's/^# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/' /etc/redis/redis.conf
systemctl restart redis-server

# 9. FAIL2BAN
echo -e "${YELLOW}[9/10] Configurando Fail2Ban...${NC}"
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log
EOF
systemctl enable fail2ban
systemctl start fail2ban

# 10. CRIAR DIRETÓRIOS
echo -e "${YELLOW}[10/10] Criando estrutura de diretórios...${NC}"
mkdir -p /var/log/{django-bot,celery-bot}
mkdir -p /var/run/celery-bot
mkdir -p /home/bottrader/backups
chown -R bottrader:bottrader /var/log/{django-bot,celery-bot}
chown -R bottrader:bottrader /var/run/celery-bot
chown -R bottrader:bottrader /home/bottrader

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ SETUP CONCLUÍDO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}⚠️  AÇÕES NECESSÁRIAS:${NC}"
echo "1. Trocar senha bottrader: sudo passwd bottrader"
echo "2. Trocar senha PostgreSQL: sudo -u postgres psql"
echo "3. Configurar SSH (porta 2222): /etc/ssh/sshd_config"
echo "4. Adicionar chaves SSH: ~/.ssh/authorized_keys"
echo "5. Deploy código: scp/git clone"
echo "6. Configurar .env com secrets"
echo "7. Criar systemd services"
echo "8. Configurar Nginx"
echo "9. Obter SSL: sudo certbot --nginx"
echo ""
echo -e "${GREEN}📖 Guia completo: SERVIDOR_UBUNTU_BOT_TRADING.md${NC}"



