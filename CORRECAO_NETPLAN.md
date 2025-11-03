# 🔧 CORREÇÃO DO ERRO NETPLAN

## ❌ **ERRO QUE VOCÊ RECEBEU**

```
WARNING: Permissions for /etc/netplan/01-netcfg.yaml are too open
Invalid YAML: mapping values are not allowed in this context
```

---

## ✅ **SOLUÇÃO**

### **Problema 1: Permissões**
```bash
sudo chmod 600 /etc/netplan/01-netcfg.yaml
```

### **Problema 2: YAML Inválido**

**O que enviei estava ERRADO! Use este (CORRETO):**

```bash
sudo nano /etc/netplan/01-netcfg.yaml
```

**Apague tudo e cole isto:**

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp3s0:
      dhcp4: no
      addresses:
        - 192.168.0.100/24
      routes:
        - to: default
          via: 192.168.0.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

**IMPORTANTE:** Substitua `enp3s0` pelo nome da sua interface!

### **Como descobrir o nome da interface:**

```bash
ip a
```

Procure algo como:
- `enp3s0` (Ethernet)
- `wlp2s0` (WiFi)
- `eth0` (antigo)

---

## 📝 **PASSO A PASSO CORRETO**

```bash
# 1. Ver nome da interface
ip a

# 2. Editar netplan (COPIE EXATAMENTE!)
sudo nano /etc/netplan/01-netcfg.yaml
```

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    SUA_INTERFACE_AQUI:
      dhcp4: no
      addresses:
        - 192.168.0.100/24
      routes:
        - to: default
          via: 192.168.0.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

```bash
# 3. Corrigir permissões
sudo chmod 600 /etc/netplan/01-netcfg.yaml

# 4. Testar configuração
sudo netplan try

# 5. Se OK, aplicar
sudo netplan apply

# 6. Verificar
ip a
ping 8.8.8.8
```

---

## ✅ **ALTERNATIVA MAIS FÁCIL**

**Se continuar dando erro, use DHCP (mais simples):**

```yaml
network:
  version: 2
  ethernets:
    enp3s0:
      dhcp4: yes
```

Depois configure IP fixo no **roteador** (DHCP Reservation).

---

## 🎯 **PRÓXIMO PASSO**

Após corrigir rede:

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar dependências
sudo apt install python3.10 python3-pip git nginx -y

# Criar usuário
sudo useradd -m -s /bin/bash auronex
sudo passwd auronex

# Criar pasta
sudo mkdir -p /var/www/auronex
sudo chown auronex:auronex /var/www/auronex
```

**Continue com:** `DEPLOY_COM_DOMINIO.md`

---

**Corrija o netplan com o YAML acima!** ✅

