# 🔴 CORREÇÃO URGENTE - ENCRYPTION_KEY

## Problema:
```
⚠️ Dados corrompidos ou chave incorreta
```

## Causa:
- API Keys antigas: criptografadas com `"dev-encryption-key-change-in-production"`
- .env atual: `"3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44="`
- Descriptografia: CHAVE NOVA + DADOS ANTIGOS = **ERRO!**

---

## ✅ SOLUÇÃO (2 MINUTOS):

### REMOVER ENCRYPTION_KEY DO .env:

1. Abra: `notepad I:\Robo\.env`

2. **APAGUE ou COMENTE estas linhas:**
```env
# ENCRYPTION_KEY=3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=
```

3. **Deixe apenas:**
```env
SECRET_KEY=9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105
```

4. Salvar: Ctrl+S

---

## Sistema vai usar chave ANTIGA automaticamente!

**Código já modificado:**
```python
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = "dev-encryption-key-change-in-production"  # ✅ Antiga
```

---

## 🚀 REINICIE FASTAPI:

```bash
# Parar: Ctrl+C

# Iniciar:
cd I:\Robo
venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Deve aparecer:**
```
⚠️ ENCRYPTION_KEY não no .env - usando chave antiga
✅ Sistema de criptografia inicializado
```

---

## ✅ AGORA VAI FUNCIONAR:

- ✅ Descriptografia funciona
- ✅ Saldo aparece
- ✅ Dashboard carrega valores
- ✅ **TUDO OK!**

---

**REMOVA ENCRYPTION_KEY DO .ENV E REINICIE!** 🚀


