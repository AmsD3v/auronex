# 🌐 COMO VERIFICAR SEU IP PÚBLICO

## 💻 **NO SERVIDOR (XUBUNTU)**

```bash
# Opção 1: curl
curl ifconfig.me

# Opção 2: wget
wget -qO- ifconfig.me

# Opção 3: dig
dig +short myip.opendns.com @resolver1.opendns.com

# Opção 4: ip público do roteador
curl ipinfo.io/ip
```

**Exemplo de saída:**
```
189.123.45.67
```

**Este é seu IP público!**

---

## 🌍 **NO WINDOWS (SEU PC)**

### **Método 1: Site (Mais fácil)**
```
Acesse: https://meuip.com.br/
ou
https://www.whatismyip.com/
```

### **Método 2: PowerShell**
```powershell
(Invoke-WebRequest -Uri "https://api.ipify.org").Content
```

### **Método 3: CMD**
```
nslookup myip.opendns.com resolver1.opendns.com
```

---

## ⚠️ **IMPORTANTE**

### **IP Dinâmico vs Estático**

**Verifique com sua operadora:**
```
IP Dinâmico: Muda quando reinicia modem
IP Estático: Sempre o mesmo (ideal!)
```

### **Soluções se IP muda:**

**Opção A: No-IP (GRÁTIS)**
```
1. Cadastre: www.noip.com
2. Crie hostname: auronex.ddns.net
3. Instale cliente No-IP no servidor
4. Atualiza IP automaticamente
```

**Opção B: DuckDNS (GRÁTIS)**
```
1. duckdns.org
2. Crie: auronex.duckdns.org
3. Atualiza via script/cron
```

**Opção C: Contratar IP Fixo**
```
Ligue para operadora
Custo: ~R$ 20-50/mês extra
```

---

## 🔧 **USAR NO DOMÍNIO**

**Após descobrir IP público:**

```
Exemplo: 189.123.45.67

No Registro.br:
  Tipo: A
  Nome: @
  Dados: 189.123.45.67
  TTL: 3600
```

**Aguardar:** 1-24h (propagação DNS)

**Testar:**
```bash
ping auronex.com.br
# Deve responder com seu IP!
```

---

**Descubra seu IP público com:** `curl ifconfig.me` 🌐


