# 🔑 COMO ADICIONAR API KEY - BINANCE TESTNET

**Tempo:** 5 minutos  
**Custo:** GRÁTIS

---

## 📋 PASSO 1: Criar Conta Testnet Binance

### Acesse:
```
https://testnet.binance.vision/
```

### Login/Registro:
- Clique em **"Log In / Register"**
- Escolha **"Sign in with GitHub"** OU **"Sign in with Google"**
- Autorize o acesso

✅ **Pronto! Conta criada!**

---

## 🔑 PASSO 2: Gerar API Key

### 1. No menu superior, clique em **"API Key"**

### 2. Clique em **"Generate HMAC_SHA256 Key"**

### 3. Sistema vai gerar:
```
API Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Secret Key: yyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### 4. **COPIE AMBAS!** (você vai precisar)

⚠️ **IMPORTANTE:** Secret Key aparece **UMA VEZ APENAS**! Copie agora!

---

## 💰 PASSO 3: Adicionar Saldo Testnet (GRÁTIS)

### No dashboard Testnet:

1. Clique em **"Get Test Funds"** ou **"Faucet"**
2. Selecione **USDT**
3. Clique em **"Get 1000 USDT"**

✅ **Pronto! Você tem $1.000 USDT de teste!**

---

## 🔧 PASSO 4: Configurar no Auronex

### Opção A: Script Interativo ⭐ (Mais Fácil)

```bash
cd I:\Robo
python scripts/configurar_api_keys.py
```

**O script vai perguntar:**
```
Selecione a exchange:
1. BINANCE

Numero: 1

API Key: [COLE AQUI]
Secret Key: [COLE AQUI]
É Testnet? (s/n): s
```

✅ **Pronto! API Key configurada e criptografada!**

---

### Opção B: Via Dashboard

1. Abra: http://localhost:8501
2. Login: admin@robotrader.com / admin123
3. Menu → **API Keys**
4. Botão: **"Adicionar API Key"**
5. Preencher:
   - Exchange: Binance
   - API Key: [cole aqui]
   - Secret Key: [cole aqui]
   - Testnet: ✅ (marcar)
6. Salvar

✅ **Pronto!**

---

### Opção C: Direto no .env

Edite o arquivo `.env`:

```env
# Encontre estas linhas e preencha:
BINANCE_TESTNET_API_KEY=cole_sua_api_key_aqui
BINANCE_TESTNET_SECRET_KEY=cole_sua_secret_key_aqui
```

Salve e reinicie.

⚠️ **Menos seguro** - Keys ficam em texto (serão criptografadas só quando usar)

---

## 🔄 PASSO 5: Reiniciar e Testar

```bash
cd I:\Robo
MATAR_TUDO.bat
TESTAR_SERVER_LOCAL_09_11_25.bat
```

### Testar Saldo:

1. Abra: http://localhost:8501
2. Login
3. Dashboard → **Saldo deve aparecer:** $1.000 USDT ✅

---

## ✅ CHECKLIST

- [ ] Criar conta Testnet Binance
- [ ] Gerar API Key + Secret
- [ ] Adicionar saldo teste ($1.000 USDT)
- [ ] Configurar no Auronex (script/dashboard/.env)
- [ ] Reiniciar serviços
- [ ] Verificar saldo aparece

---

## 🎯 RESULTADO

**Após configurar:**
- ✅ Saldo $1.000 USDT aparece
- ✅ Pode criar bots
- ✅ Bots podem fazer trades (simulados)
- ✅ Zero risco (é testnet!)

---

## 💡 DICAS

### Testnet vs Produção:

**Testnet (Recomendado para começar):**
- ✅ Grátis
- ✅ Sem risco
- ✅ Dados reais do mercado
- ✅ Perfeito para testar

**Produção (Só depois de testar):**
- ⚠️ Dinheiro real
- ⚠️ Risco de perda
- ⚠️ Só use após testar MUITO

---

## 🚀 LINKS ÚTEIS

**Binance Testnet:**
- Site: https://testnet.binance.vision/
- Docs: https://testnet.binance.vision/

**Bybit Testnet:**
- Site: https://testnet.bybit.com/

**Outras exchanges:**
- Configure depois conforme precisar

---

## 🎊 PRONTO!

**Siga os 5 passos acima e em 5 minutos terá:**
- ✅ API Key configurada
- ✅ $1.000 USDT de teste
- ✅ Sistema funcionando 100%

---

**Tempo:** 5 minutos  
**Custo:** $0 (tudo grátis!)  
**Resultado:** Sistema completo funcionando! ✅





