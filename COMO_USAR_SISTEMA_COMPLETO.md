# 📖 COMO USAR O ROBOTRADER - GUIA COMPLETO

## 🚀 **INÍCIO RÁPIDO:**

### **Passo 1: Iniciar os Servidores**

**Terminal 1 - Django (Gerenciamento):**
```bash
cd I:\Robo
.\venv\Scripts\activate
cd saas
python manage.py runserver 8001
```

**Terminal 2 - Streamlit (Dashboard Visual):**
```bash
cd I:\Robo
.\venv\Scripts\activate
streamlit run dashboard_master.py
```

**Terminal 3 - Bot (Opcional - para bot local):**
```bash
cd I:\Robo
.\venv\Scripts\activate
python bot_adaptativo.py
```

✅ **3 sistemas rodando simultaneamente!**

---

### **Passo 2: Criar Conta**

1. Abrir navegador: http://localhost:8001/
2. Clicar em "Começar Agora"
3. Preencher cadastro:
   ```
   Nome: Seu Nome
   Sobrenome: Seu Sobrenome
   Email: seu@email.com
   Senha: suasenha123 (mínimo 8 caracteres)
   ```
4. Clicar em "Criar Conta"
5. ✅ Redirecionado para /dashboard/

---

### **Passo 3: Adicionar API Keys**

1. No dashboard, clicar em "Gerenciar API Keys"
2. OU acessar diretamente: http://localhost:8001/api-keys/
3. Clicar em "+ Adicionar API Key"
4. Preencher:
   ```
   Corretora: Binance
   API Key: FuwPLJl7mDJH6t4HaWjn4eCqFAQJOccvhCqCLxAcP6vx6ZdjHIysqQ0KGcqPnmef
   Secret Key: qKeH7VI6AEGiR7un7uGyazh9EaKYUugh1sZccVbCPAZ2TerJ3PT7b9F4v5pumF85
   Passphrase: (deixar vazio para Binance/Bybit)
   Testnet: ☐ (desmarcar para produção real)
   ```
5. Clicar em "Adicionar"
6. ✅ API Key salva e criptografada!

---

### **Passo 4: Criar Bot**

1. No dashboard, clicar em "Gerenciar Bots"
2. OU acessar diretamente: http://localhost:8001/bots/
3. Clicar em "+ Criar Bot"
4. Preencher formulário:
   ```
   Nome do Bot: Meu Bot Scalper
   Corretora: Binance
   Criptomoedas (uma por linha):
     BTCUSDT
     ETHUSDT
     SOLUSDT
   Capital (USDT): 500
   Estratégia: Mean Reversion
   Timeframe: 15m
   Stop Loss (%): 1.5
   Take Profit (%): 3.0
   ```
5. Clicar em "Criar Bot"
6. ✅ Bot criado!
7. **Popup aparece:** "Bot criado! Deseja abrir Dashboard Completo?"
8. Clicar em "OK"
9. ✅ Dashboard Streamlit abre em nova aba!

---

### **Passo 5: Iniciar Bot**

1. Na lista de bots, encontrar "Meu Bot Scalper"
2. Status: 🔴 Parado
3. Clicar em "▶️ Iniciar"
4. Status muda para: 🟢 Ativo
5. ✅ Bot começou a operar!

---

### **Passo 6: Monitorar no Dashboard Streamlit**

1. Já está aberto de: http://localhost:8501/
2. OU clicar em "📈 Dashboard Completo" em qualquer página
3. Ver:
   ```
   ✅ Gráficos de candlestick
   ✅ Bollinger Bands
   ✅ Rankings de criptos
   ✅ Feed de atividades:
      "🟢 Comprando BTCUSDT a $42,500"
      "🔴 Vendendo ETHUSDT a $2,250 (+$7.50)"
   ✅ Portfolio atualizado
   ```
4. Ajustar configurações se necessário:
   ```
   - Frequência de atualização
   - Moeda de exibição
   - Perfil de trader
   ```
5. ✅ Monitoramento em tempo real!

---

### **Passo 7: Ver Histórico de Trades**

