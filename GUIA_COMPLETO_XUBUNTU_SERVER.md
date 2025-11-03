# 🖥️ GUIA COMPLETO - SERVIDOR XUBUNTU 22.04 LTS

**Hardware:** Intel i7-3517U | 4GB RAM | 240GB SSD  
**OS:** Xubuntu 22.04.5 LTS (Jammy Jellyfish)  
**Uso:** Trading Bot RoboTrader 24/7  
**Editor:** NANO (mais fácil que VIM)

---

## 📋 **ÍNDICE**

1. [Preparação Inicial](#1-preparação-inicial)
2. [Segurança](#2-segurança)
3. [Otimização](#3-otimização)
4. [PostgreSQL](#4-postgresql)
5. [Redis](#5-redis)
6. [Deploy Bot](#6-deploy-bot)
7. [Nginx](#7-nginx)
8. [SSL/HTTPS](#8-ssl-https)
9. [Monitoramento](#9-monitoramento)
10. [Backup](#10-backup)

---

## 1. PREPARAÇÃO INICIAL

### **1.1. Descobrir IPs do Servidor:**

**Execute no Xubuntu:**

```bash
# IP Local (rede interna - ex: 192.168.x.x)
hostname -I
# Anote este IP!

# IP Público (internet - ex: 200.x.x.x)
curl ifconfig.me
# Anote este IP também!
```

**Exemplo de resultado:**
```
IP LOCAL: 192.168.15.110     ← Para acessar na sua rede WiFi
IP PÚBLICO: 177.50.100.200   ← Para domínio e acesso externo
```

**Anote estes IPs! Vai usar depois.**

### **1.2. Primeiro Login:**

```bash
# Login com seu usuário criado na instalação
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Reiniciar se necessário
sudo reboot
```

### **1.3. Instalar Ferramentas Essenciais:**

```bash
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
python3 --version  # Deve ser 3.10.x
psql --version     # Deve ser 14.x
redis-server --version  # Deve ser 6.x
nginx -v           # Deve ser 1.18.x
```

### **1.4. Criar Usuário Dedicado:**

```bash
# Criar usuário para o bot (segurança)
sudo adduser bottrader

# Adicionar ao grupo sudo
sudo usermod -aG sudo bottrader

# Definir senha forte
# Digite quando solicitado

# Trocar para novo usuário
su - bottrader
```

---

## 2. SEGURANÇA

### **2.1. Instalar e Verificar SSH:**

```bash
# Verificar se SSH está instalado
sudo systemctl status ssh

# Se não estiver, instalar:
sudo apt update
sudo apt install openssh-server -y

# Habilitar e iniciar SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# Verificar status
sudo systemctl status ssh
# Deve mostrar: "Active: active (running)"
```

### **2.2. Configurar Firewall (UFW):**

```bash
# Configurar firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir SSH (porta customizada para segurança)
sudo ufw allow 2222/tcp

# Permitir HTTP e HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar firewall
sudo ufw enable

# Verificar status
sudo ufw status verbose
```

### **2.3. SSH Seguro:**

```bash
# Editar configuração SSH usando NANO
sudo nano /etc/ssh/sshd_config

# Buscar (Ctrl + W) e modificar estas linhas:
# (Se linha tiver # no início, remova o #)

Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Reiniciar SSH (no Ubuntu/Xubuntu é 'ssh', não 'sshd'!)
sudo systemctl restart ssh
```

### **2.4. Chaves SSH (Acesso sem Senha):**

**No seu PC Windows (PowerShell):**
```powershell
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"

# Exibir chave pública
Get-Content ~/.ssh/id_ed25519.pub
```

**No Xubuntu Server:**
```bash
# Criar diretório .ssh
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Editar arquivo de chaves autorizadas
nano ~/.ssh/authorized_keys

# Cole a chave pública copiada do Windows
# (Ctrl + Shift + V no terminal)

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Permissões corretas
chmod 600 ~/.ssh/authorized_keys
```

**Testar conexão (do Windows):**
```powershell
# Conectar com chave SSH (sem senha!)
ssh -p 2222 bottrader@IP_DO_SERVIDOR
```

### **2.5. Fail2Ban (Anti-Bruteforce):**

```bash
# Configurar Fail2Ban
sudo nano /etc/fail2ban/jail.local

# Cole este conteúdo:
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Iniciar Fail2Ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Verificar status
sudo fail2ban-client status
```

---

## 3. OTIMIZAÇÃO

### **3.1. Criar Swap (4GB):**

```bash
# Criar arquivo swap de 4GB
sudo fallocate -l 4G /swapfile

# Permissões corretas
sudo chmod 600 /swapfile

# Criar swap
sudo mkswap /swapfile

# Ativar swap
sudo swapon /swapfile

# Verificar
free -h  # Deve mostrar 4GB de swap

# Tornar permanente (editar fstab)
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Otimizar swappiness (usar RAM primeiro)
sudo sysctl vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# Verificar
cat /proc/sys/vm/swappiness  # Deve mostrar 10
```

### **3.2. Aumentar Limites do Sistema:**

```bash
# Editar limits.conf
sudo nano /etc/security/limits.conf

# Adicionar no final do arquivo:
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Aplicar
sudo sysctl -p

# Verificar
ulimit -n  # Deve mostrar 65536
```

---

## 4. POSTGRESQL

### **4.1. Criar Database e Usuário:**

```bash
# Entrar no PostgreSQL como postgres
sudo -u postgres psql

# Criar database
CREATE DATABASE robotrader;

# Criar usuário (TROQUE A SENHA!)
CREATE USER botuser WITH PASSWORD 'SUA_SENHA_SUPER_FORTE_AQUI';

# Dar permissões
GRANT ALL PRIVILEGES ON DATABASE robotrader TO botuser;

# Sair
\q
```

### **4.2. Otimizar PostgreSQL para 4GB RAM:**

```bash
# Editar configuração
sudo nano /etc/postgresql/14/main/postgresql.conf

# Buscar (Ctrl + W) e modificar estas linhas:

shared_buffers = 1GB
effective_cache_size = 3GB
maintenance_work_mem = 256MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Reiniciar PostgreSQL
sudo systemctl restart postgresql

# Verificar status
sudo systemctl status postgresql
```

---

## 5. REDIS

### **5.1. Otimizar Redis:**

```bash
# Editar configuração
sudo nano /etc/redis/redis.conf

# Buscar (Ctrl + W) e modificar:

maxmemory 512mb
maxmemory-policy allkeys-lru
save ""

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Reiniciar Redis
sudo systemctl restart redis-server

# Verificar status
sudo systemctl status redis-server

# Testar conexão
redis-cli ping  # Deve retornar "PONG"
```

---

## 6. DEPLOY BOT

### **6.1. Transferir Código:**

**Opção A - SCP do Windows:**
```powershell
# No seu PC Windows
scp -P 2222 -r I:\Robo bottrader@IP_SERVIDOR:~/robotrader
```

**Opção B - Git:**
```bash
# No Xubuntu
cd ~
git clone https://github.com/SEU_USUARIO/robotrader.git
cd robotrader
```

### **6.2. Criar Ambiente Virtual:**

```bash
cd ~/robotrader

# Criar venv
python3 -m venv venv

# Ativar venv
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Instalar extras para produção
pip install gunicorn psycopg2-binary
```

### **6.3. Configurar .env:**

```bash
# Criar arquivo .env
nano ~/robotrader/.env

# Cole e preencha:
DEBUG=False
DJANGO_SECRET_KEY='GERAR_CHAVE_LONGA_AQUI'
DATABASE_URL=postgresql://botuser:SUA_SENHA@localhost:5432/robotrader
REDIS_URL=redis://localhost:6379/0
SITE_URL=https://seudominio.com

# Stripe PRODUÇÃO
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Mercado Pago PRODUÇÃO
MERCADOPAGO_PUBLIC_KEY=APP_USR-...
MERCADOPAGO_ACCESS_TOKEN=APP_USR-...

# Encryption (gerar chave Fernet)
ENCRYPTION_KEY='GERAR_CHAVE_FERNET_AQUI'

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X
```

**Gerar chaves:**
```bash
# Django Secret Key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Fernet Key
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### **6.4. Migrations e Superuser:**

```bash
cd ~/robotrader/saas
source ../venv/bin/activate

# Migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@robotrader.com
# Password: SENHA_FORTE

# Collectstatic
python manage.py collectstatic --noinput
```

### **6.5. Criar Systemd Services:**

**Django (Gunicorn):**
```bash
sudo nano /etc/systemd/system/django-bot.service

# Cole:
[Unit]
Description=RoboTrader Django API
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

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X
```

**Streamlit:**
```bash
sudo nano /etc/systemd/system/streamlit-bot.service

# Cole:
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

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X
```

**Celery Worker:**
```bash
sudo nano /etc/systemd/system/celery-bot.service

# Cole:
[Unit]
Description=Celery Worker Trading Bot
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

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X
```

**Celery Beat:**
```bash
sudo nano /etc/systemd/system/celerybeat-bot.service

# Cole:
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

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X
```

### **6.6. Criar Diretórios de Log:**

```bash
# Criar diretórios
sudo mkdir -p /var/log/{django-bot,celery-bot}
sudo mkdir -p /var/run/celery-bot
sudo mkdir -p /home/bottrader/backups

# Permissões
sudo chown -R bottrader:bottrader /var/log/{django-bot,celery-bot}
sudo chown -R bottrader:bottrader /var/run/celery-bot
sudo chown -R bottrader:bottrader /home/bottrader
```

### **6.7. Iniciar Serviços:**

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar auto-start
sudo systemctl enable django-bot
sudo systemctl enable streamlit-bot
sudo systemctl enable celery-bot
sudo systemctl enable celerybeat-bot

# Iniciar serviços
sudo systemctl start django-bot
sudo systemctl start streamlit-bot
sudo systemctl start celery-bot
sudo systemctl start celerybeat-bot

# Verificar status
sudo systemctl status django-bot
sudo systemctl status streamlit-bot
sudo systemctl status celery-bot
sudo systemctl status celerybeat-bot
```

---

## 7. NGINX

### **7.1. Configurar Nginx:**

```bash
# Copiar configuração do projeto
sudo cp ~/robotrader/deploy/nginx-robotrader.conf /etc/nginx/sites-available/robotrader

# Editar para seu domínio
sudo nano /etc/nginx/sites-available/robotrader

# Buscar (Ctrl + W): "seudominio.com"
# Substituir por seu domínio real (ex: robotrader.com.br)
# Trocar TODAS as ocorrências!

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Ativar site
sudo ln -s /etc/nginx/sites-available/robotrader /etc/nginx/sites-enabled/

# Desativar site padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t
# Deve mostrar: "syntax is ok"

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar status
sudo systemctl status nginx
```

---

## 8. SSL/HTTPS

### **8.1. Obter Certificado SSL (Let's Encrypt):**

**Certifique que seu domínio aponta para o IP do servidor!**

```bash
# Obter certificado (TROCAR seudominio.com!)
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Seguir instruções:
# 1. Email: seu@email.com
# 2. Aceitar ToS: Y
# 3. Compartilhar email: N
# 4. Redirecionar HTTP → HTTPS: 2 (Yes)

# Verificar certificado
sudo certbot certificates

# Testar renovação
sudo certbot renew --dry-run
```

**Renovação automática já configurada!**

---

## 9. MONITORAMENTO

### **9.1. Ver Logs em Tempo Real:**

```bash
# Django
sudo journalctl -u django-bot -f

# Streamlit
sudo journalctl -u streamlit-bot -f

# Celery
tail -f /var/log/celery-bot/worker.log

# Nginx
tail -f /var/log/nginx/robotrader_error.log

# Todos juntos
sudo journalctl -u django-bot -u streamlit-bot -u celery-bot -f
```

### **9.2. Monitor de Recursos:**

```bash
# Instalar htop (interface visual)
sudo apt install htop -y

# Executar
htop

# Comandos htop:
# F10 ou q: Sair
# F3: Buscar processo
# F4: Filtrar
# F9: Matar processo
```

### **9.3. Script de Health Check:**

```bash
# Criar script
nano ~/health-check.sh

# Cole:
#!/bin/bash
echo "=== ROBOTRADER HEALTH CHECK ==="
echo ""
echo "Servicos:"
systemctl is-active django-bot && echo "  Django: OK" || echo "  Django: PARADO"
systemctl is-active streamlit-bot && echo "  Streamlit: OK" || echo "  Streamlit: PARADO"
systemctl is-active celery-bot && echo "  Celery: OK" || echo "  Celery: PARADO"
systemctl is-active postgresql && echo "  PostgreSQL: OK" || echo "  PostgreSQL: PARADO"
systemctl is-active redis-server && echo "  Redis: OK" || echo "  Redis: PARADO"
systemctl is-active nginx && echo "  Nginx: OK" || echo "  Nginx: PARADO"
echo ""
echo "Recursos:"
free -h | grep Mem | awk '{print "  RAM: "$3" usado de "$2}'
df -h / | tail -1 | awk '{print "  Disco: "$3" usado de "$2" ("$5")"}'
echo ""
echo "Processos Python:" $(ps aux | grep python | grep -v grep | wc -l)
uptime

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Tornar executável
chmod +x ~/health-check.sh

# Executar
./health-check.sh
```

---

## 10. BACKUP

### **10.1. Script de Backup Automático:**

```bash
# Criar script
nano ~/backup-db.sh

# Cole:
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/bottrader/backups"

# Backup PostgreSQL
sudo -u postgres pg_dump robotrader > $BACKUP_DIR/db_$DATE.sql

# Compactar
gzip $BACKUP_DIR/db_$DATE.sql

# Manter apenas últimos 7 dias
find $BACKUP_DIR -type f -name "*.gz" -mtime +7 -delete

echo "Backup concluído: db_$DATE.sql.gz"

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Tornar executável
chmod +x ~/backup-db.sh

# Testar
./backup-db.sh
```

### **10.2. Agendar Backup Automático:**

```bash
# Editar crontab
crontab -e

# Se perguntar editor, escolha nano (opção 1)

# Adicionar (backup diário às 3h):
0 3 * * * /home/bottrader/backup-db.sh >> /var/log/backup.log 2>&1

# Backup código (semanal domingo 2h)
0 2 * * 0 tar -czf /home/bottrader/backups/code_$(date +\%Y\%m\%d).tar.gz /home/bottrader/robotrader

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Verificar agendamentos
crontab -l
```

---

## 📊 **VERIFICAR TUDO FUNCIONANDO**

```bash
# 1. Health check
./health-check.sh

# 2. Testar Django
curl http://localhost:8000

# 3. Testar Nginx
curl http://localhost

# 4. Testar HTTPS (se configurou SSL)
curl https://seudominio.com

# 5. Ver logs
sudo journalctl -u django-bot -n 50
```

---

## 🔄 **ATUALIZAR BOT**

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

# Verificar
./health-check.sh
```

---

## 🆘 **TROUBLESHOOTING**

### **Serviço não inicia:**
```bash
# Ver erro
sudo journalctl -u NOME_SERVICO -n 50

# Exemplo:
sudo journalctl -u django-bot -n 50
```

### **Erro 502 Bad Gateway:**
```bash
# Verificar socket
ls -la ~/robotrader/gunicorn.sock

# Se não existir, Django não iniciou
sudo systemctl status django-bot

# Ver logs
sudo journalctl -u django-bot -n 100
```

### **Memória alta:**
```bash
# Ver processos
htop

# Liberar cache
sudo sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

### **Disco cheio:**
```bash
# Ver uso
df -h

# Limpar logs antigos
sudo journalctl --vacuum-time=7d

# Limpar apt cache
sudo apt clean
sudo apt autoclean
```

---

## 📋 **COMANDOS ÚTEIS NANO**

```
Ctrl + O  →  Salvar
Ctrl + X  →  Sair
Ctrl + W  →  Buscar
Ctrl + K  →  Cortar linha
Ctrl + U  →  Colar linha
Ctrl + _  →  Ir para linha específica
Ctrl + G  →  Ajuda
```

---

## ✅ **CHECKLIST COMPLETO**

- [ ] Sistema atualizado
- [ ] Ferramentas instaladas
- [ ] Usuário bottrader criado
- [ ] Firewall configurado (UFW)
- [ ] SSH porta 2222 + chaves
- [ ] Fail2Ban ativo
- [ ] Swap 4GB criado
- [ ] Limites sistema aumentados
- [ ] PostgreSQL criado e otimizado
- [ ] Redis otimizado
- [ ] Código transferido
- [ ] Venv criado e deps instaladas
- [ ] .env configurado
- [ ] Migrations aplicadas
- [ ] Superuser criado
- [ ] Systemd services criados
- [ ] Logs dirs criados
- [ ] Serviços iniciados
- [ ] Nginx configurado
- [ ] SSL/HTTPS obtido
- [ ] Backup script criado
- [ ] Cron backup configurado
- [ ] Health check funcionando

---

## 🎯 **TEMPO TOTAL: ~30 MINUTOS**

```
Setup inicial: 10 min
Segurança: 5 min
Deploy bot: 10 min
Nginx + SSL: 5 min
```

---

## 🚀 **RESULTADO**

**Bot RoboTrader rodando 24/7 em Xubuntu!**

- ✅ HTTPS seguro
- ✅ Auto-start ao ligar
- ✅ Backup automático
- ✅ Monitoramento completo
- ✅ Otimizado para 4GB RAM
- ✅ Firewall ativo
- ✅ SSH seguro

**Acesse:** https://seudominio.com

---

**📖 Use NANO para editar arquivos - Muito mais fácil!** ✅

