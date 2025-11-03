# 🚀 Guia Rápido - RoboTrader

## ⚡ Instalação em 5 Minutos

### 1. Instalar Python
```bash
# Baixe Python 3.10+ de: https://www.python.org/downloads/
# IMPORTANTE: Marque "Add Python to PATH"
```

### 2. Instalar Dependências
```bash
cd I:\Robo
pip install -r requirements.txt
```

### 3. Configurar API Keys

#### Opção A: Testnet (RECOMENDADO para começar)
1. Acesse: https://testnet.binance.vision/
2. Faça login com GitHub
3. Clique em "Generate HMAC_SHA256 Key"
4. Copie API Key e Secret Key

#### Opção B: Produção (Apenas após MUITOS testes)
1. Acesse: https://www.binance.com/
2. Conta > API Management
3. Crie nova API Key
4. **IMPORTANTE**: Ative apenas "Enable Reading" e "Enable Spot & Margin Trading"

### 4. Configurar .env
```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar com suas chaves (use Notepad ou VS Code)
# Cole suas API Keys no arquivo
```

**Exemplo de .env para TESTNET:**
```env
USE_TESTNET=True
BINANCE_TESTNET_API_KEY=sua_chave_aqui
BINANCE_TESTNET_SECRET_KEY=sua_secret_aqui
TRADING_SYMBOL=BTCUSDT
TIMEFRAME=15m
STRATEGY=trend_following
PAPER_TRADING=True
```

## 🧪 Testar Instalação

### Passo 1: Testar Conexão
```bash
python scripts/test_connection.py
```

**Se funcionar, você verá:**
```
✅ Conexão OK!
Modo: TESTNET
Símbolo: BTCUSDT
Preço Atual: $67,234.50
Saldo USDT: $10,000.00
```

### Passo 2: Baixar Dados Históricos
```bash
python scripts/download_data.py --days 30
```

### Passo 3: Executar Backtest
```bash
python scripts/run_backtest.py
```

**Resultado esperado:**
```
📊 RESUMO DO BACKTEST
================================================
💰 CAPITAL:
  Inicial:        $10,000.00
  Final:          $10,234.50
  P&L Total:      +$234.50
  Retorno:        +2.35%

📈 TRADES:
  Total:          15
  Vencedores:     9 🟢
  Perdedores:     6 🔴
  Taxa de Acerto: 60.00%
```

## 🤖 Executar o Bot

### Modo Paper Trading (Simulado)
```bash
python main.py
```

**O que acontece:**
- Bot analisa mercado em tempo real
- Gera sinais de compra/venda
- **NÃO executa ordens reais** (apenas simula)
- Registra tudo nos logs

### Ativar Trading Real (Testnet)

**Edite .env:**
```env
PAPER_TRADING=False
```

**Execute:**
```bash
python main.py
```

**IMPORTANTE:** 
- Ainda está no Testnet (dinheiro virtual)
- Ordens são executadas de verdade, mas sem risco
- Use para testar por SEMANAS antes de produção

## 📊 Monitorar o Bot

### Logs em Tempo Real
```bash
# Os logs aparecem no terminal
# Também são salvos em: logs/robotrader_YYYYMMDD.log
```

### Ver Performance
```python
# O bot imprime estatísticas periodicamente:
📊 Posição LONG @ $67,234.50 | Atual: $67,500.00 | P&L: +$26.55 (+0.39%)
```

### Banco de Dados
```
# Todos os trades são salvos em: data/trading.db
# Use DB Browser for SQLite para visualizar
```

## ⚙️ Ajustar Configurações

### Arquivo: .env

**Símbolos populares:**
```env
TRADING_SYMBOL=BTCUSDT    # Bitcoin
TRADING_SYMBOL=ETHUSDT    # Ethereum
TRADING_SYMBOL=BNBUSDT    # Binance Coin
TRADING_SYMBOL=SOLUSDT    # Solana
```

**Timeframes:**
```env
TIMEFRAME=1m      # 1 minuto (muito rápido)
TIMEFRAME=5m      # 5 minutos
TIMEFRAME=15m     # 15 minutos (recomendado)
TIMEFRAME=1h      # 1 hora (mais estável)
TIMEFRAME=4h      # 4 horas (day trading)
```

