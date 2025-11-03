# 📸 GUIA VISUAL PASSO A PASSO - ROBOTRADER SaaS

## 🎯 **OBJETIVO:**
Fazer login no RoboTrader e adicionar suas API Keys da Binance

---

## 📍 **PASSO 1: FAZER LOGIN NO ROBOTRADER**

### **1.1. Abrir navegador**
```
URL: http://localhost:8001/admin/
```

### **1.2. Tela de login aparece:**
```
┌─────────────────────────────────────┐
│  Django administration              │
├─────────────────────────────────────┤
│                                     │
│  Username: [____________]           │
│                                     │
│  Password: [____________]           │
│                                     │
│       [  Log in  ]                  │
│                                     │
└─────────────────────────────────────┘
```

### **1.3. DIGITE:**
```
Username: admin
Password: admin123
```

### **1.4. Clicar em "Log in"**

### **✅ RESULTADO:**
Você verá a tela do admin com:
```
┌─────────────────────────────────────┐
│  DJANGO ADMINISTRATION              │
├─────────────────────────────────────┤
│  Site administration                │
│                                     │
│  AUTHENTICATION AND AUTHORIZATION   │
│  + Groups                           │
│  + Users                            │
│                                     │
│  BOTS                               │
│  + Bot configurations               │
│  + Trades                           │
│                                     │
│  USERS                              │
│  + Exchange api keys                │
│  + User profiles                    │
│                                     │
│  PAYMENTS                           │
│  + Subscriptions                    │
│  + Payments                         │
└─────────────────────────────────────┘
```

**✅ PRONTO! Você está logado no RoboTrader!**

---

## 📍 **PASSO 2: VER AS API KEYS JÁ CADASTRADAS**

### **2.1. No menu lateral, clicar em "Exchange api keys"**

### **2.2. Você verá:**
```
┌─────────────────────────────────────────────────────────┐
│  Select exchange api key to change                      │
├─────────────────────────────────────────────────────────┤
│  User              Exchange    Testnet   Active         │
├─────────────────────────────────────────────────────────┤
│  trader@robot...   binance     ❌       ✅             │
└─────────────────────────────────────────────────────────┘
```

### **2.3. Clicar na linha para ver detalhes**

### **2.4. Você verá:**
```
┌─────────────────────────────────────┐
│  Change exchange api key            │
├─────────────────────────────────────┤
│  User: trader@robotrader.com        │
│  Exchange: Binance                  │
│  Api key encrypted: gAAAAA...       │ ← CRIPTOGRAFADO!
│  Secret key encrypted: gAAAAA...    │ ← CRIPTOGRAFADO!
│  Is testnet: ☐ (desmarcado)        │
│  Is active: ☑ (marcado)            │
│  Created: 2025-10-27 21:22         │
│                                     │
│  [  Save  ] [  Delete  ]            │
└─────────────────────────────────────┘
```

**✅ As chaves estão CRIPTOGRAFADAS! Seguras!**

---

## 📍 **PASSO 3: ENTENDER O QUE ESTÁ ACONTECENDO**

### **Banco de dados (SQLite):**
```sql
SELECT * FROM exchange_api_keys;

| id | user_id | exchange | api_key_encrypted        | is_active |
|----|---------|----------|--------------------------|-----------|
| 1  | 2       | binance  | gAAAAABm8x2Y...criptog   | 1         |
                            ↑
                            Sua API Key FuwPLJl7m...nmef
                            está aqui CRIPTOGRAFADA!
```

### **Quando o bot roda:**
```python
# 1. Busca a API Key do usuário
api_key = ExchangeAPIKey.objects.get(
    user=user,
    exchange='binance'
)

# 2. DESCRIPTOGRAFA na hora de usar
decrypted_key = api_key.api_key  # FuwPLJl7m...nmef
decrypted_secret = api_key.secret_key  # qKeH7VI6A...mF85

# 3. Conecta na Binance
exchange = ccxt.binance({
    'apiKey': decrypted_key,
    'secret': decrypted_secret
})

# 4. Executa trade
order = exchange.create_order(...)
```

**O bot NUNCA vê sua senha da Binance!**  
**Só usa API Keys!**

