# 🚀 EXECUTE ESTES COMANDOS NO SERVIDOR (LINHA POR LINHA)

**Problema:** Script está em cache  
**Solução:** Executar comandos diretos  

---

## 📝 COPIE E COLE LINHA POR LINHA

### **No servidor (SSH):**

```bash
# 1. Ir para pasta React
cd /home/serverhome/auronex/auronex-dashboard
```

```bash
# 2. Limpar node_modules e cache
rm -rf node_modules .next
```

```bash
# 3. Instalar TODAS dependências (NÃO usar --production!)
npm install
```

**Aguarde ~3-4 minutos** (vai instalar 454 packages!)

**Deve mostrar:**
```
added 454 packages  ← Deve ser ~450, NÃO 110!
```

---

```bash
# 4. Build
npm run build
```

**Aguarde ~2-3 minutos**

**Deve mostrar:**
```
✓ Compiled successfully
Route (app)              Size
○ /                      138 B
○ /dashboard             23 kB
○ /login                 3.44 kB
```

**SEM erros!** ✅

---

```bash
# 5. Parar React antigo
pm2 delete auronex-dashboard
```

```bash
# 6. Iniciar React novo
pm2 start ecosystem.config.js
```

```bash
# 7. Salvar config PM2
pm2 save
```

```bash
# 8. Ver status
pm2 status
```

**Deve mostrar:**
```
auronex-dashboard│ online  │ 8501
```

---

```bash
# 9. Testar porta
curl http://localhost:8501
```

**Deve retornar:** HTML do Next.js ✅

---

```bash
# 10. Ver logs (se necessário)
pm2 logs auronex-dashboard --lines 50
```

---

## ✅ QUANDO FUNCIONAR

**Acesse no navegador:**
```
https://app.auronex.com.br
```

**Deve aparecer:**
- ✅ Dashboard React
- ✅ **SEM popup de autorização!**
- ✅ Tela de login
- ✅ Funcionando!

---

## 🎯 POR QUE npm install (não npm ci --production)?

```bash
# npm ci --production
→ Instala apenas 111 packages (dependencies)
→ NÃO instala Tailwind, TypeScript, etc
→ Build FALHA! ❌

# npm install
→ Instala 454 packages (dependencies + devDependencies)
→ Instala Tailwind, TypeScript, PostCSS, etc
→ Build FUNCIONA! ✅
```

---

## 📊 VERIFICAR INSTALAÇÃO

**Após `npm install`, verifique:**

```bash
# Ver número de packages
ls node_modules | wc -l
# Deve ser ~450-500

# Verificar se Tailwind existe
ls node_modules/tailwindcss
# Deve mostrar: bin  lib  package.json  ...
```

---

**EXECUTE OS COMANDOS ACIMA LINHA POR LINHA!** ⚡

**Build vai funcionar!** ✅


