# 🔧 SOLUÇÃO: npm: comando não encontrado

**Erro:** `npm: comando não encontrado`  
**Causa:** Node.js não está instalado no servidor  
**Solução:** Instalar Node.js antes de rodar o script  

---

## ✅ SOLUÇÃO RÁPIDA (2 comandos)

### **No servidor (SSH):**

```bash
# 1. Instalar Node.js (script automático)
chmod +x SETUP_SERVIDOR_NODEJS.sh
./SETUP_SERVIDOR_NODEJS.sh
```

**Aguarde ~3-5 minutos** (download + instalação)

```bash
# 2. Executar script de atualização novamente
./ATUALIZAR_SERVIDOR_REACT.sh
```

**Agora vai funcionar!** ✅

---

## 📋 O QUE O SCRIPT FAZ

**SETUP_SERVIDOR_NODEJS.sh:**

1. ✅ Verifica se Node.js já está instalado
2. ✅ Adiciona repositório NodeSource
3. ✅ Instala Node.js 20 LTS
4. ✅ Instala npm automaticamente
5. ✅ Instala PM2 globalmente
6. ✅ Configura PM2 startup

**Resultado:**
- ✅ Node.js v20.x
- ✅ npm v10.x
- ✅ PM2 v5.x
- ✅ Pronto para React!

---

## 🎯 PASSO A PASSO COMPLETO

### **1. Conectar no servidor:**
```bash
ssh serverhome@servidor
```

### **2. Ir para pasta do projeto:**
```bash
cd /home/serverhome/auronex
# OU
cd /home/serverhome/robo
```

### **3. Instalar Node.js:**
```bash
chmod +x SETUP_SERVIDOR_NODEJS.sh
./SETUP_SERVIDOR_NODEJS.sh
```

**Aguarde aparecer:**
```
✅ NODE.JS CONFIGURADO COM SUCESSO!

Node.js: v20.x.x
npm: v10.x.x
PM2: v5.x.x
```

### **4. Executar PM2 startup (SE PEDIR):**

O script vai mostrar um comando, exemplo:
```bash
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u serverhome --hp /home/serverhome
```

**Copie e execute!**

### **5. Atualizar servidor:**
```bash
./ATUALIZAR_SERVIDOR_REACT.sh
```

**Agora vai funcionar!** ✅

**Aguarde ~3-5 minutos**

### **6. Verificar:**
```bash
pm2 status
```

**Deve mostrar:**
```
fastapi-app      │ online  │ 8001
auronex-dashboard│ online  │ 8501
```

### **7. Testar:**
```
https://app.auronex.com.br
```

**FUNCIONANDO!** 🎉

---

## 🐛 SE AINDA DER ERRO

### **Instalação manual do Node.js:**

```bash
# Adicionar repositório
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Instalar
sudo apt-get install -y nodejs

# Verificar
node --version
npm --version

# Instalar PM2
sudo npm install -g pm2

# Executar script novamente
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

## 📊 SOBRE MULTI-SERVIDOR

**Sua pergunta:** "Usar 2+ notebooks para mesmo bot?"

**Resposta curta:** SIM! ✅

**Guia completo já criado:**
```
ARQUITETURA_MULTI_SERVIDOR_ENTERPRISE.md
```

**Resumo:**
- **Agora:** 1 notebook (suficiente!)
- **Com 50+ clientes:** PostgreSQL cloud + 2º notebook
- **Com 500+ clientes:** Redis + Load Balancer + 3-5 notebooks
- **Custo:** R$ 0-200/mês
- **Capacidade:** Até 1000+ clientes

**Foco agora:** Instalar Node.js e fazer deploy! 🚀

---

## ✅ COMANDOS RESUMIDOS

```bash
# No servidor:

# 1. Instalar Node.js (PRIMEIRA VEZ)
./SETUP_SERVIDOR_NODEJS.sh

# 2. Atualizar sistema
./ATUALIZAR_SERVIDOR_REACT.sh

# 3. Verificar
pm2 status

# 4. Testar
curl http://localhost:8501
```

---

**EXECUTE `SETUP_SERVIDOR_NODEJS.sh` NO SERVIDOR AGORA!** 🎯

**Depois execute `ATUALIZAR_SERVIDOR_REACT.sh` novamente!** 🚀


