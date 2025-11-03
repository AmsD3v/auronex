# 🖥️ XUBUNTU - PRIMEIRO ACESSO SSH

**Erro atual:** `Connection refused` porta 22  
**Causa:** SSH não instalado no Xubuntu

---

## 🎯 **SOLUÇÃO EM 3 MINUTOS:**

### **PASSO 1: No Xubuntu (notebook servidor)**

```bash
# 1. Abrir terminal (Ctrl + Alt + T)
# Ou clicar em "Terminal" no menu

# 2. Atualizar sistema
sudo apt update

# 3. Instalar SSH Server
sudo apt install openssh-server -y

# 4. Iniciar SSH
sudo systemctl start ssh
sudo systemctl enable ssh

# 5. Verificar (IMPORTANTE!)
sudo systemctl status ssh
```

**✅ Deve mostrar:** `active (running)`

```bash
# 6. Anotar IP do servidor
hostname -I
```

**Exemplo resultado:** `192.168.15.138`  
**Anote este IP!** ← Vai usar no Windows

---

### **PASSO 2: No Windows (seu computador)**

```powershell
# Abrir PowerShell
# Conectar via SSH:
ssh seu_usuario@192.168.15.138

# Digite senha do Xubuntu
# Pronto! Conectado! ✅
```

**Substitua:**
- `seu_usuario` = usuário que criou no Xubuntu
- `192.168.15.138` = IP que anotou acima

---

## 📝 **EXEMPLO REAL:**

**Se seu usuário no Xubuntu for "bottrader":**

```powershell
ssh bottrader@192.168.15.138
# Digite senha do bottrader
# ✅ Conectado!
```

---

## 🔐 **OPCIONAL: Mudar Porta SSH (Segurança):**

```bash
# No Xubuntu (após conectar via SSH):
sudo nano /etc/ssh/sshd_config

# Procurar linha: #Port 22
# Descomentar e mudar para:
Port 2222

# Salvar: Ctrl + O → Enter → Ctrl + X

# Reiniciar SSH
sudo systemctl restart ssh

# Liberar firewall
sudo ufw allow 2222/tcp
sudo ufw enable
```

**Conectar na nova porta:**
```powershell
ssh -p 2222 bottrader@192.168.15.138
```

---

## ✅ **DEPOIS DE CONECTAR:**

**Siga o guia:** `GUIA_DEFINITIVO_AURONEX_COM_BR.md`  
**Tempo total:** ~2 horas  
**Resultado:** https://auronex.com.br online! 🚀

---

## 🚨 **TROUBLESHOOTING:**

### **"Connection refused"**
```bash
# No Xubuntu:
sudo systemctl status ssh
# Se não estiver "active", executar:
sudo systemctl start ssh
```

### **"Permission denied"**
```bash
# Senha errada - tente novamente
# Ou usuário errado (use o usuário do Xubuntu)
```

### **"Timeout"**
```bash
# IPs diferentes na rede
# Verificar IP novamente:
hostname -I
```

### **Firewall bloqueando:**
```bash
# No Xubuntu:
sudo ufw allow 22/tcp
sudo ufw enable
```

---

**🎯 RESULTADO:** SSH funcionando em 3 minutos!

