# 🔐 CONECTAR SSH - GUIA COMPLETO PASSO A PASSO

**IP do Servidor:** 192.168.15.138  
**Usuário:** bottrader  
**Objetivo:** Conectar do Windows no Xubuntu via SSH

---

## 📋 **ETAPA 1: PREPARAR XUBUNTU (Servidor)**

### **1.1. Abrir Terminal no Xubuntu:**

```
Xubuntu Desktop:
1. Clique no ícone "Terminal" no menu
   OU
2. Pressione: Ctrl + Alt + T
```

Terminal aberto! Você verá algo como:
```
bottrader@bottraer-AMS:~$  ← Prompt pronto para comandos
```

---

### **1.2. Instalar SSH Server:**

**Digite no terminal (letra por letra ou copie):**

```bash
sudo apt update
```

**Pressione Enter**

```
[sudo] password for bottrader: _  ← Digite SUA senha
```

**Digite a senha do usuário bottrader** (não aparece nada enquanto digita - é normal!)

**Pressione Enter**

Vai baixar lista de pacotes (~10 segundos). Aguarde terminar.

---

**Agora instale o SSH:**

```bash
sudo apt install openssh-server -y
```

**Pressione Enter**

Instalação (~30-60 segundos). Aguarde mensagens:
```
Reading package lists... Done
Building dependency tree... Done
...
Setting up openssh-server...
```

---

### **1.3. Iniciar e Habilitar SSH:**

```bash
sudo systemctl start ssh
```
**Pressione Enter**

```bash
sudo systemctl enable ssh
```
**Pressione Enter**

```bash
sudo systemctl status ssh
```
**Pressione Enter**

**Deve mostrar:**
```
● ssh.service - OpenBSD Secure Shell server
   Active: active (running) since...  ← VERDE = BOM!
```

**Pressione 'q' para sair da visualização**

---

### **1.4. Verificar Porta Atual:**

```bash
sudo ss -tulpn | grep ssh
```
**Pressione Enter**

**Resultado:**
```
tcp  LISTEN  0  0.0.0.0:22  0.0.0.0:*  users:(("sshd",...))
                      ↑↑
                 Porta 22 (padrão)
```

**Anote: Porta é 22 (por enquanto)**

---

## 📋 **ETAPA 2: TESTAR CONEXÃO DO WINDOWS**

### **2.1. Abrir PowerShell no Windows:**

**Windows 10/11:**
```
Método 1:
1. Pressione: Windows + R
2. Digite: powershell
3. Pressione: Enter

Método 2:
1. Pressione: Windows + X
2. Clique: "Windows PowerShell" ou "Terminal"

Método 3:
1. Barra de busca Windows
2. Digite: PowerShell
3. Clique em "Windows PowerShell"
```

PowerShell aberto! Você verá:
```
PS C:\Users\SeuNome>  ← Prompt pronto
```

---

### **2.2. Testar Ping (Verificar Rede):**

**No PowerShell, digite:**

```powershell
ping 192.168.15.138
```

**Pressione Enter**

**Resultado A - Sucesso:**
```
Resposta de 192.168.15.138: bytes=32 tempo<1ms TTL=64
Resposta de 192.168.15.138: bytes=32 tempo<1ms TTL=64
...
Pacotes: Enviados = 4, Recebidos = 4, Perdidos = 0 (0% de perda)
```
✅ **ÓTIMO! Rede funcionando!** Continue para 2.3

**Resultado B - Falha:**
```
Solicitação de tempo limite
...
Pacotes: Enviados = 4, Recebidos = 0, Perdidos = 4 (100% de perda)
```
❌ **PROBLEMA DE REDE!**

**Soluções:**
1. Verificar se Xubuntu está na mesma rede WiFi
2. Verificar se Xubuntu tem internet (executar `ping 8.8.8.8` no Xubuntu)
3. Reiniciar roteador

---

### **2.3. Conectar SSH (Porta 22):**

**No PowerShell, digite:**

```powershell
ssh bottrader@192.168.15.138
```

**(SEM -p 2222 ainda! Porta é 22 por enquanto!)**

**Pressione Enter**

---

**Primeira vez conectando, aparece:**
```
The authenticity of host '192.168.15.138 (192.168.15.138)' can't be established.
ED25519 key fingerprint is SHA256:abcdefghijklmnop1234567890...
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

**Digite:** `yes`  
**Pressione Enter**

```
Warning: Permanently added '192.168.15.138' (ED25519) to the list of known hosts.
```

---

**Agora pede senha:**
```
bottrader@192.168.15.138's password: _
```

**Digite a senha do usuário bottrader**  
**(Não aparece nada enquanto digita - segurança!)**  
**Pressione Enter**

---

**Se senha correta, você verá:**
```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux ...)
...
Last login: ...
bottrader@bottraer-AMS:~$  ← CONECTADO! ✅✅✅
```

**PARABÉNS! Está conectado via SSH!** 🎉

---

## 📋 **ETAPA 3: CONFIGURAR PORTA 2222 (Opcional mas Recomendado)**

**Agora você está conectado no Xubuntu via SSH. Continue no terminal SSH:**

### **3.1. Editar Configuração SSH:**

```bash
sudo nano /etc/ssh/sshd_config
```
**Pressione Enter**

```
[sudo] password for bottrader: _
```
**Digite senha, pressione Enter**

**Editor NANO abre o arquivo.**

---

### **3.2. Buscar e Modificar Porta:**

**No NANO:**

```
1. Pressione: Ctrl + W  (buscar)
2. Digite: Port
3. Pressione: Enter
```

**Cursor pula para linha:**
```
#Port 22  ← Pode ter # na frente
```

---

**Modificar:**

**Se tiver #:**
```
#Port 22

