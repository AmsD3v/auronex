# 🔑 COMO CONFIGURAR API KEYS - GUIA COMPLETO

## 📋 OPÇÕES DISPONÍVEIS

### **Opção 1: Script Interativo** ⭐ (Recomendado)
Script pergunta tudo e configura automaticamente

### **Opção 2: Usar Existentes** 
Se já tem API Keys no banco, apenas ativar

### **Opção 3: Via Dashboard**
Adicionar pelo painel web (quando .env estiver ok)

---

## 🚀 OPÇÃO 1: SCRIPT INTERATIVO

### Passo 1: Criar .env PRIMEIRO

**IMPORTANTE:** O script precisa do .env configurado!

```bash
# Copie .env.local para .env
copy I:\Robo\.env.local I:\Robo\.env

# OU abra .env.local e Salvar Como .env
```

### Passo 2: Executar Script

```bash
cd I:\Robo
python scripts/configurar_api_keys.py
```

### O Script Vai Perguntar:

```
1. Qual exchange? (binance, bybit, etc)
2. API Key: [digite aqui]
3. Secret Key: [digite aqui]
4. É Testnet? (s/n)
```

### Vai Fazer Automaticamente:
- ✅ Criptografar credenciais (AES-256)
- ✅ Salvar no banco
- ✅ Validar formato
- ✅ Ativar automaticamente

---

## 🔍 OPÇÃO 2: VERIFICAR EXISTENTES

### Ver se já tem API Keys:

```bash
python scripts/verificar_api_keys_existentes.py
```

### Se aparecer API Keys:
```
Usuario: admin@robotrader.com (ID: 1)
API Keys: 2

  - BINANCE
    ID: 5
    Tipo: Testnet
    Status: Ativa
    Criada: 13/11/2025 14:30
```

**Então já está configurado!** ✅

---

## 🌐 OPÇÃO 3: VIA DASHBOARD

### Quando .env estiver ok:

1. Abra: http://localhost:8501
2. Login: admin@robotrader.com / admin123
3. Menu: API Keys
4. Clique: Adicionar Nova
5. Preencha formulário
6. Salvar

---

## 🎯 SE NÃO TEM CREDENCIAIS

### Para Testnet Binance (GRÁTIS):

1. **Acesse:** https://testnet.binance.vision/
2. **Login/Registro** com GitHub ou Google
3. **API Management** → Create API Key
4. **Copie:**
   - API Key: `xxxxxxxxxxxxxxxxxxxxxx`
   - Secret Key: `yyyyyyyyyyyyyyyyyyyy`

### Para Bybit Testnet (GRÁTIS):

1. **Acesse:** https://testnet.bybit.com/
2. **Login/Registro**
3. **API Management** → Create New Key
4. **Copie as credenciais**

---

## 📝 EXEMPLO DE USO

### Script Interativo:

```bash
$ python scripts/configurar_api_keys.py

======================================================================
  CONFIGURADOR DE API KEYS - AURONEX
======================================================================

[OK] ENCRYPTION_KEY configurada
[OK] Modulos importados
[OK] Usuario encontrado: admin@robotrader.com (ID: 1)

======================================================================
  EXCHANGES DISPONIVEIS:
======================================================================
1. BINANCE
2. BYBIT
3. MERCADOBITCOIN
4. OKX
5. KRAKEN
6. GATEIO
7. KUCOIN
8. FOXBIT
9. NOVADAX

Opcoes:
1. Adicionar nova API Key
2. Listar API Keys existentes
3. Remover API Key
0. Sair

Escolha uma opcao: 1

======================================================================
  ADICIONAR NOVA API KEY
======================================================================

Selecione a exchange:
1. BINANCE
2. BYBIT
...

Numero da exchange: 1
[OK] Exchange selecionada: BINANCE

Digite as credenciais da BINANCE:

API Key: ************************
Secret Key: ************************
E Testnet? (s/n, padrao: s): s

Criptografando credenciais...
[OK] Credenciais criptografadas

Salvando no banco de dados...
[OK] API Key salva com sucesso!

Exchange: BINANCE
Testnet: Sim
Status: Ativa
```

---

## ⚠️ SEGURANÇA

### ✅ O Script É Seguro:
- Usa `getpass` (não mostra senha na tela)
- Criptografa com AES-256
- Salva apenas versão criptografada
- Credenciais originais nunca salvas em plaintext

### ❌ NUNCA:
- Compartilhe suas API Keys
- Commite API Keys no Git
- Use mesmo par Key/Secret em múltiplas plataformas

---

## 🔧 TROUBLESHOOTING

### Erro: "ENCRYPTION_KEY não configurada"
```bash
# Criar .env primeiro
copy .env.local .env
```

### Erro: "Usuario não encontrado"
```bash
# Criar usuário admin
python criar_usuario_fastapi.py
```

### Erro: "Módulos não importados"
```bash
# Instalar dependências
pip install -r requirements.txt
```

---

## 📊 RESUMO

### Sem API Keys:
→ **Use Opção 1** (script interativo)

### Com API Keys existentes:
→ **Use Opção 2** (verificar e ativar)

### Prefere interface:
→ **Use Opção 3** (dashboard web)

---

## 🎯 APÓS CONFIGURAR

### Testar Conexão:

```python
# Criar arquivo teste_conexao.py
import ccxt

exchange = ccxt.binance({
    'apiKey': 'SUA_API_KEY',
    'secret': 'SUA_SECRET',
    'enableRateLimit': True
})

exchange.set_sandbox_mode(True)  # Testnet

balance = exchange.fetch_balance()
print(f"Saldo USDT: {balance['USDT']['free']}")
```

```bash
python teste_conexao.py
```

---

## 🚀 PRÓXIMO PASSO

1. **Configure .env** (se ainda não fez)
2. **Execute:** `python scripts/configurar_api_keys.py`
3. **Siga as instruções** interativas
4. **Teste** no dashboard

---

**Tempo:** 5-10 minutos  
**Resultado:** API Keys configuradas e criptografadas! 🔐






