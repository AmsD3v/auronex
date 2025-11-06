# 🚀 COMO USAR O DASHBOARD REACT

**Guia rápido para iniciar o dashboard**

---

## 📋 PRÉ-REQUISITOS

1. ✅ Node.js 18+ instalado
2. ✅ Backend FastAPI rodando (porta 8001)
3. ✅ NPM instalado

---

## 🚀 INICIAR DASHBOARD

### **Opção 1: Windows (Script Batch)**

```bash
# Na raiz do projeto (I:\Robo)
INICIAR_REACT_DASHBOARD.bat
```

### **Opção 2: Manual**

```bash
# Navegar para pasta
cd auronex-dashboard

# Instalar dependências (primeira vez)
npm install

# Rodar
npm run dev
```

### **Opção 3: PowerShell**

```powershell
cd I:\Robo\auronex-dashboard
npm run dev
```

---

## 🌐 ACESSAR

Abra o navegador em:
```
http://localhost:8501
```

---

## 🔐 FAZER LOGIN

**Credenciais:**
- Email: seu@email.com (mesmas do FastAPI)
- Senha: sua_senha

**Se não tem conta:**
1. Criar em: http://localhost:8001/register
2. Ou usar painel admin: http://localhost:8001/admin/

---

## ✅ VERIFICAR SE ESTÁ FUNCIONANDO

### **1. Backend rodando?**
```bash
# Abrir: http://localhost:8001/health

# Deve retornar:
{
  "status": "healthy",
  "service": "robotrader-api-fastapi"
}
```

### **2. Frontend rodando?**
```bash
# Terminal deve mostrar:
✓ Ready in 2.5s
○ Local:   http://localhost:8501
```

### **3. Login funciona?**
- Preencher email e senha
- Clicar "Entrar"
- Deve redirecionar para /dashboard

---

## 🔄 ATUALIZAÇÃO TEMPO REAL

O dashboard atualiza **AUTOMATICAMENTE**:

- ⚡ **Saldo**: a cada 1 segundo
- 🤖 **Bots**: a cada 5 segundos
- 📈 **Trades**: a cada 5 segundos
- 📊 **Stats**: a cada 10 segundos

**SEM RECARREGAR PÁGINA!** ✅

---

## 🐛 PROBLEMAS COMUNS

### **Erro: Cannot find module**
```bash
# Reinstalar dependências
cd auronex-dashboard
rm -rf node_modules package-lock.json
npm install
```

### **Erro: Port 3000 already in use**
```bash
# Usar porta diferente
npm run dev -- -p 3001
```

### **Erro: Failed to fetch**
- Verificar se FastAPI está rodando
- Verificar URL da API em `.env.local`

### **Login não funciona**
- Verificar credenciais
- Verificar se usuário existe no FastAPI
- Ver console do navegador (F12)

---

## 📊 COMPARAR COM STREAMLIT

Rodar ambos simultaneamente:

```bash
# Terminal 1: Backend
uvicorn fastapi_app.main:app --port 8001

# Terminal 2: Streamlit (ANTIGO)
streamlit run dashboard_streamlit_fastapi.py --server.port 8501

# Terminal 3: React (NOVO)
cd auronex-dashboard
npm run dev
```

**Acessar:**
- Streamlit: http://localhost:8501
- React: http://localhost:8501

**Comparar:**
- ✅ Performance
- ✅ Tempo real
- ✅ UX
- ✅ Animações

---

## 🎯 PRÓXIMOS PASSOS

Após confirmar que funciona:

1. ✅ Testar todas funcionalidades
2. ✅ Comparar com Streamlit
3. ✅ Decidir manter qual
4. ✅ Deploy (Vercel)

---

## 📞 SUPORTE

Se tiver problemas, me avise com:
1. Print do erro
2. Console do navegador (F12)
3. Terminal output

---

**Pronto para usar!** 🚀

