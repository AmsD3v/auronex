# 🚀 GUIA COMPLETO - DEPLOY NO SERVIDOR

**Passo a passo detalhado para deploy do Dashboard React**

---

## 📋 PRÉ-REQUISITOS NO SERVIDOR

```bash
# SSH no servidor
ssh usuario@servidor

# Verificar instalações:
node --version   # v18+
npm --version    # v9+
pm2 --version    # 5.x
```

**Se algo faltar:**
```bash
# Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# PM2
sudo npm install -g pm2
```

---

## 🚀 DEPLOY PASSO A PASSO

### **PASSO 1: Enviar arquivos (no seu PC)**

```bash
# Opção A: Git (Recomendado)
cd I:\Robo
git add .
git commit -m "Dashboard React Enterprise - Porta 8501"
git push origin main
```

```bash
# Opção B: SCP (Manual)
cd I:\Robo
scp -r auronex-dashboard usuario@servidor:/home/usuario/robo/
```

---

### **PASSO 2: No servidor, executar script**

```bash
# SSH
ssh usuario@servidor

# Ir para pasta
cd /home/usuario/robo

# Dar permissão ao script
chmod +x ATUALIZAR_SERVIDOR_REACT.sh

# EXECUTAR! (Faz tudo automaticamente)
./ATUALIZAR_SERVIDOR_REACT.sh
```

**Aguarde ~3-5 minutos**

**O script faz:**
1. ✅ Para Streamlit antigo
2. ✅ Git pull (se usou Git)
3. ✅ npm install
4. ✅ npm run build
5. ✅ Inicia FastAPI (porta 8001)
6. ✅ Inicia React (porta 8501)
7. ✅ Verifica Cloudflare Tunnel
8. ✅ Salva configuração PM2

---

### **PASSO 3: Verificar se funcionou**

```bash
# Ver status
pm2 status

# Deve mostrar:
# fastapi-app      │ online  │ 8001
# auronex-dashboard│ online  │ 8501
```

---

### **PASSO 4: Testar no navegador**

```
https://app.auronex.com.br
```

**Deve aparecer:**
- ✅ Dashboard React
- ✅ Tela de login
- ✅ Sem erros

**Fazer login:**
- ✅ Dashboard carrega
- ✅ Métricas aparecem
- ✅ Bots listados
- ✅ Tempo real funciona

---

## 🔍 VERIFICAÇÕES

### **1. Porta 8501 está aberta?**
```bash
netstat -tulnp | grep 8501
```

**Deve mostrar:**
```
tcp  0  0  0.0.0.0:8501  0.0.0.0:*  LISTEN  12345/node
```

---

### **2. React está respondendo?**
```bash
curl http://localhost:8501
```

**Deve retornar:** HTML do Next.js

---

### **3. FastAPI está respondendo?**
```bash
curl http://localhost:8001/health
```

**Deve retornar:**
```json
{"status":"healthy"}
```

---

### **4. Cloudflare Tunnel ativo?**
```bash
sudo systemctl status cloudflared
```

**Deve mostrar:** `active (running)`

---

## 🐛 ERROS COMUNS

### **Erro: "npm: command not found"**

```bash
# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

### **Erro: "pm2: command not found"**

```bash
# Instalar PM2 globalmente
sudo npm install -g pm2

# Configurar startup
pm2 startup
# Copiar e executar comando que aparecer
```

---

### **Erro: "Permission denied"**

```bash
# Dar permissão ao script
chmod +x ATUALIZAR_SERVIDOR_REACT.sh

# Executar novamente
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

### **Erro: "Port 8501 already in use"**

```bash
# Ver o que está usando
sudo lsof -i :8501

# Matar processo
sudo kill -9 PID

# Reiniciar React
pm2 restart auronex-dashboard
```

---

### **Erro: Build failed**

```bash
# Limpar e reinstalar
cd auronex-dashboard
rm -rf node_modules .next
npm install
npm run build
```

---

## 🎯 COMANDOS RÁPIDOS

### **Reiniciar tudo:**
```bash
./ATUALIZAR_SERVIDOR_REACT.sh
```

### **Ver logs:**
```bash
pm2 logs auronex-dashboard --lines 50
pm2 logs fastapi-app --lines 50
```

### **Reiniciar individual:**
```bash
pm2 restart auronex-dashboard
pm2 restart fastapi-app
```

### **Parar tudo:**
```bash
pm2 stop all
```

### **Iniciar tudo:**
```bash
pm2 start all
```

---

## 📊 CLOUDFLARE TUNNEL - CONFIG

**Arquivo:** `/etc/cloudflared/config.yml`

**Configuração atual (NÃO PRECISA MUDAR!):**

```yaml
tunnel: seu-tunnel-id
credentials-file: /root/.cloudflared/credentials.json

ingress:
  # Landing + API Backend
  - hostname: auronex.com.br
    service: http://localhost:8001
  
  # Admin Panel
  - hostname: admin.auronex.com.br
    service: http://localhost:8001
  
  # Dashboard React (PORTA 8501 - JÁ CONFIGURADA!)
  - hostname: app.auronex.com.br
    service: http://localhost:8501
  
  # Catch-all
  - service: http_status:404
```

**✅ Porta 8501 já está configurada!**  
**✅ Só substituir Streamlit por React!**

---

## 🎊 RESULTADO ESPERADO

**Após executar script:**

```
pm2 status
┌──────────────────┬────┬─────────┬──────┐
│ Name             │ id │ status  │ port │
├──────────────────┼────┼─────────┼──────┤
│ fastapi-app      │ 0  │ online  │ 8001 │
│ auronex-dashboard│ 1  │ online  │ 8501 │
└──────────────────┴────┴─────────┴──────┘
```

**URLs funcionando:**
- ✅ https://auronex.com.br (landing + API)
- ✅ https://admin.auronex.com.br (admin)
- ✅ https://app.auronex.com.br (dashboard React)

---

**SCRIPT PRONTO PARA USAR!** ✅

**EXECUTE NO SERVIDOR:** `./ATUALIZAR_SERVIDOR_REACT.sh` 🚀