Use tecla Delete ou Backspace para apagar #:
Port 22

Use setas → para ir até 22:
Port 22
     ↑

Apague 22 (Backspace 2 vezes):
Port 

Digite 2222:
Port 2222  ← PRONTO!
```

---

### **3.3. Salvar Arquivo:**

```
1. Pressione: Ctrl + O  (letra O)
   
Aparece:
File Name to Write: /etc/ssh/sshd_config
                                        ↑ Cursor aqui

2. Pressione: Enter

Mensagem:
[ Wrote 125 lines ]

3. Pressione: Ctrl + X

# Volta para terminal SSH
```

---

### **3.4. Reiniciar SSH:**

```bash
sudo systemctl restart ssh
```
**Pressione Enter**

**Aguarde 2 segundos (não mostra nada se sucesso)**

```bash
sudo systemctl status ssh
```
**Pressione Enter**

**Deve mostrar:**
```
● ssh.service - OpenBSD Secure Shell server
   Active: active (running) since...  ← BOM!
```

**Pressione 'q' para sair**

---

### **3.5. Verificar Porta 2222:**

```bash
sudo ss -tulpn | grep :2222
```
**Pressione Enter**

**Deve mostrar:**
```
tcp  LISTEN  0.0.0.0:2222  0.0.0.0:*  users:(("sshd",...))
                    ↑↑↑↑
              Porta 2222 ativa! ✅
```

---

### **3.6. Liberar Firewall:**

```bash
sudo ufw allow 2222/tcp
```
**Pressione Enter**

```bash
sudo ufw reload
```
**Pressione Enter**

```bash
exit
```
**Pressione Enter** (desconecta SSH)

---

## 📋 **ETAPA 4: CONECTAR NA PORTA 2222**

**De volta ao PowerShell do Windows:**

```powershell
ssh -p 2222 bottrader@192.168.15.138
```

**Pressione Enter**

```
bottrader@192.168.15.138's password: _
```

**Digite senha, pressione Enter**

```
Welcome to Ubuntu 22.04.5 LTS
bottrader@bottraer-AMS:~$  ← CONECTADO NA PORTA 2222! ✅
```

**SUCESSO! Porta 2222 configurada!** 🎉

---

## ✅ **COMANDOS FINAIS RESUMIDOS:**

### **Primeira Conexão (Porta 22):**
```powershell
# Windows PowerShell:
ssh bottrader@192.168.15.138
```

### **Depois de Configurar (Porta 2222):**
```powershell
# Windows PowerShell:
ssh -p 2222 bottrader@192.168.15.138
```

---

## 🎯 **SE AINDA NÃO FUNCIONAR:**

### **Verifique tudo no Xubuntu:**

```bash
# 1. SSH instalado e rodando?
sudo systemctl status ssh
# Deve: active (running)

# 2. Qual porta SSH usa?
sudo ss -tulpn | grep ssh
# Deve mostrar: :22 ou :2222

# 3. Firewall liberou?
sudo ufw status
# Deve mostrar: 22/tcp ou 2222/tcp ALLOW

# 4. Qual seu IP?
hostname -I
# Deve: 192.168.15.138
```

### **Verifique no Windows:**

```powershell
# 1. Ping funciona?
ping 192.168.15.138
# Deve: Recebeu 4 pacotes

# 2. SSH instalado?
ssh
# Deve: mostrar ajuda do SSH (não "comando não encontrado")

# 3. Mesma rede?
ipconfig
# Procure: 192.168.15.xxx (mesmo começo)
```

---

## 📞 **ÚLTIMA OPÇÃO:**

**Se NADA funcionar, me envie:**

### **Do Xubuntu:**
```bash
# Copie e execute TUDO de uma vez:
echo "=== DIAGNÓSTICO XUBUNTU ==="
echo "IP: $(hostname -I)"
echo "SSH Status:"
sudo systemctl status ssh | grep Active
echo "Porta SSH:"
sudo ss -tulpn | grep ssh
echo "Firewall:"
sudo ufw status
echo "==========================="
```

### **Do Windows:**
```powershell
# Copie e execute:
echo "=== DIAGNÓSTICO WINDOWS ==="
ping -n 2 192.168.15.138
ipconfig | findstr "IPv4"
echo "==========================="
```

**Me envie o resultado e eu ajusto!**

---

## ✅ **99% DOS CASOS:**

**O problema é um destes:**
1. ✅ SSH não instalado → `sudo apt install openssh-server`
2. ✅ Porta errada → Use 22 primeiro, depois mude para 2222
3. ✅ Firewall bloqueando → `sudo ufw allow 22/tcp`
4. ✅ Redes diferentes → Conecte na mesma WiFi

**Siga o guia passo a passo e vai funcionar!** 🚀


