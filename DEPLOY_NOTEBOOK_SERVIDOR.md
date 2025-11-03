# 💻 DEPLOY NO SEU NOTEBOOK COMO SERVIDOR

**Hardware:** Intel i7-3517U, 4GB RAM, 240GB SSD  
**Objetivo:** Transformar notebook em servidor do Auronex

---

## ✅ **SEU NOTEBOOK SERVE PERFEITAMENTE!**

**Especificações:**
- ✅ i7-3517U: Suficiente para 50-100 usuários simultâneos
- ✅ 4GB RAM: OK (FastAPI é leve)
- ✅ 240GB SSD: Ótimo para banco de dados
- ✅ **SERVE!**

---

## 🔧 **OPÇÕES DE DEPLOY (NOTEBOOK)**

### **OPÇÃO 1: Git Local (RECOMENDADO!)**

**Vantagens:**
- ✅ Controle de versão completo
- ✅ Fácil sincronizar (git push/pull)
- ✅ Mesmo fluxo que produção
- ✅ Backup automático

**Setup:**

**1. No PC de desenvolvimento (seu atual):**
```bash
cd I:\Robo

# Criar repositório Git
git init
git add .
git commit -m "Sistema Auronex v1.0"
```

**2. No notebook servidor:**

**Opção A: Repositório local (Rede)**
```bash
# No notebook:
cd C:\AuronexServer
git init --bare auronex-repo.git

# No PC dev (conectado na mesma rede):
git remote add notebook \\NOTEBOOK-IP\AuronexServer\auronex-repo.git
git push notebook main

# No notebook (área de trabalho):
git clone C:\AuronexServer\auronex-repo.git C:\Auronex
```

**Opção B: Pen Drive/Compartilhamento**
```bash
# Copiar pasta I:\Robo para pendrive
# Conectar pendrive no notebook
# Copiar para C:\Auronex
# Usar Git normalmente
```

**3. Atualizar depois:**
```bash
# PC dev:
git add .
git commit -m "Corrigido navbar"
git push notebook main

# Notebook servidor:
cd C:\Auronex
git pull
# Reiniciar serviço
```

---

### **OPÇÃO 2: Compartilhamento de Rede (MAIS FÁCIL)**

**Setup:**

**1. No notebook servidor:**
```
- Compartilhe pasta C:\Auronex
- Permissões: Leitura/Escrita
- Anote IP do notebook
```

**2. No PC dev:**
```
- Mapeie \\NOTEBOOK-IP\Auronex como unidade de rede
- Use como Z:\
- Desenvolva normalmente
- Arquivos já estarão no servidor!
```

**Vantagem:** Sincronização instantânea!  
**Desvantagem:** Sem controle de versão

---

### **OPÇÃO 3: Sincronização Automática**

**Ferramentas:**
- **SyncThing:** Sincroniza pastas automaticamente
- **Resilio Sync:** Similar
- **Rclone:** Via linha de comando

**Setup:**
```
1. Instale SyncThing em ambos (PC + Notebook)
2. Configure pasta I:\Robo (PC) ↔ C:\Auronex (Notebook)
3. Sincronização automática a cada mudança!
```

---

## 🌐 **CONFIGURAR NOTEBOOK COMO SERVIDOR**

### **1. Sistema Operacional:**

**Windows (atual):**
```
✅ Funciona
⚠️ Precisa configurar:
  - Firewall (liberar porta 8001)
  - IP fixo local
  - Desligar suspensão automática
```

**Linux (recomendado):**
```
✅ Melhor performance
✅ Menos recursos (sobra RAM)
✅ Mais estável

Instale: Ubuntu Server 22.04
```

### **2. IP Fixo Local:**

**No roteador:**
```
1. Acesse painel (192.168.0.1)
2. DHCP → Reserva de IP
3. MAC do notebook → IP fixo (ex: 192.168.0.100)
```

### **3. Acesso Externo (Internet):**

**Opção A: No-IP (GRÁTIS):**
```
1. Cadastre: www.noip.com
2. Crie hostname: auronex.ddns.net
3. Instale cliente No-IP no notebook
4. Atualiza IP automaticamente
```

**Opção B: Ngrok:**
```bash
# Instalar ngrok
ngrok http 8001

# Recebe URL:
https://abc123.ngrok.io → localhost:8001

# Webhooks funcionam!
```

### **4. SSL/HTTPS:**

**Após ter domínio (auronex.ddns.net):**
```bash
# Instalar Certbot
pip install certbot

# Gerar certificado SSL GRÁTIS
certbot certonly --standalone -d auronex.ddns.net
```

---

## 🚀 **INICIAR NO NOTEBOOK (Windows)**

### **1. Configurar ambiente:**
```powershell
# Instalar Python 3.10
# Download: python.org

# Criar pasta
New-Item -Path "C:\Auronex" -ItemType Directory

# Copiar arquivos (via Git ou manualmente)
cd C:\Auronex

# Criar venv
python -m venv venv
.\venv\Scripts\activate

# Instalar
pip install -r requirements_fastapi.txt
```

### **2. Configurar para iniciar automaticamente:**

**Criar arquivo:** `C:\Auronex\INICIAR_SERVIDOR.bat`
```batch
@echo off
cd C:\Auronex
call venv\Scripts\activate
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
```

**Adicionar ao Windows Startup:**
```
1. Win+R → shell:startup
2. Criar atalho para INICIAR_SERVIDOR.bat
3. Notebook reinicia → Servidor inicia automaticamente!
```

---

## 📊 **CAPACIDADE DO SEU NOTEBOOK**

**i7-3517U + 4GB RAM pode suportar:**
- ✅ 50-100 usuários simultâneos
- ✅ Bot de trading 24/7
- ✅ Dashboard Streamlit
- ✅ FastAPI (muito leve!)

**Otimizações:**
- Feche programas desnecessários
- Desative suspensão automática
- Use SSD (você já tem!)
- Ventilação adequada

---

## 🎯 **MINHA RECOMENDAÇÃO PARA SEU CASO**

### **MELHOR OPÇÃO: Git + Compartilhamento de Rede**

**Por quê:**
1. Controle de versão (Git)
2. Fácil desenvolver (rede compartilhada)
3. Atualizar rápido (git pull)
4. Backup (GitHub privado)

**Setup (30 min):**

**No notebook:**
```
1. Instale Git for Windows
2. Compartilhe C:\Auronex
3. Configure IP fixo
4. Libere firewall (porta 8001)
5. Clone repositório
6. Rode INICIAR_SERVIDOR.bat
```

**No PC dev:**
```
1. Mapeie \\NOTEBOOK-IP\Auronex
2. git push quando atualizar
3. No notebook: git pull
4. Restart automático
```

---

## ⚠️ **ATENÇÃO**

**Energia:**
- Notebook sempre ligado → Alta conta de luz
- Use modo "Alto desempenho"
- Mantenha ventilado

**Backup:**
- Faça backup semanal do banco
- Git já é um backup
- Considere nuvem para dados críticos

---

## 🏆 **RESUMO**

**Seu notebook SERVE como servidor!**

**Melhor opção:** Git local + Compartilhamento  
**Custo:** R$ 0 (só energia)  
**Setup:** 30 minutos  
**Atualização:** 1 minuto (git pull)  

**Leia:** `DEPLOY_NOTEBOOK_SERVIDOR.md` (arquivo completo)

---

**Quer que eu prepare os arquivos para deploy no notebook?** 🚀




