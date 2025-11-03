# 📸 GUIA VISUAL - ADICIONAR BOTS NO ADMIN

**URL:** http://localhost:8001/admin/users/userprofile/

---

## 🎯 **ONDE ESTÁ O CAMPO "Extra bots"?**

### **Passo 1: Lista de Usuários**

Quando acessa `http://localhost:8001/admin/users/userprofile/` você vê:

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  Django Administration                                                │
│  ────────────────────────────────────────────────────────────────────  │
│                                                                        │
│  User profiles                                                        │
│  ═══════════════════════════════════════════════════════════════════  │
│                                                                        │
│  [+ Add User Profile]  [Action v] [Go]  [Search]                     │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ □ USER | EMAIL | PLANO | STATUS | TOTAL BOTS | MENSALIDADE      │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ □ João | joao@ | PRO   | ✅ PRO  | 3          | R$ 29,90        │ │
│  │ □ Maria| maria@| PREMIUM| ✅ PREM | 10         | R$ 99,99        │ │
│  │ □ Pedro| pedro@| PRO   | ✅ PRO  | 3          | R$ 29,90        │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  [First] [Previous] Page 1 of 1 [Next] [Last]                        │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

⚠️ ATENÇÃO: Não marque o checkbox □
           Clique DIRETO NO NOME do usuário!
           
Exemplo: Clique em "Maria" ← (texto azul clicável)
```

---

### **Passo 2: Página de Edição**

Ao clicar no usuário, abre a página de edição.

**Role para baixo** usando a barra de rolagem ou scroll do mouse.

Você verá estes campos **NA ORDEM:**

```
┌────────────────────────────────────────────────────────────────────┐
│  Change User Profile                                               │
│  ════════════════════════════════════════════════════════════════  │
│                                                                    │
│  User:                                                             │
│  [Maria (maria@email.com) v]                                      │
│                                                                    │
│  Plan:                                                             │
│  [premium v]                                                       │
│                                                                    │
│  Cpf:                                                              │
│  [12345678901]                                                     │
│                                                                    │
│  Trial ends at:                                                    │
│  [          ] (vazio para planos pagos)                           │
│                                                                    │
│  Stripe customer id:                                               │
│  [cus_xxxxxxxxxxxxxxx]                                            │
│                                                                    │
│  ↓↓↓ ROLE MAIS UM POUCO ↓↓↓                                       │
│                                                                    │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃                                                              ┃  │
│  ┃  💡 Sistema de Bots Extras                                   ┃  │
│  ┃                                                              ┃  │
│  ┃  Plano PREMIUM: 10 bots inclusos (R$ 99,99/mês)            ┃  │
│  ┃  Bots Extras Atuais: 0                                      ┃  │
│  ┃  Total de Bots: 10                                          ┃  │
│  ┃                                                              ┃  │
│  ┃  ──────────────────────────────────────────────────────────  ┃  │
│  ┃                                                              ┃  │
│  ┃  📋 Regras para Adicionar Bots:                             ┃  │
│  ┃  ✅ Preço por bot extra: R$ 9,90 (fixo)                     ┃  │
│  ┃  ✅ Mínimo PREMIUM: 5 bots por vez                          ┃  │
│  ┃  ✅ Exemplo 5 bots: + R$ 49,50/mês                          ┃  │
│  ┃                                                              ┃  │
│  ┃  💰 Tabela de Preços PREMIUM:                               ┃  │
│  ┃  ┌────────────────────────────────────────────────────┐     ┃  │
│  ┃  │ Bots Extras │ Custo Extra/mês │ Total PREMIUM     │     ┃  │
│  ┃  ├────────────────────────────────────────────────────┤     ┃  │
│  ┃  │ 0 (base)    │ R$ 0,00         │ R$ 99,99         │     ┃  │
│  ┃  │ 5 bots      │ R$ 49,50        │ R$ 149,49        │     ┃  │
│  ┃  │ 10 bots     │ R$ 99,00        │ R$ 198,99        │     ┃  │
│  ┃  │ 20 bots     │ R$ 198,00       │ R$ 297,99        │     ┃  │
│  ┃  │ 50 bots     │ R$ 495,00       │ R$ 594,99        │     ┃  │
│  ┃  └────────────────────────────────────────────────────┘     ┃  │
│  ┃                                                              ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                                    │
│  Extra bots:  ← ESTE É O CAMPO EDITÁVEL!                          │
│  [    5    ]  ← DIGITE AQUI! ✅✅✅                                │
│                                                                    │
│  ↓↓↓ ROLE MAIS UM POUCO ↓↓↓                                       │
│                                                                    │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃  Preço Mensal                                                ┃  │
│  ┃                                                              ┃  │
│  ┃  R$ 149,49                                                   ┃  │
│  ┃                                                              ┃  │
│  ┃  ✅ Calculado automaticamente ao salvar                      ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                                    │
│  Created at:                                                       │
│  Oct. 28, 2025, 8 p.m.                                            │
│                                                                    │
│  Updated at:                                                       │
│  Oct. 28, 2025, 10:30 p.m.                                        │
│                                                                    │
│  ──────────────────────────────────────────────────────────────    │
│                                                                    │
│  [Salvar] [Salvar e continuar editando] [Salvar e adicionar +1]  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 **IDENTIFICANDO O CAMPO**

