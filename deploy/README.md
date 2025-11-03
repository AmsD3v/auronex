# 🚀 DEPLOY ROBOTRADER - UBUNTU SERVER

Scripts para deploy automatizado do RoboTrader em Ubuntu Server 22.04.

---

## 📋 **ORDEM DE EXECUÇÃO**

### **1. Setup Inicial (Como Root)**
```bash
# Tornar executável
chmod +x setup-ubuntu-server.sh

# Executar como root
sudo ./setup-ubuntu-server.sh
```

**O que faz:**
- ✅ Atualiza sistema
- ✅ Instala dependências
- ✅ Cria usuário bottrader
- ✅ Configura firewall (UFW)
- ✅ Cria swap 4GB
- ✅ Otimiza limites sistema
- ✅ Configura PostgreSQL
- ✅ Configura Redis
- ✅ Configura Fail2Ban
- ✅ Cria diretórios

**Tempo:** ~10 minutos

---

### **2. Transferir Código**

**Opção A - Git:**
```bash
su - bottrader
git clone https://github.com/SEU_USUARIO/robotrader.git
cd robotrader
```

**Opção B - SCP (do Windows):**
```powershell
# No seu PC Windows
scp -P 2222 -r I:\Robo bottrader@IP_SERVIDOR:~/robotrader
```

---

### **3. Configurar .env**
```bash
cd ~/robotrader
cp .env.example .env
vim .env
```

**IMPORTANTE:** Preencher TODAS as variáveis!

---

### **4. Deploy Bot (Como bottrader)**
```bash
# Tornar executável
chmod +x deploy-bot.sh

# Executar
./deploy-bot.sh
```

**O que faz:**
- ✅ Cria venv
- ✅ Instala dependências
- ✅ Executa migrations
- ✅ Coleta static files
- ✅ Cria superuser
- ✅ Cria systemd services
- ✅ Inicia serviços

**Tempo:** ~5 minutos

---

### **5. Configurar Nginx**
```bash
# Copiar config
sudo cp nginx-robotrader.conf /etc/nginx/sites-available/robotrader

# EDITAR: trocar "seudominio.com" pelo seu domínio!
sudo vim /etc/nginx/sites-available/robotrader

# Ativar site
sudo ln -s /etc/nginx/sites-available/robotrader /etc/nginx/sites-enabled/

# Testar config
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

### **6. SSL (Let's Encrypt)**
```bash
# Obter certificado (TROCAR DOMÍNIO!)
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Seguir instruções
# Email de notificação: seu@email.com
# Aceitar ToS: Yes
# Redirecionar HTTP → HTTPS: Yes
```

**Renovação automática já configurada!**

---

### **7. Verificar**
```bash
# Status serviços
sudo systemctl status django-bot
sudo systemctl status streamlit-bot
sudo systemctl status celery-bot
sudo systemctl status celerybeat-bot

# Ou usar monitor
chmod +x monitor.sh
./monitor.sh
```

---

## 📊 **MONITORAMENTO**

### **Health Check:**
```bash
./monitor.sh
```

Mostra:
- ✅ Status serviços
- 💾 Uso RAM/Disco/CPU
- 🐍 Processos Python
- 🌐 Conexões rede
- ⚠️ Últimos erros
- 🗄️ Tamanho banco
- 🔒 Certificado SSL

---

## 📝 **LOGS**

### **Ver logs em tempo real:**
```bash
# Django
sudo journalctl -u django-bot -f

# Streamlit
sudo journalctl -u streamlit-bot -f

# Celery Worker
tail -f /var/log/celery-bot/worker.log

# Celery Beat
tail -f /var/log/celery-bot/beat.log

# Nginx Access
tail -f /var/log/nginx/robotrader_access.log

# Nginx Errors
tail -f /var/log/nginx/robotrader_error.log
```

### **Ver últimas 50 linhas:**
```bash
sudo journalctl -u django-bot -n 50
sudo journalctl -u celery-bot -n 50
```

---

## 🔄 **ATUALIZAR BOT**

```bash
cd ~/robotrader
source venv/bin/activate

