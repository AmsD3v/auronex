# 📚 GUIA COMPLETO - ATUALIZAR SISTEMA

## 🎯 VISÃO GERAL

```
WINDOWS (Desenvolvimento)
    ↓ git push
GITHUB (Nuvem)
    ↓ git pull
XUBUNTU (Servidor)
    ↓ restart
CLIENTES (Veem mudanças!)
```

---

## 1️⃣ WINDOWS → GITHUB

### **Passo 1.1: Verificar mudanças**

```powershell
# Abrir PowerShell
# Ir para pasta do projeto
cd I:\Robo

# Ver o que mudou
git status
```

**Vai mostrar:**
```
modified:   dashboard_streamlit_fastapi.py
modified:   dashboard_styles.py
new file:   novo_arquivo.py
```

---

### **Passo 1.2: Adicionar arquivos**

```powershell
# Adicionar TODOS os arquivos modificados
git add .

# OU adicionar específicos
git add dashboard_streamlit_fastapi.py
git add dashboard_styles.py
```

---

### **Passo 1.3: Commit (salvar mudanças)**

```powershell
# Commit com mensagem descritiva
git commit -m "redesign: Layout minimalista completo"
```

**Mensagens recomendadas:**
```
feat: Nova funcionalidade
fix: Correção de bug
redesign: Mudança visual
refactor: Refatoração
docs: Documentação
```

---

### **Passo 1.4: Push (enviar para GitHub)**

```powershell
# Enviar para GitHub
git push origin main
```

**Deve mostrar:**
```
Enumerating objects...
Counting objects...
Writing objects: 100%...
To https://github.com/AmsD3v/auronex.git
   abc1234..def5678  main -> main
```

**✅ PRONTO! Código está no GitHub!**

---

## 2️⃣ GITHUB → XUBUNTU

### **Passo 2.1: PARAR SERVIÇOS PRIMEIRO!**

**⚠️ IMPORTANTE: Sempre pare antes de atualizar!**

**Terminal FastAPI (Xubuntu):**
```bash
Ctrl+C
```

**Terminal Streamlit (Xubuntu):**
```bash
Ctrl+C
```

**Aguarde ambos pararem completamente!**

---

### **Passo 2.2: Resolver conflitos (se tiver)**

```bash
# Ir para pasta
cd ~/auronex

# Se banco SQLite conflitar
git stash

# OU
git checkout db.sqlite3
```

---

### **Passo 2.3: Pull (baixar do GitHub)**

```bash
# Baixar atualizações
git pull origin main
```

**Deve mostrar:**
```
Updating 2f63e9f..ed345af
Fast-forward
 dashboard_streamlit_fastapi.py | 150 +++++++++++
 dashboard_styles.py            | 350 +++++++++++
 2 files changed, 500 insertions(+)
```

**✅ PRONTO! Código atualizado no servidor!**

---

### **Passo 2.4: Verificar arquivos**

```bash
# Ver último commit
git log -1

# Ver arquivos que mudaram
ls -la dashboard_streamlit_fastapi.py
```

---

## 3️⃣ REINICIAR SERVIÇOS

### **Passo 3.1: Terminal 1 - FastAPI**

```bash
# Ir para pasta
cd ~/auronex

# Ativar ambiente virtual
source venv/bin/activate

# Deve aparecer: (venv) no início da linha

# Iniciar FastAPI
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
```

**Aguarde aparecer:**
```
INFO: Uvicorn running on http://0.0.0.0:8001
[OK] Bot Controller agendado...
```

---

### **Passo 3.2: Terminal 2 - Streamlit**

**Abrir NOVO terminal (Ctrl+Alt+T):**

```bash
# Ir para pasta
cd ~/auronex

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar Streamlit
streamlit run dashboard_streamlit_fastapi.py
```

**Aguarde aparecer:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

### **Passo 3.3: Testar mudanças**

**No navegador:**

```
http://auronex.com.br/
http://auronex.com.br/app
```

**OU com IP:**

```
http://179.118.172.82/
http://179.118.172.82/app
```

**Deve ver novo layout!** ✅

---

## 🚨 TROUBLESHOOTING

### **Problema: "Porta já em uso"**

```bash
# Matar processo
sudo pkill -f uvicorn
sudo pkill -f streamlit

# Aguardar 5 segundos
sleep 5

# Iniciar novamente
```

---

### **Problema: "Mudanças não aparecem"**

```bash
# Hard refresh no navegador
Ctrl+Shift+R

# OU limpar cache Streamlit
rm -rf ~/.streamlit/cache/
```

---

### **Problema: "Conflito Git"**

```bash
# Guardar mudanças locais
git stash

# Pull
git pull origin main

# Restaurar (se necessário)
git stash pop
```

---

## ✅ CHECKLIST COMPLETO

### **Windows:**
- [ ] cd I:\Robo
- [ ] git status (ver mudanças)
- [ ] git add .
- [ ] git commit -m "mensagem"
- [ ] git push origin main
- [ ] Aguardar "100% done"

### **Xubuntu:**
- [ ] Ctrl+C (parar FastAPI)
- [ ] Ctrl+C (parar Streamlit)
- [ ] cd ~/auronex
- [ ] git stash (se conflito)
- [ ] git pull origin main
- [ ] Ver mensagem "Fast-forward"
- [ ] source venv/bin/activate (Terminal 1)
- [ ] python -m uvicorn... (Terminal 1)
- [ ] source venv/bin/activate (Terminal 2)
- [ ] streamlit run... (Terminal 2)
- [ ] Testar no navegador

### **Navegador:**
- [ ] Ctrl+Shift+R (hard reload)
- [ ] Ver novo layout
- [ ] Testar funcionalidades

---

## ⏰ TEMPO TOTAL

- Windows (commit/push): 1 minuto
- Xubuntu (pull): 30 segundos
- Xubuntu (restart): 1 minuto
- **TOTAL: 2-3 minutos!**

---

## 🎯 RESUMO ULTRA RÁPIDO

### **Windows:**
```powershell
cd I:\Robo
git add .
git commit -m "mudança X"
git push origin main
```

### **Xubuntu:**
```bash
# Parar serviços (Ctrl+C nos 2 terminais)
cd ~/auronex
git stash
git pull origin main
# Reiniciar serviços (comandos acima)
```

### **Navegador:**
```
Ctrl+Shift+R em http://auronex.com.br/app
```

**PRONTO!** ✅

---

**Desenvolvido por:** Claude Sonnet 4.5  
**Tokens:** 613k / 1M  
**21+ horas de trabalho!**

