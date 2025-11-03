# 🏗️ ARQUITETURA ROBOTRADER SaaS

## **VISÃO GERAL**

```
┌─────────────┐
│   USUÁRIO   │
│  (Browser)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│    FRONTEND (React/Next.js)     │
│  - Landing Page                 │
│  - Dashboard                     │
│  - Configurações                │
└──────┬──────────────────────────┘
       │ HTTPS/REST API
       ▼
┌─────────────────────────────────┐
│      BACKEND (Django)           │
│  - Autenticação (JWT)           │
│  - API REST                      │
│  - Gerenciamento de Usuários    │
│  - Configurações de Bots        │
└──────┬──────────────────────────┘
       │
       ├─────────┬──────────┬──────────┐
       ▼         ▼          ▼          ▼
   ┌────────┐ ┌──────┐ ┌────────┐ ┌──────┐
   │Postgres│ │Redis │ │Celery  │ │CCXT  │
   │  DB    │ │Cache │ │Workers │ │  API │
   └────────┘ └──────┘ └────────┘ └──────┘
                          │
                          ▼
                    ┌──────────────┐
                    │   EXCHANGES  │
                    │ Binance/Bybit│
                    └──────────────┘
```

---

## **COMPONENTES PRINCIPAIS**

### **1. Frontend (Futuro - React/Next.js)**
```
src/
├── pages/
│   ├── index.tsx         (Landing)
│   ├── login.tsx         (Login)
│   ├── register.tsx      (Cadastro)
│   └── dashboard/
│       ├── index.tsx     (Overview)
│       ├── bots.tsx      (Gerenciar Bots)
│       ├── trades.tsx    (Histórico)
│       └── settings.tsx  (Configurações)
├── components/
│   ├── Layout.tsx
│   ├── BotCard.tsx
│   ├── TradeTable.tsx
│   └── Chart.tsx
└── api/
    └── client.ts         (Axios config)
```

**Tecnologias:**
- Next.js 14
- TypeScript
- TailwindCSS
- Chart.js / Recharts
- Axios

---

### **2. Backend (Django) - ATUAL**
```
saas/
├── settings.py           (Configurações)
├── urls.py              (Rotas)
├── wsgi.py              (Deploy)
├── celery.py            (Background tasks)
├── models_users.py      (Banco de dados)
├── serializers.py       (API serialization)
├── views.py             (Lógica de negócio)
└── apps/
    ├── users/           (Usuários)
    ├── bots/            (Bots e trades)
    └── payments/        (Stripe)
```

**Tecnologias:**
- Django 4.2
- Django REST Framework
- JWT Authentication
- Celery
- CCXT

---

### **3. Banco de Dados (PostgreSQL)**

**Schema:**

```sql
-- Usuários
users
├── id
├── email
├── password (hash)
├── created_at

user_profiles
├── id
├── user_id (FK)
├── plan (free/pro/premium)
├── stripe_customer_id

-- API Keys (criptografadas)
exchange_api_keys
├── id
├── user_id (FK)
├── exchange (binance/bybit)
├── api_key_encrypted
├── secret_key_encrypted
├── is_testnet
├── is_active

-- Configurações de Bot
bot_configurations
├── id
├── user_id (FK)
├── name
├── exchange
├── symbols (JSON)
├── capital
├── strategy
├── is_active

-- Trades
trades
├── id
├── user_id (FK)
├── bot_config_id (FK)
├── symbol
├── side (buy/sell)
├── entry_price
├── exit_price
├── profit_loss
├── entry_time
├── exit_time
├── status (open/closed)

-- Pagamentos
subscriptions
├── id
├── user_id (FK)
├── plan
├── status
├── stripe_subscription_id

payments
├── id
├── user_id (FK)
├── amount
├── stripe_payment_id
```

---

### **4. Celery (Bot Engine)**

**Workers:**

```python
# Worker 1: Trading Bot
@app.task
def run_trading_bot(bot_config_id):
    # 1. Buscar configuração
    # 2. Conectar exchange (CCXT)
    # 3. Analisar mercado
    # 4. Executar trades
    # 5. Salvar no banco
    pass

# Worker 2: Monitor de Preços
@app.task
def monitor_prices():
    # Atualizar preços em tempo real
    pass

# Worker 3: Notificações
@app.task
def send_notifications(user_id, message):
    # Email/SMS de trades
    pass
```

**Scheduling (Celery Beat):**
```python
CELERY_BEAT_SCHEDULE = {
    'run-active-bots': {
        'task': 'check_active_bots',
        'schedule': 5.0,  # A cada 5s
    },
    'update-rankings': {
        'task': 'update_crypto_rankings',
        'schedule': 300.0,  # A cada 5min
    },
}
```

