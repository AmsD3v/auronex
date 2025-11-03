# 🚀 COMO INICIAR O SISTEMA AURONEX

## ✅ **ARQUIVO ÚNICO - TUDO EM UMA JANELA!**

### **Para INICIAR:**

```
INICIAR_AURONEX_COMPLETO.bat
```

**O que faz:**
1. ✅ Ativa venv
2. ✅ Inicia FastAPI (porta 8001)
3. ✅ Inicia Streamlit (porta 8501)
4. ✅ Inicia Celery Worker (bot)
5. ✅ Inicia Celery Beat (scheduler)
6. ✅ Mostra status em tempo real

**Tudo em UMA ÚNICA JANELA!** ✅

---

### **Para PARAR:**

```
PARAR_AURONEX.bat
```

**Ou:** Feche a janela do INICIAR_AURONEX_COMPLETO.bat

---

## 🌐 **URLs DO SISTEMA**

```
Site Principal:    http://localhost:8001/
Admin:             http://localhost:8001/admin/
Dashboard Visual:  http://localhost:8501/
API Docs:          http://localhost:8001/docs
```

---

## 🔑 **LOGIN ADMIN**

```
Email: admin@robotrader.com
Senha: admin123
```

---

## ⚠️ **IMPORTANTE**

**Ao fechar CMD/PowerShell:**
- Todos os processos param automaticamente
- Use PARAR_AURONEX.bat para parar limpo

**Primeira vez:**
- Aguarde 30-40 segundos
- Serviços demoram para iniciar

---

## 🎯 **VERIFICAR SE ESTÁ RODANDO**

```
netstat -ano | findstr "8001 8501"
```

**Deve mostrar:**
- `:8001` → FastAPI
- `:8501` → Streamlit

---

## 🏆 **SISTEMA COMPLETO**

**Um único comando inicia:**
- ✅ Backend (FastAPI)
- ✅ Frontend (HTML)
- ✅ Dashboard Visual (Streamlit)
- ✅ Bot de Trading (Celery)
- ✅ Scheduler (Celery Beat)

**Tudo em uma janela!** 🚀

---

**Execute:** `INICIAR_AURONEX_COMPLETO.bat`




