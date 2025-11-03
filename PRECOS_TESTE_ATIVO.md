# ⚠️ VALORES DE TESTE ATIVOS!

## 🧪 Status Atual: MODO TESTE

Você alterou os valores para testar pagamentos:

| Plano | Valor TESTE | Valor REAL (Original) |
|-------|-------------|------------------------|
| Pro | **R$2.00/mês** | R$145/mês (~$29) |
| Premium | **R$5.00/mês** | R$490/mês (~$99) |

---

## ✅ ONDE FORAM ALTERADOS:

### 1. Backend (Pagamentos)
**Arquivo:** `saas/views_payment.py`
```python
# Linha 45-49
prices = {
    'pro': 50,  # $0.50 (TESTE)
    'premium': 100  # $1.00 (TESTE)
}
```

### 2. Landing Page
**Arquivo:** `saas/templates/landing.html`
- Linha 241: `$0.50/mês` (era $29)
- Linha 258: `$1.00/mês` (era $99)

### 3. Página de Registro
**Arquivo:** `saas/templates/register.html`
- Linha 211: `Pro - $0.50/mês 🧪`
- Linha 216: `Premium - $1.00/mês 🧪`

---

## 🔄 COMO VOLTAR PARA PREÇOS REAIS

### Quando terminar os testes, siga estes passos:

#### 1️⃣ **Backend - `saas/views_payment.py`**
```python
# MUDAR DE:
prices = {
    'pro': 200,  # R$2.00 (TESTE)
    'premium': 500  # R$5.00 (TESTE)
}
currency: 'brl'

# PARA:
prices = {
    'pro': 14500,  # R$145.00
    'premium': 49000  # R$490.00
}
currency: 'brl'
```

#### 2️⃣ **Landing Page - `saas/templates/landing.html`**
```html
<!-- MUDAR DE: -->
<div class="price">R$2<small>/mês</small></div>
<p>🧪 TESTE - Mais popular</p>

<!-- PARA: -->
<div class="price">R$145<small>/mês</small></div>
<p>Mais popular</p>

<!-- E também: -->
<div class="price">R$5<small>/mês</small></div>
<p>🧪 TESTE - Para profissionais</p>

<!-- PARA: -->
<div class="price">R$490<small>/mês</small></div>
<p>Para profissionais</p>
```

#### 3️⃣ **Registro - `saas/templates/register.html`**
```javascript
// MUDAR DE:
'pro': {
    name: 'Pro - R$2/mês 🧪',
    details: '🧪 VALOR DE TESTE - Renovação automática mensal...',
    color: '#667eea'
},
'premium': {
    name: 'Premium - R$5/mês 🧪',
    details: '🧪 VALOR DE TESTE - Renovação automática mensal...',
    color: '#764ba2'
}

// PARA:
'pro': {
    name: 'Pro - R$145/mês',
    details: 'Renovação automática mensal. Cancele quando quiser.',
    color: '#667eea'
},
'premium': {
    name: 'Premium - R$490/mês',
    details: 'Renovação automática mensal. Todos os recursos inclusos.',
    color: '#764ba2'
}
```

---

## 🧪 TESTANDO AGORA:

```bash
✅ 1. Servidor recarregou automaticamente
✅ 2. Acesse: http://localhost:8001
✅ 3. Veja novos preços: Pro R$2 | Premium R$5
✅ 4. Escolha um plano e cadastre-se
✅ 5. Será redirecionado para Stripe
✅ 6. Pague apenas R$2 ou R$5 💰
✅ 7. Teste completo!
```

---

## ⚠️ IMPORTANTE:

### **NÃO ESQUEÇA de voltar aos preços reais antes de lançar!**

- ❌ **Não lance em produção com preços de teste**
- ❌ Clientes pagarão apenas $0.50 ao invés de $29
- ❌ Você perderá muito dinheiro!

### **Checklist antes do lançamento:**

- [ ] Voltei preços em `views_payment.py`
- [ ] Voltei preços em `landing.html`
- [ ] Voltei preços em `register.html`
- [ ] Testei que Stripe mostra $29 e $99
- [ ] Removi emojis 🧪 de TESTE
- [ ] Webhook configurado
- [ ] SSL/HTTPS ativo

---

## 📊 HISTÓRICO DE TRANSAÇÕES DE TESTE:

Todas as transações feitas com estes valores de teste ficam registradas no Stripe.

**Acesse:** https://dashboard.stripe.com/payments

Você verá:
- Pagamentos de R$2.00 (Pro)
- Pagamentos de R$5.00 (Premium)

**Isso é normal durante testes!**

---

## 💡 DICA:

Se quiser testar sem pagar nada:

1. Use chaves **TEST** do Stripe (pk_test_ e sk_test_)
2. Use cartão: `4242 4242 4242 4242`
3. Nenhuma cobrança real acontece
4. Depois volte para chaves LIVE

---

**📅 Data da alteração:** 28 de Outubro de 2025  
**🎯 Motivo:** Facilitar testes de pagamento  
**⏰ Lembrar:** Voltar aos preços reais antes do lançamento!