---

## **FLUXO DE DADOS**

### **Fluxo de Registro:**
```
1. User acessa /register
2. Frontend → POST /api/auth/register
3. Django cria user + profile
4. Retorna JWT token
5. Frontend salva token
6. Redirect para /dashboard
```

### **Fluxo de Trading:**
```
1. User configura bot no dashboard
2. Frontend → POST /api/bots/
3. Django salva config no banco
4. User clica "Start Bot"
5. Frontend → POST /api/bots/{id}/start
6. Django ativa bot (is_active=True)
7. Celery Beat detecta bot ativo
8. Celery Worker executa run_trading_bot()
9. Bot analisa mercado via CCXT
10. Bot executa trade
11. Trade salvo no banco
12. Frontend busca trades via GET /api/trades/
13. Dashboard atualiza em tempo real
```

### **Fluxo de Pagamento:**
```
1. User escolhe plano Pro
2. Frontend → POST /api/payments/checkout
3. Django cria Stripe Checkout Session
4. User paga no Stripe
5. Stripe webhook → Django
6. Django atualiza subscription
7. User profile agora é "Pro"
```

---

## **SEGURANÇA**

### **API Keys (Criptografia):**
```python
from cryptography.fernet import Fernet

# Gerar chave
key = Fernet.generate_key()

# Criptografar
f = Fernet(key)
encrypted = f.encrypt(b"user_api_key")

# Descriptografar (só quando necessário)
decrypted = f.decrypt(encrypted)
```

**Chaves NUNCA são retornadas pela API!**

### **Autenticação:**
```python
# JWT Token
{
    "user_id": 123,
    "email": "user@example.com",
    "exp": 1234567890  # Expira em 24h
}
```

### **Permissões:**
```python
# User só acessa seus próprios dados
def get_queryset(self):
    return BotConfiguration.objects.filter(
        user=self.request.user
    )
```

---

## **ESCALABILIDADE**

### **Fase 1 (MVP - Atual):**
```
- 1-100 usuários
- Heroku Hobby ($21/mês)
- 1 Web dyno
- 1 Worker dyno
```

### **Fase 2 (Growth):**
```
- 100-1000 usuários
- Heroku Standard ($50-100/mês)
- 2 Web dynos (load balancer)
- 3 Worker dynos
- Redis caching
```

### **Fase 3 (Scale):**
```
- 1000+ usuários
- AWS/GCP ($200-500/mês)
- Auto-scaling
- CDN (CloudFlare)
- Multiple regions
```

---

## **MONITORAMENTO**

### **Logs:**
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Trade executado: {symbol} {side}")
logger.error(f"Erro na execução: {e}")
```

### **Métricas:**
```
- Trades/hora
- Latência média
- Taxa de erro
- Usuários ativos
- Revenue (MRR)
```

### **Alertas:**
```
- Bot parou (Slack/Email)
- Erro crítico (PagerDuty)
- Alto volume de erros (Sentry)
```

---

## **BACKUP & DISASTER RECOVERY**

### **Backup Automático:**
```bash
# PostgreSQL backup (diário)
pg_dump robotrader_saas > backup_$(date +%Y%m%d).sql

# Upload para S3
aws s3 cp backup_*.sql s3://robotrader-backups/
```

### **Recovery:**
```bash
# Restaurar backup
psql robotrader_saas < backup_20250127.sql
```

---

## **CUSTOS ESTIMADOS (PRODUÇÃO)**

```
Heroku (Starter):
├── PostgreSQL Hobby: $0
├── Redis Hobby: $0
├── Web dyno: $7/mês
├── Worker dyno: $7/mês
├── Beat dyno: $7/mês
└── Total: ~$21/mês

Stripe:
└── 2.9% + $0.30 por transação

SendGrid:
└── 100 emails/dia: $0
```

**Break-even:** ~10 clientes Pro ($29/mês)

---

## **ROADMAP TÉCNICO**

### **Q1 2025 (MVP):**
- ✅ Backend Django completo
- ⏳ Frontend básico (Streamlit)
- ⏳ Deploy Heroku
- ⏳ 2 Corretoras (Binance + Bybit)

### **Q2 2025 (Beta):**
- ⏳ Frontend React/Next.js
- ⏳ 5 Corretoras
- ⏳ Pagamentos Stripe
- ⏳ Email notifications

### **Q3 2025 (Launch):**
- ⏳ Marketing
- ⏳ 100 usuários
- ⏳ Mobile app (React Native)

### **Q4 2025 (Growth):**
- ⏳ 1000 usuários
- ⏳ Estratégias avançadas
- ⏳ API pública

---

**Arquitetura profissional, escalável e segura!** 🏆

