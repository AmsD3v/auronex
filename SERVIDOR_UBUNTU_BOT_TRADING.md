# 🖥️ SERVIDOR UBUNTU 22.04 - BOT TRADING PROFISSIONAL

**Hardware:** Intel i7-3517U | 4GB RAM | 240GB SSD  
**OS:** Ubuntu Server 22.04 LTS  
**Uso:** Trading Bot 24/7 + Django + Streamlit  
**Otimização:** Performance + Segurança Enterprise

---

## 📋 **ÍNDICE**

1. [Instalação Inicial](#1-instalação-inicial)
2. [Segurança](#2-segurança)
3. [Otimização](#3-otimização)
4. [Deploy Bot](#4-deploy-bot)
5. [Monitoramento](#5-monitoramento)
6. [Backup](#6-backup)
7. [Manutenção](#7-manutenção)

---

## 1. INSTALAÇÃO INICIAL

### **1.1. Primeiro Boot Ubuntu Server**

```bash
# Login: usuario criado na instalação
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar ferramentas essenciais
sudo apt install -y \
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
```

### **1.2. Criar Usuário para o Bot**

```bash
# Criar usuário dedicado (segurança)
sudo adduser bottrader
sudo usermod -aG sudo bottrader

# Trocar para novo usuário
su - bottrader
```

---

## 2. SEGURANÇA

### **2.1. Firewall (UFW)**

```bash
# Configurar firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir SSH (MUDE A PORTA!)
sudo ufw allow 2222/tcp  # Nova porta SSH

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar firewall
sudo ufw enable
sudo ufw status verbose
```

### **2.2. SSH Seguro**

```bash
# Editar config SSH
sudo vim /etc/ssh/sshd_config

# Adicionar/modificar:
Port 2222                      # Mudar porta padrão
PermitRootLogin no             # Bloquear root
PasswordAuthentication no      # Só chaves SSH
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2

# Reiniciar SSH
sudo systemctl restart sshd
```

### **2.3. Fail2Ban (Anti-Bruteforce)**

```bash
# Configurar Fail2Ban
sudo vim /etc/fail2ban/jail.local

# Adicionar:
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log

# Iniciar Fail2Ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### **2.4. Chaves SSH (Acesso Seguro)**

**No seu PC Windows:**
```powershell
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"

# Copiar chave pública
Get-Content ~/.ssh/id_ed25519.pub | clip
```

**No Ubuntu Server:**
```bash
# Adicionar chave autorizada
mkdir -p ~/.ssh
vim ~/.ssh/authorized_keys
# Cole a chave pública aqui
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## 3. OTIMIZAÇÃO

### **3.1. Swap (Compensar 4GB RAM)**

```bash
# Criar swap de 4GB
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Tornar permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Otimizar swappiness (usar RAM primeiro)
sudo sysctl vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
```

### **3.2. Limites de Sistema**

```bash
# Aumentar limites para trading (muitas conexões)
sudo vim /etc/security/limits.conf

# Adicionar:
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768

# Aplicar
sudo sysctl -p
```

### **3.3. PostgreSQL para Produção**

```bash
# Configurar PostgreSQL
sudo -u postgres psql

-- Criar database e usuário
CREATE DATABASE robotrader;
CREATE USER botuser WITH PASSWORD 'SENHA_SUPER_FORTE_AQUI';
GRANT ALL PRIVILEGES ON DATABASE robotrader TO botuser;
\q

# Otimizar PostgreSQL para 4GB RAM
sudo vim /etc/postgresql/14/main/postgresql.conf

# Modificar:
shared_buffers = 1GB                 # 25% da RAM
effective_cache_size = 3GB           # 75% da RAM
maintenance_work_mem = 256MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1               # SSD!
effective_io_concurrency = 200       # SSD!
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### **3.4. Redis para Cache**

```bash
# Otimizar Redis
sudo vim /etc/redis/redis.conf

# Modificar:
maxmemory 512mb
maxmemory-policy allkeys-lru
save ""  # Desativar persistência (cache volátil)

# Reiniciar Redis
sudo systemctl restart redis-server
```

---

## 4. DEPLOY BOT

### **4.1. Clonar Projeto**

```bash
# Ir para home
cd ~

# Clonar do GitHub (ou transferir arquivos)
git clone https://github.com/SEU_USUARIO/robotrader.git
cd robotrader

# Ou transferir via SCP do Windows:
# scp -P 2222 -r I:\Robo bottrader@IP_SERVIDOR:~/robotrader
```

### **4.2. Ambiente Virtual**

```bash
# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Instalar gunicorn (produção)
pip install gunicorn psycopg2-binary
```

### **4.3. Variáveis de Ambiente**

```bash
# Criar .env de produção
vim ~/robotrader/.env

# Adicionar:
DEBUG=False
DJANGO_SECRET_KEY='GERAR_NOVA_CHAVE_SUPER_LONGA_AQUI'
DATABASE_URL=postgresql://botuser:SENHA@localhost:5432/robotrader
REDIS_URL=redis://localhost:6379/0
SITE_URL=https://seudominio.com

# Stripe (PROD!)
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Mercado Pago (PROD!)
MERCADOPAGO_PUBLIC_KEY=APP_USR-...
MERCADOPAGO_ACCESS_TOKEN=APP_USR-...

# Encryption
ENCRYPTION_KEY='GERAR_NOVA_CHAVE_FERNET_AQUI'

# Exchanges (criptografados!)
# Usuários configuram via dashboard
```

### **4.4. Migrations e Static**

```bash
cd ~/robotrader/saas

# Migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Collectstatic
python manage.py collectstatic --noinput
```

### **4.5. Systemd Services**

**Django (Gunicorn):**
```bash
sudo vim /etc/systemd/system/django-bot.service

# Conteúdo:
[Unit]
Description=RoboTrader Django
After=network.target postgresql.service

[Service]
Type=notify
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/robotrader/saas
Environment="PATH=/home/bottrader/robotrader/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=saas.settings"
ExecStart=/home/bottrader/robotrader/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/bottrader/robotrader/gunicorn.sock \
    --access-logfile /var/log/django-bot/access.log \
    --error-logfile /var/log/django-bot/error.log \
    --log-level info \
    saas.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Streamlit:**
```bash
sudo vim /etc/systemd/system/streamlit-bot.service

# Conteúdo:
[Unit]
Description=RoboTrader Streamlit Dashboard
After=network.target django-bot.service

[Service]
Type=simple
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/robotrader
Environment="PATH=/home/bottrader/robotrader/venv/bin"
ExecStart=/home/bottrader/robotrader/venv/bin/streamlit run dashboard_master.py \
    --server.port 8501 \
    --server.address 127.0.0.1 \
    --server.headless true

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Bot Trading (Celery Worker):**
```bash
sudo vim /etc/systemd/system/celery-bot.service

# Conteúdo:
[Unit]
Description=Celery Worker for Trading Bot
After=network.target redis.service

[Service]
Type=forking
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/robotrader/saas
Environment="PATH=/home/bottrader/robotrader/venv/bin"
ExecStart=/home/bottrader/robotrader/venv/bin/celery -A saas worker \
    --loglevel=info \
    --logfile=/var/log/celery-bot/worker.log \
    --pidfile=/var/run/celery-bot/worker.pid

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Celery Beat (Scheduler):**
```bash
sudo vim /etc/systemd/system/celerybeat-bot.service

# Conteúdo:
[Unit]
Description=Celery Beat Scheduler
After=network.target redis.service

[Service]
Type=simple
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/robotrader/saas
Environment="PATH=/home/bottrader/robotrader/venv/bin"
ExecStart=/home/bottrader/robotrader/venv/bin/celery -A saas beat \
    --loglevel=info \
    --logfile=/var/log/celery-bot/beat.log \
    --pidfile=/var/run/celery-bot/beat.pid

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Criar logs:**
```bash
sudo mkdir -p /var/log/{django-bot,celery-bot}
sudo mkdir -p /var/run/celery-bot
sudo chown -R bottrader:bottrader /var/log/{django-bot,celery-bot}
sudo chown -R bottrader:bottrader /var/run/celery-bot
```

**Ativar todos:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable django-bot streamlit-bot celery-bot celerybeat-bot
sudo systemctl start django-bot streamlit-bot celery-bot celerybeat-bot

# Verificar status
sudo systemctl status django-bot
sudo systemctl status streamlit-bot
sudo systemctl status celery-bot
sudo systemctl status celerybeat-bot
```

### **4.6. Nginx Reverse Proxy**

```bash
sudo vim /etc/nginx/sites-available/robotrader

# Conteúdo:
upstream django {
    server unix:/home/bottrader/robotrader/gunicorn.sock fail_timeout=0;
}

upstream streamlit {
    server 127.0.0.1:8501;
}

# Redirecionar HTTP → HTTPS
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name seudominio.com www.seudominio.com;

    # SSL (Certbot configurará depois)
    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Django (API + Admin + Frontend)
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /home/bottrader/robotrader/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /home/bottrader/robotrader/media/;
        expires 30d;
    }

    # Streamlit Dashboard
    location /dashboard-stream/ {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Rate limiting (anti-DDoS)
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    client_max_body_size 10M;
}

# Ativar site
sudo ln -s /etc/nginx/sites-available/robotrader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **4.7. SSL (Let's Encrypt)**

```bash
# Certbot automático
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Renovação automática (já configurado)
sudo certbot renew --dry-run
```

---

## 5. MONITORAMENTO

### **5.1. Logs Centralizados**

```bash
# Ver logs em tempo real
sudo journalctl -u django-bot -f
sudo journalctl -u streamlit-bot -f
sudo journalctl -u celery-bot -f

# Logs específicos
tail -f /var/log/django-bot/error.log
tail -f /var/log/celery-bot/worker.log
```

### **5.2. Monitoramento de Recursos**

```bash
# Instalar htop melhorado
sudo apt install htop

# Monitorar em tempo real
htop

# Uso de disco
df -h
du -sh /home/bottrader/robotrader/*

# Memória
free -h

# Processos Python
ps aux | grep python
```

### **5.3. Alertas (Opcional - Uptime Robot)**

1. Criar conta: https://uptimerobot.com/
2. Adicionar monitor: `https://seudominio.com/health/`
3. Email de alerta se cair

### **5.4. Dashboard de Monitoramento (Opcional)**

```bash
# Instalar Grafana + Prometheus (avançado)
# https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/
```

---

## 6. BACKUP

### **6.1. Backup Banco de Dados**

```bash
# Criar script de backup
vim ~/backup-db.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/bottrader/backups"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
sudo -u postgres pg_dump robotrader > $BACKUP_DIR/db_$DATE.sql

# Compactar
gzip $BACKUP_DIR/db_$DATE.sql

# Manter apenas últimos 7 dias
find $BACKUP_DIR -type f -name "*.gz" -mtime +7 -delete

echo "Backup concluído: db_$DATE.sql.gz"

# Tornar executável
chmod +x ~/backup-db.sh
```

### **6.2. Cron para Backup Automático**

```bash
# Editar crontab
crontab -e

# Adicionar (backup diário às 3h)
0 3 * * * /home/bottrader/backup-db.sh >> /var/log/backup.log 2>&1

# Backup código (semanal domingo 2h)
0 2 * * 0 tar -czf /home/bottrader/backups/code_$(date +\%Y\%m\%d).tar.gz /home/bottrader/robotrader
```

### **6.3. Backup Remoto (Opcional)**

```bash
# Via rsync para outro servidor
rsync -avz -e "ssh -p 2222" /home/bottrader/backups/ usuario@servidor-backup:/backups/robotrader/
```

---

## 7. MANUTENÇÃO

### **7.1. Atualizar Sistema**

```bash
# Mensal
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### **7.2. Atualizar Bot**

```bash
cd ~/robotrader
source venv/bin/activate

# Pull código
git pull origin main

# Atualizar dependências
pip install -r requirements.txt --upgrade

# Migrations
cd saas
python manage.py migrate
python manage.py collectstatic --noinput

# Reiniciar serviços
sudo systemctl restart django-bot streamlit-bot celery-bot celerybeat-bot
```

### **7.3. Limpeza**

```bash
# Limpar logs antigos (mensal)
sudo journalctl --vacuum-time=30d

# Limpar cache
sudo apt clean
sudo apt autoclean
sudo apt autoremove -y
```

### **7.4. Verificação de Saúde**

```bash
# Script de health check
vim ~/health-check.sh

#!/bin/bash
echo "=== HEALTH CHECK ==="
echo ""

# Serviços
systemctl is-active django-bot || echo "❌ Django PARADO"
systemctl is-active streamlit-bot || echo "❌ Streamlit PARADO"
systemctl is-active celery-bot || echo "❌ Celery PARADO"
systemctl is-active postgresql || echo "❌ PostgreSQL PARADO"
systemctl is-active redis-server || echo "❌ Redis PARADO"
systemctl is-active nginx || echo "❌ Nginx PARADO"

# Recursos
echo ""
echo "=== RECURSOS ==="
free -h | grep Mem
df -h | grep "/$"

# Processos Python
echo ""
echo "=== PROCESSOS PYTHON ==="
ps aux | grep python | grep -v grep | wc -l

echo ""
echo "✅ Health check concluído!"

chmod +x ~/health-check.sh
```

---

## 📊 **OTIMIZAÇÕES ESPECÍFICAS TRADING**

### **Trading Bot Performance:**

```python
# settings.py produção

# Conexões DB otimizadas
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Conexões persistentes
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'
        }
    }
}

# Cache agressivo
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True
            }
        },
        'TIMEOUT': 300
    }
}

# Celery otimizado
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 4
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000
```

---

## 🔒 **CHECKLIST SEGURANÇA FINAL**

- [ ] ✅ Firewall ativo (UFW)
- [ ] ✅ SSH porta customizada (não 22)
- [ ] ✅ SSH sem senha (só chaves)
- [ ] ✅ Fail2Ban configurado
- [ ] ✅ PostgreSQL senha forte
- [ ] ✅ .env com secrets
- [ ] ✅ SSL/HTTPS ativo
- [ ] ✅ Nginx headers segurança
- [ ] ✅ Backup automático
- [ ] ✅ Usuário dedicado (não root)
- [ ] ✅ Rate limiting API

---

## 📈 **PERFORMANCE ESPERADA**

**Hardware:** i7-3517U | 4GB RAM | SSD

**Capacidade:**
- ✅ 50-100 usuários simultâneos
- ✅ 10-20 bots rodando em paralelo
- ✅ 1000+ requisições/minuto
- ✅ Latência < 100ms (API)
- ✅ 99.9% uptime

---

## 🆘 **TROUBLESHOOTING**

**Serviço não inicia:**
```bash
sudo systemctl status NOME_SERVICO
sudo journalctl -u NOME_SERVICO -n 50
```

**Alto uso memória:**
```bash
htop
# Verificar se swap está ativo
free -h
```

**Bot não conecta exchange:**
```bash
# Verificar logs Celery
tail -f /var/log/celery-bot/worker.log
```

**Webhook PIX não funciona:**
```bash
# Verificar se porta 443 está aberta
sudo ufw status
# Verificar logs Django
tail -f /var/log/django-bot/error.log
```

---

## 📞 **SUPORTE**

**Logs importantes:**
```bash
/var/log/django-bot/error.log
/var/log/celery-bot/worker.log
/var/log/nginx/error.log
sudo journalctl -u django-bot -n 100
```

---

**🚀 SERVIDOR PRONTO PARA PRODUÇÃO 24/7!**

**Tempo estimado setup completo:** 2-3 horas  
**Manutenção:** 30min/mês  
**Custo:** Apenas energia elétrica do notebook!



