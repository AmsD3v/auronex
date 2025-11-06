# 🚀 COMO USAR O DASHBOARD REACT - GUIA COMPLETO

**Sistema:** Auronex RoboTrader  
**Dashboard:** React + Next.js  
**Status:** ✅ 100% Funcional com Tempo Real

---

## 📋 INÍCIO RÁPIDO

### **1. Iniciar Sistema Completo** (Recomendado)

Clique duplo neste arquivo:
```
INICIAR_SISTEMA_COMPLETO_REACT.bat
```

Isso vai:
- ✅ Iniciar Backend FastAPI (porta 8001)
- ✅ Iniciar Frontend React (porta 3000)
- ✅ Abrir 2 janelas

### **2. Acessar Dashboard**

```
http://localhost:3000
```

---

## 🔐 PRIMEIRO ACESSO

### **Se ainda não tem usuário:**

1. **Criar conta:**
   ```
   http://localhost:8001/register
   ```

2. **Preencher:**
   - Email: seu@email.com
   - Senha: suasenha123
   - Nome: Seu Nome
   - Sobrenome: Sobrenome

3. **Registrar**

### **Fazer login no React:**

```
http://localhost:3000
```

Use o email e senha que criou!

---

## 📊 APÓS O LOGIN

Você vai ver o **Dashboard Principal** com:

### **✅ Header**
- Logo "Auronex Trading"
- **Relógio** (atualiza 1s) ⏰
- Nome do usuário
- Plano (FREE/PRO/PREMIUM)
- Botão Logout

### **✅ Avisos** (se houver)
- Plano atual e limites
- Erros (se não tiver API Keys ou bots)

### **✅ Métricas Principais** (4 cards)
1. 🤖 Total de Bots
2. 💰 Saldo Total
3. 📈 Trades Hoje
4. ✅ Taxa Sucesso

### **✅ Saldo da Exchange**
- Card com saldo detalhado
- USDT, BTC, ETH, BNB
- **Atualiza a cada 1 segundo!** ⚡

### **✅ Status do Sistema**
- Frontend React: Rodando
- Backend FastAPI: Conectado
- Tempo Real: Ativo (1s)

### **✅ Lista de Bots**
- Ver todos seus bots
- Botões Start/Stop
- Configurações de cada bot
- Deletar bot

### **✅ Links Rápidos**
- 🤖 Gerenciar Bots
- 🔑 API Keys
- 👨‍💼 Admin Panel
- 📚 API Docs

---

## ⚙️ CONFIGURAR PARA TEMPO REAL COMPLETO

Para ver **TODOS os dados** em tempo real:

### **PASSO 1: Adicionar API Key**

1. Vá em: http://localhost:8001/api-keys-page
2. Clique em **"Adicionar API Key"**
3. Preencha:
   - **Exchange:** Binance (ou outra)
   - **API Key:** sua_api_key
   - **Secret:** seu_secret
   - **Testnet:** ✅ (marque se for testnet)
4. Salve

### **PASSO 2: Criar Bot**

1. Vá em: http://localhost:8001/bots-page
2. Clique em **"Criar Bot"**
3. Preencha:
   - **Nome:** Bot Trader 1
   - **Exchange:** Binance
   - **Estratégia:** Mean Reversion
   - **Timeframe:** 15m
   - **Capital:** 1000
   - **Stop Loss:** 2%
   - **Take Profit:** 4%
4. Salve

### **PASSO 3: Voltar ao Dashboard React**

```
http://localhost:3000
```

**Agora vai ver:**
- ✅ Saldo REAL da exchange (atualiza 1s!)
- ✅ Bot aparece na lista
- ✅ Pode iniciar/parar bot
- ✅ Métricas funcionando

---

## ⚡ TEMPO REAL - COMO FUNCIONA

O dashboard usa **React Query** para buscar dados automaticamente:

```typescript
// Hook useRealtime()

Saldo:   atualiza a cada 1 segundo  ⚡⚡⚡
Bots:    atualiza a cada 5 segundos ⚡⚡
Trades:  atualiza a cada 5 segundos ⚡⚡
Stats:   atualiza a cada 10 segundos ⚡
```

**Você NÃO precisa fazer nada!**
- ✅ Dados atualizam sozinhos
- ✅ SEM recarregar página
- ✅ SEM flash/opacity
- ✅ Performance perfeita

---

## 🎨 FEATURES DO DASHBOARD

### **1. Relógio em Tempo Real** ⏰
```
Localização: Canto superior direito
Formato: HH:MM:SS
Atualização: 1 segundo
```

