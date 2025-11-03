# 🐧 RoboTrader no Ubuntu Server 22.04 - Guia Completo

## 🎯 **SOLUÇÃO PERFEITA:**

Ubuntu Server em notebook = **Servidor dedicado grátis!**
- ✅ Custo: R$ 0 (usa notebook antigo)
- ✅ Online 24/7
- ✅ Controle total
- ✅ Escalável (migra para cloud depois)

---

## 📋 **REQUISITOS:**

- Notebook com Ubuntu Server 22.04
- Mínimo 4GB RAM
- 20GB espaço em disco
- Conexão internet estável
- IP fixo (configurar no roteador)

---

## 🚀 **INSTALAÇÃO (30 MINUTOS):**

### **1. Atualizar Sistema (2 min)**

```bash
sudo apt update
sudo apt upgrade -y
```

### **2. Instalar Python e Dependências (3 min)**

```bash
sudo apt install python3.10 python3-pip python3-venv nginx postgresql redis-server -y
```

### **3. Criar Usuário para RoboTrader (1 min)**

```bash
sudo adduser robotrader
sudo usermod -aG sudo robotrader
su - robotrader
```

### **4. Clonar/Copiar Projeto (2 min)**

```bash
cd ~
# Opção A: Se tiver Git
git clone https://github.com/seu-usuario/robotrader.git

# Opção B: Copiar via SCP do Windows
# No Windows:
scp -r I:\Robo robotrader@IP_DO_SERVIDOR:/home/robotrader/
```

### **5. Criar Ambiente Virtual (2 min)**

```bash
cd ~/robotrader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **6. Configurar PostgreSQL (5 min)**

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE robotrader_db;
CREATE USER robotrader_user WITH PASSWORD 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE robotrader_db TO robotrader_user;
\q
```

### **7. Configurar Variáveis de Ambiente (3 min)**

```bash
nano ~/robotrader/saas/.env
```

```env
DJANGO_SECRET_KEY=sua-chave-django
DEBUG=False
DATABASE_URL=postgresql://robotrader_user:senha_forte_aqui@localhost:5432/robotrader_db
STRIPE_SECRET_KEY=sua-chave-stripe
MERCADOPAGO_ACCESS_TOKEN=sua-chave-mercadopago
ENCRYPTION_KEY=sua-chave-fernet
SITE_URL=http://SEU_IP:8001
```

### **8. Migrations e Static Files (2 min)**

```bash
cd ~/robotrader/saas
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### **9. Criar Serviços Systemd (10 min)**

**Django (Gunicorn):**
```bash
sudo nano /etc/systemd/system/robotrader-django.service
```

```ini
[Unit]
Description=RoboTrader Django
After=network.target

[Service]
User=robotrader
Group=www-data
WorkingDirectory=/home/robotrader/robotrader/saas
Environment="PATH=/home/robotrader/robotrader/venv/bin"
ExecStart=/home/robotrader/robotrader/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:8001 \
    saas.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Streamlit:**
```bash
sudo nano /etc/systemd/system/robotrader-streamlit.service
```

```ini
[Unit]
Description=RoboTrader Streamlit
After=network.target

[Service]
User=robotrader
WorkingDirectory=/home/robotrader/robotrader
Environment="PATH=/home/robotrader/robotrader/venv/bin"
ExecStart=/home/robotrader/robotrader/venv/bin/streamlit run dashboard_master.py --server.port 8501 --server.headless true

[Install]
WantedBy=multi-user.target
```

**Celery (Bot):**
```bash
sudo nano /etc/systemd/system/robotrader-celery.service
```

```ini
[Unit]
Description=RoboTrader Celery
After=network.target

[Service]
User=robotrader
WorkingDirectory=/home/robotrader/robotrader/saas
Environment="PATH=/home/robotrader/robotrader/venv/bin"
ExecStart=/home/robotrader/robotrader/venv/bin/celery -A saas worker -l info

[Install]
WantedBy=multi-user.target
```

### **10. Ativar e Iniciar Serviços**

```bash
sudo systemctl daemon-reload
sudo systemctl enable robotrader-django
sudo systemctl enable robotrader-streamlit
sudo systemctl enable robotrader-celery

sudo systemctl start robotrader-django
sudo systemctl start robotrader-streamlit
sudo systemctl start robotrader-celery
```

### **11. Configurar Firewall**

```bash
sudo ufw allow 8001/tcp
sudo ufw allow 8501/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### **12. Verificar Status**

```bash
sudo systemctl status robotrader-django
sudo systemctl status robotrader-streamlit
sudo systemctl status robotrader-celery
```

---

## 🌐 **ACESSAR DE QUALQUER LUGAR:**

### **Descobrir IP do servidor:**

```bash
ip addr show | grep inet
```

### **Acessar de outro PC:**

```
Django: http://192.168.X.X:8001
Streamlit: http://192.168.X.X:8501
```

**Dentro da rede local:** Qualquer um acessa!

---

## 🔧 **MANUTENÇÃO:**

**Ver logs:**
```bash
sudo journalctl -u robotrader-django -f
sudo journalctl -u robotrader-streamlit -f
```

**Reiniciar:**
```bash
sudo systemctl restart robotrader-django
sudo systemctl restart robotrader-streamlit
```

**Atualizar código:**
```bash
cd ~/robotrader
git pull
sudo systemctl restart robotrader-django
sudo systemctl restart robotrader-streamlit
```

---

## 🌍 **ACESSO EXTERNO (Internet):**

**Para acessar de fora da rede:**

1. **Configurar Port Forwarding no Roteador:**
   ```
   Porta 8001 → 192.168.X.X:8001
   Porta 8501 → 192.168.X.X:8501
   ```

2. **Descobrir IP Externo:**
   ```
   curl ifconfig.me
   ```

3. **Acessar:**
   ```
   http://SEU_IP_EXTERNO:8001
   ```

4. **Registrar Domínio (Opcional):**
   ```
   robotrader.com.br → SEU_IP_EXTERNO
   (R$ 40/ano)
   ```

---

## ⚠️ **SEGURANÇA:**

**Essencial:**
- ✅ Firewall ativo (ufw)
- ✅ Senha forte PostgreSQL
- ✅ Trocar `DEBUG=False`
- ✅ HTTPS com Let's Encrypt (grátis)

**HTTPS (SSL):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d robotrader.com.br
```

---

## 💡 **VANTAGENS UBUNTU SERVER:**

| Aspecto | Windows Localhost | Ubuntu Server |
|---------|-------------------|---------------|
| **Custo** | Grátis | Grátis |
| **Online** | Quando PC ligado | 24/7 ✅ |
| **Acesso** | Só você | Rede local |
| **Acesso Internet** | Não | Sim (port forward) |
| **Performance** | OK | Melhor ✅ |
| **Produção** | Não | Sim ✅ |
| **Escalável** | Não | Sim ✅ |

---

## 🎯 **PRÓXIMOS PASSOS:**

1. **Instalar Ubuntu Server no notebook** (1h)
2. **Seguir este guia** (30min)
3. **Testar acesso na rede local** (5min)
4. **Configurar port forward** (10min)
5. **✅ Site acessível 24/7!**

---

## 📞 **AJUDA:**

**Dúvidas durante instalação?**
- Guia oficial Ubuntu: https://ubuntu.com/server/docs
- Este guia cobre 95% dos casos

---

**Ubuntu Server = Solução profissional e gratuita! 🐧✅**

**Próxima sessão: Deploy no Ubuntu! 🚀**


