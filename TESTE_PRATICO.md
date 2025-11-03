# 🧪 TESTE PRÁTICO - PASSO A PASSO

## 🎯 **OBJETIVO:**
Você vai fazer login no RoboTrader e ver suas API Keys

---

## ✅ **TESTE 1: LOGIN NO ADMIN**

### **Passo 1:**
Abra seu navegador (Chrome, Firefox, Edge, etc.)

### **Passo 2:**
Digite na barra de endereço:
```
http://localhost:8001/admin/
```

### **Passo 3:**
Você verá uma tela de login. Digite EXATAMENTE:
```
Username: admin
Password: admin123
```

### **Passo 4:**
Clique no botão "Log in"

### **✅ RESULTADO ESPERADO:**
Você verá uma página com:
- "Django administration" no topo
- Menu lateral com: Users, Bot configurations, Exchange api keys, etc.

### **❌ SE DER ERRO:**
- Verifique se digitou EXATAMENTE: `admin` e `admin123`
- Verifique se o servidor está rodando (deve estar!)
- Tire print da tela e me mande

---

## ✅ **TESTE 2: VER USUÁRIOS**

### **Passo 1:**
No menu lateral, clique em "Users"

### **Passo 2:**
Você verá uma lista de usuários:
```
USERNAME                   EMAIL                     STAFF   SUPERUSER
admin                      admin@robotrader.com      ✅      ✅
trader@robotrader.com      trader@robotrader.com     ❌      ❌
```

### **✅ INTERPRETAÇÃO:**
- Existem 2 usuários no sistema
- `admin` é você (superuser)
- `trader@robotrader.com` é um usuário de exemplo

### **✅ CONCLUSÃO:**
Nenhum desses usuários tem relação com a Binance!
São usuários DO ROBOTRADER!

---

## ✅ **TESTE 3: VER API KEYS**

### **Passo 1:**
No menu lateral, clique em "Exchange api keys"

### **Passo 2:**
Você verá:
```
USER                      EXCHANGE    TESTNET    ACTIVE    CREATED
trader@robotrader.com     binance     ❌         ✅        Oct 27, 2025
```

### **Passo 3:**
Clique na linha para ver detalhes

### **Passo 4:**
Você verá:
```
User: trader@robotrader.com
Exchange: Binance
Api key encrypted: gAAAAABm8x2Y...
Secret key encrypted: gAAAAABm8x3Z...
Is testnet: ☐ (desmarcado)
Is active: ☑ (marcado)
```

### **✅ INTERPRETAÇÃO:**
- O usuário `trader@robotrader.com` tem uma API Key da Binance
- A API Key está CRIPTOGRAFADA (gAAAAAB...)
- Essa é a chave: FuwPLJl7m...nmef (sua!)
- Está ativa e pronta para usar

### **✅ CONCLUSÃO:**
A API Key da Binance foi adicionada COM SUCESSO!
O bot pode usar essa chave para operar!

---

## ✅ **TESTE 4: VERIFICAR NO BANCO DE DADOS**

### **Passo 1:**
Abra PowerShell e execute:
```powershell
cd I:\Robo\saas
..\venv\Scripts\activate
python manage.py shell
```

### **Passo 2:**
Cole este código:
```python
from users.models import ExchangeAPIKey

keys = ExchangeAPIKey.objects.all()
print(f"Total de API Keys: {keys.count()}\n")

for key in keys:
    print(f"Usuario: {key.user.email}")
    print(f"Corretora: {key.exchange}")
    print(f"Testnet: {key.is_testnet}")
    print(f"Ativa: {key.is_active}")
    print(f"Key (mascarada): ***{key.api_key[-4:]}")
    print("---")
```

### **✅ RESULTADO ESPERADO:**
```
Total de API Keys: 1

Usuario: trader@robotrader.com
Corretora: binance
Testnet: False
Ativa: True
Key (mascarada): ***nmef
---
```

### **✅ INTERPRETAÇÃO:**
- Existe 1 API Key cadastrada
- Pertence ao usuário `trader@robotrader.com`
- É da Binance (PRODUÇÃO, não testnet)
- Termina com "nmef" (últimos 4 caracteres de FuwPLJl7m...nmef)

---

## ✅ **TESTE 5: CRIAR UM BOT**

### **Passo 1:**
No admin, clicar em "Bot configurations"

### **Passo 2:**
Clicar em "ADD BOT CONFIGURATION" (canto superior direito)

### **Passo 3:**
Preencher:
```
User: trader@robotrader.com
Name: Meu Primeiro Bot
Exchange: binance
Symbols: ["BTCUSDT"]
Capital: 100.00
Strategy: mean_reversion
Timeframe: 15m
Stop loss percent: 1.500
Take profit percent: 3.000
Is active: ☐ (deixar desmarcado)
```

### **Passo 4:**
Clicar em "Save"

### **✅ RESULTADO:**
Bot criado com sucesso!

### **Passo 5:**
Voltar para lista de bots e ver:
```
USER                      NAME                EXCHANGE    ACTIVE
trader@robotrader.com     Meu Primeiro Bot    binance     ❌
```

### **✅ CONCLUSÃO:**
- Bot criado
- Vinculado ao usuário `trader@robotrader.com`
- Vai usar a API Key da Binance desse usuário
- Ainda não está ativo (não vai operar ainda)

---

## 🎯 **RESUMO DOS TESTES:**

```
✅ Login funcionou (admin / admin123)
✅ Viu 2 usuários no sistema
✅ Viu 1 API Key cadastrada (Binance)
✅ API Key está criptografada
✅ Criou 1 bot de exemplo

CONCLUSÃO:
- Sistema funcionando perfeitamente!
- API Keys da Binance configuradas!
- Pronto para operar!
```

---

## ❓ **PERGUNTAS FREQUENTES:**

### **P1: Por que não consigo fazer login com minha senha da Binance?**
**R:** Porque você não faz login com dados da Binance!  
Você faz login com: `admin` / `admin123`

### **P2: Onde ficam minhas API Keys da Binance?**
**R:** No menu "Exchange api keys" do admin.  
Estão criptografadas no banco de dados.

### **P3: Como o bot sabe qual API Key usar?**
**R:** Quando você cria o bot, escolhe:
- Usuário (quem é o dono)
- Exchange (Binance/Bybit/etc)

O bot busca a API Key daquele usuário para aquela corretora.

### **P4: Posso ter múltiplas API Keys?**
**R:** Sim! Você pode ter:
- 1 API Key da Binance
- 1 API Key da Bybit
- 1 API Key da OKX
- etc.

Cada bot usa a API Key da corretora escolhida.

### **P5: Minha senha da Binance fica salva no RoboTrader?**
**R:** NÃO! Nunca!  
O RoboTrader NUNCA pede sua senha da Binance!  
Só usa API Keys (que você pode revogar a qualquer momento).

---

## 🚀 **PRÓXIMOS PASSOS:**

Depois desses testes, você pode:

1. ✅ Criar mais bots
2. ✅ Adicionar API Keys de outras corretoras
3. ✅ Ativar bots para começar a operar
4. ✅ Ver trades no admin
5. ✅ Monitorar performance

---

**FAÇA ESSES TESTES AGORA E ME DIGA O RESULTADO! ✅**