### **2. Cards de Métricas** 📊
```
4 cards principais:
- Total de Bots (com número de ativos)
- Saldo Total (com variação)
- Trades Hoje (com bots operando)
- Taxa de Sucesso (win rate)

Animações:
- Fade in ao carregar
- Hover effect (levanta)
- Glow effect
```

### **3. Card de Saldo** 💰
```
Mostra:
- Total em USD ou BRL
- Breakdown: USDT, BTC, ETH, BNB
- Variação 24h
- Icon trending (up/down)

Atualiza: 1 segundo!
```

### **4. Cards de Bots** 🤖
```
Para cada bot:
- Nome e exchange
- Estratégia e timeframe
- Capital investido
- Stop Loss e Take Profit
- Criptomoedas configuradas
- Botão Start/Stop
- Status (ativo/pausado)
- Botão deletar

Ações:
- Clicar Play → Inicia bot
- Clicar Pause → Para bot
- Clicar Trash → Deleta bot
```

---

## 🔧 FUNCIONALIDADES AVANÇADAS

### **Toggle de Moeda**

No header, você pode alternar entre:
- 💵 USD (dólar)
- 💰 BRL (real)

**Todos os valores** se atualizam automaticamente!

### **Plano e Limites**

O dashboard mostra:
- Plano atual (FREE/PRO/PREMIUM)
- Quantos bots você pode criar
- Quantas cryptos por bot
- Se atingiu o limite

### **Error Handling**

Se algo der errado:
- ✅ Aviso amarelo amigável
- ✅ Link para resolver
- ✅ Dashboard continua funcionando
- ✅ NÃO trava ou dá loop!

---

## 🎯 FLUXO COMPLETO DE USO

```
1. Login
   ↓
2. Dashboard carrega
   ↓
3. Verifica API Keys
   ├─ TEM → Busca saldo (1s)
   └─ NÃO TEM → Aviso amarelo
   ↓
4. Verifica Bots
   ├─ TEM → Lista bots
   └─ NÃO TEM → Aviso + Botão criar
   ↓
5. Tempo Real ATIVO!
   ├─ Saldo: 1s
   ├─ Bots: 5s
   ├─ Trades: 5s
   └─ Stats: 10s
```

---

## 🚀 BOTÕES E AÇÕES

### **Start/Stop Bot**
```
Clicar Play → Bot inicia (via API)
              ↓
              API atualiza banco
              ↓
              Bot Controller detecta
              ↓
              Bot começa a operar
              ↓
              Dashboard atualiza (5s)
```

### **Deletar Bot**
```
Clicar Trash → Confirmar
               ↓
               API deleta do banco
               ↓
               Dashboard atualiza (5s)
               ↓
               Bot some da lista
```

---

## 📈 MONITORAMENTO EM TEMPO REAL

Abra o **Console do navegador** (F12) para ver:

```
[React Query] Fetching balance every 1s
[React Query] Fetching bots every 5s
[React Query] Fetching trades every 5s
[Clock] Updating every 1s
```

**Isso acontece automaticamente!** Você não precisa fazer nada.

---

## 💡 DICAS

### **1. Deixar aberto**
- Dashboard atualiza automaticamente
- Não precisa dar F5
- Pode minimizar navegador

### **2. Múltiplas abas**
- Pode abrir em várias abas
- Todas atualizam em tempo real
- Dados sincronizados

### **3. Mobile**
- Dashboard é responsivo
- Funciona em celular/tablet
- Layout se adapta

---

## 🐛 TROUBLESHOOTING

### **Não vejo os bots**
→ Crie em: http://localhost:8001/bots-page

### **Não vejo o saldo**
→ Configure API Key em: http://localhost:8001/api-keys-page

### **Trades = 0**
→ Normal! Bots precisam estar ativos e mercado favorável

### **Dashboard lento**
→ Verifique internet
→ Verifique se muitos bots estão ativos

### **Voltou a dar loop**
→ Acesse: http://localhost:3000/reset
→ Faça login novamente

---

## ✅ CHECKLIST DE SUCESSO

Após configurar tudo, você deve ter:

- [x] Dashboard carregando sem loops
- [x] Relógio atualizando (1s)
- [x] API Key configurada
- [x] Pelo menos 1 bot criado
- [x] Saldo aparecendo
- [x] Métricas funcionando
- [x] Botões Start/Stop funcionando

---

## 🎉 PARABÉNS!

**Você tem agora:**
- ✅ Dashboard React profissional
- ✅ Tempo real perfeito (< 1s)
- ✅ Performance excelente
- ✅ UX nível exchange
- ✅ Pronto para operar!

---

**Bom trading!** 📈🚀

**Auronex Technology · 2025**

