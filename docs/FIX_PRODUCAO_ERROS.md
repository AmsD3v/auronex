# 🔧 FIX PRODUÇÃO - Erros ao Buscar Bots/API Keys

**Erro:** "Tempo Real carregando" + "Erro ao buscar bots" + "Configure API Key"

**Causa:** Banco de produção diferente do local!

---

## 🔍 DIAGNÓSTICO

**NO SERVIDOR (execute):**

```bash
cd /home/serverhome/auronex
source venv/bin/activate

# 1. Verificar bots
python -c "from fastapi_app.database import SessionLocal; from fastapi_app.models import BotConfiguration; db = SessionLocal(); bots = db.query(BotConfiguration).all(); print(f'Bots: {len(bots)}'); db.close()"

# 2. Verificar API Keys  
python -c "from fastapi_app.database import SessionLocal; from fastapi_app.models import ExchangeAPIKey; db = SessionLocal(); keys = db.query(ExchangeAPIKey).all(); print(f'API Keys: {len(keys)}'); db.close()"

# 3. Verificar usuários
python -c "from fastapi_app.database import SessionLocal; from fastapi_app.models import User; db = SessionLocal(); users = db.query(User).all(); print(f'Usuarios: {len(users)}'); [print(f'  {u.id}: {u.email}') for u in users]; db.close()"
```

---

## ✅ SOLUÇÃO

**Se retornar 0 para qualquer um:**

### **1. Criar usuário admin:**
```bash
python -c "
from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from fastapi_app.auth import get_password_hash

db = SessionLocal()

admin = User(
    email='admin@auronex.com',
    first_name='Admin',
    last_name='Auronex',
    hashed_password=get_password_hash('admin123'),
    is_active=True,
    is_staff=True,
    is_superuser=True
)

db.add(admin)
db.commit()
print(f'Admin criado: {admin.id}')
db.close()
"
```

### **2. Criar API Keys testnet:**
```bash
python criar_api_keys_testnet.py
```

### **3. Criar bot exemplo:**
```bash
python -c "
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, User

db = SessionLocal()

user = db.query(User).first()

bot = BotConfiguration(
    user_id=user.id,
    name='Bot Binance Prod',
    exchange='binance',
    symbols=['BTC/USDT', 'ETH/USDT', 'SOL/USDT'],
    capital=2.0,
    is_active=True,
    is_testnet=True,
    strategy='scalping',
    analysis_interval=5
)

db.add(bot)
db.commit()
print(f'Bot criado: {bot.id}')
db.close()
"
```

---

## 🎯 DEPOIS

**Reiniciar:**
```bash
pm2 restart all
```

**Testar:**
```
https://app.auronex.com.br/
Login: admin@auronex.com / admin123
```

**Deve funcionar!** ✅

---

**Scripts já no GitHub! Atualize servidor primeiro!** 🚀

