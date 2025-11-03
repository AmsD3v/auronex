# 🚀 INSTALAÇÃO ROBOTRADER SaaS

## **OPÇÃO 1: DESENVOLVIMENTO LOCAL**

### **1. Instalar PostgreSQL**
```bash
# Windows: Baixar de postgresql.org
# macOS: brew install postgresql
# Linux: sudo apt install postgresql
```

### **2. Criar banco de dados**
```sql
CREATE DATABASE robotrader_saas;
CREATE USER robotrader WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE robotrader_saas TO robotrader;
```

### **3. Instalar Redis**
```bash
# Windows: Baixar de redis.io
# macOS: brew install redis
# Linux: sudo apt install redis-server
```

### **4. Configurar ambiente**
```bash
cd I:\Robo\saas
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r ../requirements_saas.txt
```

### **5. Configurar .env**
```bash
cp .env.example .env
# Editar .env com suas credenciais
```

### **6. Gerar chave de criptografia**
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# Copiar para ENCRYPTION_KEY no .env
```

### **7. Rodar migrations**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### **8. Iniciar servidores**

**Terminal 1 - Django:**
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
celery -A saas worker --loglevel=info
```

**Terminal 3 - Celery Beat:**
```bash
celery -A saas beat --loglevel=info
```

**Acessar:**
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## **OPÇÃO 2: DEPLOY HEROKU (PRODUÇÃO)**

### **1. Instalar Heroku CLI**
```bash
# Baixar de heroku.com/install
heroku login
```

### **2. Criar app**
```bash
cd I:\Robo\saas
heroku create robotrader-saas

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Adicionar Redis
heroku addons:create heroku-redis:hobby-dev
```

### **3. Configurar variáveis**
```bash
heroku config:set DJANGO_SECRET_KEY="sua-chave-aqui"
heroku config:set DEBUG=False
heroku config:set ENCRYPTION_KEY="sua-chave-fernet"
```

### **4. Deploy**
```bash
git init
git add .
git commit -m "Initial SaaS deploy"
heroku git:remote -a robotrader-saas
git push heroku main
```

### **5. Rodar migrations no Heroku**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### **6. Escalar dynos**
```bash
heroku ps:scale web=1 worker=1 beat=1
```

**Acessar:**
- https://robotrader-saas.herokuapp.com

---

## **OPÇÃO 3: DEPLOY RAILWAY (MAIS FÁCIL)**

### **1. Criar conta em railway.app**

### **2. Conectar GitHub**
- Fazer push do código para GitHub
- Conectar repositório no Railway

### **3. Configurar**
Railway detecta automaticamente Django e configura:
- PostgreSQL
- Redis
- Variáveis de ambiente

### **4. Deploy automático**
Cada push para GitHub = deploy automático!

---

## **🔒 SEGURANÇA - IMPORTANTE!**

### **Nunca commitar:**
```
❌ .env (credenciais)
❌ db.sqlite3 (banco local)
❌ __pycache__/
❌ *.pyc
```

### **Criar .gitignore:**
```
.env
*.pyc
__pycache__/
db.sqlite3
venv/
staticfiles/
media/
```

---

## **📊 MONITORAMENTO**

### **Logs em produção:**
```bash
# Heroku
heroku logs --tail

# Railway
railway logs
```

### **Status dos workers:**
```bash
heroku ps
```

---

## **🎯 PRÓXIMOS PASSOS APÓS INSTALAÇÃO:**

1. **Criar conta de teste**
2. **Adicionar API Keys**
3. **Criar configuração de bot**
4. **Iniciar bot**
5. **Ver trades no dashboard**

---

## **💰 CUSTOS ESTIMADOS**

### **Desenvolvimento (Local):**
```
✅ $0 - Totalmente grátis
```

### **Produção (Heroku):**
```
PostgreSQL: $0 (hobby)
Redis: $0 (hobby)
Web dyno: $7/mês
Worker dyno: $7/mês
Beat dyno: $7/mês
---
Total: ~$21/mês
```

### **Produção (Railway):**
```
Tudo incluído: $5-10/mês
(Mais barato!)
```

---

## **❓ PROBLEMAS COMUNS**

### **"ModuleNotFoundError: No module named 'psycopg2'"**
```bash
pip install psycopg2-binary
```

### **"Connection refused" no Redis**
```bash
# Iniciar Redis
redis-server
```

### **"OperationalError: FATAL: database does not exist"**
```bash
# Criar banco manualmente
createdb robotrader_saas
```

---

**Sistema pronto para rodar! 🚀**

