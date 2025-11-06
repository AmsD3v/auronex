# 🚀 INSTRUÇÕES COMPLETAS DE DEPLOY

**Repositório:** https://github.com/AmsD3v/auronex.git  
**Sistema:** Dashboard React + FastAPI  

---

## ✅ O QUE FOI CORRIGIDO

### **1. Script DEPLOY_GITHUB_REACT.bat**

**Já envia TUDO:**
```batch
cd /d I:\Robo  ← Vai para raiz
git add .      ← Adiciona TUDO (incluindo auronex-dashboard/)
git push       ← Envia para GitHub
```

**Envia:**
- ✅ Pasta `auronex-dashboard/` (dashboard React)
- ✅ Pasta `fastapi_app/` (backend)
- ✅ Pasta `bot/` (bot trader)
- ✅ Scripts `.bat` e `.sh`
- ✅ Documentação
- ✅ **TUDO!**

---

### **2. Script ATUALIZAR_SERVIDOR_REACT.sh**

**Agora verifica se pasta existe:**
```bash
# Detecta pasta automaticamente
# Verifica se auronex-dashboard existe
# Se não existir, mostra erro claro
# Cria logs/
# Testa portas no fim
```

**Mais robusto!** ✅

---

## 🎯 DEPLOY COMPLETO - PASSO A PASSO

### **PASSO 1: No seu PC (Windows)**

```bash
# Executar script de deploy
DEPLOY_GITHUB_REACT.bat
```

**O que acontece:**
```
1. Mostra arquivos modificados (git status)
2. Aguarda 5 segundos (você vê o que vai enviar)
3. git add . (adiciona TUDO)
4. git commit -m "Dashboard React Enterprise - Update [data/hora]"
5. git push origin main
6. Envia para: https://github.com/AmsD3v/auronex.git ✅
```

**Aguarde ~30 segundos**

**Resultado:**
```
✅ DEPLOY CONCLUÍDO!

Código enviado para: https://github.com/AmsD3v/auronex
```

---

### **PASSO 2: No servidor (Linux - SSH)**

```bash
# Conectar via SSH
ssh serverhome@servidor

# Ir para pasta do projeto
cd /home/serverhome/robo

# OU se não existir ainda (primeira vez):
cd ~
git clone https://github.com/AmsD3v/auronex.git robo
cd robo
```

---

### **PASSO 3: Executar script de atualização**

```bash
# Dar permissão (primeira vez)
chmod +x ATUALIZAR_SERVIDOR_REACT.sh

# EXECUTAR!
./ATUALIZAR_SERVIDOR_REACT.sh
```

**O que acontece:**
```
[1/9] Parando serviços antigos (Streamlit)...
[2/9] Baixando código do GitHub...
[3/9] Verificando pasta auronex-dashboard...
[4/9] Instalando dependências Python...
[5/9] Instalando dependências React...
[6/9] Compilando React (build)...
[7/9] Iniciando FastAPI (porta 8001)...
[8/9] Iniciando React (porta 8501)...
[9/9] Verificando Cloudflare Tunnel...

✅ SERVIDOR ATUALIZADO!
```

**Tempo:** ~3-5 minutos

---

### **PASSO 4: Verificar status**

```bash
# Ver processos PM2
pm2 status

# Deve mostrar:
# fastapi-app      │ online  │ 8001
# auronex-dashboard│ online  │ 8501
```

---

### **PASSO 5: Testar**

**No navegador:**
```
https://app.auronex.com.br
```

**Deve aparecer:**
- ✅ Dashboard React
- ✅ Tela de login
- ✅ Funcionando!

---

## 🐛 TROUBLESHOOTING

### **Problema: "Pasta auronex-dashboard não encontrada"**

**Causa:** Git pull não trouxe a pasta (primeira vez)

**Solução:**
```bash
# Ver o que veio
ls -la

# Se não tem auronex-dashboard:
git pull origin main --rebase

# Ou clonar novamente
cd ~
rm -rf robo
git clone https://github.com/AmsD3v/auronex.git robo
cd robo
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

### **Problema: "pm2: command not found"**

**Solução:**
```bash
# Instalar PM2
sudo npm install -g pm2

# Configurar startup
pm2 startup
# Copiar e executar comando que aparecer

# Executar script novamente
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

### **Problema: "Permission denied"**

**Solução:**
```bash
chmod +x ATUALIZAR_SERVIDOR_REACT.sh
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

### **Problema: "Port 8501 already in use"**

**Solução:**
```bash
# Ver o que está usando
sudo lsof -i :8501

# Matar
sudo kill -9 [PID]

# Executar script novamente
./ATUALIZAR_SERVIDOR_REACT.sh
```

---

## 📊 ESTRUTURA NO GITHUB

```
https://github.com/AmsD3v/auronex.git
├── auronex-dashboard/          ← Dashboard React ✅
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── stores/
│   ├── types/
│   ├── package.json
│   ├── ecosystem.config.js     ← PM2 config
│   └── ...
├── fastapi_app/                ← Backend
├── bot/                        ← Bot trader
├── ATUALIZAR_SERVIDOR_REACT.sh ← Script do servidor ✅
├── DEPLOY_GITHUB_REACT.bat     ← Script de deploy ✅
└── ...
```

**Tudo vai para o GitHub!** ✅

---

## 🎯 CHECKLIST

### **No seu PC:**
- [ ] Testar local (http://localhost:8501)
- [ ] Tudo funcionando
- [ ] Executar `DEPLOY_GITHUB_REACT.bat`
- [ ] Aguardar push concluir

### **No servidor:**
- [ ] SSH conectado
- [ ] `cd /home/serverhome/robo`
- [ ] `git pull origin main` (ou executar script)
- [ ] `./ATUALIZAR_SERVIDOR_REACT.sh`
- [ ] Aguardar ~3-5 minutos
- [ ] Verificar PM2: `pm2 status`

### **Testes:**
- [ ] https://app.auronex.com.br carrega
- [ ] Login funciona
- [ ] Dashboard funciona
- [ ] Bots aparecem
- [ ] Modal Config funciona

---

## 🎊 RESUMO

**Deploy em 2 comandos:**

```bash
# No PC:
DEPLOY_GITHUB_REACT.bat

# No servidor:
./ATUALIZAR_SERVIDOR_REACT.sh
```

**Tempo total:** ~5-8 minutos  
**Resultado:** Sistema em produção! 🚀

---

**URL Repositório:** https://github.com/AmsD3v/auronex.git ✅

**Scripts prontos para usar!** ✅