1. No Django: http://localhost:8001/trades/
2. Ver:
   ```
   ✅ Total de trades: 47
   ✅ Abertos: 3
   ✅ Fechados: 44
   ✅ Lucro total: +$127.50
   ✅ Taxa de sucesso: 68.2%
   ```
3. Filtrar por status ou lado
4. Ver tabela detalhada
5. ✅ Análise completa!

---

## 🎯 **WORKFLOW DIÁRIO:**

### **Manhã:**
```
1. Abrir Django: http://localhost:8001/dashboard/
2. Ver estatísticas rápidas
3. Verificar se bots estão ativos
4. Clicar em "📈 Dashboard Completo"
5. No Streamlit, ver rankings do dia
6. Ajustar estratégia se necessário
```

### **Durante o Dia:**
```
1. Manter Streamlit aberto (http://localhost:8501/)
2. Monitorar feed de atividades
3. Ver gráficos atualizando
4. Acompanhar lucros/prejuízos
```

### **Noite:**
```
1. Abrir Django: http://localhost:8001/trades/
2. Ver resumo do dia
3. Analisar performance
4. Ajustar bots se necessário
5. Parar bots ou deixar rodando 24/7
```

---

## 📊 **MATRIZ DE FUNCIONALIDADES:**

| Funcionalidade | Django | Streamlit |
|----------------|--------|-----------|
| Criar conta | ✅ | ❌ |
| Login | ✅ | ❌ |
| Adicionar API Keys | ✅ | ❌ |
| Criar bots | ✅ | ❌ |
| Iniciar/Parar bots | ✅ | ✅ |
| Ver lista de bots | ✅ | ❌ |
| Gráficos candlestick | ❌ | ✅ |
| Bollinger Bands | ❌ | ✅ |
| Rankings | ❌ | ✅ |
| Feed ao vivo | ❌ | ✅ |
| Histórico trades | ✅ | ✅ |
| Estatísticas | ✅ | ✅ |
| Multi-moeda | ❌ | ✅ |
| Perfis trader | ❌ | ✅ |

**Os dois se complementam perfeitamente! 🎯**

---

## 🔗 **LINKS RÁPIDOS:**

### **Django (Gerenciamento):**
```
Landing:     http://localhost:8001/
Cadastro:    http://localhost:8001/register/
Login:       http://localhost:8001/login/
Dashboard:   http://localhost:8001/dashboard/
API Keys:    http://localhost:8001/api-keys/
Bots:        http://localhost:8001/bots/
Trades:      http://localhost:8001/trades/
Admin:       http://localhost:8001/admin/
```

### **Streamlit (Visualização):**
```
Dashboard:   http://localhost:8501/
```

---

## 💡 **DICAS:**

### **1. Mantenha ambos abertos:**
```
Aba 1: Django (gerenciamento)
Aba 2: Streamlit (monitoramento)
```

### **2. Use Django para configurar:**
```
- Criar/deletar bots
- Adicionar/remover API Keys
- Ver histórico detalhado
```

### **3. Use Streamlit para monitorar:**
```
- Ver gráficos em tempo real
- Acompanhar feed de atividades
- Analisar tendências
- Rankings de criptos
```

### **4. Integração perfeita:**
```
- Todos os botões no Django levam ao Streamlit
- Após criar bot, popup sugere abrir dashboard
- Experiência fluida entre os sistemas
```

---

## 🎉 **SISTEMA COMPLETO E INTEGRADO!**

```
╔══════════════════════════════════════════╗
║                                          ║
║  🌐 Django + 📊 Streamlit                ║
║                                          ║
║  ✅ 2 sistemas trabalhando juntos       ║
║  ✅ Botões de integração em toda parte  ║
║  ✅ Popup após criar bot                ║
║  ✅ Links estratégicos                  ║
║  ✅ Experiência fluida                  ║
║                                          ║
║  🚀 PRONTO PARA USAR!                   ║
║                                          ║
╚══════════════════════════════════════════╝
```

---

**Agora teste criando um bot e veja a integração funcionando! ✅🚀**
