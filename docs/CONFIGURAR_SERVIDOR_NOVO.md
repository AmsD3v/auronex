# 🚀 CONFIGURAR SERVIDOR NOVO

**Servidor:** i7-2630QM, 8GB RAM  
**OS:** Ubuntu Server 22.04 LTS (recomendado)  
**Performance:** 50-70% mais rápido que atual!

---

## 📋 PASSO A PASSO

### **1. INSTALAR UBUNTU SERVER**

1. Baixar Ubuntu 22.04 LTS
2. Criar USB bootável (Rufus)
3. Instalar (sem interface gráfica)
4. Usuário: serverhome
5. Ativar SSH na instalação

---

### **2. PRIMEIRO ACESSO (SSH)**

```bash
ssh serverhome@IP_DO_SERVIDOR

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar essenciais
sudo apt install -y git curl wget build-essential
```

---

### **3. INSTALAR PYTHON 3.10+**

```bash
sudo apt install -y python3.10 python3.10-venv python3-pip
python3 --version  # Confirmar 3.10+
```

---

### **4. INSTALAR NODE.JS 20 LTS**

```bash
# Node.js 20 LTS (suporte até 2026)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Verificar
node --version  # Deve mostrar v20.x.x
npm --version
```

---

### **5. INSTALAR PM2**

```bash
sudo npm install -g pm2
pm2 --version
```

---

### **6. CLONAR PROJETO**

```bash
cd ~
git clone https://github.com/AmsD3v/auronex.git
cd auronex
```

---

### **7. PYTHON SETUP**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### **8. REACT SETUP**

```bash
cd auronex-dashboard

# Criar .env.production
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://auronex.com.br
NODE_ENV=production
EOF

npm install
npm run build

cd ..
```

---

### **9. INICIAR SERVICOS**

```bash
# FastAPI
pm2 start "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001" --name fastapi-app

# React
pm2 start "npm --prefix auronex-dashboard start" --name auronex-dashboard

# Salvar
pm2 save
pm2 startup  # Auto-start no boot
```

---

### **10. CLOUDFLARE TUNNEL**

```bash
# Instalar
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Login (abre navegador)
cloudflared tunnel login

# Criar tunnel (se novo servidor)
cloudflared tunnel create auronex-novo

# Configurar
sudo nano /etc/cloudflared/config.yml
```

**Config:**
```yaml
tunnel: SEU_TUNNEL_ID
credentials-file: /home/serverhome/.cloudflared/TUNNEL_ID.json

ingress:
  - hostname: auronex.com.br
    service: http://localhost:8001
  
  - hostname: app.auronex.com.br
    service: http://localhost:8501
  
  - service: http_status:404
```

**Iniciar:**
```bash
nohup cloudflared tunnel run auronex-novo > ~/auronex/logs/tunnel.log 2>&1 &
```

---

### **11. POSTGRESQL (Opcional - depois)**

```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar database
sudo -u postgres psql
CREATE DATABASE auronex;
CREATE USER auronex WITH PASSWORD 'senha_forte';
GRANT ALL PRIVILEGES ON DATABASE auronex TO auronex;
\q
```

**Migração SQLite → PostgreSQL:**
```bash
pip install sqlalchemy-utils
python scripts/migrate_to_postgres.py
```

---

### **12. FIREWALL**

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

### **13. MONITORAMENTO**

```bash
# Status
pm2 status
pm2 monit  # Dashboard tempo real

# Logs
pm2 logs fastapi-app --lines 50
pm2 logs auronex-dashboard --lines 50
```

---

## ✅ RESULTADO

**URLs:**
- https://auronex.com.br (FastAPI + Landing)
- https://app.auronex.com.br (Dashboard)

**Performance:**
- ~50-70% mais rápido
- Suporta 5-10 bots simultâneos
- 8GB RAM (vs 4GB)

---

## 🎯 TEMPO ESTIMADO

- Instalação OS: 30 min
- Setup Python/Node: 20 min
- Clone + Build: 15 min
- Cloudflare: 10 min
- **Total: ~1h15min**

---

**PRONTO PARA COMEÇAR QUANDO QUISER!** 🚀

