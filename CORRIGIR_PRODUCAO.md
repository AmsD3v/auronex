# 🔧 CORRIGIR PRODUÇÃO

## 🎯 PROBLEMAS

1. **Usuário não identificado** - Mostra "Usuário" ao invés do nome
2. **Desconectado do FastAPI** - Mudanças não aparecem

---

## ✅ SOLUÇÃO

### **NO SERVIDOR (SSH):**

```bash
cd /home/serverhome/auronex/auronex-dashboard

# 1. Criar .env.production correto
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
EOF

# 2. Rebuild com env correto
npm run build

# 3. Reiniciar
pm2 restart auronex-dashboard

# 4. Ver logs
pm2 logs auronex-dashboard --lines 50
```

---

## 🔍 VERIFICAR

**No navegador (F12 → Console):**
```
Deve aparecer:
GET https://auronex.com.br/api/bots/ 200 OK
GET https://auronex.com.br/api/exchange/balance 200 OK

Se aparecer:
GET http://localhost:8001/... ❌ ERRO!
```

---

## ✅ TESTAR

Após aplicar:
- ✅ Mostra nome do usuário
- ✅ Conectado ao FastAPI
- ✅ Mudanças aparecem em tempo real

---

**EXECUTE OS COMANDOS ACIMA NO SERVIDOR!**

