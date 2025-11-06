# 🌐 CONFIGURAÇÃO DE URLs - DEFINITIVA!

**Conforme especificado pelo cliente:**

---

## 📊 MAPEAMENTO CORRETO

| Componente | Desenvolvimento (Local) | Produção (Online) |
|------------|------------------------|-------------------|
| **Backend FastAPI** | http://localhost:8001 | https://auronex.com.br |
| **Dashboard /dashboard** | http://localhost:3000/dashboard | https://api.auronex.com.br |
| **Dashboard raiz** | http://localhost:3000 | https://app.auronex.com.br |

---

## 🔧 CONFIGURAÇÃO APLICADA

### **Arquivo: `.env.production`**
```bash
# Backend FastAPI em produção
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
```

### **Arquivo: `.env.local`**
```bash
# Backend FastAPI local
NEXT_PUBLIC_API_URL=http://localhost:8001
NODE_ENV=development
```

---

## 🌐 CLOUDFLARE TUNNEL - CONFIGURAÇÃO

```yaml
# /etc/cloudflared/config.yml

ingress:
  # Backend FastAPI + Landing
  - hostname: auronex.com.br
    service: http://localhost:8001
  
  # Dashboard /dashboard (???)
  - hostname: api.auronex.com.br
    service: http://localhost:3000
    path: /dashboard
  
  # Dashboard React principal
  - hostname: app.auronex.com.br
    service: http://localhost:3000
  
  - service: http_status:404
```

---

## ✅ URLS CONFIGURADAS

**Desenvolvimento:**
- Backend: http://localhost:8001
- Dashboard: http://localhost:3000

**Produção:**
- Backend: https://auronex.com.br
- Dashboard (/dashboard): https://api.auronex.com.br
- Dashboard (raiz): https://app.auronex.com.br

---

**CONFIGURADO CONFORME ESPECIFICADO!** ✅


