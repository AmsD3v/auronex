# 🎯 PENDÊNCIAS PARA PRÓXIMA SESSÃO

## ✅ O QUE JÁ FUNCIONA (Deploy hoje)
- Dashboard React Enterprise ✅
- Bot Async 3-5x mais rápido ✅
- Conversão BRL/USD ✅
- Top 5 Performance ✅
- Capital Investido ✅
- Log de Atividades ✅
- Validação 1+ cripto ✅
- Input min=0 ✅
- Admin Panel usuários ✅
- Trades salvos no banco (2 trades) ✅

---

## 🚨 PROBLEMAS PENDENTES (Próxima sessão)

### **1. admin#bots não carrega** 🔥 CRÍTICO
- Endpoint existe: /api/admin/bots/all
- JS chama mas não renderiza
- SOLUÇÃO: Verificar showSection('bots') chama loadBots()

### **2. Modal: Saldo Corretora não aparece VISÍVEL** 🔥
- Código existe mas pode não estar no HTML final
- SOLUÇÃO: Verificar se label renderiza: "Investimento (BRL) * | Saldo Corretora: R$ XX"

### **3. Validação não BLOQUEIA salvar** 🔥 CRÍTICO
- Código valida mas não impede mutate()
- SOLUÇÃO: Adicionar return ANTES de updateBotMutation.mutate()

### **4. Saldo Total: só Binance (R$ 232)** 🔥
- Deve somar: Binance + Mercado Bitcoin = R$ 242
- Endpoint: /api/exchange/balance SEM parâmetro
- SOLUÇÃO: Verificar se frontend chama sem exchange param

### **5. Bot trades não afetam saldo REAL** 🔥 CRÍTICO
- Bot salva no banco mas saldo não muda
- Exchange API não recalcula
- SOLUÇÃO: Trade fechado deve atualizar balance no exchange

### **6. Cryptos só para Binance**
- API /symbols funciona para todas
- Frontend pode não chamar ao mudar exchange
- SOLUÇÃO: useEffect([exchange]) → loadSymbols(exchange)

### **7. Login único**
- Middleware existe mas desativei (causava erro)
- SOLUÇÃO: Reimplementar sem causar erro logout

---

## 📝 TESTES NECESSÁRIOS

```
1. Admin → Bots → Deve carregar lista
2. Criar bot → Ver "Saldo Corretora: R$ XX" ao lado
3. Colocar invest > saldo → Clicar salvar → DEVE BLOQUEAR
4. Ver Saldo Total = soma de TODAS exchanges
5. Bot fazer trade → Aguardar 3s → Saldo DEVE mudar
6. Mudar exchange → Cryptos DEVEM carregar
7. Login 2x → 2ª deve invalidar 1ª
```

---

## 🎯 PRIORIDADES PRÓXIMA SESSÃO

**CRÍTICO (fazer primeiro):**
1. Validação BLOQUEAR salvar
2. Saldo Total somar todas
3. Bot trades afetam saldo

**IMPORTANTE:**
4. admin#bots carregar
5. Saldo corretora visível
6. Cryptos todas exchanges

**BAIXA:**
7. Login único

---

**DEPLOY AGORA com o que funciona!**
**Próxima sessão: resolver 7 pendências!**

