# 🚀 COMANDOS FINAIS - SERVIDOR

**Arquivo useWebSocket.ts corrigido e enviado para GitHub!**

---

## ✅ EXECUTE NO SERVIDOR (COPIE E COLE)

```bash
# 1. Parar crash loop
pm2 stop all
pm2 delete all
```

```bash
# 2. Ir para pasta
cd /home/serverhome/auronex/auronex-dashboard
```

```bash
# 3. Puxar correção do GitHub
git pull origin main
```

```bash
# 4. Limpar tudo
rm -rf node_modules .next
```

```bash
# 5. Instalar TODAS dependências
npm install
```

**Aguarde ~3-4 min** → Deve mostrar: `added 454 packages`

---

```bash
# 6. BUILD (agora vai funcionar!)
npm run build
```

**Aguarde ~2-3 min**

**Deve compilar SEM erros!** ✅

---

```bash
# 7. Iniciar FastAPI
cd /home/serverhome/auronex
source venv/bin/activate
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app
```

```bash
# 8. Iniciar React
cd auronex-dashboard
pm2 start ecosystem.config.js
```

```bash
# 9. Salvar
pm2 save
```

```bash
# 10. Ver status
pm2 status
```

**Deve mostrar:**
```
fastapi-app      │ online  │ 8001  │ ↺ 0
auronex-dashboard│ online  │ 8501  │ ↺ 0
```

---

## 🌐 Testar

```
https://app.auronex.com.br/
```

**Deve funcionar!** ✅

---

**EXECUTE OS COMANDOS!** 🚀


