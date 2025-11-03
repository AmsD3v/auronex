# 🎯 COMO ADICIONAR BOTS EXTRAS NO ADMIN

**URL:** http://localhost:8001/admin/users/userprofile/

---

## 📍 **PASSO A PASSO COM IMAGENS**

### **1. Acessar Lista de Usuários:**

```
http://localhost:8001/admin/users/userprofile/

Você verá uma lista com colunas:
┌─────────────────────────────────────────────────────────────────┐
│ USER | EMAIL | PLANO | STATUS | TOTAL BOTS | MENSALIDADE        │
├─────────────────────────────────────────────────────────────────┤
│ João | joao@ | PRO   | ✅ PRO  | 3          | R$ 29,90          │
│ Maria| maria@| PREMIUM| ✅ PREM | 10         | R$ 99,99          │
└─────────────────────────────────────────────────────────────────┘
```

---

### **2. Clicar no Usuário:**

**Clique no nome do usuário (ex: "Maria")** ou clique na linha inteira.

Abrirá a página de edição.

---

### **3. Rolar Para Baixo:**

Role a página até encontrar a seção:

```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  User:  [Maria (maria@email.com) v]                      │
│                                                           │
│  Plan:  [premium v]  ← Pode editar aqui                  │
│                                                           │
│  Cpf:   [12345678901]                                     │
│                                                           │
│  Trial ends at: [vazio]                                   │
│                                                           │
│  Stripe customer id: [cus_xxxxx]                          │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 💡 Sistema de Bots Extras                          │ │
│  │                                                     │ │
│  │ Plano PREMIUM: 10 bots inclusos (R$ 99,99/mês)    │ │
│  │ Bots Extras Atuais: 0                              │ │
│  │ Total de Bots: 10                                  │ │
│  │                                                     │ │
│  │ ───────────────────────────────────────────────    │ │
│  │                                                     │ │
│  │ 📋 Regras para Adicionar Bots:                     │ │
│  │ ✅ Preço por bot extra: R$ 9,90 (fixo)            │ │
│  │ ✅ Mínimo PREMIUM: 5 bots por vez                 │ │
│  │ ✅ Exemplo 5 bots: + R$ 49,50/mês                 │ │
│  │                                                     │ │
│  │ 💰 Tabela de Preços PREMIUM:                       │ │
│  │ ┌────────────────────────────────────────────┐    │ │
│  │ │ Bots   │ Custo Extra │ Total PREMIUM      │    │ │
│  │ ├────────────────────────────────────────────┤    │ │
│  │ │ 0      │ R$ 0,00     │ R$ 99,99          │    │ │
│  │ │ +5     │ R$ 49,50    │ R$ 149,49         │    │ │
│  │ │ +10    │ R$ 99,00    │ R$ 198,99         │    │ │
│  │ │ +20    │ R$ 198,00   │ R$ 297,99         │    │ │
│  │ │ +50    │ R$ 495,00   │ R$ 594,99         │    │ │
│  │ └────────────────────────────────────────────┘    │ │
│  │                                                     │ │
│  │ 💡 Dica: Digite a quantidade e clique Salvar      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Extra bots:  [    5    ]  ← DIGITE AQUI! ✅             │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Preço Mensal                                        │ │
│  │ R$ 149,49                                           │ │
│  │ ✅ Calculado automaticamente ao salvar              │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Created at: [2025-10-28 20:00:00]                       │
│                                                           │
│  Updated at: [2025-10-28 22:00:00]                       │
│                                                           │
│  [Salvar] [Salvar e continuar editando] [Salvar e +1]   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

### **4. Digite a Quantidade de Bots Extras:**

**No campo "Extra bots":**
- Digite: `5` (para Premium)
- Ou digite: `2` (para Pro)

**Validação automática:**
- Se Premium e < 5: ❌ Erro
- Se Pro e < 2: ❌ Erro
- Se ≥ mínimo: ✅ Salva e recalcula

---

### **5. Clicar em "Salvar":**

Clique no botão **"Salvar"** no final da página.

**O sistema:**
1. ✅ Valida se quantidade é ≥ mínimo
2. ✅ Calcula novo preço automaticamente
3. ✅ Salva no banco
4. ✅ Volta para lista mostrando novo preço

---

### **6. Verificar na Lista:**

Após salvar, você verá:

```
┌─────────────────────────────────────────────────────────────────┐
│ USER  | EMAIL  | PLANO   | STATUS  | TOTAL BOTS    | MENSALIDADE│
├─────────────────────────────────────────────────────────────────┤
│ Maria | maria@ | PREMIUM | ✅ PREM | 15 (5 extras) | R$ 149,49  │
└─────────────────────────────────────────────────────────────────┘
```

**Observe:**
- ✅ Total Bots mudou: `10` → `15 (5 extras)`
- ✅ Mensalidade mudou: `R$ 99,99` → `R$ 149,49`

---

## 🔍 **LOCALIZAÇÃO EXATA DO CAMPO**

**O campo "Extra bots" está em:**

```
Página: http://localhost:8001/admin/users/userprofile/19/change/
                                                      ↑↑
                                                      ID do usuário

