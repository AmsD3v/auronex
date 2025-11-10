# 🚀 COMO FAZER DEPLOY - GUIA RÁPIDO

**Repositório:** https://github.com/AmsD3v/auronex.git

---

## 📦 DEPLOY COMPLETO (3 PASSOS)

### **PASSO 1: Enviar para GitHub (no seu PC)**

```bash
DEPLOY_GITHUB_REACT.bat
```

**O que faz:**
1. ✅ Mostra arquivos modificados
2. ✅ `git add .`
3. ✅ `git commit` com mensagem automática
4. ✅ `git push origin main`
5. ✅ Envia para https://github.com/AmsD3v/auronex.git

**Tempo:** ~30 segundos

---

### **PASSO 2: Atualizar servidor (SSH)**

```bash
# SSH no servidor
ssh usuario@servidor

# Ir para pasta
cd /home/usuario/robo

# Executar script (faz tudo!)
./ATUALIZAR_SERVIDOR_REACT.sh
```

**O que faz:**
1. ✅ Para serviços antigos (Streamlit)
2. ✅ `git pull origin main`
3. ✅ `npm install`
4. ✅ `npm run build`
5. ✅ Inicia FastAPI (porta 8001)
6. ✅ Inicia React (porta 8501)
7. ✅ Verifica Cloudflare Tunnel

**Tempo:** ~3 minutos

---

### **PASSO 3: Testar**

```
https://app.auronex.com.br
```

**Deve aparecer:**
- ✅ Dashboard React
- ✅ Tela de login
- ✅ Funcionando!

---

## 🎯 FLUXO RESUMIDO

```
Seu PC:
  1. Fazer alterações no código
  2. DEPLOY_GITHUB_REACT.bat
  3. Código vai para GitHub ✅
  
GitHub:
  Repositório atualizado
  https://github.com/AmsD3v/auronex.git
  
Servidor:
  1. ./ATUALIZAR_SERVIDOR_REACT.sh
  2. Puxa código do GitHub
  3. Builda e reinicia
  4. app.auronex.com.br ONLINE! ✅
```

**Total:** ~4 minutos do código ao online! ⚡

---

## 📝 SCRIPTS CRIADOS

**No seu PC:**
- `DEPLOY_GITHUB_REACT.bat` ← Enviar para GitHub

**No servidor:**
- `ATUALIZAR_SERVIDOR_REACT.sh` ← Atualizar e reiniciar

---

## ✅ REPOSITÓRIO

**URL:** https://github.com/AmsD3v/auronex.git  
**Branch:** main  
**Versão:** v1.0+ (incrementa automaticamente)  

---

**EXECUTE `DEPLOY_GITHUB_REACT.bat` PARA ENVIAR!** 🚀


