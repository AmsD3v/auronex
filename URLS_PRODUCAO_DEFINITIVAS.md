# 🌐 URLs DE PRODUÇÃO - DEFINITIVAS!

**Sistema:** Auronex Bot Trader  
**Arquitetura:** Multi-domínio  

---

## 📊 ESTRUTURA DE DOMÍNIOS

```
┌─────────────────────────────────────────────┐
│           AURONEX - PRODUÇÃO                 │
├─────────────────────────────────────────────┤
│                                             │
│  🌐 https://auronex.com.br                  │
│  └─ Landing Page                            │
│     ├─ Home                                 │
│     ├─ Preços (/pricing)                    │
│     ├─ Sobre (/about)                       │
│     └─ Contato (/contact)                   │
│                                             │
│  🔧 https://api.auronex.com.br              │
│  └─ FastAPI Backend                         │
│     ├─ /health                              │
│     ├─ /api/bots/                           │
│     ├─ /api/exchange/balance                │
│     ├─ /api/trades/                         │
│     └─ ... todas APIs REST                  │
│                                             │
│  📊 https://app.auronex.com.br              │
│  └─ Dashboard React (Clientes)              │
│     ├─ / (redireciona para /login)          │
│     ├─ /login                               │
│     ├─ /dashboard                           │
│     └─ /reset                               │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔧 DESENVOLVIMENTO LOCAL

```
┌─────────────────────────────────────────────┐
│           DESENVOLVIMENTO LOCAL              │
├─────────────────────────────────────────────┤
│                                             │
│  🌐 http://localhost                        │
│  └─ Landing Page (opcional)                 │
│                                             │
│  🔧 http://localhost:8001                   │
│  └─ FastAPI Backend                         │
│     ├─ /health                              │
│     ├─ /api/bots/                           │
│     └─ ... APIs                             │
│                                             │
│  📊 http://localhost:3000                   │
│  └─ Dashboard React                         │
│     ├─ /login                               │
│     ├─ /dashboard                           │
│     └─ ...                                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📁 CONFIGURAÇÃO POR AMBIENTE

### **Desenvolvimento (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
NODE_ENV=development
```

**Dashboard chama:** `http://localhost:8001/api/bots/` ✅

---

### **Produção (.env.production):**
```bash
NEXT_PUBLIC_API_URL=https://api.auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

**Dashboard chama:** `https://api.auronex.com.br/api/bots/` ✅

---

## 🚀 FLUXO DO CLIENTE - PRODUÇÃO

```
1. Cliente acessa: https://auronex.com.br
   → Vê landing page
   → Lê sobre o sistema
   → Clica "Começar Agora"

2. Redireciona para: https://app.auronex.com.br
   → Dashboard React
   → Tela de login

3. Cliente faz login
   → Token JWT
   → Redireciona para /dashboard

4. Dashboard carrega
   → Chama API: https://api.auronex.com.br/api/bots/
   → Chama API: https://api.auronex.com.br/api/exchange/balance
   → Mostra dados em tempo real

5. Cliente cria/edita bot
   → Modal abre NA FRENTE ✅
   → Escolhe corretora (14 opções)
   → Busca cryptos (400+)
   → Salva

6. Bot começa a operar
   → Backend processa
   → Dashboard atualiza em tempo real
   → Cliente vê trades acontecendo
```

---

## 🔒 SEGURANÇA - HTTPS

**Cloudflare Tunnel** garante:
- ✅ HTTPS automático (SSL/TLS)
- ✅ Proteção DDoS
- ✅ CDN global
- ✅ Zero config de certificados
- ✅ IP do servidor oculto

**Resultado:**
- Navegador mostra **🔒 Seguro**
- URLs profissionais
- Performance global

---

## 📝 RESUMO URLs

| Tipo | Local | Produção |
|------|-------|----------|
| Landing | http://localhost | https://auronex.com.br |
| API | http://localhost:8001 | https://api.auronex.com.br |
| Dashboard | http://localhost:3000 | https://app.auronex.com.br |

---

**CONFIGURAÇÃO PERFEITA!** ✅

**TESTE LOCAL AGORA (Ctrl+Shift+R no navegador)!** 🚀


