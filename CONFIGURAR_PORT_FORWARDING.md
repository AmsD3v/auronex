# 🌐 CONFIGURAR PORT FORWARDING NO ROTEADOR

## 🎯 **O QUE É PORT FORWARDING?**

Port Forwarding = Redirecionar tráfego da internet para seu notebook servidor

```
Internet → Roteador → Notebook (servidor)
Porta 80 → Roteador → 192.168.0.100:80
```

---

## 📋 **PASSO A PASSO COMPLETO**

### **1. ACESSAR O ROTEADOR**

**Descobrir IP do roteador:**

**No Windows:**
```powershell
ipconfig
# Procure "Gateway Padrão"
# Exemplo: 192.168.0.1
```

**No Linux:**
```bash
ip route | grep default
# Exemplo: default via 192.168.0.1
```

**IPs comuns:**
- 192.168.0.1
- 192.168.1.1
- 192.168.15.1
- 10.0.0.1

---

### **2. FAZER LOGIN NO ROTEADOR**

**Abra navegador:**
```
http://192.168.0.1
```

**Login padrão (varia por marca):**

**TP-Link:**
- Usuário: admin
- Senha: admin

**D-Link:**
- Usuário: admin
- Senha: (vazio) ou admin

**Intelbras:**
- Usuário: admin
- Senha: admin

**Netgear:**
- Usuário: admin
- Senha: password

**Multilaser:**
- Usuário: admin
- Senha: admin

⚠️ **Se alterou, use sua senha!**

---

### **3. ENCONTRAR MENU DE PORT FORWARDING**

**Procure por um destes nomes:**

- Port Forwarding
- Virtual Server
- NAT
- Redirecionamento de Portas
- Servidor Virtual
- Aplicações e Jogos
- Advanced → Port Forwarding

**Geralmente em:**
- Advanced → NAT Forwarding → Port Forwarding
- Firewall → Port Forwarding
- Internet → Port Forwarding

---

### **4. ADICIONAR REGRAS**

**Regra 1: HTTP (Porta 80)**

```
Nome/Descrição: Auronex HTTP
Porta Externa: 80
Porta Interna: 80
IP Interno: 192.168.0.100
Protocolo: TCP
Status: Ativado
```

**Regra 2: HTTPS (Porta 443)**

```
Nome/Descrição: Auronex HTTPS
Porta Externa: 443
Porta Interna: 443
IP Interno: 192.168.0.100
Protocolo: TCP
Status: Ativado
```

**Regra 3: SSH (Porta 22) - OPCIONAL**

```
Nome/Descrição: SSH Servidor
Porta Externa: 22
Porta Interna: 22
IP Interno: 192.168.0.100
Protocolo: TCP
Status: Ativado
```

---

### **5. SALVAR E REINICIAR**

```
1. Clique "Salvar" ou "Aplicar"
2. Aguarde 30 segundos
3. Roteador pode reiniciar (normal)
```

---

## 🔍 **EXEMPLOS POR MARCA**

### **TP-Link:**
```
Advanced → NAT Forwarding → Virtual Servers
→ Add
→ Service Port: 80
→ Internal Port: 80
→ IP Address: 192.168.0.100
→ Protocol: TCP
→ Status: Enabled
→ Save
```

### **D-Link:**
```
Advanced → Port Forwarding
→ Name: Auronex
→ Public Port: 80
→ Private Port: 80
→ Traffic Type: TCP
→ Private IP: 192.168.0.100
→ Schedule: Always
→ Apply
```

### **Intelbras:**
```
Avançado → NAT → Redirecionamento de Portas
→ Nome: Auronex
→ Porta Externa: 80
→ IP Interno: 192.168.0.100
→ Porta Interna: 80
→ Protocolo: TCP
→ Aplicar
```

---

## ✅ **TESTAR SE FUNCIONOU**

### **Teste 1: Interno (Rede Local)**

**No notebook servidor:**
```bash
# Verificar se Nginx responde
curl http://192.168.0.100

# Deve retornar HTML do site
```

### **Teste 2: Externo (Internet)**

**Use seu celular (4G - não WiFi!):**
```
Acesse: http://179.118.172.82

Deve abrir o site Auronex!
```

**Se funcionar:** Port Forwarding OK! ✅

---

## ⚠️ **PROBLEMAS COMUNS**

### **Não encontro Port Forwarding:**
```
→ Procure "Virtual Server"
→ Ou "NAT"
→ Ou veja manual do roteador
```

### **Roteador pede senha:**
```
→ Use senha da etiqueta do roteador
→ Ou resete roteador (botão reset 10s)
```

### **Teste externo não funciona:**
```
→ Verifique se regras estão ativas
→ Reinicie roteador
→ Verifique firewall do servidor
```

---

## 🔐 **SEGURANÇA**

**Após configurar:**

1. **Mude senha do roteador** (não deixe admin/admin!)
2. **Configure firewall** no servidor (ufw)
3. **Use SSL/HTTPS** (Cloudflare ou Certbot)

---

## 🎯 **RESUMO RÁPIDO**

```
1. Acesse: http://192.168.0.1
2. Login: admin/admin
3. Procure: Port Forwarding ou NAT
4. Adicione:
   - Porta 80 → 192.168.0.100:80
   - Porta 443 → 192.168.0.100:443
5. Salvar e aplicar
6. Testar com celular (4G)
```

---

**Seu IP: 179.118.172.82**  
**Configure Port Forwarding e teste!** 🚀


