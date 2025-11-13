# 🔧 FIX PRODUÇÃO - API Keys

**Problema:** "Tempo Real" carregando + "Configure API Key"

**Causa:** Produção não tem API Keys cadastradas!

---

## ✅ SOLUÇÃO (NO SERVIDOR)

### **1. Verificar se tem API Keys:**

```bash
cd /home/serverhome/auronex
source venv/bin/activate
python -c "from fastapi_app.database import SessionLocal; from fastapi_app.models import ExchangeAPIKey; db = SessionLocal(); keys = db.query(ExchangeAPIKey).all(); print(f'API Keys: {len(keys)}'); db.close()"
```

**Se retornar 0 = precisa adicionar!**

---

### **2. Adicionar API Keys:**

**TESTNET (para Paper Trading):**

```bash
cd /home/serverhome/auronex
python criar_api_keys_testnet.py
```

**Script vai criar:**
- Binance Testnet (usuário 74 ou 1)
- Mercado Bitcoin Testnet

---

### **3. Verificar endpoint:**

```bash
curl http://localhost:8001/api/exchange/balance
```

**Deve retornar:**
```json
{"total_usd": 4.0, ...}
```

**Se retornar "Not authenticated" = código antigo!**

---

## 🎯 SCRIPT PARA CRIAR (vou adicionar)

Arquivo: `criar_api_keys_testnet.py`

---

**Execute no servidor e me diga resultado!** 🎯

