# 🐧 GUIA: Deploy no Xubuntu (Linux)

## 🎯 SUA PERGUNTA

> "Quando o Bot estiver no servidor Xubuntu, como vai ser essa questão do Redis?"

**RESPOSTA:** No Linux é **MUITO MAIS FÁCIL** que no Windows! 🎉

---

## 📊 COMPARATIVO: Windows vs Linux

### ❌ WINDOWS (Atual):
```
1. Baixar .msi manualmente
2. Instalar clicando Next > Next
3. Abrir PowerShell
4. Executar redis-server
5. Deixar janela aberta
6. ⚠️ Se fechar = Redis para
```

### ✅ XUBUNTU/LINUX (Servidor):
```
1. sudo apt install redis-server
2. Pronto! Redis roda automaticamente
3. ✅ Inicia sozinho ao ligar servidor
4. ✅ Roda em background (não precisa janela)
5. ✅ Reinicia automaticamente se cair
```

**MUITO mais simples! 🚀**

---

## 🔧 INSTALAÇÃO NO XUBUNTU (Passo a Passo)

### 1. Conectar no servidor:
```bash
ssh usuario@seu-servidor-ip
```

### 2. Atualizar sistema:
```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Instalar Redis:
```bash
sudo apt install redis-server -y
```

**Pronto! Redis instalado! ✅**

### 4. Iniciar Redis:
```bash
sudo systemctl start redis-server
```

### 5. Habilitar Redis para iniciar automaticamente:
```bash
sudo systemctl enable redis-server
```

### 6. Verificar status:
```bash
sudo systemctl status redis-server
```

**DEVE APARECER:**
```
● redis-server.service - Advanced key-value store
   Loaded: loaded
   Active: active (running)
```

**Se aparecer "active (running)": ✅ Funcionando!**

---

## 🚀 INSTALAÇÃO COMPLETA DO BOT NO XUBUNTU

Aqui está o **guia completo** para colocar seu bot rodando no servidor:

### PASSO 1: Preparar o servidor

```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip -y

# 3. Instalar Redis
sudo apt install redis-server -y

# 4. Instalar PostgreSQL (melhor que SQLite para produção)
sudo apt install postgresql postgresql-contrib -y

# 5. Instalar Git
sudo apt install git -y

# 6. Instalar supervisor (para manter processos rodando)
sudo apt install supervisor -y
```

---

### PASSO 2: Clonar o projeto

```bash
# 1. Criar diretório
mkdir -p /home/usuario/apps
cd /home/usuario/apps

# 2. Clonar repositório (ou transferir arquivos)
git clone seu-repositorio.git robotrader
# OU
scp -r I:\Robo usuario@servidor:/home/usuario/apps/robotrader

# 3. Entrar no diretório
cd robotrader
```

---

### PASSO 3: Configurar ambiente Python

```bash
# 1. Criar virtualenv
python3.10 -m venv venv

# 2. Ativar virtualenv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Instalar Gunicorn (servidor de produção)
pip install gunicorn
```

---

### PASSO 4: Configurar Django

```bash
# 1. Configurar variáveis de ambiente
export DJANGO_SETTINGS_MODULE=saas.settings
export PYTHONPATH=/home/usuario/apps/robotrader

# 2. Criar banco de dados
cd saas
python manage.py migrate

# 3. Criar superusuário
python manage.py createsuperuser

# 4. Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

---

### PASSO 5: Configurar Supervisor (Processos em Background)

**Criar arquivos de configuração:**

#### `/etc/supervisor/conf.d/django.conf`
```ini
[program:django]
command=/home/usuario/apps/robotrader/venv/bin/gunicorn saas.wsgi:application --bind 0.0.0.0:8001 --workers 3
directory=/home/usuario/apps/robotrader/saas
user=usuario
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/robotrader/django.log
environment=PYTHONPATH="/home/usuario/apps/robotrader"
```

#### `/etc/supervisor/conf.d/celery-worker.conf`
```ini
[program:celery-worker]
command=/home/usuario/apps/robotrader/venv/bin/celery -A saas worker --loglevel=info
directory=/home/usuario/apps/robotrader/saas
user=usuario
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/robotrader/celery-worker.log
environment=PYTHONPATH="/home/usuario/apps/robotrader"
```

