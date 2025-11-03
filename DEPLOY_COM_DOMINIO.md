# 🌐 DEPLOY COM SEU DOMÍNIO - auronex.com.br

**Você tem:** auronex.com.br ✅  
**Servidor:** Notebook i7-3517U, 4GB RAM, 240GB SSD  
**Melhor opção:** **GIT**

---

## 🎯 **SETUP COMPLETO (PASSO A PASSO)**

### **FASE 1: Preparar Código (10 min)**

**No seu PC (I:\Robo):**

```bash
# 1. Instalar Git
# Download: https://git-scm.com/

# 2. Inicializar repositório
cd I:\Robo
git init

# 3. Criar .gitignore
echo venv/ > .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo db.sqlite3 >> .gitignore
echo .env >> .gitignore

# 4. Commit inicial
git add .
git commit -m "Auronex v1.0 - Sistema completo"

# 5. Criar repositório privado no GitHub
# Acesse: github.com
# New Repository → auronex-robo-trader
# Privado: SIM

# 6. Conectar
git remote add origin https://github.com/SEU-USUARIO/auronex-robo-trader.git
git push -u origin main
```

---

### **FASE 2: Configurar Notebook (30 min)**

**No notebook servidor:**

```bash
# 1. Instalar Python 3.10
# Download: python.org

# 2. Instalar Git
# Download: git-scm.com

# 3. Criar pasta
mkdir C:\Auronex
cd C:\Auronex

# 4. Clonar repositório
git clone https://github.com/SEU-USUARIO/auronex-robo-trader.git .

# 5. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# 6. Instalar dependências
pip install -r requirements_fastapi.txt

# 7. Criar .env (IMPORTANTE!)
# Crie arquivo C:\Auronex\.env com:
```

**.env (NO NOTEBOOK):**
```
FASTAPI_SECRET_KEY=seu-secret-key-super-seguro-aqui
DATABASE_URL=sqlite:///./auronex_production.db

MERCADOPAGO_ACCESS_TOKEN=APP_USR-7940373206085562...
STRIPE_SECRET_KEY=sk_live_51SN37vRjxbCNnFAQ...

DOMAIN=auronex.com.br
```

```bash
# 8. Criar banco de dados
python -c "from fastapi_app.database import engine, Base; Base.metadata.create_all(bind=engine)"

# 9. Criar admin
# (Use Django ou crie pelo Python)
```

---

### **FASE 3: Configurar Domínio (15 min)**

**No painel do Registro.br (ou onde comprou):**

```
1. DNS → Adicionar registro A
   Nome: @
   Tipo: A
   Valor: SEU_IP_PUBLICO
   TTL: 3600

2. DNS → Adicionar registro A
   Nome: www
   Tipo: A  
   Valor: SEU_IP_PUBLICO
   TTL: 3600

3. Aguardar propagação (até 24h, normalmente 1-2h)
```

**Descobrir seu IP público:**
```
Acesse: https://meuip.com.br/
Anote o IP
```

---

### **FASE 4: Configurar Roteador (10 min)**

**No painel do seu roteador:**

```
1. Port Forwarding:
   Porta Externa: 80
   Porta Interna: 8001
   IP: 192.168.0.X (IP fixo do notebook)

2. Port Forwarding:
   Porta Externa: 443
   Porta Interna: 8001
   IP: 192.168.0.X

3. DHCP:
   Reservar IP para MAC do notebook
   IP fixo: 192.168.0.100 (exemplo)
```

---

### **FASE 5: Instalar Nginx (20 min)**

**No notebook:**

```bash
# 1. Instalar Nginx para Windows
# Download: nginx.org/download

# 2. Configurar (C:\nginx\conf\nginx.conf):
server {
    listen 80;
    server_name auronex.com.br www.auronex.com.br;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 3. Iniciar Nginx
cd C:\nginx
nginx.exe
```

---

### **FASE 6: SSL/HTTPS (30 min)**

**Opção A: Certbot (Grátis):**
```bash
# Requer WSL ou servidor Linux
# Alternativa: ZeroSSL (manual)
```

**Opção B: Cloudflare (RECOMENDADO!):**
```
1. Criar conta: cloudflare.com
2. Adicionar site: auronex.com.br
3. Trocar nameservers (Registro.br):
   - ns1.cloudflare.com
   - ns2.cloudflare.com
4. Cloudflare → SSL/TLS → Full
5. HTTPS automático! ✅
6. DDoS protection! ✅
7. CDN global! ✅
```

---

### **FASE 7: Manter Rodando (Always On)**

**Criar serviço Windows:**

**C:\Auronex\start_auronex.bat:**
```batch
@echo off
cd C:\Auronex
call venv\Scripts\activate
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
```

**Adicionar ao Startup:**
```
1. Win+R → shell:startup
2. Criar atalho para start_auronex.bat
3. Notebook reinicia → Auronex inicia!
```

---

### **FASE 8: Webhooks REAIS (5 min)**

**Agora com domínio, webhooks funcionam!**

**MercadoPago:**
```
Painel MercadoPago → Webhooks
URL: https://auronex.com.br/api/payments/mercadopago/webhook
```

**Stripe:**
```
Dashboard Stripe → Webhooks
URL: https://auronex.com.br/api/payments/stripe/webhook
```

**Pronto! Redirecionamento automático funcionando!** ✅

---

## 🔄 **ATUALIZAÇÕES (SEMPRE)**

**No PC dev:**
```bash
cd I:\Robo
git add .
git commit -m "Corrigido navbar"
git push
```

**No notebook servidor:**
```bash
cd C:\Auronex
git pull
# Reiniciar serviço
```

**30 segundos e está atualizado!**

---

## 💡 **MELHOR CONFIGURAÇÃO**

**Hardware:**
- ✅ Notebook sempre ligado
- ✅ Ventilação adequada
- ✅ Energia estável (nobreak recomendado)
- ✅ Firewall Windows configurado

**Software:**
- ✅ Windows 10/11 (ou Ubuntu Server)
- ✅ Python 3.10
- ✅ Git
- ✅ Nginx
- ✅ Cloudflare (SSL + proteção)

---

## 🏆 **RESUMO**

**Custo total:** R$ 0 (já tem domínio!)  
**Setup:** 2-3 horas primeira vez  
**Atualizações:** 30 segundos (git push/pull)  
**Webhooks:** Funcionam 100% ✅  
**SSL:** Grátis via Cloudflare ✅  

**Capacidade:** 50-100 usuários (seu notebook aguenta!)

---

**Quer que eu prepare o .gitignore e README para deploy?** 🚀




