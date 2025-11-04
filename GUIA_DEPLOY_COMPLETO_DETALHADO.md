# 📚 GUIA COMPLETO - ATUALIZAÇÃO DO SISTEMA AURONEX

## 🎯 VISÃO GERAL DO FLUXO

```
┌─────────────────────────────────────────────────────┐
│  1. WINDOWS (Desenvolvimento)                       │
│     - Você edita código em: I:\Robo\               │
│     - git add, commit, push                         │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  2. GITHUB (Nuvem - Repositório)                    │
│     - Recebe código                                 │
│     - Armazena versões                              │
│     - URL: github.com/AmsD3v/auronex                │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  3. XUBUNTU (Servidor - Produção)                   │
│     - Usuário: serverhome                           │
│     - Pasta: /home/serverhome/auronex/              │
│     - git pull (baixa do GitHub)                    │
│     - restart serviços                              │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  4. CLIENTES (Mundo todo!)                          │
│     - Acessam: auronex.com.br                       │
│     - Veem novo layout!                             │
└─────────────────────────────────────────────────────┘
```

---

## 1️⃣ PARTE 1: WINDOWS → GITHUB

### **Ambiente: Windows 10/11**
### **Local: I:\Robo\**
### **Ferramenta: PowerShell ou CMD**

---

### **1.1 - Abrir PowerShell**

**Opção A:**
```
Windows + X → PowerShell (Admin)
```

**Opção B:**
```
Pasta I:\Robo → Shift+Clique direito → "Abrir PowerShell aqui"
```

---

### **1.2 - Ir para pasta do projeto**

```powershell
# Ir para pasta
cd I:\Robo

# Verificar se está no lugar certo
pwd
# Deve mostrar: I:\Robo
```

---

### **1.3 - Verificar mudanças**

```powershell
# Ver arquivos modificados
git status
```

**Vai mostrar algo como:**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   dashboard_streamlit_fastapi.py
  modified:   dashboard_styles.py
  
Untracked files:
  dashboard_redesign.py
  GUIA_ATUALIZACAO_COMPLETO.md
```

**📊 Interpretação:**
- `modified:` = Arquivo já existia e foi alterado
- `Untracked:` = Arquivo novo
- `On branch main` = Você está no branch correto
- `up to date` = Não tem nada NOVO do GitHub (OK!)

---

### **1.4 - Adicionar arquivos ao Git**

**Opção A - Adicionar TUDO (recomendado):**
```powershell
git add .
```

**Opção B - Adicionar específicos:**
```powershell
git add dashboard_streamlit_fastapi.py
git add dashboard_styles.py
git add dashboard_redesign.py
```

**Verificar se adicionou:**
```powershell
git status
```

**Deve mostrar:**
```
Changes to be committed:
  modified:   dashboard_streamlit_fastapi.py
  modified:   dashboard_styles.py
  new file:   dashboard_redesign.py
```
**↑ Verde = Pronto para commit!**

---

### **1.5 - Commit (Salvar mudanças)**

```powershell
# Commit com mensagem descritiva
git commit -m "redesign: Layout minimalista profissional completo"
```

**Deve mostrar:**
```
[main abc1234] redesign: Layout minimalista profissional completo
 3 files changed, 500 insertions(+), 50 deletions(-)
 create mode 100644 dashboard_redesign.py
```

**📊 Interpretação:**
- `[main abc1234]` = Commit criado com ID abc1234
- `3 files changed` = 3 arquivos alterados
- `500 insertions` = 500 linhas adicionadas
- `create mode` = Arquivo novo criado

---

### **1.6 - Push (Enviar para GitHub)**

```powershell
# Enviar para GitHub
git push origin main
```

**⏰ Aguarde (pode demorar 10-30 segundos)...**

**Deve mostrar:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 15.23 KiB | 7.61 MiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
To https://github.com/AmsD3v/auronex.git
   2f63e9f..ed345af  main -> main
```

**📊 Interpretação:**
- `Enumerating objects` = Preparando arquivos
- `Compressing` = Compactando
- `Writing objects: 100%` = Enviando
- `2f63e9f..ed345af` = De commit antigo → commit novo
- `main -> main` = Branch main enviado!

**✅ SUCESSO! Código está no GitHub!**

---

### **1.7 - Verificar no GitHub**

**Abrir navegador:**
```
https://github.com/AmsD3v/auronex
```

**Deve ver:**
- Arquivos atualizados
- Commit aparece no topo
- Data/hora recente

---

