# 🔧 RESOLVER ERROS LOCAL

## 🚨 ERROS
```
⚠️ Erro ao buscar bots
⚠️ Erro ao buscar saldo
```

## 🔍 POSSÍVEIS CAUSAS

1. **Não autenticado**
   - Token não está sendo enviado
   - Token inválido/expirado
   
2. **Endpoints com erro 500**
   - /api/bots/ falhando
   - /api/exchange/balance falhando

3. **CORS bloqueando**
   - localhost:8501 → localhost:8001
   - Mas CORS está configurado

---

## ✅ SOLUÇÃO

### **1. Limpar localStorage no navegador**
```
F12 → Application → Storage → Clear
```

### **2. Fazer login novamente**
- Email: catheriine.fake@gmail.com
- Senha: (sua senha)

### **3. Ver console (F12)**
```
[Auth] Login OK! Token: eyJhbGc...
[Auth] User: catheriine...
```

Se aparecer = autenticou!

Se depois ver: "401 Unauthorized" = token não está indo

---

## 🎯 TESTE

1. Limpar localStorage
2. Recarregar página (F5)
3. Fazer login
4. Ver se bots carregam

---

**Se não funcionar:** Me mostre console (F12) e vejo o erro!

