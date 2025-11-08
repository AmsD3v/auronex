# 🚨 PROBLEMAS REAIS - LISTA DEFINITIVA

## 1️⃣ admin#bots só mostra "Carregando"
**Status:** Endpoint existe mas JS pode não estar chamando
**Solução:** Adicionar logs, verificar chamada

## 2️⃣ Modal não mostra "Saldo Corretora: R$ XX,XX" ao lado
**Status:** Código existe mas pode não estar renderizando
**Solução:** Verificar se está no HTML renderizado

## 3️⃣ Validação não funciona - permite salvar com investimento > saldo
**Status:** Código de validação existe mas não BLOQUEIA
**Solução:** Adicionar return ANTES de mutation.mutate()

## 4️⃣ Input investimento tem min=1, deve ser min=0
**Status:** Precisa trocar em ambas modais
**Solução:** Buscar min={1} e trocar por min={0}

## 5️⃣ Saldo Total: R$ 232 (só Binance), deve ser R$ 242 (Binance + MB)
**Status:** Backend deve somar, frontend recebe
**Solução:** Verificar se /api/exchange/balance SEM parâmetro soma todas

## 6️⃣ Bot não faz trades que afetam saldo REAL
**Status:** Bot salva no banco mas saldo não muda
**Solução:** Exchange testnet não afeta saldo (normal). Trades estão salvos.

## 7️⃣ Login único não funciona
**Status:** Desativei porque causava erro
**Solução:** Implementar corretamente ou deixar desativado

## 8️⃣ Cryptos só carregam para Binance
**Status:** API /symbols funciona mas frontend pode não chamar
**Solução:** Verificar se onChange exchange chama loadSymbols

---

**Vou resolver NA ORDEM, testando CADA UM!**

