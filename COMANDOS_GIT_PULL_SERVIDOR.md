# 🔧 Git Pull no Servidor - Resolver Conflitos

**Problema:** `db.sqlite3` foi modificado localmente (dados do servidor)  
**Solução:** Stash (guardar) antes do pull  

---

## ✅ COMANDOS (COPIE E COLE)

```bash
# 1. Guardar mudanças locais (db.sqlite3)
git stash

# 2. Pull do GitHub
git pull origin main

# 3. Restaurar db.sqlite3 local (dados do servidor)
git checkout stash -- db.sqlite3

# 4. Limpar stash
git stash drop
```

**Pronto!** ✅

---

## 📝 EXPLICAÇÃO

```
git stash
  → Guarda db.sqlite3 temporariamente
  
git pull
  → Baixa código novo (sem sobrescrever db)
  
git checkout stash -- db.sqlite3
  → Restaura db.sqlite3 do servidor (com seus dados!)
  
git stash drop
  → Limpa stash (não precisa mais)
```

---

## 🚀 DEPOIS DO PULL

```bash
cd auronex-dashboard
npm install
npm run build
pm2 restart all
```

---

**EXECUTE OS 4 COMANDOS ACIMA!** ✅


