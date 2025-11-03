# 🔑 COMO ADICIONAR API KEYS NO SaaS

## 📍 **MÉTODO 1: VIA ADMIN PANEL (Mais Fácil)**

### **Passo 1: Fazer Login no Admin**
```
1. Abrir: http://localhost:8001/admin/
2. Login: admin / admin123
```

### **Passo 2: Criar um Usuário Normal**
```
1. Clicar em "Users" → "Add User"
2. Preencher:
   - Username: seu_email@email.com
   - Password: senha123
   - Password confirmation: senha123
3. Clicar em "Save"
```

### **Passo 3: Adicionar API Key da Binance**
```
1. No menu lateral, clicar em "Exchange api keys"
2. Clicar em "Add Exchange api key"
3. Preencher:
   - User: selecionar o usuário criado
   - Exchange: Binance
   - Api key encrypted: (vai ser preenchido automaticamente)
   - Secret key encrypted: (vai ser preenchido automaticamente)
   - Is testnet: DESMARCAR (para produção)
   - Is active: MARCAR
4. Clicar em "Save"
```

⚠️ **PROBLEMA:** O admin não tem campo para inserir as chaves em texto plano!

---

## 📍 **MÉTODO 2: VIA PYTHON SHELL (Recomendado)**

### **Execute este script:**

```bash
cd I:\Robo\saas
python manage.py shell
```

### **Cole este código:**

```python
from django.contrib.auth.models import User
from users.models import ExchangeAPIKey

# Criar ou buscar usuário
user, created = User.objects.get_or_create(
    username='seu_email@email.com',
    defaults={
        'email': 'seu_email@email.com',
        'first_name': 'Seu Nome'
    }
)

# Definir senha (se for novo usuário)
if created:
    user.set_password('senha123')
    user.save()
    print(f"✅ Usuário criado: {user.email}")
else:
    print(f"ℹ️  Usuário já existe: {user.email}")

# Adicionar API Key da Binance
api_key_obj = ExchangeAPIKey(
    user=user,
    exchange='binance',
    is_testnet=False,  # PRODUÇÃO
    is_active=True
)

# Salvar chaves (criptografadas automaticamente!)
api_key_obj.save_keys(
    api_key='FuwPLJl7mDJH6t4HaWjn4eCqFAQJOccvhCqCLxAcP6vx6ZdjHIysqQ0KGcqPnmef',
    secret_key='qKeH7VI6AEGiR7un7uGyazh9EaKYUugh1sZccVbCPAZ2TerJ3PT7b9F4v5pumF85'
)

print(f"✅ API Key da Binance adicionada!")
print(f"   User: {user.email}")
print(f"   Exchange: Binance (PRODUÇÃO)")
print(f"   Key (mascarada): ***{api_key_obj.api_key[-4:]}")
```

---

## 📍 **MÉTODO 3: VIA API REST (Como usuário faria)**

### **1. Criar conta:**

```bash
curl -X POST http://localhost:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seu_email@email.com",
    "password": "senha123",
    "first_name": "Seu Nome"
  }'
```

**Resposta:**
```json
{
  "message": "Usuário criado com sucesso!",
  "access": "TOKEN_JWT_AQUI",
  "refresh": "REFRESH_TOKEN_AQUI"
}
```

### **2. Adicionar API Key da Binance:**

```bash
curl -X POST http://localhost:8001/api/api-keys/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_JWT_AQUI" \
  -d '{
    "exchange": "binance",
    "api_key": "FuwPLJl7mDJH6t4HaWjn4eCqFAQJOccvhCqCLxAcP6vx6ZdjHIysqQ0KGcqPnmef",
    "secret_key": "qKeH7VI6AEGiR7un7uGyazh9EaKYUugh1sZccVbCPAZ2TerJ3PT7b9F4v5pumF85",
    "is_testnet": false
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "exchange": "binance",
  "api_key_masked": "***nmef",
  "is_testnet": false,
  "is_active": true,
  "created_at": "2025-10-27T21:00:00Z"
}
```

---

## 🎯 **RECOMENDAÇÃO:**

Use **MÉTODO 2 (Python Shell)** - é o mais rápido e seguro!

---

## ⚠️ **SEGURANÇA:**

✅ **O que acontece ao salvar:**
1. Suas chaves são criptografadas com Fernet
2. Armazenadas no banco como texto criptografado
3. Nunca retornadas pela API (só mascaradas: ***XYZ)
4. Só descriptografadas quando o bot precisa usar

✅ **Quem pode ver:**
- Admin: Vê que a chave existe, mas vê mascarada (***nmef)
- Usuário: Via API, vê mascarada também
- Bot: Descriptografa só quando precisa executar trade

---

## 📊 **VERIFICAR SE FUNCIONOU:**

```bash
cd I:\Robo\saas
python manage.py shell
```

```python
from users.models import ExchangeAPIKey

# Listar todas as keys
keys = ExchangeAPIKey.objects.all()
for key in keys:
    print(f"User: {key.user.email}")
    print(f"Exchange: {key.exchange}")
    print(f"Testnet: {key.is_testnet}")
    print(f"Ativa: {key.is_active}")
    print(f"Key (mascarada): ***{key.api_key[-4:]}")
    print("---")
```

---

## 🎉 **PRONTO!**

Agora suas chaves da Binance estão:
- ✅ Criptografadas no banco
- ✅ Vinculadas ao seu usuário
- ✅ Prontas para uso pelo bot

**Cada usuário do SaaS faria o mesmo processo!**

