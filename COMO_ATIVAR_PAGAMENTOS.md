# 💳 Como Ativar Pagamentos - Guia Visual

## ⚠️ MENSAGEM DE ERRO QUE VOCÊ VIU:

```
"Erro ao processar pagamento. Indo para dashboard..."
```

**Por quê?** As chaves do Stripe não estão configuradas ainda.

---

## 🎯 SOLUÇÃO EM 3 PASSOS

### ✅ Passo 1: Criar Conta no Stripe

**SIM, você precisa criar uma conta!**

1. Acesse: **https://dashboard.stripe.com/register**
2. Preencha seus dados
3. ✅ Conta criada! (modo test ativo automaticamente)

---

### ✅ Passo 2: Copiar Suas Chaves

1. No painel do Stripe, vá em: **Developers** → **API Keys**
2. Você verá algo assim:

```
📌 Test mode

Publishable key    pk_test_51NxXxXxXxXxXxXxXx...    [Reveal test key]
Secret key         sk_test_51NxXxXxXxXxXxXxXxXx...    [Reveal test key]
```

3. Clique em **"Reveal test key"** em ambas
4. **Copie as duas chaves**

---

### ✅ Passo 3: Adicionar no Projeto

#### 📁 Opção A: Arquivo .env (Recomendado)

1. Crie um arquivo chamado `.env` na pasta `I:\Robo\`
2. Cole este conteúdo e **substitua pelas suas chaves**:

```env
# Stripe
STRIPE_PUBLIC_KEY=pk_test_cole_sua_chave_aqui
STRIPE_SECRET_KEY=sk_test_cole_sua_chave_aqui
STRIPE_WEBHOOK_SECRET=
SITE_URL=http://localhost:8001
```

**Exemplo real:**
```env
STRIPE_PUBLIC_KEY=pk_test_51NxABC123xyz...
STRIPE_SECRET_KEY=sk_test_51NxDEF456abc...
STRIPE_WEBHOOK_SECRET=
SITE_URL=http://localhost:8001
```

#### 📁 Opção B: Variáveis de Ambiente do Windows

1. Abra PowerShell como Admin
2. Execute:

```powershell
[System.Environment]::SetEnvironmentVariable('STRIPE_PUBLIC_KEY', 'pk_test_sua_chave', 'User')
[System.Environment]::SetEnvironmentVariable('STRIPE_SECRET_KEY', 'sk_test_sua_chave', 'User')
```

3. Reinicie o PowerShell

---

### ✅ Passo 4: Reiniciar Servidor

**IMPORTANTE:** O servidor precisa reiniciar para carregar as novas variáveis!

```bash
# Pare o servidor (Ctrl+C)
# Reinicie:
cd I:\Robo\saas
python manage.py runserver 8001
```

---

## 🧪 Testar Agora!

1. ✅ Acesse: http://localhost:8001
2. ✅ Clique em **"Plano Pro"** ou **"Premium"**
3. ✅ Cadastre-se normalmente
4. ✅ **Você será redirecionado para o Stripe!**
5. ✅ Use cartão teste: `4242 4242 4242 4242`
6. ✅ Data: `12/25` (qualquer data futura)
7. ✅ CVC: `123` (qualquer)
8. ✅ Clique em **Pay**
9. ✅ Voltará para `/payment/success/`
10. ✅ Seu plano estará ativo!

---

## 🎨 Fluxo Visual

```
┌─────────────────────┐
│   Landing Page      │
│   Escolher Plano    │ ✅ Free, Pro ou Premium
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Página Cadastro   │
│   Preencher Dados   │ ✅ Nome, Email, CPF, Senha
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Plano Free?  │
    └───┬──────┬───┘
        │      │
       Sim    Não (Pro/Premium)
        │      │
        │      ▼
        │  ┌─────────────────────┐
        │  │   Stripe Checkout   │ 🔐 Pagamento Seguro
        │  │   Pagar com Cartão  │
        │  └──────────┬──────────┘
        │             │
        │             ▼
        │  ┌─────────────────────┐
        │  │  Payment Success    │ ✅ Confirmação
        │  └──────────┬──────────┘
        │             │
        ▼             ▼
┌─────────────────────────┐
│      Dashboard          │ 🎉 Plano Ativo!
│   - API Keys            │
│   - Bots                │
│   - Trades              │
└─────────────────────────┘
```

---

## ❓ Perguntas Frequentes

### **1. Preciso MESMO criar conta no Stripe?**
✅ **Sim!** O Stripe é quem processa os pagamentos. É como o Mercado Pago ou PayPal, mas mais usado no mundo.

### **2. É grátis?**
✅ **Sim!** Criar conta é grátis. Você paga apenas uma pequena % quando **receber** um pagamento.

### **3. Preciso adicionar conta bancária agora?**
❌ **Não!** Para testes, use modo test (pk_test_). Só precisa de conta bancária quando for receber pagamentos reais.

### **4. O cartão 4242... é real?**
❌ **Não!** É um cartão de **teste** do Stripe. Funciona apenas em modo test. Nenhuma cobrança real é feita.

### **5. E se eu não configurar agora?**
✅ **Tudo bem!** Usuários podem se cadastrar no **plano Free** normalmente. Quando tentarem planos pagos, verão: "Pagamentos em configuração. Use plano Free por enquanto."

### **6. Quanto cobra o Stripe?**
💰 **2.9% + R$ 0.30** por transação (padrão internacional)

---

## 🚨 Problemas Comuns

### ❌ Ainda vejo "Erro ao processar pagamento"

**Checklist:**
- [ ] Criei conta no Stripe?
- [ ] Copiei as chaves **test** (pk_test_ e sk_test_)?
- [ ] Colei no arquivo `.env` ou variáveis de ambiente?
- [ ] **Reiniciei o servidor** depois de adicionar?

### ❌ As chaves não funcionam

- Use chaves **test** (não live) durante desenvolvimento
- Verifique se copiou a chave completa (não cortou no meio)
- Certifique-se de que não há espaços em branco

### ❌ Webhook não funciona

- Para testes locais, **deixe vazio** por enquanto
- Funciona automaticamente em produção

---

## 📞 Precisa de Ajuda?

1. **Guia Rápido:** Leia `STRIPE_QUICK_START.md`
2. **Guia Completo:** Leia `PAYMENT_SETUP.md`
3. **Suporte Stripe:** https://support.stripe.com

---

## ✅ Checklist Final

Antes de testar pagamento, confirme:

- [ ] Conta no Stripe criada
- [ ] Chaves copiadas (pk_test_ e sk_test_)
- [ ] Chaves adicionadas no `.env` ou variáveis de ambiente
- [ ] Servidor Django reiniciado
- [ ] Tentou cadastrar com plano Pro/Premium
- [ ] Foi redirecionado para Stripe
- [ ] Testou com cartão 4242 4242 4242 4242

---

**🎉 Com essas 3 configurações simples, pagamentos funcionarão perfeitamente!**

Tempo total: **5 minutos** ⏱️