#### `/etc/supervisor/conf.d/celery-beat.conf`
```ini
[program:celery-beat]
command=/home/usuario/apps/robotrader/venv/bin/celery -A saas beat --loglevel=info
directory=/home/usuario/apps/robotrader/saas
user=usuario
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/robotrader/celery-beat.log
environment=PYTHONPATH="/home/usuario/apps/robotrader"
```

#### `/etc/supervisor/conf.d/streamlit.conf`
```ini
[program:streamlit]
command=/home/usuario/apps/robotrader/venv/bin/streamlit run dashboard_master.py --server.port 8501 --server.address 0.0.0.0
directory=/home/usuario/apps/robotrader
user=usuario
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/robotrader/streamlit.log
```

---

### PASSO 6: Criar diretório de logs

```bash
sudo mkdir -p /var/log/robotrader
sudo chown usuario:usuario /var/log/robotrader
```

---

### PASSO 7: Iniciar tudo

```bash
# 1. Recarregar configurações do Supervisor
sudo supervisorctl reread
sudo supervisorctl update

# 2. Iniciar todos os processos
sudo supervisorctl start django
sudo supervisorctl start celery-worker
sudo supervisorctl start celery-beat
sudo supervisorctl start streamlit

# 3. Verificar status
sudo supervisorctl status
```

**DEVE APARECER:**
```
django          RUNNING   pid 1234
celery-worker   RUNNING   pid 1235
celery-beat     RUNNING   pid 1236
streamlit       RUNNING   pid 1237
redis-server    RUNNING   (via systemd)
```

**Todos RUNNING: ✅ Sistema funcionando!**

---

## 🌐 CONFIGURAR NGINX (Proxy Reverso)

Para acessar via domínio (ex: bot.seusite.com):

### 1. Instalar Nginx:
```bash
sudo apt install nginx -y
```

### 2. Configurar site:

**Criar:** `/etc/nginx/sites-available/robotrader`

```nginx
server {
    listen 80;
    server_name bot.seusite.com;

    # Django Admin/API
    location /admin {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Dashboard Streamlit
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 3. Ativar site:
```bash
sudo ln -s /etc/nginx/sites-available/robotrader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Configurar SSL (HTTPS):
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d bot.seusite.com
```

**Pronto! HTTPS configurado automaticamente! 🔒**

---

## 🔄 GERENCIAR O BOT NO SERVIDOR

### Ver logs em tempo real:
```bash
# Django
sudo tail -f /var/log/robotrader/django.log

# Celery Worker (trades)
sudo tail -f /var/log/robotrader/celery-worker.log

# Celery Beat (análises)
sudo tail -f /var/log/robotrader/celery-beat.log

# Dashboard
sudo tail -f /var/log/robotrader/streamlit.log
```

### Reiniciar componentes:
```bash
# Reiniciar tudo
sudo supervisorctl restart all

# Reiniciar apenas um
sudo supervisorctl restart celery-worker
```

### Parar/Iniciar bot:
```bash
# Parar bot (mas deixar Django rodando)
sudo supervisorctl stop celery-worker
sudo supervisorctl stop celery-beat