Localização na página:
├── User (dropdown)
├── Plan (dropdown)
├── CPF (texto)
├── Trial ends at (data)
├── Stripe customer id (texto)
├── [SEÇÃO VISUAL AZUL COM TABELA] ← Instruções
├── Extra bots [CAMPO EDITÁVEL] ← AQUI! ✅
├── [SEÇÃO VERDE COM PREÇO] ← Preço calculado
├── Created at (readonly)
└── Updated at (readonly)
```

---

## ⚠️ **SE NÃO ESTIVER VENDO O CAMPO:**

### **Possível Causa 1: Cache do navegador**

**Solução:**
```
Ctrl + Shift + R (forçar refresh)
Ou
Ctrl + F5
```

### **Possível Causa 2: Está na lista, não na edição**

**Solução:**
```
Na lista, CLIQUE NO USUÁRIO (nome ou linha)
Não use checkbox (é para deletar)
```

### **Possível Causa 3: Django não atualizou**

**Solução:**
```
Verifique o terminal do Django
Deve ter mostrado:
"I:\Robo\saas\users\admin.py changed, reloading."
```

---

## 📊 **TABELAS QUE VÊ NO ADMIN**

### **Se usuário é PRO:**
```
Bots Extras | Custo Extra | Total PRO
─────────────────────────────────────
0 (base)    | R$ 0,00     | R$ 29,90
+2 bots     | R$ 19,80    | R$ 49,70
+5 bots     | R$ 49,50    | R$ 79,40
+10 bots    | R$ 99,00    | R$ 128,90
```

### **Se usuário é PREMIUM:**
```
Bots Extras | Custo Extra | Total PREMIUM
──────────────────────────────────────────
0 (base)    | R$ 0,00     | R$ 99,99
+5 bots     | R$ 49,50    | R$ 149,49 ✅
+10 bots    | R$ 99,00    | R$ 198,99
+20 bots    | R$ 198,00   | R$ 297,99
+50 bots    | R$ 495,00   | R$ 594,99
```

---

## ✅ **EXEMPLO COMPLETO**

### **Cenário: Cliente Premium pede +5 bots**

**1. Cliente envia email:**
```
"Olá, preciso de mais 5 bots para diversificar estratégias.
Qual o custo?"
```

**2. Você responde:**
```
"Olá! Bots extras custam R$ 9,90 cada.

Para 5 bots extras:
- Custo extra: R$ 49,50/mês
- Nova mensalidade: R$ 149,49/mês
- Total de bots: 15

Ativo agora mesmo! ✅"
```

**3. Você acessa admin:**
```
http://localhost:8001/admin/users/userprofile/

1. Clica no cliente
2. Campo "Extra bots": 0 → 5
3. Salvar
4. ✅ Pronto!
```

**4. Cliente vê no dashboard:**
```
Streamlit mostra: "Você pode criar até 15 bots"
Limite aumentado automaticamente!
```

---

## 🎯 **RESUMO**

**O campo JÁ EXISTE e está funcionando!**

**Localização:**
```
Admin → UserProfile → Clique no usuário → Role para baixo

Você verá:
1. Seção azul com tabela (informações)
2. Campo "Extra bots" (editável) ← AQUI!
3. Seção verde com preço (calculado)
```

**Se não estiver vendo:**
1. Ctrl + Shift + R (limpar cache)
2. Verificar se clicou NO usuário (não checkbox)
3. Verificar se Django recarregou (terminal)

---

**O sistema está 100% funcional! Apenas precisa encontrar o campo!** ✅

**Tente agora e me diga se encontrou!** 🚀



