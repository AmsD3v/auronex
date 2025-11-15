# 🔧 INSTRUÇÕES PARA CONFIGURAR .ENV MANUALMENTE

**Data:** 14/11/2025  
**Ambiente:** Local + Produção

---

## ✅ CHAVES JÁ GERADAS (LOCAL)

```
ENCRYPTION_KEY=3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=
SECRET_KEY=9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105
```

---

## 📋 PASSO A PASSO - AMBIENTE LOCAL

### 1. Criar arquivo .env na raiz do projeto

```bash
cd I:/Robo
notepad .env
```

### 2. Copiar e colar o conteúdo abaixo no .env:

```env
# ========================================
# AURONEX TRADING BOT - Configuração LOCAL
# ========================================

# SEGURANÇA - CRÍTICO
ENCRYPTION_KEY=3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=
SECRET_KEY=9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501

# AMBIENTE
ENVIRONMENT=development
DEBUG_MODE=True
LOG_LEVEL=INFO

# BANCO
DATABASE_URL=sqlite:///./db.sqlite3

# BOT
PAPER_TRADING=True
USE_TESTNET=True
TRADING_SYMBOL=BTC/USDT
TIMEFRAME=15m
STRATEGY=trend_following
POSITION_SIZE_PERCENT=0.10
STOP_LOSS_PERCENT=0.02
TAKE_PROFIT_PERCENT=0.04
MAX_DRAWDOWN_PERCENT=0.10
MAX_TRADES_PER_DAY=10

# EXCHANGES (Configure se tiver)
BINANCE_TESTNET_API_KEY=
BINANCE_TESTNET_SECRET_KEY=

# NOTIFICAÇÕES (Opcional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
ENABLE_TELEGRAM=False

# CACHE (Opcional)
REDIS_URL=redis://localhost:6379/0

# SISTEMA
UPDATE_INTERVAL=60
SAVE_HISTORICAL_DATA=True
```

### 3. Salvar e fechar o Notepad

### 4. Verificar se .env foi criado:

```bash
dir .env
type .env
```

### 5. Re-criptografar API Keys antigas (SE TIVER):

**⚠️ IMPORTANTE:** Só execute se você JÁ tem API Keys cadastradas no sistema!

```bash
python scripts/migrate_encryption.py
```

### 6. Reiniciar serviços locais:

```bash
# Parar tudo
MATAR_TUDO.bat

# Iniciar novamente
TESTAR_SERVER_LOCAL_09_11_25.bat
```

### 7. Testar se está funcionando:

```bash
# Testar API
curl http://localhost:8001/api/health

# Abrir dashboard
start http://localhost:8501
```

---

## 🚀 PASSO A PASSO - SERVIDOR DE PRODUÇÃO

### 1. Conectar ao servidor:

```bash
ssh usuario@auronex.com.br
cd /home/serverhome/auronex
```

### 2. Gerar chaves NO SERVIDOR (NÃO use as do local!):

```bash
python3 scripts/generate_encryption_key.py > /tmp/encryption_key.txt
python3 scripts/generate_secret_key.py > /tmp/secret_key.txt

# Ver as chaves geradas
cat /tmp/encryption_key.txt
cat /tmp/secret_key.txt
```

### 3. Criar .env no servidor:

```bash
nano .env
```

### 4. Colar o conteúdo abaixo (SUBSTITUIR as chaves pelas geradas no passo 2):