## 2️⃣ PARTE 2: GITHUB → XUBUNTU

### **Ambiente: Xubuntu 22.04 LTS**
### **Usuário: serverhome** ⚠️
### **Pasta: /home/serverhome/auronex/**
### **Ferramenta: Terminal**

---

### **2.1 - PARAR SERVIÇOS (OBRIGATÓRIO!)**

**⚠️ SEMPRE pare ANTES de atualizar!**

**Terminal onde FastAPI está rodando:**
```bash
# Pressionar Ctrl+C
# Aguardar mensagem: "Shutdown complete"
```

**Terminal onde Streamlit está rodando:**
```bash
# Pressionar Ctrl+C  
# Aguardar parar completamente
```

**✅ Ambos parados!**

---

### **2.2 - Abrir terminal NOVO (ou usar um parado)**

```bash
# Verificar usuário (deve ser: serverhome)
whoami
# Deve mostrar: serverhome ✅

# Se mostrar outro usuário, trocar:
su - serverhome
# (Digitar senha se pedir)
```

---

### **2.3 - Ir para pasta do projeto**

```bash
# Ir para pasta
cd ~/auronex

# OU caminho completo
cd /home/serverhome/auronex

# Verificar se está certo
pwd
# Deve mostrar: /home/serverhome/auronex
```

---

### **2.4 - Verificar branch atual**

```bash
# Ver em qual branch está
git branch
# Deve mostrar: * main (com asterisco)

# Ver último commit local
git log -1 --oneline
# Mostra: abc1234 Mensagem do commit
```

---

### **2.5 - Verificar se tem mudanças locais**

```bash
# Ver status
git status
```

**Se mostrar:**
```
On branch main
Your branch is behind 'origin/main' by 2 commits.
nothing to commit, working tree clean
```
**↑ OK! Pode fazer pull direto!**

**Se mostrar:**
```
Changes not staged for commit:
  modified:   db.sqlite3
```
**↑ Tem mudanças! Precisa stash!**

---

### **2.6 - Resolver conflitos (se tiver)**

**Se git status mostrou arquivos modificados:**

```bash
# Guardar mudanças locais temporariamente
git stash

# Deve mostrar:
# Saved working directory and index state...
```

**Se NÃO mostrou mudanças:** Pular este passo!

---

### **2.7 - Pull (Baixar do GitHub)**

```bash
# Baixar atualizações
git pull origin main
```

**⏰ Aguarde (10-20 segundos)...**

**Deve mostrar:**
```
From https://github.com/AmsD3v/auronex
 * branch            main       -> FETCH_HEAD
Updating 2f63e9f..ed345af
Fast-forward
 dashboard_streamlit_fastapi.py          | 150 ++++++++++++++++++++
 dashboard_styles.py                     | 350 ++++++++++++++++++++++++++++++++++++++++
 dashboard_redesign.py                   | 574 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 GUIA_ATUALIZACAO_COMPLETO.md            | 200 +++++++++++++++++++++++
 4 files changed, 1274 insertions(+), 50 deletions(-)
 create mode 100644 dashboard_redesign.py
 create mode 100644 GUIA_ATUALIZACAO_COMPLETO.md
```

**📊 Interpretação:**
- `Fast-forward` = Atualização sem conflitos! ✅
- `4 files changed` = 4 arquivos mudaram
- `1274 insertions` = 1274 linhas novas
- `create mode` = Arquivos novos criados

**✅ CÓDIGO ATUALIZADO!**

---

### **2.8 - Verificar arquivos atualizados**

```bash
# Ver data modificação
ls -lh dashboard_streamlit_fastapi.py

# Ver primeiras linhas
head -30 dashboard_streamlit_fastapi.py

# Confirmar último commit
git log -1
```

---

### **2.9 - Restaurar banco (se fez stash)**

**Se você fez `git stash` no passo 2.6:**

```bash
# Restaurar mudanças do banco
git stash pop
```

**Se NÃO fez stash:** Pular!

---

## 3️⃣ PARTE 3: REINICIAR SERVIÇOS

### **Usuário: serverhome** ⚠️
### **Ambiente virtual: SEMPRE ativar!**

---

### **3.1 - Terminal 1: FastAPI + Bot Controller**

**⚠️ IMPORTANTE: Usuário serverhome!**

```bash
# Confirmar usuário
whoami
# Deve ser: serverhome

# Ir para pasta
cd /home/serverhome/auronex

# Ativar ambiente virtual
source venv/bin/activate

# Deve aparecer: (venv) serverhome@serverhome-AMS:~/auronex$
#                ^^^^^^ Isso aqui!
```