**Estratégias:**
```env
STRATEGY=trend_following    # Seguir tendência (mercados em alta/baixa)
STRATEGY=mean_reversion     # Reversão à média (mercados laterais)
```

**Risco:**
```env
POSITION_SIZE_PERCENT=0.10  # 10% do saldo por trade (padrão)
STOP_LOSS_PERCENT=0.02      # 2% de stop loss (padrão)
TAKE_PROFIT_PERCENT=0.04    # 4% de take profit (padrão)
```

## 🔔 Configurar Telegram (Opcional)

### 1. Criar Bot
1. Abra Telegram
2. Procure por: @BotFather
3. Envie: `/newbot`
4. Siga as instruções
5. Copie o **token**

### 2. Obter Chat ID
1. Inicie conversa com seu bot
2. Envie qualquer mensagem
3. Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
4. Procure por `"chat":{"id":123456789`
5. Copie o número

### 3. Configurar .env
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
ENABLE_TELEGRAM=True
```

**Você receberá notificações:**
- 🟢 Quando bot entrar em trade
- 🔴 Quando bot sair de trade
- ⚠️ Alertas de risco
- 📊 Resumo diário

## 🛠️ Comandos Úteis

```bash
# Testar conexão
python scripts/test_connection.py

# Baixar mais dados históricos
python scripts/download_data.py --days 90

# Backtest com parâmetros personalizados
python scripts/run_backtest.py --symbol ETHUSDT --days 60 --strategy mean_reversion

# Executar bot
python main.py

# Parar bot (Ctrl+C no terminal)
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

### Erro: "API Key não configurada"
```bash
# Verificar se .env existe e tem as chaves corretas
# Lembre-se: USE_TESTNET=True para testnet
```

### Erro: "Connection refused"
```bash
# Verificar internet
# Testar acesso: https://testnet.binance.vision/
```

### Bot não está fazendo trades
**Possíveis motivos:**
1. `PAPER_TRADING=True` (apenas simulando)
2. Mercado lateral (estratégia aguardando melhor momento)
3. Confiança dos sinais baixa (< 65%)
4. Limite de trades diários atingido

**Verificar:**
```bash
# Ver logs em tempo real
tail -f logs/robotrader_*.log
```

## 📈 Próximos Passos

### Fase 1: Aprendizado (Semanas 1-2)
- ✅ Rodar backtests com diferentes configurações
- ✅ Entender os indicadores (EMA, RSI, Bollinger)
- ✅ Ler logs e entender decisões do bot

### Fase 2: Testnet (Semanas 3-8)
- ✅ Deixar bot rodando 24/7 no testnet
- ✅ Testar diferentes estratégias
- ✅ Ajustar parâmetros de risco
- ✅ Simular diferentes condições de mercado

### Fase 3: Produção (Apenas se resultados consistentes)
- ⚠️ Começar com $50-100 USDT
- ⚠️ Monitorar MUITO de perto
- ⚠️ Estar preparado para perder tudo
- ⚠️ **NUNCA** investir dinheiro que não pode perder

## ⚠️ AVISOS FINAIS

### ❌ NÃO FAÇA:
- ❌ Usar dinheiro real sem testar por MESES
- ❌ Investir mais do que pode perder
- ❌ Esperar ficar rico rapidamente
- ❌ Ignorar os riscos
- ❌ Mexer nas configurações enquanto bot está rodando

### ✅ FAÇA:
- ✅ Testar exaustivamente no testnet
- ✅ Começar com valores MUITO pequenos
- ✅ Monitorar constantemente
- ✅ Aprender continuamente
- ✅ Aceitar que pode perder dinheiro

## 📞 Suporte

**Problemas?**
- 📖 Leia o README.md completo
- 📋 Verifique os logs em `logs/`
- 🔍 Google o erro específico
- 📚 Leia documentação da Binance API

---

**Boa sorte e trade com responsabilidade! 🚀**

**Lembre-se:** A maioria dos traders perde dinheiro. Este bot é uma ferramenta de aprendizado, não uma garantia de lucros.

