# 🌐 GUIA DEFINITIVO - AURONEX.COM.BR NO XUBUNTU

**Domínio:** https://auronex.com.br ✅ (Já comprado!)  
**Servidor:** Notebook Xubuntu 22.04  
**Hardware:** i7-3517U | 4GB RAM | 240GB SSD  
**Objetivo:** Bot trading 24/7 profissional

---

## 📋 **ÍNDICE RÁPIDO**

**Tempo total: ~2 horas**

1. [Preparar Xubuntu](#1-preparar-xubuntu) - 30min
2. [Transferir Código](#2-transferir-código) - 10min
3. [Deploy Bot](#3-deploy-bot) - 20min
4. [Configurar Domínio](#4-configurar-domínio) - 15min
5. [SSL/HTTPS](#5-ssl-https) - 10min
6. [Testar Tudo](#6-testar-tudo) - 15min
7. [Monitoramento](#7-monitoramento) - 10min

---

## 1. PREPARAR XUBUNTU

### **IMPORTANTE: Execute no Xubuntu (notebook servidor)!**

### **1.1. Login Inicial:**

```bash
# Login com usuário criado na instalação do Xubuntu
# Senha que definiu durante instalação
```

### **1.2. Instalar SSH (ESSENCIAL!):**

```bash
# Abrir terminal (Ctrl + Alt + T)

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar SSH Server
sudo apt install openssh-server -y

# Iniciar SSH
sudo systemctl start ssh
sudo systemctl enable ssh

# Verificar
sudo systemctl status ssh
# Deve mostrar: "active (running)" ✅

# Anotar seu IP
hostname -I
# Exemplo: 192.168.15.138  ← Anote!
```

**✅ AGORA pode conectar do Windows!**

```powershell
# Do Windows:
ssh seu_usuario@192.168.15.138
# Digite a senha
# ✅ Conectado!
```

---

### **1.3. Setup Completo Automático:**

```bash
# Criar usuário dedicado
sudo adduser bottrader
# Senha: SENHA_FORTE_AQUI
# Aceitar padrões (Enter em tudo)

# Adicionar ao sudo
sudo usermod -aG sudo bottrader

# Trocar para bottrader
su - bottrader
# Digite senha do bottrader
```

### **1.4. Instalar Dependências:**

```bash
# Ferramentas essenciais
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    nano \
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

# Verificar versões
python3 --version  # 3.10.x
nginx -v          # 1.18.x
psql --version    # 14.x
```

### **1.5. Configurar Firewall:**

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status verbose
```

### **1.6. Criar Swap 4GB:**

```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo sysctl vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
free -h  # Verificar - deve mostrar 4GB swap
```

### **1.7. PostgreSQL:**

```bash
# Criar database
sudo -u postgres psql << EOF
CREATE DATABASE auronex;
CREATE USER botuser WITH PASSWORD 'SENHA_DB_SUPER_FORTE';
GRANT ALL PRIVILEGES ON DATABASE auronex TO botuser;
\q
EOF

# Verificar
sudo -u postgres psql -l | grep auronex
```

### **1.8. Redis:**

```bash
# Otimizar Redis
sudo nano /etc/redis/redis.conf

# Modificar (Ctrl + W para buscar):
maxmemory 512mb
maxmemory-policy allkeys-lru

# Salvar: Ctrl + O → Enter → Ctrl + X

# Reiniciar
sudo systemctl restart redis-server
sudo systemctl status redis-server
```

---

## 2. TRANSFERIR CÓDIGO

### **2.1. Do Windows para Xubuntu:**

**No Windows (PowerShell):**

```powershell
# Transferir via SCP
scp -r I:\Robo bottrader@192.168.15.138:~/auronex

# Digite senha do bottrader
# Aguarde transferência (~5-10 minutos)
```

**Ou via Git (se tiver repositório):**

```bash
# No Xubuntu:
cd ~
git clone https://github.com/SEU_USUARIO/auronex.git
cd auronex
```

---

## 3. DEPLOY BOT

### **3.1. Criar Ambiente Virtual:**

```bash
cd ~/auronex
python3 -m venv venv
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Instalar extras produção
pip install gunicorn psycopg2-binary
```

### **3.2. Configurar .env:**

```bash
nano ~/auronex/.env

# Cole e preencha:
DEBUG=False
DJANGO_SECRET_KEY='gere_chave_aqui'
DATABASE_URL=postgresql://botuser:SENHA_DB@localhost:5432/auronex
REDIS_URL=redis://localhost:6379/0
SITE_URL=https://auronex.com.br

# Stripe PRODUÇÃO
STRIPE_PUBLIC_KEY=pk_live_51SN37vRjxbCNnFAQ14aGnoYQd5YElcrVB4hKXa98M42R0Qun9p7DN64ff2SDu0u24IJjIS06cGSYzajaeau9fpOc00JgDpcJhI
STRIPE_SECRET_KEY=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

# Mercado Pago PRODUÇÃO (quando ativar)
MERCADOPAGO_PUBLIC_KEY=APP_USR_sua_chave
MERCADOPAGO_ACCESS_TOKEN=APP_USR_seu_token

# Encryption
ENCRYPTION_KEY='7aJpcn7FFrn_WbhNFHe6fi5nSIg12a30Z262gt1p_tQ='

# Salvar: Ctrl + O → Enter → Ctrl + X
```

**Gerar chaves:**
```bash
# Secret Key Django
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **3.3. Migrations e Static:**

```bash
cd ~/auronex/saas
source ../venv/bin/activate

# Migrations
python manage.py migrate

# Superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@auronex.com.br
# Password: SENHA_ADMIN_FORTE

# Static files
python manage.py collectstatic --noinput
```

### **3.4. Criar Systemd Services:**

**Django:**
```bash
sudo nano /etc/systemd/system/auronex-django.service

# Cole:
[Unit]
Description=Auronex Django API
After=network.target postgresql.service

[Service]
Type=notify
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/auronex/saas
Environment="PATH=/home/bottrader/auronex/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=saas.settings"
ExecStart=/home/bottrader/auronex/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/bottrader/auronex/gunicorn.sock \
    --access-logfile /var/log/auronex/access.log \
    --error-logfile /var/log/auronex/error.log \
    --log-level info \
    saas.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Salvar: Ctrl + O → Enter → Ctrl + X
```

**Streamlit:**
```bash
sudo nano /etc/systemd/system/auronex-streamlit.service

# Cole:
[Unit]
Description=Auronex Streamlit Dashboard
After=network.target auronex-django.service

[Service]
Type=simple
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/auronex
Environment="PATH=/home/bottrader/auronex/venv/bin"
ExecStart=/home/bottrader/auronex/venv/bin/streamlit run dashboard_master.py \
    --server.port 8501 \
    --server.address 127.0.0.1 \
    --server.headless true

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Salvar: Ctrl + O → Enter → Ctrl + X
```

**Celery:**
```bash
sudo nano /etc/systemd/system/auronex-celery.service

# Cole:
[Unit]
Description=Auronex Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=bottrader
Group=bottrader
WorkingDirectory=/home/bottrader/auronex/saas
Environment="PATH=/home/bottrader/auronex/venv/bin"
ExecStart=/home/bottrader/auronex/venv/bin/celery -A saas worker \
    --loglevel=info \
    --logfile=/var/log/auronex/celery.log \
    --pidfile=/var/run/auronex/celery.pid

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Salvar: Ctrl + O → Enter → Ctrl + X
```

**Criar logs:**
```bash
sudo mkdir -p /var/log/auronex
sudo mkdir -p /var/run/auronex
sudo chown -R bottrader:bottrader /var/log/auronex
sudo chown -R bottrader:bottrader /var/run/auronex
```

**Iniciar tudo:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable auronex-django auronex-streamlit auronex-celery
sudo systemctl start auronex-django auronex-streamlit auronex-celery

# Verificar
sudo systemctl status auronex-django
sudo systemctl status auronex-streamlit
sudo systemctl status auronex-celery
```

---

## 4. CONFIGURAR DOMÍNIO

### **4.1. Descobrir IP Público:**

```bash
# No Xubuntu
curl ifconfig.me

# Anote o IP (exemplo: 177.50.100.200)
```

### **4.2. Configurar DNS (onde comprou domínio):**

**No painel de controle do registro.br ou onde comprou:**

```
Tipo: A
Nome: @
Conteúdo: SEU_IP_PUBLICO (ex: 177.50.100.200)
TTL: 3600

Tipo: A
Nome: www
Conteúdo: SEU_IP_PUBLICO
TTL: 3600

Tipo: CNAME
Nome: api
Conteúdo: auronex.com.br
TTL: 3600
```

**Salvar e aguardar propagação (5min a 24h)**

**Testar propagação:**
```bash
# No Xubuntu ou Windows
nslookup auronex.com.br
# Deve retornar seu IP público
```

### **4.3. Port Forwarding no Roteador:**

```
Painel admin do roteador (ex: 192.168.15.1)

Adicionar regras:
1. Porta Externa: 80 → IP: 192.168.15.138 → Porta: 80
2. Porta Externa: 443 → IP: 192.168.15.138 → Porta: 443
3. Porta Externa: 22 → IP: 192.168.15.138 → Porta: 22

Salvar e reiniciar roteador
```

---

## 5. NGINX + SSL

### **5.1. Configurar Nginx:**

```bash
sudo nano /etc/nginx/sites-available/auronex

# Cole esta configuração completa:
```

```nginx
upstream django {
    server unix:/home/bottrader/auronex/gunicorn.sock;
}

upstream streamlit {
    server 127.0.0.1:8501;
}

# HTTP → HTTPS redirect
server {
    listen 80;
    server_name auronex.com.br www.auronex.com.br;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name auronex.com.br www.auronex.com.br;

    # SSL (Certbot configurará)
    # ssl_certificate /etc/letsencrypt/live/auronex.com.br/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/auronex.com.br/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Logs
    access_log /var/log/nginx/auronex_access.log;
    error_log /var/log/nginx/auronex_error.log;

    # Django (API + Admin + Frontend)
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/bottrader/auronex/staticfiles/;
        expires 30d;
    }

    # Streamlit Dashboard
    location /dashboard-stream/ {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # Webhooks (sem rate limit)
    location /api/payment/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Salvar: Ctrl + O → Enter → Ctrl + X**

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/auronex /etc/nginx/sites-enabled/

# Remover default
sudo rm /etc/nginx/sites-enabled/default

# Testar config
sudo nginx -t

# Reiniciar
sudo systemctl restart nginx
```

### **5.2. Obter SSL (HTTPS):**

```bash
# Let's Encrypt (GRÁTIS!)
sudo certbot --nginx -d auronex.com.br -d www.auronex.com.br

# Email: seu@email.com
# ToS: Y
# Compartilhar: N
# Redirecionar: 2 (Yes)

# Pronto! SSL ativo! ✅
```

**Renovação automática já configurada!**

---

## 6. TESTAR TUDO

### **6.1. Testar Localmente:**

```bash
# No Xubuntu
curl http://localhost
# Deve retornar HTML

curl http://auronex.com.br
# Deve redirecionar ou retornar HTML
```

### **6.2. Testar do Windows:**

**Navegador:**
```
https://auronex.com.br  ← Deve abrir landing page! ✅
https://auronex.com.br/admin/  ← Admin panel
```

**Cadastro:**
```
https://auronex.com.br/register/
→ Criar conta
→ Escolher plano
→ Pagar (Stripe/PIX)
→ ✅ Tudo funcionando!
```

---

## 7. MONITORAMENTO

### **7.1. Ver Logs:**

```bash
# Django
sudo journalctl -u auronex-django -f

# Streamlit
sudo journalctl -u auronex-streamlit -f

# Celery
tail -f /var/log/auronex/celery.log

# Nginx
tail -f /var/log/nginx/auronex_error.log
```

### **7.2. Health Check:**

```bash
# Criar script
nano ~/health.sh

# Cole:
#!/bin/bash
echo "=== AURONEX HEALTH ==="
systemctl is-active auronex-django && echo "Django: OK" || echo "Django: PARADO"
systemctl is-active auronex-streamlit && echo "Streamlit: OK" || echo "Streamlit: PARADO"
systemctl is-active auronex-celery && echo "Celery: OK" || echo "Celery: PARADO"
free -h | grep Mem
df -h / | tail -1

# Salvar e sair

chmod +x ~/health.sh
./health.sh
```

### **7.3. Backup Automático:**

```bash
# Criar script backup
nano ~/backup.sh

# Cole:
#!/bin/bash
DATE=$(date +%Y%m%d)
sudo -u postgres pg_dump auronex | gzip > ~/backups/db_$DATE.sql.gz
find ~/backups -name "*.gz" -mtime +7 -delete

# Salvar e sair

chmod +x ~/backup.sh
mkdir -p ~/backups

# Agendar (diário 3h)
crontab -e
# Adicionar:
0 3 * * * /home/bottrader/backup.sh
```

---

## 8. CONFIGURAÇÕES FINAIS

### **8.1. Atualizar URLs no Código:**

```bash
# Editar settings.py
nano ~/auronex/saas/settings.py

# Verificar:
SITE_URL = 'https://auronex.com.br'
ALLOWED_HOSTS = ['auronex.com.br', 'www.auronex.com.br', 'localhost']

# Salvar

# Reiniciar
sudo systemctl restart auronex-django
```

### **8.2. Webhook PIX (Produção):**

```
Mercado Pago Dashboard:
Webhook URL: https://auronex.com.br/api/payment/mercadopago-webhook/

Stripe Dashboard:
Webhook URL: https://auronex.com.br/api/payment/webhook/
```

---

## ✅ **RESULTADO FINAL:**

```
✅ https://auronex.com.br (SSL ativo!)
✅ Cadastro funcionando
✅ Pagamentos Stripe + PIX
✅ Dashboard Streamlit
✅ Admin panel
✅ Bot trading 24/7
✅ Backup automático
✅ Monitoramento ativo
✅ Auto-restart se cair
```

---

## 📊 **URLS FINAIS:**

```
Landing:   https://auronex.com.br/
Cadastro:  https://auronex.com.br/register/
Login:     https://auronex.com.br/login/
Dashboard: https://auronex.com.br/dashboard/
Admin:     https://auronex.com.br/admin/
API:       https://auronex.com.br/api/
```

---

## 🎯 **COMANDOS RÁPIDOS:**

### **Reiniciar tudo:**
```bash
sudo systemctl restart auronex-django auronex-streamlit auronex-celery nginx
```

### **Ver status:**
```bash
./health.sh
```

### **Ver logs:**
```bash
sudo journalctl -u auronex-django -f
```

### **Atualizar código:**
```bash
cd ~/auronex
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
cd saas
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart auronex-django auronex-streamlit auronex-celery
```

---

## 📞 **SUPORTE:**

**Problema Django caindo:**
```bash
# Ver logs
sudo journalctl -u auronex-django -n 100

# Reiniciar
sudo systemctl restart auronex-django

# Ver se está rodando
sudo systemctl status auronex-django
```

**Problema SSL:**
```bash
# Verificar certificado
sudo certbot certificates

# Renovar
sudo certbot renew
```

**Problema DNS:**
```bash
# Verificar propagação
nslookup auronex.com.br

# Aguardar até 24h
```

---

## 🚀 **TEMPO ESTIMADO:**

```
Setup Xubuntu: 30 min
Transferir código: 10 min
Deploy bot: 20 min
Nginx + SSL: 10 min
Testar: 15 min
Configurar backup: 10 min

TOTAL: ~1h30 (trabalho real)
+ Aguardar DNS: 5min a 24h
```

---

## ✅ **CHECKLIST FINAL:**

- [ ] SSH instalado e funcionando
- [ ] Código transferido
- [ ] Venv criado e deps instaladas
- [ ] .env configurado
- [ ] PostgreSQL criado
- [ ] Migrations aplicadas
- [ ] Systemd services criados
- [ ] Nginx configurado
- [ ] DNS apontando para IP
- [ ] SSL/HTTPS ativo
- [ ] Firewall configurado
- [ ] Port forwarding no roteador
- [ ] Backup agendado
- [ ] Health check funcionando
- [ ] Site acessível: https://auronex.com.br

---

**🎉 AURONEX.COM.BR ONLINE 24/7!**

**Tempo total: ~2 horas**  
**Custo: R$ 40/ano (domínio) + Energia**  
**Resultado: Site profissional HTTPS!** 🚀

