# 🖥️ SETUP XUBUNTU - COMANDOS ALTERNATIVOS SEM VIM

**Problema:** `vim` não instalado por padrão no Xubuntu

**Solução:** Usar `nano` (editor simples) ou instalar `vim`

---

## 📝 **OPÇÃO 1: USAR NANO (RECOMENDADO)**

### **Nano é mais fácil para iniciantes!**

**Substituir todos os comandos `vim` por `nano`:**

```bash
# ANTES (vim):
sudo vim /etc/ssh/sshd_config

# AGORA (nano):
sudo nano /etc/ssh/sshd_config
```

**Comandos do Nano:**
- **Editar:** Use setas para navegar, digite normalmente
- **Salvar:** `Ctrl + O` → Enter
- **Sair:** `Ctrl + X`
- **Buscar:** `Ctrl + W`
- **Ajuda:** `Ctrl + G`

---

## 📝 **OPÇÃO 2: INSTALAR VIM**

```bash
# Instalar vim
sudo apt update
sudo apt install vim -y

# Agora pode usar vim normalmente
sudo vim /etc/ssh/sshd_config
```

**Comandos básicos Vim:**
- **Modo Edição:** Pressione `i`
- **Sair Edição:** Pressione `Esc`
- **Salvar e sair:** Digite `:wq` e Enter
- **Sair sem salvar:** Digite `:q!` e Enter

---

## 🔧 **SETUP XUBUNTU - VERSÃO NANO**

### **SSH Seguro com Nano:**

```bash
# Editar config SSH
sudo nano /etc/ssh/sshd_config

# Encontre e modifique estas linhas:
# (Use Ctrl+W para buscar)

Port 2222                      # Busque "Port" e mude para 2222
PermitRootLogin no             # Busque "PermitRootLogin" e mude para no
PasswordAuthentication no      # Busque "PasswordAuthentication" e mude para no
PubkeyAuthentication yes       # Certifique que está yes

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Reiniciar SSH
sudo systemctl restart sshd
```

---

### **PostgreSQL com Nano:**

```bash
# Otimizar PostgreSQL
sudo nano /etc/postgresql/14/main/postgresql.conf

# Busque (Ctrl + W) e modifique:
shared_buffers = 1GB
effective_cache_size = 3GB
maintenance_work_mem = 256MB

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

---

### **Redis com Nano:**

```bash
# Otimizar Redis
sudo nano /etc/redis/redis.conf

# Busque e modifique:
maxmemory 512mb
maxmemory-policy allkeys-lru

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Reiniciar Redis
sudo systemctl restart redis-server
```

---

### **Fail2Ban com Nano:**

```bash
# Configurar Fail2Ban
sudo nano /etc/fail2ban/jail.local

# Cole (Ctrl + Shift + V):
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Iniciar Fail2Ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

### **Nginx com Nano:**

```bash
# Copiar config do projeto
sudo cp ~/robotrader/deploy/nginx-robotrader.conf /etc/nginx/sites-available/robotrader

# Editar para trocar domínio
sudo nano /etc/nginx/sites-available/robotrader

# Busque (Ctrl + W): "seudominio.com"
# Substitua por seu domínio real

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# Ativar site
sudo ln -s /etc/nginx/sites-available/robotrader /etc/nginx/sites-enabled/

# Testar config
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

## 🚀 **SCRIPT SETUP ATUALIZADO PARA XUBUNTU**

**Arquivo:** `deploy/setup-xubuntu-server.sh`

```bash
#!/bin/bash

# ========================================
# ROBOTRADER - SETUP XUBUNTU 22.04
# ========================================

set -e

echo "🚀 ROBOTRADER - Setup Xubuntu Server 22.04"
echo "=========================================="
echo ""

# Verificar se é root
if [ "$EUID" -ne 0 ]; then 
   echo "❌ Execute como root: sudo ./setup-xubuntu-server.sh"
   exit 1
fi

echo "✅ Executando como root"
echo ""

# 1. ATUALIZAR SISTEMA
echo "[1/11] Atualizando sistema..."
apt update && apt upgrade -y

# 2. INSTALAR VIM (para poder usar comandos vim)
echo "[2/11] Instalando vim e nano..."
apt install -y vim nano

# 3. INSTALAR DEPENDÊNCIAS
echo "[3/11] Instalando dependências..."
apt install -y \
    build-essential \
    git \
    curl \
    wget \
    htop \
    tmux \
    net-tools \
    ufw \
    fail2ban \
    nginx \
    postgresql \
    postgresql-contrib \
    redis-server \
    python3.10 \
    python3.10-venv \
    python3-pip \
    certbot \
    python3-certbot-nginx

# Continuar com resto do script...
# (mesmo código do setup-ubuntu-server.sh)
```

---

## 💡 **DICAS NANO vs VIM**

### **Nano (Fácil):**
```
✅ Mais intuitivo
✅ Comandos no rodapé
✅ Setas funcionam normalmente
✅ Ctrl + letra
✅ Recomendado para iniciantes
```

### **Vim (Poderoso):**
```
✅ Mais rápido (quando domina)
✅ Mais recursos
✅ Mais usado por profissionais
⚠️ Curva de aprendizado
⚠️ Precisa decorar comandos
```

---

## 📋 **ATALHOS NANO (PRINCIPAIS)**

```
Ctrl + O  →  Salvar (Write Out)
Ctrl + X  →  Sair (eXit)
Ctrl + W  →  Buscar (Where is)
Ctrl + K  →  Cortar linha
Ctrl + U  →  Colar linha
Ctrl + _  →  Ir para linha
Ctrl + G  →  Ajuda (Get Help)
```

---

## 🔄 **CONVERTER GUIA PARA NANO**

**Sempre que ver `vim`, substitua por `nano`:**

```bash
# Exemplos:
sudo vim arquivo.txt   →  sudo nano arquivo.txt
vim ~/.bashrc          →  nano ~/.bashrc
sudo vim /etc/hosts    →  sudo nano /etc/hosts
```

**Funciona 100% igual!** ✅

---

## 🚀 **SETUP COMPLETO XUBUNTU COM NANO**

Criei versão atualizada do guia usando NANO em vez de VIM!

**Arquivo:** Atualizarei agora o `SERVIDOR_UBUNTU_BOT_TRADING.md`

---

**Continuando com a correção do admin...**



