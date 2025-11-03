# 🚀 TESTAR PAGAMENTO AGORA - Guia Prático

## ✅ STATUS: SISTEMA PRONTO!

```
✅ Chaves Stripe LIVE configuradas
✅ Sistema pronto para pagamentos REAIS
✅ Chaves protegidas no .gitignore
⚠️ Webhook ainda não configurado (planos serão ativados manualmente)
```

---

## 🧪 COMO TESTAR (3 Opções)

### 🎯 **Opção 1: Teste com Cartão Real (Recomendado)**

**Você vai pagar de verdade, mas pode cancelar depois**

1. **Reinicie o servidor:**
   ```bash
   # Pare o servidor (Ctrl+C)
   cd I:\Robo\saas
   python manage.py runserver 8001
   ```

2. **Acesse o site:**
   ```
   http://localhost:8001
   ```

3. **Escolha plano Pro ou Premium**
   - Clique em "Escolher Pro" ($29/mês)
   - Ou "Escolher Premium" ($99/mês)

4. **Cadastre-se:**
   - Nome, email, CPF, senha
   - Clique em "Criar Conta"

5. **Será redirecionado para Stripe:**
   - ✅ Use seu cartão REAL
   - ✅ Preencha dados completos
   - ✅ Clique em "Pay"

6. **Pagamento processado:**
   - ✅ Você volta para `/payment/success/`
   - ✅ Vai para o dashboard
   - ⚠️ Plano NÃO ativa automaticamente (webhook não configurado)

7. **Ativar plano manualmente:**
   - Acesse: http://localhost:8001/admin/
   - Login: seu email de admin
   - Vá em: **User Profiles**
   - Encontre o usuário criado
   - Edite: mude `plan` para `premium` ou `pro`
   - Salve

8. **Cancelar assinatura (se foi só teste):**
   - Acesse: https://dashboard.stripe.com/subscriptions
   - Encontre a assinatura
   - Clique: **Cancel subscription**

---

### 🛡️ **Opção 2: Teste com Chaves Test (Mais Seguro)**

**Se não quiser arriscar pagamento real ainda:**

1. **Edite `saas/env_settings.py`:**
   ```python
   # Trocar LIVE por TEST temporariamente
   os.environ.setdefault('STRIPE_PUBLIC_KEY', 'pk_test_sua_chave_test')
   os.environ.setdefault('STRIPE_SECRET_KEY', 'sk_test_sua_chave_test')
   ```

2. **Obter chaves test:**
   - Acesse: https://dashboard.stripe.com/test/apikeys
   - Copie: `pk_test_...` e `sk_test_...`

3. **Reinicie servidor e teste:**
   - Use cartão: `4242 4242 4242 4242`
   - Nenhum pagamento real será feito

4. **Quando quiser LIVE de novo:**
   - Restaure as chaves `pk_live_` e `sk_live_`

---

### 👀 **Opção 3: Apenas Verificar (Sem Pagar)**

**Ver se o fluxo funciona até a página do Stripe:**

1. **Reinicie servidor:**
   ```bash
   cd I:\Robo\saas
   python manage.py runserver 8001
   ```

2. **Acesse:**
   ```
   http://localhost:8001
   ```

3. **Escolha plano pago e cadastre-se**

4. **Quando chegar na página do Stripe:**
   - ✅ Veja os dados: "RoboTrader Pro - $29.00/month"
   - ✅ Confirme que está correto
   - ❌ **Clique em "← Back" (não pague)**

5. **Você será redirecionado para `/payment/cancel/`**

---

## 📊 MONITORAR NO PAINEL STRIPE

Após processar pagamento real:

1. **Acesse:** https://dashboard.stripe.com/payments
2. **Veja:**
   - Pagamento listado
   - Valor correto ($29 ou $99)
   - Cliente criado
   - Assinatura ativa

---

## 🔧 CONFIGURAR WEBHOOK (Ativar Automaticamente)

**IMPORTANTE:** Sem webhook, você precisa ativar planos manualmente!

### Para Produção (quando subir no ar):

