# 🌐 COMO DESCOBRIR IP DO SERVIDOR XUBUNTU

---

## 🎯 **2 TIPOS DE IP:**

### **1. IP LOCAL (Rede interna):**
- Exemplo: `192.168.15.110`
- Uso: Conectar SSH na mesma rede
- Válido: Apenas na sua rede WiFi/Ethernet
- Formato: `192.168.x.x` ou `10.0.x.x`

### **2. IP PÚBLICO (Internet):**
- Exemplo: `177.50.100.200`
- Uso: Configurar domínio, acesso externo
- Válido: Em qualquer lugar do mundo
- Formato: Qualquer IP não reservado

---

## 🏠 **DESCOBRIR IP LOCAL:**

### **No Xubuntu Terminal:**

```bash
# Método 1: Mais rápido!
hostname -I
# Resultado: 192.168.15.110

# Método 2: Mais detalhado
ip addr show
# Procure linha com "inet" (não 127.0.0.1)
# inet 192.168.15.110/24

# Método 3: Tradicional
ifconfig
# Procure "inet addr: 192.168.15.110"

# Método 4: Específico interface
ip -4 addr show eth0
# ou
ip -4 addr show wlan0
```

### **No Xubuntu Interface Gráfica:**

```
1. Clique ícone rede (canto superior direito)
2. Connection Information
3. IP Address: 192.168.15.110  ← Aqui!
```

### **Verificar qual interface está ativa:**

```bash
# Ver todas interfaces
ip link show

# Resultado exemplo:
# 1: lo: ...  (loopback - ignorar)
# 2: eth0: ... state UP  ← Cabo ethernet ATIVA
# 3: wlan0: ... state DOWN  ← WiFi desligado

# Ver IP da interface ativa
ip addr show eth0
```

---

## 🌍 **DESCOBRIR IP PÚBLICO:**

### **No Xubuntu:**

```bash
# Método 1: ifconfig.me (recomendado)
curl ifconfig.me
# Resultado: 177.50.100.200

# Método 2: ipinfo.io
curl ipinfo.io/ip
# Resultado: 177.50.100.200

# Método 3: icanhazip.com
curl icanhazip.com
# Resultado: 177.50.100.200

# Método 4: OpenDNS
dig +short myip.opendns.com @resolver1.opendns.com
# Resultado: 177.50.100.200

# Método 5: wget
wget -qO- ifconfig.me
# Resultado: 177.50.100.200
```

### **No Navegador (qualquer PC):**

Acesse qualquer um destes sites:
- https://www.whatismyip.com/
- https://www.meuip.com.br/
- https://ipinfo.io/
- https://ifconfig.me/

**O IP mostrado é o IP PÚBLICO da sua rede!**

---

## 💡 **DO WINDOWS (Descobrir IP do Xubuntu):**

### **Se estão na mesma rede:**

```powershell
# Método 1: arp -a (ver todos dispositivos)
arp -a

# Procure linha do Xubuntu:
# 192.168.15.110  aa-bb-cc-dd-ee-ff  dinâmico

# Método 2: Ping pelo nome (se souber hostname)
ping xubuntu-server

# Método 3: nmap (se instalado)
nmap -sn 192.168.15.0/24
# Mostra todos IPs da rede
```

---

## 🔍 **EXEMPLO PRÁTICO COMPLETO:**

### **Cenário Real:**

**No Xubuntu Server, você executa:**

```bash
# Ver IP local
hostname -I
# Resultado: 192.168.15.110 fe80::1234:5678:abcd:ef01

# Pegar apenas IPv4
hostname -I | awk '{print $1}'
# Resultado: 192.168.15.110  ← IP LOCAL

# Ver IP público
curl ifconfig.me
# Resultado: 177.50.100.200  ← IP PÚBLICO
```

**Do Windows, você conecta:**

```powershell
# Se estão na mesma casa/rede WiFi:
ssh -p 2222 bottrader@192.168.15.110  ✅

# Se você está em outro local (internet):
ssh -p 2222 bottrader@177.50.100.200  ✅
# ⚠️ Precisa port forwarding no roteador!
```

---

## 🏠 **IP ESTÁTICO LOCAL (RECOMENDADO):**

**Para servidor 24/7, fixe o IP local no roteador:**

### **No roteador:**
```
1. Acesse: http://192.168.15.1 (ou http://192.168.0.1)
2. Login admin do roteador
3. DHCP → Reserva de IP (ou "Static DHCP")
4. MAC Address: (do Xubuntu)
5. IP: 192.168.15.100  ← Fixo!
6. Salvar
```

**Descobrir MAC Address:**
```bash
# No Xubuntu
ip link show eth0

# Procure:
# link/ether aa:bb:cc:dd:ee:ff  ← MAC Address
```

---

## 🌐 **PORT FORWARDING (Para acesso externo):**

**Se quiser acessar de fora da rede:**

### **No roteador:**
```
1. Acesse painel admin do roteador
2. Seção "Port Forwarding" ou "NAT"
3. Adicionar regra:
   - Porta Externa: 2222
   - Porta Interna: 2222
   - IP Interno: 192.168.15.110  ← IP do Xubuntu
   - Protocolo: TCP
4. Salvar
```

**Testar:**
```powershell
# Do Windows (usando 4G ou rede diferente):
ssh -p 2222 bottrader@SEU_IP_PUBLICO
```

---

## 📊 **RESUMO VISUAL:**

```
┌────────────────────────────────────────────┐
│  SUA CASA/REDE                             │
│  ┌──────────────────────────────────────┐  │
│  │ ROTEADOR                             │  │
│  │ IP Público: 177.50.100.200           │  │
│  └──────────────────────────────────────┘  │
│         ↓                                  │
│  ┌──────────────────────────────────────┐  │
│  │ Xubuntu Server                       │  │
│  │ IP Local: 192.168.15.110             │  │
│  └──────────────────────────────────────┘  │
│         ↓                                  │
│  ┌──────────────────────────────────────┐  │
│  │ Seu PC Windows                       │  │
│  │ IP Local: 192.168.15.5               │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘

Conexões:
• Windows → Xubuntu (mesma rede):
  ssh -p 2222 bottrader@192.168.15.110

• Internet → Xubuntu (via roteador):
  ssh -p 2222 bottrader@177.50.100.200
  (precisa port forwarding!)

• DNS (domínio):
  robotrader.com.br → 177.50.100.200
```

---

## ✅ **COMANDOS FINAIS:**

### **Para descobrir AGORA no Xubuntu:**

```bash
echo "=================================="
echo "IP LOCAL: $(hostname -I | awk '{print $1}')"
echo "IP PÚBLICO: $(curl -s ifconfig.me)"
echo "=================================="
```

**Resultado:**
```
==================================
IP LOCAL: 192.168.15.110
IP PÚBLICO: 177.50.100.200
==================================
```

**Use estes IPs conforme necessário!** ✅

---

## 🚀 **PRÓXIMOS PASSOS:**

### **1. Conectar SSH (mesma rede):**
```powershell
# Do Windows
ssh -p 2222 bottrader@IP_LOCAL_DO_XUBUNTU
```

### **2. Transferir código:**
```powershell
scp -P 2222 -r I:\Robo bottrader@IP_LOCAL_DO_XUBUNTU:~/robotrader
```

### **3. Configurar domínio:**
```
DNS: robotrader.com.br → IP_PÚBLICO
```

---

**Agora você sabe encontrar ambos os IPs!** ✅🎯

**Execute no Xubuntu:**
```bash
hostname -I | awk '{print $1}'  # ← IP LOCAL
curl ifconfig.me                # ← IP PÚBLICO
```



