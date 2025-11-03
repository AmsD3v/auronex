# 🚀 Configuração Rápida do Stripe (5 minutos)

## ✅ SIM, você precisa criar uma conta no Stripe!

O Stripe é o processador de pagamentos. Ele cuida de:
- ✅ Aceitar cartões de crédito
- ✅ Cobranças mensais automáticas
- ✅ Segurança PCI (você não precisa armazenar dados de cartão)
- ✅ Anti-fraude

## 📋 Passo a Passo Rápido

### 1️⃣ Criar Conta no Stripe (2 min)

1. Acesse: **https://dashboard.stripe.com/register**
2. Preencha:
   - Email
   - Nome completo
   - País: Brasil
   - Senha
3. Clique em **Create account**
4. ✅ Pronto! Você terá acesso ao painel

**⚠️ IMPORTANTE:** Comece em **modo test** (não precisa adicionar dados bancários agora)

---

### 2️⃣ Copiar Chaves da API (1 min)

1. No painel do Stripe, procure por **"Developers"** no menu lateral
2. Clique em **API Keys**
3. Você verá:
   
   ```
   Publishable key:  pk_test_xxxxxxxxxxxxx  [Reveal test key]
   Secret key:       sk_test_xxxxxxxxxxxxx  [Reveal test key]
   ```

4. Clique em **"Reveal test key"** em ambas
5. **Copie as duas chaves**

---

### 3️⃣ Adicionar no seu Projeto (1 min)

1. Abra o arquivo `.env` (se não existir, crie na raiz do projeto `I:\Robo\.env`)

2. Adicione essas linhas:

```env
# Stripe - Modo Test
STRIPE_PUBLIC_KEY=pk_test_cole_sua_chave_aqui
STRIPE_SECRET_KEY=sk_test_cole_sua_chave_aqui
STRIPE_WEBHOOK_SECRET=whsec_deixe_vazio_por_enquanto
SITE_URL=http://localhost:8001
```

**Exemplo real:**
```env
STRIPE_PUBLIC_KEY=pk_test_51ABcDefGhIjKlMnOpQrStUvWx
STRIPE_SECRET_KEY=sk_test_51ABcDefGhIjKlMnOpQrStUvWx
STRIPE_WEBHOOK_SECRET=
SITE_URL=http://localhost:8001
```

---

### 4️⃣ Reiniciar Servidor (1 min)

1. Pare o servidor Django (Ctrl+C no terminal)
2. Reinicie:

```bash
cd I:\Robo\saas
python manage.py runserver 8001
```

---

### 5️⃣ Testar! (5 segundos)

1. Acesse: http://localhost:8001
2. Escolha **Plano Pro** ou **Premium**
3. Cadastre-se
4. **Agora você será redirecionado para o Stripe!**
5. Use cartão de teste:
   - Número: `4242 4242 4242 4242`
   - Data: qualquer data futura (ex: 12/25)
   - CVC: `123`
   - CEP: `12345`

---

## 🧪 Cartões de Teste

| Cenário | Número |
|---------|--------|
| ✅ Sucesso | 4242 4242 4242 4242 |
| ❌ Falha | 4000 0000 0000 0002 |
| 🔐 Requer autenticação | 4000 0027 6000 3184 |

**Dica:** Use sempre data futura e qualquer CVC (3 dígitos)

---

## 🎯 Pronto para Produção?

Quando quiser aceitar pagamentos **reais** (não teste):

1. No painel do Stripe, clique em **"Activate your account"**
2. Preencha dados da empresa/pessoa física
3. Adicione conta bancária para receber os pagamentos
4. Troque as chaves test por **chaves live**:

```env
STRIPE_PUBLIC_KEY=pk_live_xxxxx  # Live key (não mais test)
STRIPE_SECRET_KEY=sk_live_xxxxx  # Live key (não mais test)
```

---

## ❓ FAQ

### **Por que Stripe e não outro processador?**
- Mais usado no mundo (Shopify, Uber, Amazon usam)
- Fácil de integrar
- Aceita cartões internacionais
- Taxa justa: 2.9% + R$ 0.30 por transação

### **Preciso pagar para usar Stripe?**
- ❌ Não! É grátis criar conta
- ✅ Você paga apenas uma % quando **receber pagamentos**
- Modo test é 100% grátis, sem limites

### **Posso usar no Brasil?**
- ✅ Sim! Stripe funciona no Brasil
- Receba em reais ou dólares
- Pagamentos internacionais aceitos

### **Meus clientes precisam ter conta Stripe?**
- ❌ Não! Eles só precisam de um cartão de crédito
- É como qualquer compra online

### **E se eu não configurar agora?**
- Usuários podem se cadastrar normalmente no plano **Free**
- Quando tentarem planos pagos, verão: "Pagamentos em configuração"
- Você pode configurar depois sem problemas

---

## 🔧 Problemas Comuns

### ❌ "Erro ao processar pagamento"
**Solução:** Verifique se copiou as chaves corretas no `.env` e reiniciou o servidor

### ❌ Chaves não funcionam
**Solução:** Use chaves **test** (pk_test_ e sk_test_) durante desenvolvimento

### ❌ Webhook não funciona localmente
**Solução:** Para testes locais, deixe `STRIPE_WEBHOOK_SECRET` vazio. Webhooks funcionarão em produção automaticamente.

---

## 📞 Precisa de Ajuda?

- **Documentação Stripe:** https://stripe.com/docs
- **Suporte Stripe:** https://support.stripe.com
- **Painel Stripe:** https://dashboard.stripe.com

---

## ✅ Checklist

- [ ] Criar conta no Stripe
- [ ] Copiar chaves da API (pk_test_ e sk_test_)
- [ ] Adicionar chaves no `.env`
- [ ] Reiniciar servidor Django
- [ ] Testar com cartão 4242 4242 4242 4242
- [ ] Verificar se pagamento funciona

---

**🎉 Pronto! Em 5 minutos você tem pagamentos funcionando!**

Qualquer dúvida, consulte o guia completo em `PAYMENT_SETUP.md`

