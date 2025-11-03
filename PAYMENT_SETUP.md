# 💳 Guia de Configuração de Pagamentos - RoboTrader

## 📋 Resumo

O sistema de pagamentos está integrado com o **Stripe** para processar assinaturas mensais dos planos **Pro ($29/mês)** e **Premium ($99/mês)**.

## 🚀 Como Funciona

### 1. **Fluxo do Usuário**

1. **Escolher Plano:** Usuário escolhe um plano na landing page (Free, Pro ou Premium)
2. **Registro:** Preenche formulário com email, CPF, senha
3. **Pagamento (apenas planos pagos):**
   - Free: vai direto para o dashboard
   - Pro/Premium: é redirecionado para página de pagamento do Stripe
4. **Confirmação:** Após pagamento, volta para `/payment/success/` e o plano é ativado automaticamente via webhook

### 2. **Fluxo Técnico**

```
Registro → API `/api/auth/register/` → Criar usuário com plano
                                      ↓
                    Plano Pago? → `/api/payment/create-checkout/` → Stripe Checkout
                                      ↓
                    Pagamento OK → Webhook `/api/payment/webhook/` → Ativar plano
                                      ↓
                                   `/payment/success/` → Dashboard
```

## 🔧 Configuração do Stripe

### Passo 1: Criar conta no Stripe

1. Acesse: https://dashboard.stripe.com/register
2. Crie uma conta (pode começar em modo test)

### Passo 2: Obter chaves API

1. No painel do Stripe, vá em **Developers → API Keys**
2. Copie:
   - **Publishable key** (pk_test_... ou pk_live_...)
   - **Secret key** (sk_test_... ou sk_live_...)

### Passo 3: Criar produtos no Stripe

1. Vá em **Products** → **Add Product**
2. Crie dois produtos:
   
   **Produto 1: RoboTrader Pro**
   - Nome: RoboTrader Pro
   - Descrição: Plano Pro mensal
   - Preço: $29.00 USD
   - Tipo: Recurring (mensal)
   - Copie o **Price ID** (price_xxx...)

   **Produto 2: RoboTrader Premium**
   - Nome: RoboTrader Premium
   - Descrição: Plano Premium mensal
   - Preço: $99.00 USD
   - Tipo: Recurring (mensal)
   - Copie o **Price ID** (price_xxx...)

### Passo 4: Configurar Webhook

1. No Stripe, vá em **Developers → Webhooks**
2. Clique em **Add Endpoint**
3. URL do endpoint: `https://seu-dominio.com/api/payment/webhook/`
   - Para testes locais, use **Stripe CLI** (veja abaixo)
4. Eventos para escutar:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
5. Copie o **Webhook Secret** (whsec_...)

### Passo 5: Configurar variáveis de ambiente

Adicione ao seu `.env`:

```env
# Stripe (Pagamentos)
STRIPE_PUBLIC_KEY=pk_test_seu_publico_key_aqui
STRIPE_SECRET_KEY=sk_test_seu_secret_key_aqui
STRIPE_WEBHOOK_SECRET=whsec_seu_webhook_secret_aqui

# URL do site (para redirects)
SITE_URL=http://localhost:8001
```

**Para produção:**
```env
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
SITE_URL=https://robotrader.com
```

### Passo 6: Atualizar Price IDs (opcional)

Se você quiser usar os Price IDs do Stripe ao invés dos valores hardcoded, edite `saas/views_payment.py`:

```python
price_ids = {
    'pro': 'price_1ABC123...',  # Cole seu Price ID aqui
    'premium': 'price_1DEF456...'  # Cole seu Price ID aqui
}
```

## 🧪 Testar Localmente

### 1. Instalar Stripe CLI

Windows:
```bash
scoop install stripe
```

Ou baixe em: https://github.com/stripe/stripe-cli/releases

### 2. Login no Stripe

```bash
stripe login
```

### 3. Encaminhar webhooks para localhost

```bash
stripe listen --forward-to http://localhost:8001/api/payment/webhook/
```

Isso irá gerar um webhook secret temporário. Copie-o e use no `.env`:
```
whsec_xxx
```

### 4. Testar pagamento

1. Inicie o servidor Django:
```bash
cd I:\Robo\saas
python manage.py runserver 8001
```

2. Acesse: http://localhost:8001
3. Escolha plano Pro ou Premium
4. Cadastre-se
5. Use cartão de teste do Stripe:
   - Número: `4242 4242 4242 4242`
   - Data: qualquer data futura
   - CVC: qualquer 3 dígitos

## 🔒 Cartões de Teste (Stripe)

| Cenário | Número do Cartão |
|---------|------------------|
| Sucesso | 4242 4242 4242 4242 |
| Falha | 4000 0000 0000 0002 |
| Requer autenticação | 4000 0027 6000 3184 |

Data de validade: qualquer data futura
CVC: qualquer 3 dígitos

## 📊 Acompanhamento

### Logs de Pagamento

Os logs aparecem no terminal quando:
- ✅ Pagamento confirmado
- ⚠️ Assinatura cancelada
- ❌ Falha no pagamento

### Verificar no Admin

1. Acesse: http://localhost:8001/admin/
2. Vá em **User Profiles**
3. Veja:
   - Plano atual do usuário
   - `stripe_customer_id`
   - `trial_ends_at`

## 🔄 Fluxo de Cancelamento

Quando um usuário cancela a assinatura no Stripe:
1. Webhook recebe evento `customer.subscription.deleted`
2. Sistema faz downgrade para plano Free
3. Usuário ganha 7 dias de trial gratuito
4. Após 7 dias, conta é pausada (já implementado no `is_trial_expired()`)

## 💰 Valores dos Planos

| Plano | Preço | Corretoras | Criptos por Bot | Bots |
|-------|-------|------------|-----------------|------|
| Free | Grátis (7 dias) | 1 (Binance) | 1 | 1 |
| Pro | $29/mês | 2 | 5 | 3 |
| Premium | $99/mês | Ilimitado | 10 | Ilimitado |

## 🚨 Importante

1. **Sempre use modo test durante desenvolvimento**
2. **Nunca commite as chaves secretas no Git**
3. **Configure SSL (HTTPS) em produção para webhooks**
4. **Teste webhooks localmente com Stripe CLI antes de deploy**

## 📚 Recursos Úteis

- [Documentação Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [Webhooks do Stripe](https://stripe.com/docs/webhooks)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)

## ✅ Checklist de Deploy

- [ ] Criar conta Stripe de produção
- [ ] Criar produtos Pro e Premium no Stripe
- [ ] Configurar webhook de produção
- [ ] Atualizar variáveis de ambiente com chaves `pk_live_` e `sk_live_`
- [ ] Configurar SSL/HTTPS no servidor
- [ ] Testar fluxo completo de pagamento
- [ ] Configurar notificações por email (opcional)
- [ ] Implementar página de gerenciamento de assinatura (opcional)

---

**Dúvidas?** Consulte a documentação do Stripe ou entre em contato com o suporte.

