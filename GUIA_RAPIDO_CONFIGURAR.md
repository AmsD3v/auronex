# ⚡ GUIA RÁPIDO - CONFIGURAR .ENV

**Tempo:** 5 minutos

---

## 🔥 PASSO 1: Criar .env (2 min)

```bash
# Abrir Notepad
notepad I:/Robo/.env
```

---

## 📝 PASSO 2: Copiar e Colar (1 min)

```env
ENCRYPTION_KEY=3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=
SECRET_KEY=9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
ENVIRONMENT=development
DEBUG_MODE=True
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./db.sqlite3
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
BINANCE_TESTNET_API_KEY=
BINANCE_TESTNET_SECRET_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
ENABLE_TELEGRAM=False
REDIS_URL=redis://localhost:6379/0
UPDATE_INTERVAL=60
SAVE_HISTORICAL_DATA=True
```

**Salvar:** Ctrl+S  
**Fechar:** Ctrl+W

---

## 🔄 PASSO 3: Reiniciar (2 min)

```bash
cd I:/Robo
MATAR_TUDO.bat

```

---

## ✅ PASSO 4: Testar (30 seg)

```bash
curl http://localhost:8001/api/health
start http://localhost:8501
```

**Login:** admin@robotrader.com / admin123

---

## 🎉 PRONTO!

Sistema configurado e funcionando com **10 correções de segurança**! ✅

---

**Dúvidas?** Leia: `LEIA_ISTO_AGORA_IMPORTANTE.md`