1. **Acesse:** https://dashboard.stripe.com/webhooks
2. **Add endpoint:**
   - URL: `https://seu-dominio.com/api/payment/webhook/`
   - Eventos:
     - `checkout.session.completed`
     - `customer.subscription.deleted`
     - `invoice.payment_failed`
3. **Copie Webhook Secret** (whsec_...)
4. **Adicione em `saas/env_settings.py`:**
   ```python
   os.environ.setdefault('STRIPE_WEBHOOK_SECRET', 'whsec_...')
   ```

### Para Testes Locais:

1. **Instalar Stripe CLI:**
   - Windows: `scoop install stripe`
   - Ou: https://github.com/stripe/stripe-cli/releases

2. **Login:**
   ```bash
   stripe login
   ```

3. **Encaminhar webhooks:**
   ```bash
   stripe listen --forward-to http://localhost:8001/api/payment/webhook/
   ```

4. **Copiar whsec_xxx** que aparece e adicionar em `env_settings.py`

5. **Agora planos ativam automaticamente!** ✅

---

## 🚨 CUIDADOS IMPORTANTES

### ⚠️ Antes de Aceitar Clientes Reais:

- [ ] Testou fluxo completo com seu cartão
- [ ] Verificou que pagamento aparece no Stripe
- [ ] Configurou webhook (para ativação automática)
- [ ] Certificado SSL/HTTPS configurado (segurança)
- [ ] Domínio próprio (não localhost)
- [ ] Termos de serviço publicados
- [ ] Política de privacidade (LGPD)
- [ ] Suporte ao cliente definido

### 💰 Taxas Stripe (Brasil):

```
3.49% + R$ 0.40 por transação

Exemplo:
Cliente paga: R$ 100
Stripe cobra: R$ 3.90
Você recebe: R$ 96.10
```

### 🔄 Assinaturas Mensais:

- ✅ Cobrança automática todo mês
- ✅ Cliente pode cancelar quando quiser
- ✅ Você pode cancelar também
- ⚠️ Reembolsos são permitidos (você perde a taxa do Stripe)

---

## 📞 SUPORTE

### Se algo der errado:

1. **Verifique logs do Django:**
   ```bash
   # Terminal onde roda o servidor
   # Procure por erros em vermelho
   ```

2. **Verifique painel Stripe:**
   - https://dashboard.stripe.com/logs
   - Veja erros de API

3. **Teste modo test:**
   - Use chaves `pk_test_` temporariamente
   - Veja se funciona

4. **Suporte Stripe:**
   - Email: support@stripe.com
   - Chat: https://dashboard.stripe.com

---

## ✅ CHECKLIST DE TESTE

Marque conforme for testando:

### Teste Básico:
- [ ] Servidor reiniciado
- [ ] Landing page carrega (http://localhost:8001)
- [ ] Clicou em plano Pro/Premium
- [ ] Cadastro funciona
- [ ] Redirecionado para Stripe
- [ ] Página Stripe mostra valor correto

### Teste de Pagamento:
- [ ] Inseriu cartão real
- [ ] Pagamento processado
- [ ] Voltou para /payment/success/
- [ ] Pagamento aparece em https://dashboard.stripe.com/payments
- [ ] Cliente criado no Stripe
- [ ] Assinatura ativa no Stripe

### Teste de Ativação:
- [ ] Plano ativo no admin Django
- [ ] Usuário consegue criar bots
- [ ] Usuário consegue adicionar API keys
- [ ] Limites do plano funcionam

---

## 🎉 TUDO CERTO!

Se todos os testes passarem, seu sistema está **100% funcional** e pronto para receber clientes pagantes!

**Próximo passo:**
1. Configurar webhook (essencial)
2. Subir em produção (HTTPS + domínio)
3. Divulgar! 🚀

---

**Data:** 28 de Outubro de 2025  
**Status:** Sistema LIVE e Operacional  
**Valores:** Pro $29/mês | Premium $99/mês  
**Chaves:** LIVE (Produção - Pagamentos Reais)





