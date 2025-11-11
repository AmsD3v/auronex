# 🚨 PROBLEMA LOGIN 401 - ANÁLISE

**Sintoma:** Login sempre retorna 401 Unauthorized

**Console mostra:**
```
401 Unauthorized @ /api/auth/login/
Token inválido - fazendo logout
```

---

## 🔍 CAUSAS POSSÍVEIS

1. **Senha no banco está errada**
   - Hash não corresponde à senha digitada
   - Hash corrompido

2. **Endpoint /auth/login/ com bug**
   - Verificação de senha falhando
   - Comparação bcrypt com erro

3. **Campo password_hash vs hashed_password**
   - Model tem nome diferente
   - Script salva no campo errado

---

## ✅ SOLUÇÃO

**Verificar nome correto do campo:**
```python
from fastapi_app.models import User
# Ver: password_hash OU hashed_password?
```

**Resetar com endpoint FastAPI:**
```
http://localhost:8001/admin/
Editar usuário
Trocar senha
```

**OU criar usuário novo:**
```
Email: teste@teste.com
Senha: 123456
```

---

**Tokens:** 431k/1M (56.9% disponível)