# Pull código
git pull origin main

# Atualizar deps
pip install -r requirements.txt --upgrade

# Migrations
cd saas
python manage.py migrate
python manage.py collectstatic --noinput

# Reiniciar
sudo systemctl restart django-bot streamlit-bot celery-bot celerybeat-bot
```

---

## 🆘 **TROUBLESHOOTING**

### **Serviço não inicia:**
```bash
# Ver erro
sudo journalctl -u NOME_SERVICO -n 50

# Testar manual
cd ~/robotrader
source venv/bin/activate
cd saas
python manage.py runserver 8000
```

### **Django dá erro 502:**
```bash
# Verificar socket
ls -la ~/robotrader/gunicorn.sock

# Verificar permissões
sudo chown -R bottrader:bottrader ~/robotrader

# Reiniciar
sudo systemctl restart django-bot nginx
```

### **Webhook PIX não funciona:**
```bash
# Verificar se porta 443 aberta
sudo ufw status

# Verificar SSL
sudo certbot certificates

# Testar webhook manualmente
curl -X POST https://seudominio.com/api/payment/mercadopago-webhook/ \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### **Memória alta:**
```bash
# Ver processos
htop

# Verificar swap
free -h

# Limpar cache
sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

---

## 🔐 **SEGURANÇA**

### **Checklist:**
- [ ] ✅ SSH porta customizada (2222)
- [ ] ✅ SSH sem senha (só chaves)
- [ ] ✅ Firewall ativo
- [ ] ✅ Fail2Ban rodando
- [ ] ✅ SSL/HTTPS ativo
- [ ] ✅ .env com secrets fortes
- [ ] ✅ PostgreSQL senha forte
- [ ] ✅ Usuário dedicado (não root)

### **Trocar senhas:**
```bash
# Usuário bottrader
sudo passwd bottrader

# PostgreSQL
sudo -u postgres psql
\password botuser
\q

# Django admin
cd ~/robotrader/saas
source ../venv/bin/activate
python manage.py changepassword admin
```

---

## 📦 **BACKUP**

### **Manual:**
```bash
# Banco
sudo -u postgres pg_dump robotrader > backup_$(date +%Y%m%d).sql
gzip backup_$(date +%Y%m%d).sql

# Código
tar -czf code_backup_$(date +%Y%m%d).tar.gz ~/robotrader
```

### **Automático (já configurado via cron):**
```bash
# Ver agendamentos
crontab -l

# Editar
crontab -e
```

---

## 🔗 **URLs**

Após deploy:

```
https://seudominio.com/              ← Landing Page
https://seudominio.com/register/     ← Cadastro
https://seudominio.com/login/        ← Login
https://seudominio.com/dashboard/    ← Dashboard Django
https://seudominio.com/admin/        ← Admin Panel
```

---

## 💡 **DICAS**

1. **Sempre use tmux para sessões longas:**
   ```bash
   tmux new -s deploy
   # Fazer deploy
   # Ctrl+B, D para desconectar
   # tmux attach -t deploy para voltar
   ```

2. **Monitorar logs em tempo real:**
   ```bash
   sudo journalctl -u django-bot -u celery-bot -f
   ```

3. **Verificar saúde regularmente:**
   ```bash
   ./monitor.sh
   ```

4. **Atualizar sistema mensalmente:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo reboot
   ```

---

## 📞 **SUPORTE**

**Guia completo:** `SERVIDOR_UBUNTU_BOT_TRADING.md`

**Logs importantes:**
- `/var/log/django-bot/error.log`
- `/var/log/celery-bot/worker.log`
- `/var/log/nginx/robotrader_error.log`

**Comandos úteis:**
```bash
# Status geral
./monitor.sh

# Reiniciar tudo
sudo systemctl restart django-bot streamlit-bot celery-bot celerybeat-bot nginx

# Ver uso recursos
htop
df -h
free -h
```

---

**✅ DEPLOY PRONTO EM 20 MINUTOS!**

**🚀 Bot rodando 24/7 no Ubuntu Server!**