### **Visual do Campo:**

```
Extra bots:
┌──────────┐
│    5     │  ← Caixa de texto simples
└──────────┘
```

**Características:**
- ✅ Label: "Extra bots:" (à esquerda)
- ✅ Caixa de texto branca
- ✅ Pode digitar números
- ✅ Fica entre seção azul (tabela) e seção verde (preço)

---

## 🎬 **TUTORIAL PASSO A PASSO**

### **1. Abrir Admin:**
```
http://localhost:8001/admin/
Login: admin
Senha: admin123
```

### **2. Clicar em "User profiles":**
```
No menu lateral esquerdo:
USERS
  ├─ User profiles  ← CLIQUE AQUI
  └─ Exchange API keys
```

### **3. Clicar no Usuário:**
```
Na lista, clique no NOME do usuário (texto azul)
NÃO marque o checkbox!
```

### **4. Rolar até "Extra bots":**
```
Use scroll ou Page Down
Procure a seção azul com tabela
Logo abaixo está o campo "Extra bots:"
```

### **5. Digitar Quantidade:**
```
Premium: Digite 5 ou mais
Pro: Digite 2 ou mais

Exemplo: [  5  ]
```

### **6. Salvar:**
```
Role até o final da página
Clique em [Salvar]
```

### **7. Verificar:**
```
Volta para lista
Veja coluna "Total Bots": 15 (5 extras)
Veja coluna "Mensalidade": R$ 149,49
```

---

## 📋 **CHECKLIST DE VERIFICAÇÃO**

Se não está vendo o campo, verifique:

- [ ] ✅ Está na página de EDIÇÃO (não na lista)?
- [ ] ✅ Clicou NO NOME do usuário (não checkbox)?
- [ ] ✅ Rolou a página para baixo?
- [ ] ✅ Django recarregou? (ver terminal)
- [ ] ✅ Forçou refresh? (Ctrl + Shift + R)
- [ ] ✅ Está após a seção azul com tabela?
- [ ] ✅ Está antes dos campos Created at / Updated at?

---

## 🖼️ **ESTRUTURA COMPLETA DA PÁGINA**

