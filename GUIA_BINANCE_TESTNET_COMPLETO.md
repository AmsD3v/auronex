# 🧪 GUIA COMPLETO: BINANCE TESTNET

## 🎯 SITUAÇÃO ATUAL

**SISTEMA:**
- ✅ Django funcionando
- ✅ Celery funcionando
- ✅ Redis funcionando
- ✅ 3 bots ativos

**PROBLEMA:**
- ❌ `Invalid Api-Key ID` (API Key antiga de produção)
- ❌ `API Key não encontrada`

**SOLUÇÃO:**
- ✅ Deletar API Keys antigas
- ✅ Adicionar API Keys da Binance TESTNET
- ✅ Solicitar fundos de teste (10.000 USDT grátis!)

---

## 📋 PASSO A PASSO COMPLETO

### ETAPA 1: Deletar API Keys antigas

**1.1 - Acesse:**
```
http://localhost:8001/admin
```

**1.2 - Login** com superusuário

**1.3 - Vá em:**
```
Users > Exchange API Keys
```

**1.4 - DELETE todas as API Keys antigas:**
- Clique em cada uma
- Role até o fim
- Clique em **"Delete"**
- Confirme

**1.5 - Verifique:**
- Tabela deve ficar **vazia** (0 api keys)

---

### ETAPA 2: Criar conta na Binance Testnet

**2.1 - Acesse:**
```
https://testnet.binance.vision/
```

**2.2 - Clique em:** `Register` (canto superior direito)

**2.3 - Preencha:**
- **Email:** Use um email válido (pode ser o mesmo de produção)
- **Password:** Crie uma senha forte
- **Confirm Password:** Repita a senha

**2.4 - Clique em:** `Register`

**2.5 - Verifique o email:**
- Abra seu email
- Procure email da Binance Testnet
- Clique no link de confirmação

**2.6 - Login:**
- Volte para https://testnet.binance.vision/
- Clique em `Login`
- Entre com email e senha

---

### ETAPA 3: Solicitar fundos de teste (GRÁTIS!)

**3.1 - Após login, clique no ícone do seu perfil** (canto superior direito)

**3.2 - Vá em:** `Faucet` ou `Test Funds`

**OU procure no menu por:** `Faucet`

**3.3 - Você verá uma página com opções:**
- BNB Testnet
- USDT Testnet
- BTC Testnet
- ETH Testnet

**3.4 - Clique em:** `Get USDT` ou `Request USDT`

**3.5 - PRONTO!** Você receberá instantaneamente:
- 💰 **10.000 USDT** (testnet)
- 💰 Pode pedir mais BNB, BTC, etc (todos fake para teste)

**3.6 - Verificar saldo:**
- Clique em: `Wallet` (menu superior)
- Vá em: `Spot Wallet`
- **Deve aparecer:**
  ```
  USDT: 10,000.00000000
  ```

**SE APARECER:** ✅ Fundos recebidos!

---

### ETAPA 4: Criar API Key na Binance Testnet

**4.1 - Clique no ícone do perfil** (canto superior direito)

**4.2 - Vá em:** `API Management`

**4.3 - Clique em:** `Create API` ou `Create API Key`

**4.4 - Escolha tipo:**
- Selecione: **System Generated** (mais simples)

**4.5 - Digite o nome:**
- Label: `RoboTrader_Test_2024`

**4.6 - Clique em:** `Create`

**4.7 - Você verá:**
```
✅ API Key: abc123def456ghi789...
✅ Secret Key: xyz987uvw654rst321...
```

**🚨 MUITO IMPORTANTE:**
- **COPIE E SALVE** ambas as chaves **AGORA!**
- Elas **SÓ APARECEM 1 VEZ!**
- Se não copiar, terá que criar nova

**4.8 - Clique no lápis** (Edit) ao lado da API Key criada

**4.9 - Configure permissões:**
- ✅ **Enable Reading** ← Marcar!
- ✅ **Enable Spot & Margin Trading** ← Marcar!
- ❌ **Enable Withdrawals** ← DEIXAR DESMARCADO!
- ❌ **Enable Futures** ← DEIXAR DESMARCADO!

