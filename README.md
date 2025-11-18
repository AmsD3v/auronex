# 🤖 RoboTrader - Bot de Trading de Criptomoedas

> **Bot automatizado de trading desenvolvido para operar 24/7 no mercado de criptomoedas**

## 📋 Sobre o Projeto

Sistema completo de trading algorítmico com:
- ✅ Suporte a Binance (Spot e Futures)
- ✅ Múltiplas estratégias implementadas
- ✅ Sistema de backtesting robusto
- ✅ Gerenciamento de risco avançado
- ✅ Notificações via Telegram
- ✅ Testnet para testes sem risco
- ✅ 100% gratuito e open-source

## ⚠️ AVISO IMPORTANTE

**TRADING ENVOLVE RISCO DE PERDA TOTAL DO CAPITAL**
- Este bot é para fins educacionais
- Não há garantia de lucros
- Teste EXTENSIVAMENTE antes de usar dinheiro real
- Comece sempre com valores pequenos
- Nunca invista dinheiro que não pode perder

## 🛠️ Ferramentas Necessárias (TODAS GRATUITAS)

### 1. Python 3.10+
- Download: https://www.python.org/downloads/
- **IMPORTANTE**: Marque "Add Python to PATH" na instalação

### 2. Git (opcional, mas recomendado)
- Download: https://git-scm.com/downloads

### 3. Conta na Binance
- Site: https://www.binance.com/
- **TESTNET** (para testes): https://testnet.binance.vision/

### 4. Editor de Código (escolha um)
- VS Code: https://code.visualstudio.com/ (recomendado)
- PyCharm Community: https://www.jetbrains.com/pycharm/download/

### 5. Bot do Telegram (opcional, para notificações)
- Fale com @BotFather no Telegram para criar seu bot

## 🚀 Instalação Rápida

### Passo 1: Criar Ambiente Virtual (Recomendado)

```bash
# Criar venv
python -m venv venv

# Ativar venv
# Windows PowerShell:
.\venv\Scripts\activate

# Windows CMD:
venv\Scripts\activate.bat

# Linux/macOS:
source venv/bin/activate
```

### Passo 2: Instalar Dependências

```bash
# Com venv ativado (verá "(venv)" no prompt)
pip install -r requirements.txt
```

📖 **Leia**: `COMO_USAR_VENV.md` para entender melhor

### Passo 2: Configurar Variáveis de Ambiente

1. Copie o arquivo `.env.example` para `.env`:
```bash
copy .env.example .env
```

2. Edite o arquivo `.env` com suas credenciais

### Passo 3: Testar Conexão

```bash
python scripts/test_connection.py
```

### Passo 4: Rodar Backtest

```bash
python scripts/run_backtest.py
```

### Passo 5: Executar Bot (Testnet)

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
I:\Robo\
├── bot/                    # Código principal do bot
│   ├── __init__.py
│   ├── exchange.py         # Conexão com exchanges
│   ├── strategies/         # Estratégias de trading
│   │   ├── __init__.py
│   │   ├── base.py         # Classe base para estratégias
│   │   ├── trend_following.py
│   │   └── mean_reversion.py
│   ├── backtesting/        # Sistema de backtesting
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── visualizer.py
│   ├── risk_management.py  # Gerenciamento de risco
│   ├── data_manager.py     # Coleta e armazenamento de dados
│   └── notifier.py         # Sistema de notificações
├── config/                 # Configurações
│   ├── __init__.py
│   └── settings.py
├── data/                   # Dados históricos (SQLite)
│   └── .gitkeep
├── logs/                   # Logs do sistema
│   └── .gitkeep
├── scripts/                # Scripts auxiliares
│   ├── test_connection.py
│   ├── run_backtest.py
│   └── download_data.py
├── tests/                  # Testes unitários
│   └── __init__.py
├── .env.example            # Exemplo de configuração
├── .gitignore
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 📊 Estratégias Disponíveis

