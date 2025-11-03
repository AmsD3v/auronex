# 📦 Guia de Instalação Completo - RoboTrader

## 🎯 Requisitos do Sistema

### Mínimos
- **SO**: Windows 10/11, Linux ou macOS
- **RAM**: 4GB mínimo (8GB recomendado)
- **Armazenamento**: 500MB livres
- **Internet**: Conexão estável (bot precisa estar online 24/7)

### Software Necessário
- Python 3.10 ou superior
- pip (geralmente vem com Python)
- Git (opcional, mas recomendado)

---

## 🪟 Instalação no Windows

### Passo 1: Instalar Python

1. **Baixar Python**
   - Acesse: https://www.python.org/downloads/
   - Baixe Python 3.10+ (versão mais recente estável)

2. **Instalar**
   - Execute o instalador
   - ⚠️ **IMPORTANTE**: Marque a opção **"Add Python to PATH"**
   - Clique em "Install Now"

3. **Verificar Instalação**
   ```powershell
   python --version
   # Deve mostrar: Python 3.10.x ou superior
   
   pip --version
   # Deve mostrar a versão do pip
   ```

### Passo 2: Instalar Dependências

1. **Abrir PowerShell ou CMD**
   - Pressione `Win + R`
   - Digite: `powershell`
   - Enter

2. **Navegar até a pasta do projeto**
   ```powershell
   cd I:\Robo
   ```

3. **Instalar bibliotecas**
   ```powershell
   pip install -r requirements.txt
   ```
   
   Isso pode levar alguns minutos. Aguarde até terminar.

### Passo 3: Configurar Binance Testnet

1. **Criar conta no Testnet**
   - Acesse: https://testnet.binance.vision/
   - Clique em "Log in with GitHub"
   - Autorize o acesso

2. **Gerar API Keys**
   - Na página do testnet, clique no seu avatar (canto superior direito)
   - Clique em "API Keys"
   - Clique em "Generate HMAC_SHA256 Key"
   - Dê um nome (ex: "RoboTrader")
   - **COPIE** tanto a API Key quanto a Secret Key
   - ⚠️ **IMPORTANTE**: A Secret Key só aparece UMA VEZ!

### Passo 4: Configurar o Bot

1. **Copiar arquivo de configuração**
   ```powershell
   copy .env.example .env
   ```

2. **Editar arquivo .env**
   - Abra o arquivo `.env` com Notepad ou VS Code
   - Cole suas API Keys:
   
   ```env
   # Para TESTNET
   BINANCE_TESTNET_API_KEY=sua_api_key_aqui
   BINANCE_TESTNET_SECRET_KEY=sua_secret_key_aqui
   
   USE_TESTNET=True
   PAPER_TRADING=True
   
   # Configurações básicas
   TRADING_SYMBOL=BTCUSDT
   TIMEFRAME=15m
   STRATEGY=trend_following
   ```

3. **Salvar e fechar**

### Passo 5: Testar Instalação

```powershell
# Testar conexão com Binance
python scripts/test_connection.py
```

**Resultado esperado:**
```
✅ Conexão OK!
Modo: TESTNET
Símbolo: BTCUSDT
Preço Atual: $67,234.50
Saldo USDT: $10,000.00
```

Se funcionou, parabéns! Instalação completa! 🎉

---

## 🐧 Instalação no Linux/macOS

### Passo 1: Instalar Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

**macOS (com Homebrew):**
```bash
brew install python@3.10
```

### Passo 2: Criar ambiente virtual (recomendado)

```bash
cd I:/Robo  # ou caminho do seu projeto

# Criar venv
python3 -m venv venv

# Ativar venv
source venv/bin/activate  # Linux/macOS
```

### Passo 3: Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 4-5: Mesmos passos do Windows

---

## 🔧 Verificação Completa

Execute os seguintes testes para garantir que tudo está funcionando:

### 1. Verificar Python e pip
```bash
python --version
pip --version
```

### 2. Verificar dependências instaladas
```bash
pip list
```

