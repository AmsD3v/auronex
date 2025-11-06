# 🚀 DEPLOY EM PRODUÇÃO - https://auronex.com.br

**Sistema:** Dashboard React + Next.js  
**Ambiente:** Servidor (já rodando site principal)  
**Domínio:** https://auronex.com.br (Dashboard React em /)  
**Porta Antiga:** 8501 (Streamlit)  
**Porta Nova:** 3000 (React)  

---

## 📋 PRÉ-REQUISITOS NO SERVIDOR

### **1. Node.js instalado**

```bash
# Verificar
node --version  # Mínimo v18.17.0
npm --version

# Se não tiver, instalar:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### **2. PM2 instalado**

```bash
# Instalar PM2 globalmente
sudo npm install -g pm2

# Configurar PM2 para iniciar no boot
pm2 startup
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp $HOME
```

---

## 📦 PREPARAÇÃO DOS ARQUIVOS

### **1. Build Local (no seu PC)**

```bash
cd I:\Robo\auronex-dashboard
npm run build
```

**Resultado:** Pasta `.next` com build otimizado

---

### **2. Arquivos para enviar ao servidor**

**Lista completa:**
```
auronex-dashboard/
├── .next/              ← Build compilado
├── public/             ← Assets estáticos
├── node_modules/       ← Dependências (ou instalar no servidor)
├── app/                ← Código fonte
├── components/
├── hooks/
├── lib/
├── stores/
├── types/
├── package.json
├── package-lock.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── .env.production     ← Configuração de produção
└── ecosystem.config.js ← PM2 config
```

**Recomendação:** Enviar TUDO exceto `node_modules` (instalar no servidor)

---

## 🔧 CONFIGURAÇÃO DO CLOUDFLARE TUNNEL

### **Atual (Streamlit - porta 8501):**
```yaml
# tunnel.yml
ingress:
  - hostname: app.auronex.com.br
    service: http://localhost:8501
```

### **Novo (React - porta 3000):**
```yaml
# tunnel.yml - ATUALIZADO
ingress:
  - hostname: app.auronex.com.br
    service: http://localhost:3000  # ✅ Porta 3000 (React)
    
  # Opcional: Manter Streamlit em subdomínio
  - hostname: streamlit.auronex.com.br
    service: http://localhost:8501
```

---

## 🚀 DEPLOY PASSO A PASSO

### **PASSO 1: Enviar arquivos ao servidor**

```bash
# No seu PC (PowerShell/CMD):

# Criar zip dos arquivos
cd I:\Robo
tar -czf auronex-dashboard.tar.gz auronex-dashboard/

# Enviar via SCP
scp auronex-dashboard.tar.gz usuario@servidor:/home/usuario/

# OU usar WinSCP/FileZilla se preferir interface gráfica
```

---

### **PASSO 2: No servidor, descompactar**

```bash
# SSH no servidor
ssh usuario@servidor

# Ir para pasta do projeto
cd /home/usuario

# Descompactar
tar -xzf auronex-dashboard.tar.gz

# Entrar na pasta
cd auronex-dashboard
```

---

### **PASSO 3: Instalar dependências**

```bash
# Instalar dependências (produção)
npm ci --production

# Ou se precisar build no servidor:
npm install
npm run build
```

---

### **PASSO 4: Configurar variáveis de ambiente**

```bash
# Verificar .env.production
cat .env.production

# Deve mostrar:
# NEXT_PUBLIC_API_URL=https://auronex.com.br/api
```

---

### **PASSO 5: Iniciar com PM2**

```bash
# Parar Streamlit antigo (porta 8501)
pm2 stop streamlit  # Se estiver rodando com PM2
# OU
pkill -f streamlit

# Iniciar React (porta 3000)
pm2 start ecosystem.config.js

# Verificar status
pm2 status

# Ver logs
pm2 logs auronex-dashboard

# Salvar configuração PM2
pm2 save
```

---

### **PASSO 6: Atualizar Cloudflare Tunnel**

```bash
# Editar config do tunnel
sudo nano /etc/cloudflared/config.yml

# Alterar porta:
# service: http://localhost:8501  # ANTES (Streamlit)
# service: http://localhost:3000  # AGORA (React)

# Reiniciar tunnel
sudo systemctl restart cloudflared

