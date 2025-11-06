# 🔧 CORRIGIR: React Não Inicia (ERR_CONNECTION_REFUSED)

**Erro:** `ERR_CONNECTION_REFUSED` na porta 3000  
**Causa:** React não está rodando  

---

## 🎯 SOLUÇÃO PASSO A PASSO

### **PASSO 1: Verificar se React está rodando**

Abra **Gerenciador de Tarefas** (Ctrl+Shift+Esc):

1. Vá na aba **"Processos"**
2. Procure por **"Node.js"**
3. Se encontrar:
   - ✅ React está rodando
   - Aguarde 20-30 segundos
   - Tente acessar `http://localhost:3000`

4. Se **NÃO** encontrar:
   - ❌ React não está rodando
   - **Vá para PASSO 2**

---

### **PASSO 2: Iniciar React manualmente**

#### **Opção A: Via Script** ⭐ (Mais fácil)

```bash
REINICIAR_REACT_SIMPLES.bat
```

**Aguarde aparecer:**
```
✓ Compiled
- Local: http://localhost:3000
```

---

#### **Opção B: Manual**

```bash
# Abrir PowerShell ou CMD

# Ir para pasta
cd I:\Robo\auronex-dashboard

# Verificar se node_modules existe
dir node_modules

# Se NÃO existir, instalar:
npm install

# Iniciar
npm run dev
```

**Aguarde ~20-30 segundos** até aparecer:
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000
  
✓ Compiled in XXs
```

---

### **PASSO 3: Verificar erros no terminal**

Se aparecer **ERRO** no terminal, copie e me mostre!

**Erros comuns:**

#### **"Cannot find module"**
```bash
# Solução: Reinstalar dependências
cd I:\Robo\auronex-dashboard
rmdir /s /q node_modules
npm install
```

#### **"Port 3000 is already in use"**
```bash
# Solução: Matar processo
taskkill /F /IM node.exe

# Depois iniciar novamente
npm run dev
```

#### **"ENOENT: no such file"**
```bash
# Solução: Reconstruir
npm run build
npm run dev
```

---

### **PASSO 4: Verificar se porta está aberta**

```bash
# PowerShell
netstat -ano | findstr ":3000"
```

**Se aparecer resultado:**
```
TCP    0.0.0.0:3000    0.0.0.0:0    LISTENING    12345
```

- ✅ React está rodando (PID 12345)
- Acesse: `http://localhost:3000`

**Se NÃO aparecer:**
- ❌ React não está rodando
- Volte ao PASSO 2

---

## 🚀 SOLUÇÃO RÁPIDA - TUDO DE UMA VEZ

```bash
# 1. Matar todos Node.js
taskkill /F /IM node.exe

# 2. Ir para pasta
cd I:\Robo\auronex-dashboard

# 3. Limpar cache
rmdir /s /q .next

# 4. Instalar dependências (se necessário)
npm install

# 5. Iniciar
npm run dev

# 6. Aguardar ~30 segundos

# 7. Acessar
http://localhost:3000
```

---

## 🔍 CHECKLIST DE VERIFICAÇÃO

### **Antes de iniciar:**
- [ ] Node.js instalado? (`node --version`)
- [ ] npm instalado? (`npm --version`)
- [ ] Pasta existe? (`cd auronex-dashboard`)
- [ ] node_modules existe? (`dir node_modules`)

### **Durante inicialização:**
- [ ] Terminal mostra "Compiled"?
- [ ] Mostra "Local: http://localhost:3000"?
- [ ] Sem erros vermelhos?

### **Após iniciar:**
- [ ] Porta 3000 aberta? (`netstat -ano | findstr ":3000"`)
- [ ] Navegador carrega? (`http://localhost:3000`)
- [ ] Sem ERR_CONNECTION_REFUSED?

---

## 🐛 ERROS ESPECÍFICOS

### **"EPERM: operation not permitted"**

**Causa:** Permissões

**Solução:**
```bash
# Executar PowerShell como Administrador
# Depois rodar npm install
```

---

### **"Python não encontrado"**

**Causa:** Algumas dependências precisam de Python

**Solução:**
```bash
# Ignorar (não é crítico)
# OU instalar Python 3.10+
```

---

### **"Cannot find module '@/...'**"

**Causa:** Aliases TypeScript não configurados

**Solução:**
```bash
# Verificar tsconfig.json
cat tsconfig.json

# Deve ter:
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## 📝 SE NADA FUNCIONAR

**Criar projeto limpo:**

```bash
cd I:\Robo

# Renomear antigo
ren auronex-dashboard auronex-dashboard-backup

# Copiar arquivos essenciais
xcopy auronex-dashboard-backup\app auronex-dashboard\app /E /I
xcopy auronex-dashboard-backup\components auronex-dashboard\components /E /I
xcopy auronex-dashboard-backup\hooks auronex-dashboard\hooks /E /I
xcopy auronex-dashboard-backup\lib auronex-dashboard\lib /E /I
xcopy auronex-dashboard-backup\stores auronex-dashboard\stores /E /I
xcopy auronex-dashboard-backup\types auronex-dashboard\types /E /I

# Copiar configs
copy auronex-dashboard-backup\package.json auronex-dashboard\
copy auronex-dashboard-backup\tsconfig.json auronex-dashboard\
copy auronex-dashboard-backup\tailwind.config.ts auronex-dashboard\
copy auronex-dashboard-backup\next.config.js auronex-dashboard\

# Instalar e rodar
cd auronex-dashboard
npm install
npm run dev
```

---

## ✅ QUANDO FUNCIONAR

Você deve ver:

```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  
○ Compiling / ...
✓ Compiled / in 2.3s
```

**Acesse:**
```
http://localhost:3000
```

**Deve aparecer:**
- ✅ Página de login
- ✅ Sem erros

---

**ME MOSTRE O QUE APARECE NO TERMINAL QUANDO RODA `npm run dev`!**

**Tire um print ou copie o texto!**


