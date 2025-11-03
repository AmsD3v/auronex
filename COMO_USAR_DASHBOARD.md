# 🎨 **Como Usar o Dashboard + Bot 2 Horas**

## 🚀 **DUAS FORMAS DE USAR:**

---

## **OPÇÃO 1: Dashboard Web (Recomendado!)** 🌐

### **O Que É:**
Uma interface web LINDA que você abre no navegador e vê:
- 📊 Gráficos ao vivo
- 💰 Preço em tempo real
- 🎯 Sinais da estratégia
- 📈 Indicadores técnicos
- Auto-refresh a cada 30 segundos

### **Como Usar:**

```powershell
cd I:\Robo
.\venv\Scripts\activate
streamlit run dashboard.py
```

**Vai abrir automaticamente no navegador em:**
```
http://localhost:8501
```

### **O Dashboard Mostra:**
- ✅ Preço atual do Ethereum
- ✅ Sinal (COMPRAR/VENDER/AGUARDAR)
- ✅ Confiança do sinal
- ✅ Gráfico de candlestick com Bandas de Bollinger
- ✅ Indicadores técnicos (RSI, etc)
- ✅ Informações de mercado 24h

### **Recursos:**
- **Sidebar**: Escolha símbolo, estratégia, timeframe
- **Auto-refresh**: Atualiza sozinho a cada 30s
- **Gráficos interativos**: Zoom, hover para detalhes
- **Dark mode**: Bonito e profissional!

---

## **OPÇÃO 2: Bot Rodando 2 Horas** 🤖

### **O Que É:**
Bot roda por 2 horas em background, analisando a cada minuto e salvando tudo em arquivo JSON.

### **Como Usar:**

```powershell
cd I:\Robo
.\venv\Scripts\activate
python run_bot_2hours.py
```

### **O Bot Vai:**
- ✅ Analisar mercado a cada 60 segundos
- ✅ Detectar sinais fortes
- ✅ Salvar tudo em `bot_2hours_results.json`
- ✅ Mostrar progresso no terminal
- ✅ Gerar estatísticas finais

### **Arquivo de Resultados:**
Cria `bot_2hours_results.json` com:
- Todas as análises (timestamp, preço, sinal)
- Todos os sinais fortes detectados
- Estatísticas (variação de preço, etc)

---

## **🔥 MELHOR: Usar AMBOS JUNTOS!** 

### **Como Fazer:**

#### **1. Abra DOIS terminais**

**Terminal 1 - Dashboard:**
```powershell
cd I:\Robo
.\venv\Scripts\activate
streamlit run dashboard.py
```

**Terminal 2 - Bot 2 horas:**
```powershell
cd I:\Robo
.\venv\Scripts\activate
python run_bot_2hours.py
```

#### **2. Use Assim:**
- 🌐 **Navegador**: Abra `http://localhost:8501` para ver dashboard
- 📊 **Dashboard**: Monitore em tempo real
- 🤖 **Bot**: Roda em background salvando tudo
- 📄 **Resultados**: Depois veja `bot_2hours_results.json`

---

## **📊 Personalizar Dashboard**

No sidebar você pode mudar:

### **Símbolo:**
- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum) ⭐
- BNBUSDT (Binance Coin)
- SOLUSDT (Solana)

### **Estratégia:**
- mean_reversion (Reversão à Média) ⭐
- trend_following (Seguir Tendência)

### **Timeframe:**
- 1m (1 minuto)
- 5m (5 minutos)
- 15m (15 minutos) ⭐
- 1h (1 hora)

### **Auto-refresh:**
- ✅ Ativo: Atualiza a cada 30s
- ❌ Desativo: Só atualiza manualmente

---

## **💡 Dicas de Uso**

### **1. Monitoramento Contínuo:**
```
Dashboard aberto no navegador (F11 para fullscreen)
Bot rodando 2h no background
Você faz outras coisas e olha de vez em quando!
```

### **2. Análise Rápida:**
```
Só dashboard, veja sinais em tempo real
Sem salvar histórico
```

### **3. Teste Longo:**
```
Bot 2h salvando tudo
Depois analise os resultados no JSON
```

---

## **🛑 Como Parar**

### **Dashboard:**
- No terminal: `Ctrl + C`
- Fecha automaticamente

### **Bot 2 Horas:**
- No terminal: `Ctrl + C`
- Salva resultados parciais antes de fechar

---

## **📁 Arquivos Gerados**

### **Dashboard:**
- Nenhum (só visualização)

### **Bot 2 Horas:**
- `bot_2hours_results.json` - Resultados completos
- `bot_5min_test.log` - Log detalhado

---

## **🎯 Exemplos de Uso**

### **Exemplo 1: Quero só ver agora**
```powershell
streamlit run dashboard.py
```
Abre navegador, vê tudo, fecha quando quiser.

### **Exemplo 2: Quero analisar 2 horas**
```powershell
python run_bot_2hours.py
```
Bot roda 2h, você faz outra coisa, volta depois.

### **Exemplo 3: Monitoramento profissional**
```powershell
# Terminal 1
streamlit run dashboard.py

# Terminal 2
python run_bot_2hours.py
```
Dashboard no navegador + Bot rodando = Setup completo!

---

## **⚠️ Importante**

1. ✅ **Sempre ative o venv** antes: `.\venv\Scripts\activate`
2. ✅ Dashboard usa porta **8501** (não pode ter outra coisa usando)
3. ✅ Bot 2h pode ser interrompido com `Ctrl+C` sem problemas
4. ✅ Tudo é **Paper Trading** - sem risco!

---

## **🐛 Problemas Comuns**

### **Dashboard não abre:**
```powershell
# Verifique se streamlit foi instalado
pip show streamlit

# Tente:
python -m streamlit run dashboard.py
```

### **"Port already in use":**
Dashboard já está rodando. Feche ou use:
```powershell
streamlit run dashboard.py --server.port 8502
```

### **Erro de import:**
```powershell
# Certifique-se que está no venv
.\venv\Scripts\activate

# Reinstale streamlit
pip install --upgrade streamlit
```

---

## **🎉 Aproveite!**

Você tem agora:
- ✅ Dashboard profissional web
- ✅ Bot que roda por horas
- ✅ Análises em tempo real
- ✅ Histórico completo salvo

**Perfeito para monitorar e aprender!** 🚀

---

**Para começar AGORA:**
```powershell
cd I:\Robo
.\venv\Scripts\activate
streamlit run dashboard.py
```








