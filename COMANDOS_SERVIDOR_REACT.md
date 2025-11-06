# 🚀 COMANDOS DO SERVIDOR - DASHBOARD REACT

**Guia rápido de comandos para gerenciar o servidor**

---

## 📦 DEPLOY INICIAL (Primeira vez)

```bash
# SSH no servidor
ssh usuario@servidor

# Ir para pasta do projeto
cd /home/usuario/robo

# Pull do GitHub
git pull origin main

# Executar script de atualização
chmod +x ATUALIZAR_SERVIDOR_REACT.sh
./ATUALIZAR_SERVIDOR_REACT.sh
```

**Aguarde ~3-5 minutos**

**Resultado:**
- ✅ FastAPI rodando (porta 8001)
- ✅ React rodando (porta 8501)
- ✅ Cloudflare Tunnel rodando
- ✅ https://app.auronex.com.br ONLINE!

---

## 🔄 ATUALIZAR CÓDIGO (Atualizações futuras)

```bash
# SSH no servidor
ssh usuario@servidor

# Ir para pasta
cd /home/usuario/robo

# Executar script (faz tudo automaticamente!)
./ATUALIZAR_SERVIDOR_REACT.sh
```

**O script faz:**
1. ✅ Para serviços antigos
2. ✅ Git pull
3. ✅ npm install
4. ✅ npm run build
5. ✅ Reinicia FastAPI
6. ✅ Reinicia React
7. ✅ Verifica Tunnel
8. ✅ Salva PM2

**Tempo:** ~3 minutos ⚡

---

## 🔍 VERIFICAR STATUS

### **Ver todos os serviços:**
```bash
pm2 status
```

**Deve mostrar:**
```
┌──────────────────┬────┬─────────┬──────┐
│ Name             │ id │ status  │ port │
├──────────────────┼────┼─────────┼──────┤
│ fastapi-app      │ 0  │ online  │ 8001 │
│ auronex-dashboard│ 1  │ online  │ 8501 │
└──────────────────┴────┴─────────┴──────┘
```

---

### **Ver logs em tempo real:**
```bash
# Dashboard React
pm2 logs auronex-dashboard --lines 50

# FastAPI
pm2 logs fastapi-app --lines 50

# Ambos
pm2 logs --lines 30
```

---

### **Verificar Cloudflare Tunnel:**
```bash
sudo systemctl status cloudflared
```

**Deve mostrar:** `active (running)`

---

## 🔧 COMANDOS ÚTEIS

### **Reiniciar serviços:**
```bash
# Reiniciar React
pm2 restart auronex-dashboard

# Reiniciar FastAPI
pm2 restart fastapi-app

# Reiniciar tudo
pm2 restart all
```

---

### **Parar serviços:**
```bash
# Parar React
pm2 stop auronex-dashboard

# Parar FastAPI
pm2 stop fastapi-app

# Parar tudo
pm2 stop all
```

---

### **Iniciar serviços:**
```bash
# Iniciar React
pm2 start auronex-dashboard

# Iniciar FastAPI
pm2 start fastapi-app

# Iniciar tudo
pm2 start all
```

---

### **Deletar e recriar:**
```bash
# Se precisar recriar do zero
pm2 delete auronex-dashboard
pm2 delete fastapi-app

# Depois executar script novamente
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

## 🐛 TROUBLESHOOTING

### **Problema: app.auronex.com.br não carrega**

```bash
# 1. Verificar se React está rodando
pm2 status | grep auronex-dashboard

# 2. Ver logs
pm2 logs auronex-dashboard --lines 100

# 3. Verificar porta 8501
netstat -tulnp | grep 8501

# 4. Reiniciar
pm2 restart auronex-dashboard
```

---

### **Problema: CORS error**

```bash
# Editar FastAPI para adicionar domínio
nano fastapi_app/main.py

# Adicionar em allow_origins:
# "https://app.auronex.com.br"

# Reiniciar FastAPI
pm2 restart fastapi-app
```

---

### **Problema: 502 Bad Gateway**

```bash
# React não respondendo
pm2 restart auronex-dashboard

# Esperar 10s
sleep 10

# Testar novamente
curl http://localhost:8501
```

---

### **Problema: Build falha**

```bash
# Limpar e reinstalar
cd auronex-dashboard
rm -rf node_modules .next
npm install
npm run build
pm2 restart auronex-dashboard
```

---

## 📊 MONITORAMENTO

### **Dashboard PM2:**
```bash
# Abrir dashboard PM2 (interface web)
pm2 web

# Acessa em:
http://seu-ip:9615
```

---

### **Recursos do sistema:**
```bash
# CPU e memória
pm2 monit

# Uso detalhado
htop
```

---

### **Logs contínuos:**
```bash
# Seguir logs em tempo real
pm2 logs auronex-dashboard -f

# Ctrl+C para sair
```

---

## 🔄 ROTINA DE MANUTENÇÃO

### **Diária (automática):**
```bash
# PM2 já faz restart automático se crashar
# Configurado em ecosystem.config.js:
# autorestart: true
```

---

### **Semanal (manual):**
```bash
# Verificar status
pm2 status

# Ver logs de erros
pm2 logs --err --lines 100

# Reiniciar se necessário
pm2 restart all
```

---

### **Mensal (atualização):**
```bash
# Pull do GitHub
git pull origin main

# Executar script de atualização
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

## 📝 CHECKLIST PÓS-DEPLOY

### **Verificar:**
- [ ] https://auronex.com.br carrega (landing)
- [ ] https://admin.auronex.com.br carrega (admin)
- [ ] https://app.auronex.com.br carrega (dashboard React)
- [ ] Login funciona
- [ ] Dashboard carrega
- [ ] Bots aparecem
- [ ] Modal Config funciona
- [ ] Tempo real funciona (<5s)

---

## 🎊 COMANDOS RESUMIDOS

```bash
# Atualizar tudo (após git push)
./ATUALIZAR_SERVIDOR_REACT.sh

# Ver status
pm2 status

# Ver logs
pm2 logs auronex-dashboard

# Reiniciar
pm2 restart auronex-dashboard

# Parar tudo
pm2 stop all
```

---

**SCRIPT CRIADO:** `ATUALIZAR_SERVIDOR_REACT.sh` ✅

**PRONTO PARA USAR NO SERVIDOR!** 🚀