# Verificar status
sudo systemctl status cloudflared
```

---

### **PASSO 7: Atualizar FastAPI CORS**

**Arquivo:** `fastapi_app/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://auronex.com.br",  # ✅ Adicionar
        "https://auronex.com.br",
        "https://www.auronex.com.br",
        "*"  # Permitir todos (ou remover em produção)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Reiniciar FastAPI no servidor:**
```bash
pm2 restart fastapi-app  # Se estiver com PM2
```

---

## 🔍 VERIFICAÇÃO

### **1. Testar localmente:**
```
https://auronex.com.br
```

Deve aparecer:
- ✅ Página de login
- ✅ Sem erros CORS
- ✅ Assets carregando

### **2. Testar API:**
```
https://auronex.com.br/api/health
```

Deve retornar:
```json
{"status": "healthy"}
```

### **3. Testar login:**
- ✅ Fazer login
- ✅ Dashboard carrega
- ✅ Saldo aparece
- ✅ Bots listados

---

## 🐛 TROUBLESHOOTING

### **Problema: CORS Error**

**Solução:** Adicionar domínio no CORS do FastAPI (linha 38)

### **Problema: API não conecta**

**Solução:** Verificar se FastAPI está rodando na porta 8001:
```bash
pm2 list
curl http://localhost:8001/health
```

### **Problema: Página não carrega**

**Solução:** Verificar Cloudflare Tunnel:
```bash
sudo systemctl status cloudflared
sudo journalctl -u cloudflared -f
```

### **Problema: Erros 502/504**

**Solução:** Verificar Next.js está rodando:
```bash
pm2 logs auronex-dashboard
pm2 restart auronex-dashboard
```

---

## 📊 ARQUITETURA FINAL

```
┌─────────────────────────────────────────────┐
│          CLIENTE (Navegador)                 │
│      https://auronex.com.br              │
└─────────────┬───────────────────────────────┘
              │ HTTPS (443)
              ▼
┌─────────────────────────────────────────────┐
│        Cloudflare Tunnel                     │
│     (túnel seguro para localhost)            │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│         SERVIDOR (Notebook)                  │
├─────────────────────────────────────────────┤
│                                             │
│  Next.js (PM2)                              │
│  ├─ Porta: 3000                             │
│  ├─ URL: http://localhost:3000              │
│  └─ Frontend React                          │
│                                             │
│  FastAPI (PM2)                              │
│  ├─ Porta: 8001                             │
│  ├─ URL: http://localhost:8001              │
│  └─ Backend API                             │
│                                             │
│  Bot Controller                             │
│  └─ Gerencia bots em background             │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎯 COMANDOS RÁPIDOS NO SERVIDOR

### **Ver status:**
```bash
pm2 status
```

### **Ver logs:**
```bash
pm2 logs auronex-dashboard
pm2 logs fastapi-app
```

### **Reiniciar:**
```bash
pm2 restart auronex-dashboard
pm2 restart fastapi-app
```

### **Parar tudo:**
```bash
pm2 stop all
```

### **Iniciar tudo:**
```bash
pm2 start all
```

---

## 📝 CHECKLIST DEPLOY

### **Antes de enviar:**
- [x] Build local OK (`npm run build`)
- [x] Sem erros TypeScript (`npm run type-check`)
- [x] .env.production configurado
- [x] ecosystem.config.js criado

### **No servidor:**
- [ ] Arquivos enviados
- [ ] Dependências instaladas (`npm ci`)
- [ ] PM2 start
- [ ] Cloudflare Tunnel atualizado (porta 3000)
- [ ] FastAPI CORS atualizado

### **Testes:**
- [ ] https://auronex.com.br carrega
- [ ] Login funciona
- [ ] Dashboard funciona
- [ ] Bots funcionam
- [ ] Tempo real funciona

---

## 🎊 URL FINAL

**Produção:**
```
https://auronex.com.br  ✅ PROFISSIONAL!
```

**NÃO usar:**
```
http://auronex.com.br/dashboard  ❌
https://auronex.com.br/dashboard  ❌ (redundante)
```

**URL limpa e profissional!** 🏆

---

**Arquivos de produção criados!**  
**Próximo:** Enviar ao servidor! 🚀


