# 🚨 LEIA URGENTE - REACT NÃO ESTÁ RODANDO!

**Problema:** `ERR_CONNECTION_REFUSED` ao acessar `http://localhost:3000`  
**Causa:** React **não está rodando**!  

---

## ✅ SOLUÇÃO IMEDIATA (1 MINUTO)

### **PASSO 1: Abrir PowerShell ou CMD**

Pressione:
- **Windows + R**
- Digite: `powershell`
- Enter

---

### **PASSO 2: Executar comandos**

**Cole e execute LINHA POR LINHA:**

```powershell
# Ir para pasta
cd I:\Robo\auronex-dashboard

# Matar Node.js anterior
taskkill /F /IM node.exe

# Aguardar 2 segundos
timeout /t 2

# Iniciar React
npm run dev
```

---

### **PASSO 3: Aguardar compilar**

**Deve aparecer:**
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  
✓ Compiled in 5.2s
```

**Aguarde ~20-30 segundos!**

---

### **PASSO 4: Acessar navegador**

```
http://localhost:3000
```

**Deve funcionar!** ✅

---

## 🐛 SE DER ERRO

**Me mostre:**
1. O que aparece no terminal (todo o texto)
2. Print do erro

**Erros comuns:**

### **"npm: command not found"**

**Solução:** Instalar Node.js
```
https://nodejs.org/
```

Baixe e instale. Depois reinicie PowerShell.

---

### **"Cannot find module"**

**Solução:**
```bash
cd I:\Robo\auronex-dashboard
npm install
npm run dev
```

---

### **"Port 3000 already in use"**

**Solução:**
```bash
taskkill /F /IM node.exe
npm run dev
```

---

### **"EPERM: operation not permitted"**

**Solução:** Abrir PowerShell **como Administrador**
- Botão direito no PowerShell
- "Executar como administrador"
- Repetir comandos

---

## 📝 COMANDO ÚNICO (COPIE E COLE)

**Copie TUDO de uma vez:**

```powershell
cd I:\Robo\auronex-dashboard; taskkill /F /IM node.exe 2>$null; timeout /t 2; npm run dev
```

**Aguarde ~30 segundos e acesse:**
```
http://localhost:3000
```

---

## ✅ QUANDO FUNCIONAR

**Terminal mostra:**
```
✓ Compiled /
- Local: http://localhost:3000
```

**Navegador mostra:**
```
Tela de login Auronex ✅
```

---

## 🎯 CORREÇÕES APLICADAS (Enquanto isso)

Enquanto você inicia o React, já corrigi:

1. ✅ URL API: `https://auronex.com.br/api` (sem "app.")
2. ✅ Modal z-index 9999 (sempre visível)
3. ✅ Botões fixos no fim (sempre aparecem)
4. ✅ 14 corretoras adicionadas
5. ✅ Busca de cryptos completa
6. ✅ Sem duplicatas
7. ✅ Limites atualizados

**Tudo pronto!** Só falta React rodar!

---

**EXECUTE O COMANDO ACIMA E ME AVISE!** 🚀

**Cole:**
```
cd I:\Robo\auronex-dashboard; npm run dev
```