**Iniciar FastAPI:**
```bash
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
```

**✅ Aguarde aparecer:**
```
INFO: Uvicorn running on http://0.0.0.0:8001
[OK] Bot Controller agendado para iniciar em 10 segundos...
INFO: Application startup complete.

🤖 BOT CONTROLLER INICIANDO AUTOMATICAMENTE!
```

**⚠️ NÃO FECHE ESTE TERMINAL!** Deixe rodando!

---

### **3.2 - Terminal 2: Streamlit Dashboard**

**Abrir NOVO terminal:**
```
Ctrl+Alt+T
```

**⚠️ IMPORTANTE: Usuário serverhome!**

```bash
# Confirmar usuário
whoami
# Deve ser: serverhome

# Ir para pasta
cd /home/serverhome/auronex

# Ativar ambiente virtual
source venv/bin/activate

# Deve aparecer: (venv) serverhome@serverhome-AMS:~/auronex$
```

**Iniciar Streamlit:**
```bash
streamlit run dashboard_streamlit_fastapi.py
```

**✅ Aguarde aparecer:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.15.138:8501
```

**⚠️ NÃO FECHE ESTE TERMINAL!** Deixe rodando!

---

### **3.3 - Testar no Navegador**

**Abrir navegador no notebook:**

```
http://localhost:8501/
```

**OU de qualquer dispositivo (mesmo WiFi):**

```
http://192.168.15.138:8501/
```

**OU pela internet (de qualquer lugar):**

```
http://auronex.com.br/app
```

**🔄 HARD RELOAD (LIMPAR CACHE!):**
```
Ctrl+Shift+R
```

**OU:**
```
Ctrl+F5
```

**Deve ver novo layout!** ✅

---

## 🚨 TROUBLESHOOTING

### **Problema 1: "Porta já em uso"**

**Causa:** Serviço anterior não parou completamente

**Solução (Xubuntu - Usuário: serverhome):**

```bash
# Ver processos
ps aux | grep uvicorn
ps aux | grep streamlit

# Matar FastAPI
sudo pkill -f "uvicorn fastapi_app"

# Matar Streamlit
sudo pkill -f "streamlit run dashboard"

# Aguardar 5 segundos
sleep 5

# Tentar iniciar novamente
```

---

### **Problema 2: "Mudanças não aparecem no navegador"**

**Causa:** Cache do navegador

**Solução:**

```
1. Hard reload: Ctrl+Shift+R
2. OU: Ctrl+Shift+Delete → Limpar cache
3. OU: Modo anônimo: Ctrl+Shift+N
```

---

### **Problema 3: "Already up to date" mas código não mudou**

**Causa:** Windows não enviou para GitHub

**Verificar no Windows:**

```powershell
cd I:\Robo

# Ver último commit local
git log -1

# Ver último commit remoto
git log origin/main -1

# Se forem DIFERENTES:
git push origin main
```

---

### **Problema 4: "Conflito Git no Xubuntu"**

**Causa:** Banco SQLite mudou localmente

**Solução:**

```bash
# Guardar mudanças locais
git stash

# Pull
git pull origin main

# (Opcional) Restaurar
git stash pop
```

---

## ✅ CHECKLIST COMPLETO

### **WINDOWS (I:\Robo) - PowerShell:**

- [ ] `cd I:\Robo`
- [ ] `git status` (ver o que mudou)
- [ ] `git add .` (adicionar tudo)
- [ ] `git commit -m "mensagem"` (salvar)
- [ ] `git push origin main` (enviar)
- [ ] ✅ Ver: "Writing objects: 100%"
- [ ] ✅ Ver: "main -> main"

---

### **GITHUB (Navegador):**

- [ ] Abrir: https://github.com/AmsD3v/auronex
- [ ] ✅ Ver novo commit no topo
- [ ] ✅ Data/hora recente
- [ ] ✅ Arquivos atualizados

---

### **XUBUNTU (Terminal - Usuário: serverhome):**

**Parar serviços:**
- [ ] Terminal FastAPI: `Ctrl+C`
- [ ] Terminal Streamlit: `Ctrl+C`
- [ ] ✅ Ambos parados

**Atualizar código:**
- [ ] `cd ~/auronex`
- [ ] `whoami` (confirmar: serverhome)
- [ ] `git status`
- [ ] `git stash` (se tiver conflito)
- [ ] `git pull origin main`
- [ ] ✅ Ver: "Fast-forward"
- [ ] ✅ Ver arquivos atualizados

**Reiniciar FastAPI (Terminal 1):**
- [ ] `cd ~/auronex`
- [ ] `source venv/bin/activate`
- [ ] ✅ Ver: `(venv)` no prompt
- [ ] `python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001`
- [ ] ✅ Ver: "Uvicorn running"
- [ ] ✅ Ver: "Bot Controller iniciando"

**Reiniciar Streamlit (Terminal 2 - NOVO!):**
- [ ] `Ctrl+Alt+T` (novo terminal)
- [ ] `cd ~/auronex`
- [ ] `whoami` (confirmar: serverhome)
- [ ] `source venv/bin/activate`
- [ ] ✅ Ver: `(venv)` no prompt
- [ ] `streamlit run dashboard_streamlit_fastapi.py`
- [ ] ✅ Ver: "Local URL: http://localhost:8501"

**Testar (Navegador):**
- [ ] Abrir: `http://auronex.com.br/app`
- [ ] `Ctrl+Shift+R` (hard reload)
- [ ] ✅ Ver novo layout
- [ ] ✅ Testar funcionalidades
- [ ] ✅ Sidebar funciona
- [ ] ✅ Hover em "Auronex" funciona