**4.10 - API Access Restrictions:**
- **IP Whitelist:** Deixe em branco (unrestricted)
- OU adicione seu IP: `Meu IP Atual` (botão)

**4.11 - Clique em:** `Save`

---

### ETAPA 5: Adicionar API Key no RoboTrader

**5.1 - Acesse:**
```
http://localhost:8001/api-keys/
```

**5.2 - Login** (se pedir)

**5.3 - Clique em:** `Add API Key` ou `+`

**5.4 - Preencha EXATAMENTE assim:**
- **Exchange:** `binance` (TUDO MINÚSCULO!)
- **API Key:** Cole a API Key copiada da Binance Testnet
- **Secret Key:** Cole o Secret copiado da Binance Testnet
- **is_testnet:** ✅ **MARCAR!** (checkbox marcado)
- **is_active:** ✅ **MARCAR!** (checkbox marcado)

**5.5 - Clique em:** `Save`

**5.6 - Verifique:**
```
✅ API Key salva com sucesso!
✅ is_testnet: True
✅ is_active: True
```

---

### ETAPA 6: Verificar Bot Configuration

**6.1 - Acesse:**
```
http://localhost:8001/admin
```

**6.2 - Vá em:** `Bots` → `Bot Configurations`

**6.3 - Você verá:** `3 bots ativos` (segundo seus logs)

**6.4 - Clique em CADA bot** e verifique:
- **User:** Correto?
- **Exchange:** `binance` (minúsculo!)
- **Symbols:** `["BTCUSDT"]` ou similar (formato JSON array)
- **Capital:** > 0 (ex: 100)
- **is_active:** ✅ MARCADO

**6.5 - Se houver bots duplicados ou errados:**
- Delete os duplicados
- Mantenha apenas 1 bot bem configurado

---

## ⏱️ AGUARDAR PRIMEIRO TRADE

**Após tudo configurado:**

**1. Observe logs do Celery Worker:**

**DEVE MUDAR de:**
```
❌ 'API Key não encontrada'
```

**Para:**
```
✅ 'Bot executado: 0 trades realizados em 1 símbolos'
✅ Analisando BTCUSDT...
✅ Preço atual: $67,234.56
```

**2. Quando tiver oportunidade:**
```
✅ 🟢 COMPRA (1/3): BTCUSDT @ $67,200.00 | Qtd: 0.001487
```

**3. Vá no Dashboard:**
- http://localhost:8501
- **📺 Operações Recentes**
- **Trade aparece!** ✅

**4. Tempo estimado até primeiro trade:**
- Mercado volátil: 5-30 minutos
- Mercado médio: 30min - 2 horas
- Mercado calmo: 2-6 horas

---

## 🆘 TROUBLESHOOTING

### "Não acho o Faucet na Binance Testnet"

**SOLUÇÃO:**

**Opção 1 - Via menu:**
1. Login na testnet
2. Clique no **ícone do perfil** (canto superior direito)
3. Procure: **Faucet** ou **Test Funds**

**Opção 2 - Link direto:**
1. Acesse: https://testnet.binance.vision/en/faucet
2. Ou procure na página inicial por "Faucet"

**Opção 3 - Via Wallet:**
1. Vá em: `Wallet` → `Spot Wallet`
2. Procure botão: `Get Test Funds` ou `Faucet`

---

### "Não consigo criar API Key na Testnet"

**SOLUÇÃO:**

1. Certifique-se de estar em: https://testnet.binance.vision/ (não .com!)
2. Faça login
3. Perfil → API Management
4. Create API Key
5. Se não aparecer, tente outro navegador (Chrome, Firefox)

---

### "API Key continua inválida no sistema"

**VERIFIQUE:**

1. **Exchange está em minúsculo?**
   - ✅ Correto: `binance`
   - ❌ Errado: `Binance` ou `BINANCE`

