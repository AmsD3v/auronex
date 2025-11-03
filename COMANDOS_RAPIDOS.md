# ⚡ COMANDOS RÁPIDOS - AURONEX/ROBOTRADER

**Última atualização:** 29 Outubro 2025

---

## 🚀 **WINDOWS (DESENVOLVIMENTO):**

### **Iniciar Sistemas:**
```powershell
# RECOMENDADO - Com monitor keep-alive:
.\INICIAR_COM_MONITOR.bat

# Alternativa - Sem monitor:
.\INICIAR_SISTEMA_COMPLETO.bat
```

### **Parar Sistemas:**
```powershell
# Fechar janelas PowerShell
# Ou:
taskkill /F /IM python.exe
taskkill /F /IM streamlit.exe
```

### **URLs Desenvolvimento:**
```
Django Backend:  http://localhost:8001
Admin Panel:     http://localhost:8001/admin/
API Docs:        http://localhost:8001/api/
Streamlit:       http://localhost:8501
```

---

## 🖥️ **XUBUNTU (PRODUÇÃO):**

### **Primeiro Acesso (SSH):**
```bash
# No Xubuntu (terminal local):
sudo apt install openssh-server -y
sudo systemctl start ssh
hostname -I  # Anotar IP

# Do Windows:
ssh seu_usuario@IP_ANOTADO
```

### **Status Sistemas:**
```bash
# Ver tudo de uma vez:
./health.sh

# Ou individual:
sudo systemctl status auronex-django
sudo systemctl status auronex-streamlit
sudo systemctl status auronex-celery
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis
```

### **Reiniciar Sistemas:**
```bash
# Tudo de uma vez:
sudo systemctl restart auronex-django auronex-streamlit auronex-celery nginx

# Individual:
sudo systemctl restart auronex-django
sudo systemctl restart auronex-streamlit
sudo systemctl restart auronex-celery
```

### **Ver Logs:**
```bash
# Django (tempo real):
sudo journalctl -u auronex-django -f

# Streamlit:
sudo journalctl -u auronex-streamlit -f

# Celery:
tail -f /var/log/auronex/celery.log

# Nginx errors:
tail -f /var/log/nginx/auronex_error.log

# Nginx access:
tail -f /var/log/nginx/auronex_access.log

# Todos últimos 100:
sudo journalctl -u auronex-django -n 100
```

### **Atualizar Código:**
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

### **Backup Manual:**
```bash
~/backup.sh
```

### **Ver IPs:**
```bash
# IP Local:
hostname -I

# IP Público:
curl ifconfig.me
```

---

## 🌐 **URLS PRODUÇÃO:**

```
Landing Page:    https://auronex.com.br/
Cadastro:        https://auronex.com.br/register/
Login:           https://auronex.com.br/login/
Dashboard:       https://auronex.com.br/dashboard/
Admin:           https://auronex.com.br/admin/
API:             https://auronex.com.br/api/
```

---

## 🔐 **CERTIFICADO SSL:**

```bash
# Ver status:
sudo certbot certificates

# Renovar (manual):
sudo certbot renew

# Testar renovação:
sudo certbot renew --dry-run
```

---

## 🗄️ **POSTGRESQL:**

```bash
# Conectar:
sudo -u postgres psql

# Ver databases:
\l

# Conectar database:
\c auronex

# Ver tabelas:
\dt

# Backup:
sudo -u postgres pg_dump auronex | gzip > backup_$(date +%Y%m%d).sql.gz

# Restaurar:
gunzip -c backup_20251029.sql.gz | sudo -u postgres psql auronex
```

---

## 📊 **REDIS:**

```bash
# Conectar:
redis-cli

# Ver chaves:
KEYS *

# Limpar cache:
FLUSHALL

# Sair:
exit
```

---

## 🔥 **FIREWALL:**

```bash
# Status:
sudo ufw status verbose

# Permitir porta:
sudo ufw allow 2222/tcp

# Recarregar:
sudo ufw reload

# Desabilitar (cuidado!):
sudo ufw disable
```

---

## 🐛 **TROUBLESHOOTING:**

### **Django não inicia:**
```bash
# Ver erro:
sudo journalctl -u auronex-django -n 50

# Testar manual:
cd ~/auronex/saas
source ../venv/bin/activate
python manage.py runserver

# Verificar porta:
sudo netstat -tulpn | grep 8001
```

### **Streamlit não conecta:**
```bash
# Ver se Django está rodando:
curl http://localhost:8001

# Reiniciar Django primeiro:
sudo systemctl restart auronex-django
sleep 5
sudo systemctl restart auronex-streamlit
```