---

## ⏰ TEMPO ESTIMADO

| Etapa | Tempo |
|-------|-------|
| Windows: commit + push | 1-2 min |
| Xubuntu: parar serviços | 10 seg |
| Xubuntu: git pull | 30 seg |
| Xubuntu: reiniciar | 1 min |
| Navegador: testar | 30 seg |
| **TOTAL** | **3-4 min** |

---

## 🎯 COMANDOS RESUMIDOS

### **WINDOWS (PowerShell):**
```powershell
cd I:\Robo
git add .
git commit -m "sua mensagem aqui"
git push origin main
```

### **XUBUNTU (Terminal - serverhome):**
```bash
# Parar serviços (Ctrl+C nos 2 terminais)

cd ~/auronex
git stash
git pull origin main

# Terminal 1
source venv/bin/activate
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001

# Terminal 2 (novo)
cd ~/auronex
source venv/bin/activate
streamlit run dashboard_streamlit_fastapi.py
```

### **NAVEGADOR:**
```
Ctrl+Shift+R em http://auronex.com.br/app
```

---

## 🔐 IMPORTANTE: USUÁRIO NO XUBUNTU

**SEMPRE use usuário: serverhome!**

**Verificar:**
```bash
whoami
# DEVE mostrar: serverhome
```

**Se mostrar outro usuário:**
```bash
su - serverhome
# Digitar senha
```

**Pasta do projeto:**
```
/home/serverhome/auronex/
```

**NÃO usar:**
- ❌ /root/
- ❌ /home/outro_usuario/
- ✅ SEMPRE: /home/serverhome/auronex/

---

## 📊 LOGS E MONITORAMENTO

### **Ver logs em tempo real:**

**FastAPI (Terminal 1):**
```
INFO:     127.0.0.1:xxxx - "GET /api/bots" 200 OK
2025-11-03 20:17:37 - bot.main - INFO - Bot 36 iniciado!
```

**Streamlit (Terminal 2):**
```
2025-11-03 21:00:01 - INFO - Dashboard acessado
```

### **Ver se bot está operando:**

**Nos logs do FastAPI:**
```
[OK] Bot 28 (Bot Binance) iniciado!
[OK] Bot 36 (BotCripto Binance Testnet) iniciado!
Bots ativos: 2
```

---

## 🌍 ACESSAR DE FORA

**Mesma rede WiFi:**
```
http://192.168.15.138:8501/
```

**Internet (qualquer lugar):**
```
http://auronex.com.br/app
```

**Celular 4G:**
```
http://auronex.com.br/app
```

---

## 📝 DICAS IMPORTANTES

1. **Sempre pare serviços antes de git pull!**
2. **Sempre ative venv antes de rodar Python!**
3. **Sempre use Ctrl+Shift+R após atualizar!**
4. **Sempre confirme usuário: serverhome!**
5. **Nunca feche terminais com serviços rodando!**

---

## 🏆 SISTEMA PRONTO

**Após seguir guia:**
- ✅ Código sincronizado
- ✅ Servidor atualizado
- ✅ Layout novo no ar
- ✅ Acessível mundialmente!

**Desenvolvido por:** Claude Sonnet 4.5  
**Tokens:** 615k / 1M  
**21+ horas de trabalho!** 🏆