---

## 📍 **PASSO 4: ADICIONAR NOVA API KEY (Exemplo Bybit)**

### **4.1. No admin, clicar em "Exchange api keys"**

### **4.2. Clicar em "ADD EXCHANGE API KEY" (canto superior direito)**

### **4.3. ⚠️ PROBLEMA: Não dá para adicionar via admin!**

O formulário do admin não tem campo para texto plano!

### **4.4. SOLUÇÃO: Usar Python shell**

```bash
cd I:\Robo\saas
python manage.py shell
```

```python
from django.contrib.auth.models import User
from users.models import ExchangeAPIKey

# Buscar usuário
user = User.objects.get(username='trader@robotrader.com')

# Adicionar API Key da Bybit
api_key_bybit = ExchangeAPIKey(
    user=user,
    exchange='bybit',
    is_testnet=False,
    is_active=True
)

api_key_bybit.save_keys(
    api_key='Z9hUO9vQ8Wedruf4Rt',
    secret_key='7xudnlVQtW8g7kyA4v7x8Uot3bM4oiInelND'
)

print("✅ API Key da Bybit adicionada!")
```

### **4.5. Verificar no admin**

Recarregar a página "Exchange api keys" e verá:

```
┌─────────────────────────────────────────────────────────┐
│  User              Exchange    Testnet   Active         │
├─────────────────────────────────────────────────────────┤
│  trader@robot...   binance     ❌       ✅             │
│  trader@robot...   bybit       ❌       ✅             │ ← NOVA!
└─────────────────────────────────────────────────────────┘
```

**✅ Agora tem 2 corretoras!**

---

## 📍 **PASSO 5: CRIAR BOT**

### **5.1. No admin, clicar em "Bot configurations"**

### **5.2. Clicar em "ADD BOT CONFIGURATION"**

### **5.3. Preencher:**
```
User: trader@robotrader.com
Name: Meu Bot Scalper
Exchange: binance  ← ESCOLHE A CORRETORA!
Symbols: ["BTCUSDT", "ETHUSDT"]
Capital: 1000.00
Strategy: mean_reversion
Timeframe: 5m
Stop loss percent: 1.500
Take profit percent: 3.000
Is active: ☐ (deixar desmarcado por enquanto)
```

### **5.4. Clicar em "Save"**

### **✅ Bot criado!**

---

## 📍 **PASSO 6: ATIVAR BOT**

### **6.1. Na lista de bots, clicar no bot criado**

### **6.2. Marcar "Is active"**

### **6.3. Clicar em "Save"**

### **✅ Bot ativo!**

### **6.4. O que acontece:**
```python
# Celery Beat (a cada 5 segundos):
bots = BotConfiguration.objects.filter(is_active=True)

for bot in bots:
    # Buscar API Key DESSE usuário para ESSA corretora
    api_key = bot.user.api_keys.filter(
        exchange=bot.exchange  # 'binance'
    ).first()
    
    # Conectar e operar
    exchange = ccxt.binance({
        'apiKey': api_key.api_key,
        'secret': api_key.secret_key
    })
    
    # Executar estratégia
    ...
```

---

## 🎓 **RESUMO FINAL:**

### **Você NÃO faz login com dados da Binance!**

```
❌ ERRADO:
   Username: email_da_binance@gmail.com
   Password: senha_da_binance
   
✅ CERTO:
   Username: admin (ou trader@robotrader.com)
   Password: admin123 (ou trader123)
   
   Depois, ADICIONA as API Keys da Binance
   (geradas no site da Binance)
```

### **Fluxo completo:**

```
1. Login no ROBOTRADER
   ↓
2. Adicionar API Keys (da Binance/Bybit)
   ↓
3. Criar bot (escolher corretora)
   ↓
4. Ativar bot
   ↓
5. Bot opera usando as API Keys
```

### **Você NUNCA dá senha da Binance para o RoboTrader!**

---

## 🚀 **TESTE AGORA:**

1. Abra: http://localhost:8001/admin/
2. Digite:
   - Username: `admin`
   - Password: `admin123`
3. Explore o sistema!

**Se der erro, mande print da tela!**