### **Nginx erro:**
```bash
# Testar config:
sudo nginx -t

# Ver erro:
tail -f /var/log/nginx/error.log

# Reiniciar:
sudo systemctl restart nginx
```

### **Banco de dados erro:**
```bash
# Ver se está rodando:
sudo systemctl status postgresql

# Reiniciar:
sudo systemctl restart postgresql

# Ver logs:
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

---

## 📈 **MONITORAMENTO:**

### **Uso CPU/RAM:**
```bash
htop
# Ou:
top
# Sair: q
```

### **Disco:**
```bash
df -h
```

### **Memória:**
```bash
free -h
```

### **Processos Python:**
```bash
ps aux | grep python
```

### **Portas abertas:**
```bash
sudo netstat -tulpn
# Ou:
sudo ss -tulpn
```

---

## 🔄 **SYSTEMD:**

### **Habilitar auto-start:**
```bash
sudo systemctl enable auronex-django
sudo systemctl enable auronex-streamlit
sudo systemctl enable auronex-celery
```

### **Desabilitar auto-start:**
```bash
sudo systemctl disable auronex-django
```

### **Recarregar configs:**
```bash
sudo systemctl daemon-reload
```

---

## 📦 **PYTHON:**

### **Ativar venv:**
```bash
source ~/auronex/venv/bin/activate
```

### **Instalar pacote:**
```bash
pip install nome-do-pacote
pip freeze > requirements.txt
```

### **Ver pacotes:**
```bash
pip list
```

---

## 🔑 **DJANGO MANAGE:**

```bash
cd ~/auronex/saas
source ../venv/bin/activate

# Migrations:
python manage.py makemigrations
python manage.py migrate

# Criar superuser:
python manage.py createsuperuser

# Shell:
python manage.py shell

# Static files:
python manage.py collectstatic --noinput

# Ver rotas:
python manage.py show_urls
```

---

## 🌍 **DNS:**

```bash
# Verificar DNS:
nslookup auronex.com.br

# Ou:
dig auronex.com.br

# Flush DNS local (Windows):
ipconfig /flushdns
```

---

## 🚨 **EMERGÊNCIA:**

### **Site fora do ar:**
```bash
# 1. Ver se serviços estão rodando:
./health.sh

# 2. Reiniciar tudo:
sudo systemctl restart auronex-django auronex-streamlit auronex-celery nginx

# 3. Ver logs:
sudo journalctl -u auronex-django -n 100

# 4. Se nada funcionar - reboot:
sudo reboot
```

### **Banco corrompido:**
```bash
# Restaurar último backup:
gunzip -c ~/backups/db_ULTIMA_DATA.sql.gz | sudo -u postgres psql auronex
```

---

## 📞 **SUPORTE RÁPIDO:**

### **Erro "Permission denied":**
```bash
# Corrigir permissões:
sudo chown -R bottrader:bottrader ~/auronex
chmod +x ~/auronex/deploy/*.sh
```

### **Erro "Port already in use":**
```bash
# Ver quem está usando:
sudo lsof -i :8001

# Matar processo:
sudo kill -9 PID_DO_PROCESSO
```

### **Erro SSL expirado:**
```bash
# Renovar:
sudo certbot renew --force-renewal
sudo systemctl restart nginx
```

---

## 🎯 **SCRIPTS ÚTEIS:**

### **Ver tudo funcionando:**
```bash
#!/bin/bash
echo "=== AURONEX STATUS ==="
echo ""
echo "Serviços:"
systemctl is-active auronex-django && echo "✅ Django" || echo "❌ Django"
systemctl is-active auronex-streamlit && echo "✅ Streamlit" || echo "❌ Streamlit"
systemctl is-active nginx && echo "✅ Nginx" || echo "✅ Nginx"
echo ""
echo "Recursos:"
free -h | grep Mem
df -h / | tail -1
echo ""
echo "Site: https://auronex.com.br"
```

**Salvar como:** `~/status.sh`  
**Usar:** `chmod +x ~/status.sh && ./status.sh`

---

## 📚 **GUIAS COMPLETOS:**

```
Setup completo:         GUIA_DEFINITIVO_AURONEX_COM_BR.md
Checklist deploy:       CHECKLIST_FINAL_DEPLOY.md
Primeiro acesso SSH:    XUBUNTU_PRIMEIRO_ACESSO.md
Diagnóstico sistema:    DIAGNOSTICO_SISTEMA_COMPLETO.md
Resumo completo:        RESUMO_COMPLETO_29_OUT_2025.md
Este arquivo:           COMANDOS_RAPIDOS.md
```

---

**⚡ SEMPRE TENHA ESTE ARQUIVO ABERTO PARA REFERÊNCIA RÁPIDA!**