# Iniciar bot novamente
sudo supervisorctl start celery-worker
sudo supervisorctl start celery-beat
```

---

## 💰 CUSTOS (Servidor Linux)

### VPS Recomendadas:

| Provedor | Specs | Preço/mês | Redis |
|----------|-------|-----------|-------|
| **Contabo** | 4 vCPU, 8GB RAM | ~€5 (R$ 27) | ✅ Incluso |
| **DigitalOcean** | 2 vCPU, 4GB RAM | $24 (R$ 120) | ✅ Incluso |
| **Vultr** | 2 vCPU, 4GB RAM | $18 (R$ 90) | ✅ Incluso |
| **Hetzner** | 2 vCPU, 4GB RAM | €4.5 (R$ 24) | ✅ Incluso |
| **Oracle Cloud** | 1 vCPU, 1GB RAM | **GRÁTIS** | ✅ Incluso |

**Recomendação:** 
- **Teste:** Oracle Cloud (grátis)
- **Produção:** Contabo ou Hetzner (melhor custo-benefício)

---

## 🎯 VANTAGENS DO LINUX (vs Windows)

### ✅ REDIS:
```
Windows: Instalar .msi, abrir janela, deixar aberta
Linux:   sudo apt install redis-server (pronto!)
```

### ✅ PROCESSOS:
```
Windows: Abrir 4-5 janelas PowerShell, deixar todas abertas
Linux:   Supervisor gerencia tudo em background
```

### ✅ INICIALIZAÇÃO:
```
Windows: Rebootou? Precisa abrir tudo de novo manualmente
Linux:   Rebootou? Tudo inicia automaticamente
```

### ✅ LOGS:
```
Windows: Logs nas janelas (desaparecem se fechar)
Linux:   Logs salvos em arquivos permanentes
```

### ✅ ESTABILIDADE:
```
Windows: Atualizações forçadas, reinicializações
Linux:   Servidor roda meses sem reiniciar
```

### ✅ CUSTO:
```
Windows: Licença ~$200 + Servidor ~$50/mês
Linux:   Grátis + Servidor ~$5-30/mês
```

---

## 📋 CHECKLIST DE DEPLOY

```
☐ 1. Servidor Xubuntu provisionado
☐ 2. Acesso SSH configurado
☐ 3. Python 3.10+ instalado
☐ 4. Redis instalado (sudo apt install redis-server)
☐ 5. PostgreSQL instalado (opcional)
☐ 6. Projeto transferido para servidor
☐ 7. Virtualenv criado
☐ 8. Dependências instaladas
☐ 9. Migrations aplicadas
☐ 10. Superusuário criado
☐ 11. Supervisor configurado
☐ 12. Todos processos rodando
☐ 13. Nginx configurado (opcional)
☐ 14. SSL configurado (opcional)
☐ 15. Bot Configuration criado
☐ 16. API Keys adicionadas
☐ 17. Bot testado (primeiro trade)
```

---

## 🆘 SUPORTE NO DEPLOY

**Quando for fazer deploy no Xubuntu:**

1. Me avise que vou criar um **script de deploy automático**
2. Vai executar **tudo automaticamente**
3. Em **5 minutos** está rodando
4. **Zero configuração manual**

**Vou criar:**
- `deploy.sh` - Script de instalação completo
- `start.sh` - Iniciar sistema
- `stop.sh` - Parar sistema
- `logs.sh` - Ver logs
- `update.sh` - Atualizar código

---

## 💬 RESUMO: REDIS NO LINUX

**Windows (atual):**
- ❌ Baixar .msi
- ❌ Instalar manualmente
- ❌ Abrir janela
- ❌ Deixar aberta
- ❌ Fechar janela = Redis para

**Xubuntu (futuro):**
- ✅ `sudo apt install redis-server`
- ✅ Pronto!
- ✅ Roda em background
- ✅ Inicia automaticamente
- ✅ Reinicia se cair
- ✅ **MUITO MAIS FÁCIL!**

---

## 🎉 CONCLUSÃO

**Sua pergunta:** "Como vai ser Redis no Xubuntu?"

**Resposta curta:** **MUITO MAIS FÁCIL!** ✅

**Resposta longa:**
- 1 comando para instalar
- Roda automaticamente
- Inicia sozinho ao ligar
- Zero manutenção
- **Esqueça que existe!**

**No Windows:**
- Precisa abrir 5 janelas manualmente
- Se fechar = tudo para
- Se reiniciar = precisa abrir tudo de novo

**No Linux:**
- Supervisor gerencia tudo
- Roda em background
- Reinicia automaticamente
- **Set and forget!**

---

**Quando for fazer deploy, me avise que eu crio os scripts automáticos! 🚀**

*Documento criado: 30/10/2024 - 03:30 AM*  
*Guia: Deploy no Xubuntu com Redis e Supervisor*  
*Status: Completo e pronto para uso!*

