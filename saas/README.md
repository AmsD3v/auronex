# 🚀 RoboTrader SaaS - Backend Django

**Sistema de Trading Bot Multi-Usuário**

---

## 🎯 O QUE É ESTE PROJETO?

RoboTrader SaaS é uma plataforma web (SaaS) para trading automatizado de criptomoedas.

**Características:**
- 🤖 Bots de trading automatizados
- 👥 Multi-usuário (cada um com suas configs)
- 🔒 Seguro (API Keys criptografadas)
- 📊 Dashboard em tempo real
- 💰 Sistema de assinaturas (Free/Pro/Premium)

---

## 📁 ESTRUTURA DO PROJETO:

```
saas/
├── manage.py              ← CLI Django
├── settings.py            ← Configurações
├── urls.py                ← Rotas da API
├── wsgi.py                ← Deploy
├── celery.py              ← Bot engine
├── models_users.py        ← Modelos de dados
├── serializers.py         ← API serializers
├── views.py               ← Lógica de negócio
├── users/                 ← App usuários
├── bots/                  ← App bots
├── payments/              ← App pagamentos
└── templates/             ← HTML
```

---

## 🚀 INÍCIO RÁPIDO:

### 1. Instalar dependências:
```bash
cd I:\Robo
pip install -r requirements_saas.txt
```

### 2. Configurar banco de dados:
```bash
# Instalar PostgreSQL (ou usar SQLite para testes)
# Criar .env com credenciais
```

### 3. Rodar migrations:
```bash
cd saas
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Iniciar servidor:
```bash
# Terminal 1 - Django
python manage.py runserver

# Terminal 2 - Celery Worker
celery -A saas worker -l info

# Terminal 3 - Celery Beat
celery -A saas beat -l info
```

### 5. Acessar:
```
Frontend: http://localhost:8000
Admin: http://localhost:8000/admin
API Docs: http://localhost:8000/api/
```

---

## 📡 API ENDPOINTS:

### Autenticação:
```
POST /api/auth/register/       - Criar conta
POST /api/auth/login/          - Login
POST /api/auth/token/refresh/  - Refresh token
```

### Usuário:
```
GET  /api/profile/             - Ver perfil
```

### API Keys:
```
GET    /api/api-keys/          - Listar
POST   /api/api-keys/          - Adicionar
DELETE /api/api-keys/{id}/     - Remover
```

### Bots:
```
GET    /api/bots/              - Listar
POST   /api/bots/              - Criar
POST   /api/bots/{id}/start/   - Iniciar
POST   /api/bots/{id}/stop/    - Parar
```

### Trades:
```
GET /api/trades/               - Histórico
```

**Documentação completa:** `../API_DOCS.md`

---

## 🗄️ BANCO DE DADOS:

### Modelos principais:

```python
UserProfile           # Free/Pro/Premium
ExchangeAPIKey        # API Keys (criptografadas)
BotConfiguration      # Configs de bots
Trade                 # Histórico de trades
Subscription          # Assinaturas Stripe
Payment               # Pagamentos
```

---

## 🤖 CELERY - BOT ENGINE:

### Tarefas automáticas:

```python
run_trading_bot()     # Executa bot (5s)
check_active_bots()   # Verifica bots ativos
monitor_prices()      # Monitora preços
send_notifications()  # Envia alertas
```

### Configuração:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULE = {
    'run-bots': {'schedule': 5.0}
}
```

---

## 🔐 SEGURANÇA:

### API Keys:
```python
# Criptografadas com Fernet
# Nunca armazenadas em texto plano
# Nunca retornadas pela API (mascaradas)
```

### Autenticação:
```python
# JWT com expiração 24h
# Refresh tokens
# Permissões por usuário
```

---

## 🚀 DEPLOY:

### Heroku:
```bash
heroku create robotrader-saas
heroku addons:create heroku-postgresql
heroku addons:create heroku-redis
git push heroku main
```

### Railway:
```bash
# Conectar GitHub
# Deploy automático
```

**Guia completo:** `../INSTALACAO_SAAS.md`

---

## 📊 TECNOLOGIAS:

```
Backend:     Django 4.2
API:         Django REST Framework
Auth:        JWT (simplejwt)
Database:    PostgreSQL
Cache:       Redis
Queue:       Celery
Exchange:    CCXT
Payment:     Stripe (futuro)
Deploy:      Heroku/Railway
```

---

## 📚 DOCUMENTAÇÃO:

```
../SAAS_COMPLETO.md        - Visão geral
../INSTALACAO_SAAS.md      - Guia de instalação
../ARQUITETURA_SAAS.md     - Arquitetura técnica
../API_DOCS.md             - Documentação da API
../ROADMAP_SAAS.md         - Roadmap
```

---

## 🧪 TESTES:

```bash
# Rodar testes
python manage.py test

# Coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🐛 DEBUG:

### Admin Panel:
```
http://localhost:8000/admin
```

### Logs:
```bash
# Django
python manage.py runserver

# Celery
celery -A saas worker -l debug

# Heroku
heroku logs --tail
```

---

## 💰 PLANOS:

| Plano | Preço | Bots | Corretoras |
|-------|-------|------|------------|
| Free | $0 | 1 | 1 |
| Pro | $29/mês | 3 | Todas |
| Premium | $99/mês | ∞ | Todas |

---

## 🤝 CONTRIBUINDO:

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📝 LICENÇA:

Propriedade privada. Todos os direitos reservados.

---

## 👨‍💻 AUTOR:

RoboTrader Team

---

## 📞 SUPORTE:

- 📧 Email: support@robotrader.com
- 📱 Discord: discord.gg/robotrader
- 📖 Docs: docs.robotrader.com

---

**Sistema pronto para produção! 🚀**

**Última atualização:** 27/10/2025