Deve incluir:
- ccxt
- pandas
- matplotlib
- python-telegram-bot
- rich
- etc.

### 3. Testar conexão
```bash
python scripts/test_connection.py
```

### 4. Baixar dados de teste
```bash
python scripts/download_data.py --days 7
```

### 5. Executar backtest
```bash
python scripts/run_backtest.py
```

### 6. Executar bot (modo paper)
```bash
python main.py
```

Pressione `Ctrl+C` para parar.

---

## 🐛 Solução de Problemas Comuns

### "python não é reconhecido como comando"

**Problema**: Python não está no PATH

**Solução Windows**:
1. Desinstalar Python
2. Reinstalar marcando "Add Python to PATH"
3. Reiniciar o terminal

**Solução Linux/macOS**:
```bash
# Tentar python3 em vez de python
python3 --version
```

### "pip install falhou"

**Problema**: Dependência falhou ao instalar

**Solução**:
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar uma por vez para identificar problema
pip install ccxt
pip install pandas
# etc...
```

### "API Key inválida"

**Problema**: Chaves incorretas ou não configuradas

**Solução**:
1. Verificar se copiou as chaves completas
2. Verificar se está usando `USE_TESTNET=True`
3. Verificar se as chaves são do testnet
4. Gerar novas chaves se necessário

### "ModuleNotFoundError"

**Problema**: Biblioteca não instalada

**Solução**:
```bash
pip install nome_da_biblioteca
```

### "Permission denied"

**Problema**: Falta de permissões

**Solução Windows**:
```powershell
# Executar PowerShell como Administrador
```

**Solução Linux/macOS**:
```bash
# Usar venv ou
sudo pip install -r requirements.txt
```

### Bot não conecta ao testnet

**Problema**: Firewall ou proxy

**Solução**:
1. Desativar temporariamente firewall
2. Verificar se consegue acessar: https://testnet.binance.vision/
3. Verificar proxy corporativo
4. Tentar de outra rede

---

## 📚 Estrutura de Pastas Após Instalação

```
I:\Robo\
├── bot/                    # Código do bot
│   ├── strategies/         # Estratégias
│   ├── backtesting/        # Sistema de backtest
│   └── ...
├── config/                 # Configurações
├── data/                   # Banco de dados
│   └── trading.db         # (criado automaticamente)
├── logs/                   # Logs do bot
│   └── robotrader_*.log   # (criados automaticamente)
├── reports/                # Relatórios de backtest
├── scripts/                # Scripts utilitários
├── tests/                  # Testes
├── .env                    # SUAS configurações (não versionar!)
├── .env.example            # Exemplo de configuração
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências
└── README.md              # Documentação
```

---

## 🚀 Próximos Passos

Após instalação completa:

1. ✅ Leia o **README.md** completo
2. ✅ Leia o **GUIA_RAPIDO.md**
3. ✅ Execute vários backtests
4. ✅ Deixe o bot rodar no testnet por SEMANAS
5. ✅ Monitore e ajuste parâmetros
6. ⚠️ Apenas depois de MUITO teste, considere usar dinheiro real

---

## 💡 Dicas

1. **Use IDE**: VS Code ou PyCharm facilitam muito
2. **Git**: Use controle de versão para suas modificações
3. **Backups**: Faça backup do arquivo .env (mas nunca compartilhe!)
4. **Logs**: Sempre verifique os logs quando algo der errado
5. **Comunidade**: Pesquise no Google, GitHub, Stack Overflow

---

## 📞 Recursos Adicionais

- **Python**: https://docs.python.org/
- **Pandas**: https://pandas.pydata.org/
- **CCXT**: https://docs.ccxt.com/
- **Binance API**: https://binance-docs.github.io/apidocs/
- **Trading View**: https://www.tradingview.com/ (para análise de gráficos)

---

**Instalação concluída! Agora você está pronto para começar! 🚀**

**Lembre-se**: Trading envolve risco. Use apenas no testnet até dominar completamente o sistema.