2. **is_testnet está marcado?**
   - ✅ Deve estar TRUE (checkbox marcado)

3. **API Key e Secret estão corretos?**
   - Copie novamente da Binance
   - Cole no sistema
   - **SEM espaços** antes ou depois

4. **API Key tem permissão de trading?**
   - Vá na Binance Testnet
   - API Management
   - Edite a key
   - ✅ Enable Spot & Margin Trading

---

### "Bot Configuration exchange não bate com API Key"

**EXEMPLO DE PROBLEMA:**
```
Bot Config: exchange = "Binance" (com B maiúsculo)
API Key: exchange = "binance" (minúsculo)
= NÃO BATE! ❌
```

**SOLUÇÃO:**
- Ambos devem ser: `binance` (minúsculo!)

---

## 📊 VERIFICAÇÃO FINAL

**Execute este checklist:**

```
☐ API Keys antigas deletadas?
☐ Nova API Key da Binance TESTNET criada?
☐ Fundos testnet solicitados (10.000 USDT)?
☐ API Key adicionada no sistema?
☐ Exchange = "binance" (minúsculo)?
☐ is_testnet = True (marcado)?
☐ is_active = True (marcado)?
☐ Bot Configuration com exchange = "binance"?
☐ Bot Configuration com is_active = True?
☐ Symbols no formato ["BTCUSDT", "ETHUSDT"]?
```

**Todos marcados: ✅ Vai funcionar!**

---

## 🎯 COMANDOS ÚTEIS

### Criar superusuário (se precisar):
```powershell
cd I:\Robo\saas
.\venv\Scripts\activate
$env:PYTHONPATH="I:\Robo"
python manage.py createsuperuser
```

### Ver logs do Celery em tempo real:
```
Vá na janela "Celery Worker"
Observe as mensagens aparecendo
```

### Reiniciar Celery (se precisar):
```
Feche janelas do Celery (Worker e Beat)
Execute novamente: .\INICIAR_BOT_COMPLETO.bat
```

---

## 🎉 RESUMO

**SISTEMA:** ✅ Funcionando!

**FALTA:**
1. ✅ Deletar API Keys antigas de produção
2. ✅ Adicionar API Key da Binance TESTNET
3. ✅ Solicitar fundos testnet (10.000 USDT)
4. ✅ Configurar permissões corretas

**DEPOIS:**
- ⏱️ Aguardar 5-30 minutos
- 📊 Ver primeiro trade
- 🎉 Bot funcionando!

---

## 🚀 LINKS IMPORTANTES

**Binance Testnet:**
- Home: https://testnet.binance.vision/
- Login: https://testnet.binance.vision/en/login
- Register: https://testnet.binance.vision/en/register
- Faucet: https://testnet.binance.vision/en/faucet
- API Management: https://testnet.binance.vision/en/my/settings/api-management

**Seu Sistema:**
- Dashboard: http://localhost:8501
- Django Admin: http://localhost:8001/admin
- API Keys: http://localhost:8001/api-keys/

---

## 💡 DICA PRO

**Siga EXATAMENTE esta ordem:**

1. ✅ Delete API Keys antigas (Admin ou API Keys page)
2. ✅ Crie conta Binance Testnet
3. ✅ Solicite fundos (Faucet)
4. ✅ Crie API Key na Binance Testnet
5. ✅ **COPIE E SALVE** API Key + Secret
6. ✅ Adicione no sistema (http://localhost:8001/api-keys/)
7. ✅ `exchange = binance` (minúsculo!)
8. ✅ `is_testnet = True` (marcado!)
9. ✅ `is_active = True` (marcado!)
10. ✅ Aguarde 5-30 min
11. ✅ Veja primeiro trade!

**Segue esta ordem e VAI FUNCIONAR!** 🚀

---

*Guia criado: 30/10/2024 - 04:10 AM*  
*Binance Testnet: 100% grátis e seguro!*  
*Fundos de teste: 10.000 USDT instantâneo!*

**"Testnet é onde heróis nascem, produção é onde heróis brilham!"** 🦸