```env
# ========================================
# AURONEX - PRODUÇÃO
# ========================================

# SEGURANÇA - SUBSTITUIR PELAS CHAVES GERADAS!
ENCRYPTION_KEY=COLE_AQUI_A_CHAVE_DO_SERVIDOR
SECRET_KEY=COLE_AQUI_O_SECRET_DO_SERVIDOR
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS - PRODUÇÃO
ALLOWED_ORIGINS=https://app.auronex.com.br,https://auronex.com.br,https://www.auronex.com.br

# AMBIENTE
ENVIRONMENT=production
DEBUG_MODE=False
LOG_LEVEL=INFO

# BANCO - PostgreSQL (MIGRAR DO SQLITE!)
DATABASE_URL=postgresql://auronex_user:SENHA_FORTE@localhost:5432/auronex_prod

# BOT
PAPER_TRADING=True
USE_TESTNET=True
TRADING_SYMBOL=BTC/USDT
TIMEFRAME=15m
STRATEGY=trend_following
POSITION_SIZE_PERCENT=0.10
STOP_LOSS_PERCENT=0.02
TAKE_PROFIT_PERCENT=0.04
MAX_DRAWDOWN_PERCENT=0.10
MAX_TRADES_PER_DAY=10

# EXCHANGES - REAIS
BINANCE_API_KEY=SUA_API_KEY_REAL
BINANCE_SECRET_KEY=SUA_SECRET_KEY_REAL

# NOTIFICAÇÕES - RECOMENDADO EM PRODUÇÃO
TELEGRAM_BOT_TOKEN=SEU_BOT_TOKEN
TELEGRAM_CHAT_ID=SEU_CHAT_ID
ENABLE_TELEGRAM=True

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK

# CACHE
REDIS_URL=redis://localhost:6379/0

# MONITORAMENTO
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project

# SISTEMA
UPDATE_INTERVAL=60
SAVE_HISTORICAL_DATA=True
```

### 5. Salvar e sair:

```
Ctrl+X
Y
Enter
```

### 6. Proteger o .env:

```bash
chmod 600 .env
chown serverhome:serverhome .env
```

### 7. Re-criptografar API Keys (se tiver):

```bash
python3 scripts/migrate_encryption.py
```

### 8. Reiniciar serviços:

```bash
pm2 stop all
pm2 start all
pm2 save
```

### 9. Verificar logs:

```bash
pm2 logs fastapi-app --lines 50
```

### 10. Testar:

```bash
curl https://auronex.com.br/api/health
```

---

## ⚠️ SEGURANÇA CRÍTICA

### ❌ NUNCA:
- Commitar .env no Git
- Compartilhar chaves
- Usar mesmas chaves em local e produção
- Deixar .env público

### ✅ SEMPRE:
- .env no .gitignore
- Chaves diferentes local/produção
- Backup do .env em local seguro
- Permissões 600 no .env (produção)

---

## 🔍 TROUBLESHOOTING

### Erro: "ENCRYPTION_KEY não configurada"
```bash
# Verificar se .env existe
ls -la .env

# Verificar conteúdo
cat .env | grep ENCRYPTION_KEY

# Se vazio, recriar .env
```

### Erro: "SECRET_KEY não configurada"
```bash
# Mesmo processo acima
cat .env | grep SECRET_KEY
```

### Erro: "Token inválido" no login
```bash
# Verificar se SECRET_KEY mudou
# Se sim, usuários precisam fazer login novamente
# Tokens antigos ficam inválidos
```

### API Keys antigas não funcionam
```bash
# Re-criptografar com nova chave
python scripts/migrate_encryption.py
```

---

## 📊 CHECKLIST FINAL

### Local:
- [x] Chaves geradas
- [ ] .env criado
- [ ] API Keys migradas (se tiver)
- [ ] Serviços reiniciados
- [ ] Dashboard acessível
- [ ] Login funcionando

### Produção:
- [ ] Chaves geradas NO SERVIDOR
- [ ] .env criado
- [ ] PostgreSQL configurado
- [ ] API Keys migradas
- [ ] PM2 reiniciado
- [ ] HTTPS funcionando
- [ ] Monitoramento ativo

---

## 💡 PRÓXIMOS PASSOS

Após configurar .env:

1. **Testar local:**
   - Login no dashboard
   - Verificar saldo
   - Criar bot teste

2. **Migrar produção:**
   - Setup PostgreSQL
   - Configurar Alembic
   - Deploy com .env

3. **Monitoramento:**
   - Configurar Sentry
   - Ativar Telegram
   - Logs estruturados

---

## 📞 SUPORTE

Se tiver problemas:

1. Verificar logs: `pm2 logs`
2. Testar API: `curl http://localhost:8001/api/health`
3. Revisar .env: `cat .env`
4. Validar permissões: `ls -la .env`

---

**Criado em:** 14/11/2025  
**Válido para:** Auronex v1.0.05b+