### 1. Trend Following (Seguir Tendência)
- Usa médias móveis (EMA 9, 21, 50)
- Identifica direção da tendência
- Entra quando todas as médias estão alinhadas
- Ideal para mercados em alta/baixa

### 2. Mean Reversion (Reversão à Média)
- Usa Bandas de Bollinger e RSI
- Identifica pontos de sobrecompra/sobrevenda
- Entra quando preço se afasta muito da média
- Ideal para mercados laterais

### 3. Combinada (em desenvolvimento)
- Combina ambas as estratégias
- Adapta-se às condições do mercado

## 🎯 Modo de Uso

### Testnet (SEMPRE COMECE AQUI)

1. Crie conta em https://testnet.binance.vision/
2. Gere API Key no testnet
3. Configure `.env` com `USE_TESTNET=True`
4. Execute o bot

### Produção (Apenas após MUITOS testes)

1. Configure `.env` com `USE_TESTNET=False`
2. Use API Key da conta real
3. **COMECE COM VALORES PEQUENOS**
4. Monitore constantemente

## 📈 Backtesting

Teste suas estratégias com dados históricos:

```bash
# Backtest básico (últimos 30 dias)
python scripts/run_backtest.py

# Backtest personalizado
python scripts/run_backtest.py --symbol BTCUSDT --days 90 --strategy trend_following
```

## 🔔 Notificações Telegram

1. Fale com @BotFather no Telegram
2. Crie um novo bot com `/newbot`
3. Copie o token fornecido
4. Inicie conversa com seu bot
5. Obtenha seu chat_id em https://api.telegram.org/bot<TOKEN>/getUpdates
6. Configure no arquivo `.env`

## 📊 Monitoramento

- Logs salvos em `logs/`
- Banco de dados em `data/trading.db`
- Notificações em tempo real via Telegram
- Relatórios de performance

## 🛡️ Gerenciamento de Risco

O bot implementa:
- **Stop Loss**: Limite de perda por operação (padrão: 2%)
- **Take Profit**: Objetivo de lucro (padrão: 4%)
- **Trailing Stop**: Stop loss que acompanha o lucro
- **Tamanho de Posição**: Baseado no saldo (padrão: 10%)
- **Máximo de Operações**: Limite diário
- **Drawdown Máximo**: Pausa automática se perda > 10%

## 🔧 Personalização

Edite `config/settings.py` para ajustar:
- Símbolos para tradear
- Timeframes
- Parâmetros de risco
- Indicadores técnicos
- Horários de operação

## 📚 Aprendizado

### Recursos Recomendados
- **Livros**: 
  - "Trading Algorítmico" - Ernest Chan
  - "Análise Técnica dos Mercados Financeiros" - John Murphy
  
- **Cursos Gratuitos**:
  - YouTube: Série sobre algoritmos de trading
  - Binance Academy: https://academy.binance.com/

- **Documentação**:
  - Binance API: https://binance-docs.github.io/apidocs/
  - CCXT: https://docs.ccxt.com/

## 🐛 Solução de Problemas

### Erro de Conexão
- Verifique suas credenciais no `.env`
- Confirme que está usando o endpoint correto (testnet ou produção)
- Verifique sua conexão com internet

### Erro de Permissões
- Certifique-se que sua API Key tem permissões de trading
- No testnet, ative "Enable Trading" nas configurações da API

### Erro de Saldo Insuficiente
- No testnet, você pode adicionar mais fundos virtuais
- Na produção, deposite mais USDT

## 🤝 Contribuindo

Este é um projeto educacional. Sinta-se livre para:
- Reportar bugs
- Sugerir melhorias
- Adicionar novas estratégias
- Melhorar a documentação

## 📄 Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo.
Use por sua conta e risco.

## 📞 Suporte

- Issues: Abra uma issue no repositório
- Documentação: Leia este README
- Logs: Sempre verifique os logs em `logs/`

---

**Desenvolvido com 🐍 Python | Feito para aprendizado e experimentação**

**⚠️ LEMBRE-SE: Trading é arriscado. Não invista mais do que pode perder!**

"# auronexbot"  
