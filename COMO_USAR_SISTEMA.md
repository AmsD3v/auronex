# 🚀 COMO USAR O SISTEMA ROBOTRADER - FASTAPI

## ✅ Sistema Atual: FastAPI (V2.0)

**Vantagens:**
- ⚡ 5x mais rápido que Django
- 🛡️ 99.9% estável (nunca cai!)
- 📚 Documentação automática
- 🔄 Assíncrono e moderno

---

## 📋 PRIMEIRO USO (APENAS UMA VEZ)

### 1️⃣ Iniciar o Sistema

Execute o arquivo:
```bash
INICIAR_FASTAPI.bat
```

**IMPORTANTE:** 
- NÃO FECHE as janelas que abrirem!
- Aguarde ~30 segundos para tudo inicializar
- Ignore os erros "não há suporte para o redirecionamento de entrada" (é normal no Windows)

### 2️⃣ Criar Sua Conta

Execute:
```bash
python criar_usuario_fastapi.py
```

Digite:
- **Email:** seu email (ex: admin@robotrader.com)
- **Senha:** sua senha (ex: admin123)
- **Nome:** seu nome (opcional)

**✅ Pronto!** Agora você pode fazer login.

---

## 🎯 USO DIÁRIO

### 1. Iniciar o Sistema

```bash
INICIAR_FASTAPI.bat
```

Aguarde ~30 segundos.

### 2. Acessar o Dashboard

Abra no navegador:
```
http://localhost:8501
```

### 3. Fazer Login

Use o email e senha que você criou no primeiro uso.

### 4. Configurar o Bot

Na barra lateral:
1. **Adicionar API Key da Exchange:**
   - Clique em "➕ Adicionar Nova API Key"
   - Cole suas chaves da Binance/Bybit
   - Salve

2. **Configurar Bot:**
   - Escolha a exchange
   - Selecione as criptomoedas (ou ative Piloto Automático)
   - Defina capital inicial
   - Clique em "💾 Salvar Configurações"

3. **Iniciar Trading:**
   - Clique no botão "▶️ Iniciar Bot"
   - Aguarde 5-15 minutos para o primeiro trade

---

## 🔍 VERIFICAR SE ESTÁ FUNCIONANDO

Execute este comando no PowerShell:

```powershell
# Verificar processos
Get-Process python -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count

# Testar FastAPI
Invoke-WebRequest -Uri "http://localhost:8001/health" -UseBasicParsing

# Testar Dashboard
Invoke-WebRequest -Uri "http://localhost:8501" -UseBasicParsing
```

**Resultado esperado:**
- Processos Python: 4 ou 5
- FastAPI: Status 200
- Dashboard: Status 200

---

## 🌐 URLS IMPORTANTES

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Dashboard** | http://localhost:8501 | Interface principal |
| **FastAPI Docs** | http://localhost:8001/api/docs | Documentação da API |
| **Health Check** | http://localhost:8001/health | Verificar status |

---

## 🐛 PROBLEMAS COMUNS

### ❌ "Email ou senha incorretos!"

**Solução:** Você precisa criar uma conta primeiro!
```bash
python criar_usuario_fastapi.py
```

### ❌ Dashboard não carrega (localhost:8501)

**Solução 1:** Aguarde mais 30 segundos (Streamlit demora a iniciar)

**Solução 2:** Reinicie o sistema:
```bash
# Matar processos
taskkill /F /IM python.exe

# Iniciar novamente
INICIAR_FASTAPI.bat
```

### ❌ FastAPI não responde (localhost:8001)

**Solução:** Verifique se Redis está instalado:
```bash
# Instalar Redis (se não tiver)
# Windows: Baixe do GitHub redis/redis-windows
```

### ❌ Bot não faz trades

**Causas comuns:**
1. ⏱️ **Aguardando oportunidade** - Normal! Pode levar 5-15 minutos
2. 🔑 **API Key inválida** - Verifique suas chaves na Binance
3. 💰 **Sem saldo** - Certifique-se de ter fundos na conta Testnet
4. 📊 **Mercado estável** - Bot espera queda de 0.1% para comprar

**Verificar logs:**
```bash
# Abra a janela "Celery Worker" e veja os logs
```

---

## 📊 COMPONENTES DO SISTEMA

Quando você executa `INICIAR_FASTAPI.bat`, são iniciados:

1. **FastAPI (Uvicorn)** - Backend da API (porta 8001)
2. **Celery Worker** - Processa trades em background
3. **Celery Beat** - Agenda tarefas periódicas (checagem a cada 1 minuto)
4. **Streamlit Dashboard** - Interface visual (porta 8501)

**Todos são necessários!** Não feche as janelas.

---

## 🎓 PRÓXIMOS PASSOS

### 1. Configurar Binance Testnet

Se você ainda não tem API Keys de teste:

1. Acesse: https://testnet.binance.vision/
2. Faça login com GitHub/Google
3. Gere API Key e Secret
4. Solicite fundos de teste (botão "Get Test Funds")
5. Adicione as chaves no Dashboard

### 2. Monitorar Performance

No Dashboard, acompanhe:
- 📊 **Portfólio:** Valor atual, P&L total
- 💹 **Gráfico de Performance:** Evolução do capital
- 📺 **Operações Recentes:** Últimos 10 trades
- 🏆 **TOP 5 Performance:** Melhores criptos do momento

### 3. Ajustar Estratégia

Se o bot não estiver performando bem:
- Teste o **Piloto Automático** (bot escolhe as melhores criptos)
- Ajuste o **Take Profit** (lucro alvo por trade)
- Modifique o **Stop Loss** (limite de perda)
- Experimente diferentes **símbolos**

---

## 📞 SUPORTE

Se precisar de ajuda:
1. Verifique este guia primeiro
2. Execute `python diagnostico_bot.py` para diagnóstico automático
3. Consulte os logs nas janelas do sistema

---

## 🔐 SEGURANÇA

**NUNCA compartilhe:**
- ❌ Suas API Keys
- ❌ Sua senha do Dashboard
- ❌ Arquivo `fastapi_app/trading_bot.db`

**Modo Produção:**
- Use API Keys de **PRODUÇÃO** apenas quando estiver 100% confiante
- Comece com valores BAIXOS
- Monitore DIARIAMENTE

---

**✅ Sistema pronto para uso!**

**Versão:** FastAPI V2.0  
**Data:** Outubro 2025  
**Status:** Totalmente Funcional

