# 🌐 DEPLOY NO SERVIDOR - OPÇÕES E MELHORES PRÁTICAS

## 🎯 **SUAS PERGUNTAS**

### **1. Como enviar arquivos para o servidor?**
### **2. Como atualizar depois?**
### **3. Como manter controle de versão?**

---

## 📦 **OPÇÃO 1: GIT + GITHUB (RECOMENDADO!)**

### **Vantagens:**
- ✅ Controle de versão automático
- ✅ Histórico completo de mudanças
- ✅ Fácil de atualizar (git pull)
- ✅ Backup automático na nuvem
- ✅ Pode colaborar com outros devs
- ✅ **GRATUITO!**

### **Como Fazer:**

**1. Criar repositório no GitHub:**
```bash
# No seu PC (I:\Robo):
git init
git add .
git commit -m "Sistema Auronex completo"

# Criar repo no GitHub: github.com/seu-usuario/auronex-bot
git remote add origin https://github.com/seu-usuario/auronex-bot.git
git push -u origin main
```

**2. No servidor:**
```bash
# SSH no servidor
ssh usuario@seu-servidor.com

# Clonar repositório
cd /var/www/
git clone https://github.com/seu-usuario/auronex-bot.git
cd auronex-bot

# Instalar dependências
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_fastapi.txt

# Configurar .env
nano .env
# (Cole suas chaves de produção)

# Iniciar
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
```

**3. Atualizar depois:**
```bash
# No seu PC (local):
git add .
git commit -m "Corrigido navbar"
git push

# No servidor:
cd /var/www/auronex-bot
git pull
systemctl restart auronex  # Reinicia o serviço
```

**Simples e profissional!** ✅

---

## 📦 **OPÇÃO 2: FTP/SFTP (Mais Simples)**

### **Vantagens:**
- ✅ Mais fácil para iniciantes
- ✅ Interface gráfica (FileZilla)
- ✅ Arrasta e solta arquivos

### **Desvantagens:**
- ❌ Sem controle de versão
- ❌ Pode sobrescrever mudanças
- ❌ Precisa enviar tudo sempre

### **Como Fazer:**

**1. No seu PC:**
```
- Instale FileZilla
- Conecte no servidor via SFTP
- Arraste pasta I:\Robo para /var/www/auronex/
```

**2. No servidor:**
```bash
cd /var/www/auronex
pip install -r requirements_fastapi.txt
python manage.py migrate
uvicorn fastapi_app.main:app
```

**3. Atualizar:**
```
- Arraste arquivos modificados
- Sobrescreve os antigos
```

---

## 📦 **OPÇÃO 3: DOCKER (Profissional)**

### **Vantagens:**
- ✅ Ambiente isolado
- ✅ Mesmas configurações local/servidor
- ✅ Fácil de escalar
- ✅ Deploy com 1 comando

### **Desvantagens:**
- ⚠️ Mais complexo
- ⚠️ Requer conhecimento Docker

### **Como Fazer:**

**1. Criar Dockerfile:**
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements_fastapi.txt .
RUN pip install -r requirements_fastapi.txt
COPY . .
CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**2. Deploy:**
```bash
docker build -t auronex-bot .
docker push seu-registry/auronex-bot
docker pull seu-registry/auronex-bot  # No servidor
docker run -p 8001:8001 auronex-bot
```

---

## 🎯 **MINHA RECOMENDAÇÃO**

### **Para você:** OPÇÃO 1 (Git + GitHub)

**Por quê:**
1. ✅ Controle de versão profissional
2. ✅ Fácil de atualizar (git push/pull)
3. ✅ Backup automático
4. ✅ Gratuito
5. ✅ Padrão da indústria

### **Passo a Passo Completo:**

**Fase 1: Preparar Local (10 min)**
```bash
cd I:\Robo

# Criar .gitignore
echo "venv/" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "db.sqlite3" >> .gitignore
echo ".env" >> .gitignore

# Inicializar Git
git init
git add .
git commit -m "Sistema Auronex Robô Trader - v1.0"
```

**Fase 2: GitHub (5 min)**
```
1. Acesse: github.com
2. Crie conta (se não tiver)
3. "New Repository"
4. Nome: auronex-robo-trader
5. Privado: SIM (para proteger chaves)
6. Copie URL do repositório
```

**Fase 3: Conectar (2 min)**
```bash
git remote add origin https://github.com/SEU-USUARIO/auronex-robo-trader.git
git branch -M main
git push -u origin main
```

**Fase 4: Deploy no Servidor (30 min)**
```bash
# SSH no servidor
ssh root@seu-servidor.com

# Clonar
cd /var/www/
git clone https://github.com/SEU-USUARIO/auronex-robo-trader.git
cd auronex-robo-trader

# Instalar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_fastapi.txt

# Configurar
nano .env
# (Adicione suas chaves)

# Rodar
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 &
```

**Fase 5: Atualizar (sempre que mudar) (1 min)**
```bash
# Local:
git add .
git commit -m "Corrigido navbar"
git push

# Servidor:
cd /var/www/auronex-robo-trader
git pull
systemctl restart auronex
```

---

## 🔧 **FERRAMENTAS NECESSÁRIAS**

### **No seu PC:**
- ✅ Git for Windows (https://git-scm.com/)
- ✅ Conta GitHub (https://github.com/)
- ⚠️ Ou FileZilla para FTP

### **No servidor:**
- ✅ SSH access
- ✅ Python 3.10+
- ✅ Git
- ✅ Nginx (proxy reverso)
- ✅ Supervisor/systemd (manter rodando)

---

## 🌐 **SERVIDORES RECOMENDADOS**

### **1. DigitalOcean (Recomendo!)**
- Preço: $6/mês (básico)
- Ubuntu 22.04
- 1GB RAM, 25GB SSD
- SSH incluído
- Fácil de usar

### **2. AWS Lightsail**
- Preço: $3.50/mês
- Similar ao DigitalOcean
- Integração AWS

### **3. Hostinger VPS**
- Preço: R$ 20/mês
- Suporte em português
- Bom para Brasil

---

## 📝 **CHECKLIST DE DEPLOY**

**Antes de subir:**
- [ ] Criar .gitignore (não enviar venv, db.sqlite3)
- [ ] Criar .env.example (modelo sem chaves)
- [ ] Testar tudo em localhost
- [ ] Documentar no README

**No servidor:**
- [ ] Instalar Python 3.10+
- [ ] Clonar repositório
- [ ] Criar .env com chaves REAIS
- [ ] Instalar dependências
- [ ] Rodar migrações (criar tabelas)
- [ ] Configurar Nginx (proxy reverso)
- [ ] SSL/HTTPS (Let's Encrypt)
- [ ] Supervisor (manter rodando)

---

## 🎯 **RESUMO - MELHOR OPÇÃO**

**Use:** Git + GitHub + DigitalOcean

**Custo:** $6/mês  
**Tempo setup:** 1 hora primeira vez  
**Tempo updates:** 1 minuto sempre  
**Controle de versão:** ✅ Completo  

---

## 💡 **BONUS: APÓS DEPLOY**

**Webhooks vão funcionar 100%:**
```
https://auronex.com.br/api/payments/mercadopago/webhook
https://auronex.com.br/api/payments/stripe/webhook
```

Configure nos painéis e pronto! Redirecionamento automático!

---

**Quer que eu crie o .gitignore e prepare para deploy?** 🚀




