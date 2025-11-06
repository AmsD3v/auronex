# 🌐 CONFIGURAÇÃO DE URLs - DEFINITIVA!

**Conforme especificado:**

---

## 📊 MAPEAMENTO COMPLETO

| Componente | Local | Produção |
|------------|-------|----------|
| **Landing Page** | http://localhost:8001 | https://auronex.com.br |
| **Admin Panel** | http://localhost:8001/admin | https://admin.auronex.com.br |
| **API Backend** | http://localhost:8001 | https://auronex.com.br |
| **Dashboard /dashboard** | http://localhost:3000/dashboard | https://api.auronex.com.br |
| **Dashboard React** | http://localhost:3000 | https://app.auronex.com.br |

---

## 🔧 ARQUIVOS CONFIGURADOS

### **`.env.local` (Desenvolvimento):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
NODE_ENV=development
```

**Dashboard chama:** `http://localhost:8001/api/bots/` ✅

---

### **`.env.production` (Produção):**
```bash
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

**Dashboard chama:** `https://auronex.com.br/api/bots/` ✅

---

## 🌐 CLOUDFLARE TUNNEL - CONFIGURAÇÃO

```yaml
# /etc/cloudflared/config.yml

tunnel: seu-tunnel-id
credentials-file: /root/.cloudflared/credentials.json

ingress:
  # Landing Page + Backend FastAPI
  - hostname: auronex.com.br
    service: http://localhost:8001
    # Serve tanto landing quanto /api/*
  
  # Admin Panel
  - hostname: admin.auronex.com.br
    service: http://localhost:8001
    path: /admin
  
  # Dashboard /dashboard
  - hostname: api.auronex.com.br
    service: http://localhost:3000
    path: /dashboard
  
  # Dashboard React principal
  - hostname: app.auronex.com.br
    service: http://localhost:3000
  
  # Catch-all
  - service: http_status:404
```

---

## 🎯 FLUXO COMPLETO

```
┌─────────────────────────────────────────────┐
│           DESENVOLVIMENTO LOCAL              │
├─────────────────────────────────────────────┤
│                                             │
│  Backend FastAPI (porta 8001)               │
│  ├─ http://localhost:8001                   │
│  ├─ /api/bots/                              │
│  ├─ /api/exchange/balance                   │
│  ├─ /admin/                                 │
│  └─ / (landing page)                        │
│                                             │
│  Dashboard React (porta 3000)               │
│  ├─ http://localhost:3000                   │
│  ├─ /login                                  │
│  ├─ /dashboard                              │
│  └─ /                                       │
│                                             │
└─────────────────────────────────────────────┘

                    ↓ DEPLOY ↓

┌─────────────────────────────────────────────┐
│              PRODUÇÃO ONLINE                 │
├─────────────────────────────────────────────┤
│                                             │
│  https://auronex.com.br                     │
│  ├─ Landing + Backend FastAPI               │
│  ├─ /api/bots/                              │
│  └─ /api/exchange/balance                   │
│                                             │
│  https://admin.auronex.com.br               │
│  └─ Admin Panel                             │
│                                             │
│  https://api.auronex.com.br                 │
│  └─ Dashboard /dashboard                    │
│                                             │
│  https://app.auronex.com.br                 │
│  └─ Dashboard React                         │
│                                             │
└─────────────────────────────────────────────┘
```

---

**URLs CONFIGURADAS CORRETAMENTE!** ✅


