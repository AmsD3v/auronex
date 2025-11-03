# 🔑 CRIAR TOKEN DO GITHUB

## ❌ **ERRO QUE VOCÊ RECEBEU**

```
remote: Invalid username or token. 
Password authentication is not supported
```

**GitHub não aceita mais senha!** Precisa de **Personal Access Token (PAT)**

---

## ✅ **SOLUÇÃO (5 MINUTOS)**

### **1. Criar Token no GitHub:**

**Acesse:** https://github.com/settings/tokens

**Ou:**
1. GitHub → Seu perfil (canto superior direito)
2. Settings
3. Developer settings (final da lista)
4. Personal access tokens → Tokens (classic)
5. Generate new token → Generate new token (classic)

### **2. Configurar Token:**

**Nome:** `Auronex Servidor`

**Expiração:** No expiration (ou 90 days)

**Permissões (marcar):**
- ✅ repo (todos)
- ✅ workflow
- ✅ write:packages
- ✅ read:packages

**Clique:** Generate token

### **3. COPIAR TOKEN:**

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **COPIE AGORA!** Só aparece uma vez!

---

## 🔄 **USAR O TOKEN**

### **No servidor:**

```bash
cd /var/www/auronex

# Clonar com token
git clone https://SEU-TOKEN@github.com/AmsD3v/auronex.git .

# OU se já tentou clonar:
rm -rf .git

# Clonar novamente
git clone https://ghp_SeuTokenAqui@github.com/AmsD3v/auronex.git .
```

### **Formato correto:**
```
https://TOKEN@github.com/USER/REPO.git
```

---

## 💡 **ALTERNATIVA: SSH (Mais Seguro)**

**Setup SSH (recomendado para longo prazo):**

```bash
# 1. Gerar chave SSH
ssh-keygen -t ed25519 -C "angellosilvadev@gmail.com"

# 2. Ver chave pública
cat ~/.ssh/id_ed25519.pub

# 3. Copiar chave

# 4. GitHub → Settings → SSH and GPG keys → New SSH key
#    Cole a chave pública

# 5. Testar
ssh -T git@github.com

# 6. Clonar com SSH
git clone git@github.com:AmsD3v/auronex.git .
```

---

## 🎯 **PRÓXIMO PASSO**

Após clonar com sucesso:

```bash
cd /var/www/auronex

# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar
pip install -r requirements_fastapi.txt

# Criar .env
nano .env
```

**.env (IMPORTANTE!):**
```
FASTAPI_SECRET_KEY=seu-secret-super-seguro
MERCADOPAGO_ACCESS_TOKEN=APP_USR-7940...
STRIPE_SECRET_KEY=sk_live_51SN...
```

---

**Use o TOKEN do GitHub para clonar!** 🚀



