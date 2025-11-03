# 🔧 CORREÇÃO - SSH NO UBUNTU/XUBUNTU

## ❌ **ERRO COMUM:**

```bash
sudo systemctl restart sshd
# Failed to restart sshd.service: Unit sshd.service not found.
```

---

## ✅ **SOLUÇÃO:**

**No Ubuntu/Xubuntu, o serviço é `ssh` (não `sshd`)!**

```bash
# CORRETO para Ubuntu/Xubuntu:
sudo systemctl restart ssh

# CORRETO para Red Hat/CentOS/Fedora:
sudo systemctl restart sshd
```

---

## 📋 **COMANDOS SSH CORRETOS UBUNTU/XUBUNTU:**

### **Instalar SSH:**
```bash
sudo apt update
sudo apt install openssh-server -y
```

### **Gerenciar serviço:**
```bash
# Iniciar
sudo systemctl start ssh

# Parar
sudo systemctl stop ssh

# Reiniciar
sudo systemctl restart ssh

# Recarregar config
sudo systemctl reload ssh

# Habilitar auto-start
sudo systemctl enable ssh

# Verificar status
sudo systemctl status ssh

# Ver logs
sudo journalctl -u ssh -n 50
```

---

## 🔍 **IDENTIFICAR NOME DO SERVIÇO:**

### **Método 1:**
```bash
# Listar todos os serviços SSH
systemctl list-units | grep ssh

# Resultado:
# ssh.service  ← Este é o correto!
```

### **Método 2:**
```bash
# Verificar se existe
systemctl status ssh      # ✅ Funciona (Ubuntu)
systemctl status sshd     # ❌ Não encontrado (Ubuntu)
```

---

## 🖥️ **DIFERENÇAS POR SISTEMA:**

| Sistema | Serviço SSH | Config |
|---------|-------------|--------|
| Ubuntu/Xubuntu | `ssh` | `/etc/ssh/sshd_config` |
| Debian | `ssh` | `/etc/ssh/sshd_config` |
| Red Hat/CentOS | `sshd` | `/etc/ssh/sshd_config` |
| Fedora | `sshd` | `/etc/ssh/sshd_config` |
| Arch Linux | `sshd` | `/etc/ssh/sshd_config` |

**Arquivo config é o mesmo, só o nome do serviço muda!**

---

## ✅ **SETUP SSH COMPLETO XUBUNTU:**

```bash
# 1. Instalar
sudo apt install openssh-server -y

# 2. Editar config
sudo nano /etc/ssh/sshd_config

# Modificar:
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes

# Salvar: Ctrl + O → Enter
# Sair: Ctrl + X

# 3. Reiniciar (CORRETO!)
sudo systemctl restart ssh

# 4. Verificar
sudo systemctl status ssh

# 5. Abrir porta no firewall
sudo ufw allow 2222/tcp
sudo ufw reload

# 6. Testar do Windows
ssh -p 2222 usuario@IP_SERVIDOR
```

---

## 🆘 **TROUBLESHOOTING:**

### **SSH não inicia:**
```bash
# Ver erro
sudo systemctl status ssh

# Ver logs detalhados
sudo journalctl -u ssh -n 100

# Testar config
sudo sshd -t
# Ou
sudo /usr/sbin/sshd -t
```

### **Porta já em uso:**
```bash
# Ver quem usa porta 22
sudo netstat -tulpn | grep :22

# Ou
sudo ss -tulpn | grep :22

# Matar processo se necessário
sudo kill PID_DO_PROCESSO
```

### **Firewall bloqueando:**
```bash
# Verificar regras
sudo ufw status verbose

# Adicionar porta
sudo ufw allow 2222/tcp

# Recarregar
sudo ufw reload
```

---

## 📝 **CHECKLIST SSH:**

- [ ] ✅ OpenSSH instalado (`openssh-server`)
- [ ] ✅ Serviço chama-se `ssh` (não `sshd`)
- [ ] ✅ Config em `/etc/ssh/sshd_config`
- [ ] ✅ Porta customizada (ex: 2222)
- [ ] ✅ Root login desabilitado
- [ ] ✅ Password auth desabilitado
- [ ] ✅ Chaves SSH configuradas
- [ ] ✅ Firewall liberado (porta 2222)
- [ ] ✅ Serviço rodando (`status ssh`)

---

## 🚀 **RESUMO:**

**Ubuntu/Xubuntu:**
```bash
sudo systemctl restart ssh  # ✅ Correto!
```

**Red Hat/CentOS:**
```bash
sudo systemctl restart sshd  # ✅ Correto!
```

**SEMPRE use `ssh` no Ubuntu/Xubuntu!** ✅

---

**Erro resolvido! Agora o SSH vai funcionar!** 🎯