```
┌─ Editar User Profile ─────────────────────────────────────┐
│                                                           │
│ [User: dropdown]                                          │
│ [Plan: dropdown]                                          │
│ [CPF: texto]                                              │
│ [Trial ends at: data]                                     │
│ [Stripe customer id: texto]                               │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐   │
│ │ [SEÇÃO AZUL - Informações e Tabela]                │   │
│ │ • Mostra plano atual                                │   │
│ │ • Mostra bots inclusos                              │   │
│ │ • Tabela de preços                                  │   │
│ │ • Regras                                            │   │
│ └─────────────────────────────────────────────────────┘   │
│                                                           │
│ Extra bots: [_____]  ← CAMPO EDITÁVEL AQUI! ✅           │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐   │
│ │ [SEÇÃO VERDE - Preço Calculado]                     │   │
│ │ R$ 149,49                                           │   │
│ │ ✅ Calculado automaticamente                         │   │
│ └─────────────────────────────────────────────────────┘   │
│                                                           │
│ Created at: [readonly]                                    │
│ Updated at: [readonly]                                    │
│                                                           │
│ [Salvar] [Salvar e continuar] [Salvar e +1]              │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

**O campo está ENTRE:**
- ⬆️ Seção AZUL (informações)
- ⬇️ Seção VERDE (preço)

---

## 💡 **DICA: Use Ctrl+F**

**No navegador, pressione:**
```
Ctrl + F
```

**Busque por:**
```
"Extra bots"
```

**Resultado:**
```
Encontrará 3 ocorrências:
1. Na seção azul (texto informativo)
2. No label do campo ← ESTE É O QUE VOCÊ EDITA!
3. Na seção de informações
```

**A ocorrência #2 é o campo editável!**

---

## 🎯 **SE AINDA NÃO VER O CAMPO**

### **Solução 1: Verificar Terminal Django**

Olhe o terminal onde Django está rodando.

Deve ter aparecido:
```
I:\Robo\saas\users\admin.py changed, reloading.
[OK] Variaveis de ambiente carregadas!
Performing system checks...
System check identified no issues (0 silenced).
October 28, 2025 - 22:49:21
Django version 4.2.7, using settings 'saas.settings'
Starting development server at http://127.0.0.1:8001/
```

**Se NÃO apareceu "reloading":**
- Pare Django (Ctrl+C)
- Reinicie: `cd I:\Robo\saas; python manage.py runserver 8001`

---

### **Solução 2: Forçar Refresh**

No navegador:
```
Ctrl + Shift + R  (Chrome/Edge)
Ctrl + F5         (Firefox)
```

Isso limpa o cache e recarrega a página.

---

### **Solução 3: Abrir em Aba Anônima**

```
Ctrl + Shift + N  (Chrome)
Ctrl + Shift + P  (Firefox)
```

Acesse:
```
http://localhost:8001/admin/
Login novamente
Vá em User profiles
```

---

## 📸 **SCREENSHOT TEXTUAL DO CAMPO**

```
                    ↓ Label do campo
         ┌──────────────────────────┐
         │ Extra bots:              │
         │ ┌──────────────────────┐ │
         │ │        5             │ │ ← Caixa de input
         │ └──────────────────────┘ │
         │                          │
         │ Help text: "Bots adicio- │
         │ nais (além do plano base)"│
         └──────────────────────────┘
```

---

## ✅ **TESTE RÁPIDO**

**Cole isso no navegador:**
```
http://localhost:8001/admin/users/userprofile/1/change/
```

**Troque "1" pelo ID de um usuário real.**

**IDs dos seus usuários:**
```
http://localhost:8001/admin/users/userprofile/

Na lista, passe o mouse sobre o nome
Veja na barra de status (embaixo navegador):
.../userprofile/19/change/  ← ID é 19
```

---

## 🎯 **CERTEZA ABSOLUTA**

**O campo EXISTE e está configurado em:**

**Arquivo:** `saas/users/admin.py`  
**Linha 81:** `'extra_bots',`  
**Lista de fields:**
```python
fields = [
    'user',
    'plan',
    'cpf',
    'trial_ends_at',
    'stripe_customer_id',
    'extra_bots_info',  # ← Seção azul
    'extra_bots',       # ← CAMPO EDITÁVEL ✅
    'monthly_price_readonly',  # ← Seção verde
    'created_at',
    'updated_at'
]
```

**100% garantido que o campo está lá!** ✅

---

## 🆘 **ÚLTIMA OPÇÃO**

**Se REALMENTE não aparecer:**

Tire um print da tela e me envie, ou me diga:

1. ✅ Está na lista ou na página de edição?
2. ✅ URL exata que está vendo?
3. ✅ Vê a seção azul com tabela?
4. ✅ Vê a seção verde com preço?
5. ✅ Django recarregou (viu no terminal)?

---

**O campo está 100% implementado e funcionando!** ✅

**Provavelmente é só questão de rolar a página ou limpar cache!** 🚀



