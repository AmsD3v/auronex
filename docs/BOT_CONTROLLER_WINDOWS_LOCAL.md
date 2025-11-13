# 🖥️ BOT CONTROLLER - WINDOWS LOCAL

**Pergunta:** PM2 auto-start funciona no Windows local?

---

## ❌ NÃO! PM2 é para SERVIDOR LINUX

**PM2:**
- Funciona: Linux, Mac
- NÃO funciona bem: Windows

**Por quê:**
- PM2 usa processos daemon (Linux)
- Windows usa serviços diferentes

---

## ✅ SOLUÇÃO WINDOWS: TASK SCHEDULER

### **Criar Serviço Windows:**

**Método 1: Task Scheduler (Nativo)**
```
1. Win + R → taskschd.msc
2. Create Task
3. Name: Auronex Bot Controller
4. Trigger: At startup
5. Action: Start program
   - Program: I:\Robo\venv\Scripts\python.exe
   - Arguments: -m bot.bot_controller
   - Start in: I:\Robo
6. Settings:
   - Run whether user is logged in or not ✅
   - Run with highest privileges ✅
   - Restart if fails ✅
```

**Método 2: NSSM (Recomendado)**
```bash
# Baixar NSSM: https://nssm.cc/download
choco install nssm

# Instalar serviço:
nssm install AuronexBotController "I:\Robo\venv\Scripts\python.exe"
nssm set AuronexBotController AppParameters "-m bot.bot_controller"
nssm set AuronexBotController AppDirectory "I:\Robo"
nssm set AuronexBotController AppStdout "I:\Robo\logs\bot_controller.log"
nssm set AuronexBotController AppStderr "I:\Robo\logs\bot_controller_error.log"

# Iniciar:
nssm start AuronexBotController

# Status:
nssm status AuronexBotController
```

---

## 🎯 PARA SEU CASO

**Servidor (Linux):**
- ✅ PM2 auto-start JÁ implementado!
- Script: `ATUALIZAR_SERVER_PRODUCAO_09_11_25.sh`
- Commit: `46090ca`

**Local (Windows):**
- ❌ PM2 não é ideal
- ✅ Usar NSSM ou Task Scheduler
- OU simplesmente: deixar janela CMD aberta!

---

## 💡 RECOMENDAÇÃO

**Desenvolvimento Local:**
- Deixar janela CMD aberta
- Fácil de parar/reiniciar
- Ver logs em tempo real

**Produção (Servidor Linux):**
- PM2 auto-start ✅ (JÁ implementado!)
- Reinicia automático ✅
- Logs persistentes ✅

---

## 📊 RESUMO

| Ambiente | Solução | Status |
|----------|---------|--------|
| **Servidor Linux** | PM2 auto-start | ✅ Implementado! |
| **Windows Local** | CMD aberta OU NSSM | Manual OK |

---

**Servidor: PRONTO!** ✅  
**Local: Deixar CMD aberta OK!** ✅

