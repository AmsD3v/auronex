# 📋 MELHORIAS - IMPLEMENTADAS E PENDENTES

**Data:** 30 de Outubro de 2025  
**Status:** Em andamento - 60% completo

---

## ✅ **JÁ IMPLEMENTADO**

### **1. Cadastro com CPF + Celular + Confirmação Senha**

**Arquivos alterados:**
- `fastapi_app/models.py` - Adicionado `cpf` e `celular` ao User
- `fastapi_app/schemas.py` - Adicionado validação de CPF e confirm_password
- `fastapi_app/templates/register.html` - Adicionado 3 novos campos
- `fastapi_app/routers/pages.py` - Processamento com validação

**Funcionalidades:**
- ✅ CPF único (não permite duplicados)
- ✅ Email único
- ✅ Celular obrigatório
- ✅ Confirmação de senha obrigatória
- ✅ Formatação automática (JavaScript)
- ✅ Validação em tempo real

### **2. Fluxo de Cadastro Otimizado**

**Novo fluxo:**
```
Cadastro → Login Automático → Dashboard (Free)
```

**Implementado:**
- ✅ Criação de assinatura FREE automática
- ✅ Token JWT gerado automaticamente
- ✅ Cookie httponly configurado
- ✅ Redirecionamento para `/dashboard`

### **3. Sistema de Autenticação para Páginas**

**Arquivo criado:**
- `fastapi_app/utils/auth_pages.py`

**Funções:**
- ✅ `get_current_user_from_cookie()` - Ler usuário do cookie
- ✅ `require_auth()` - Exigir login
- ✅ `require_admin()` - Exigir admin
- ✅ `get_user_plan()` - Obter plano do usuário

---

## ⚠️ **PENDENTE (FAZER AGORA)**

### **1. Aplicar Proteção nas Páginas Privadas**

**Páginas que precisam proteção:**

```python
# fastapi_app/routers/pages.py

# ANTES (SEM PROTEÇÃO):
@router.get("/dashboard")
async def dashboard_page(request: Request):
    ...

# DEPOIS (COM PROTEÇÃO):
@router.get("/dashboard")
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    user = require_auth(request, db)  # Redireciona se não logado!
    plan = get_user_plan(request, db)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard",
        "user": user,
        "plan": plan
    })
```

**Páginas para proteger:**
- [ ] `/dashboard`
- [ ] `/api-keys-page`
- [ ] `/bots-page`
- [ ] `/admin-panel` (requer admin!)

### **2. Navbar Dinâmica**

**Arquivo:** `fastapi_app/templates/base.html`

**Mudanças necessárias:**

```html
<!-- ANTES -->
<li class="nav-item">
    <a class="nav-link" href="/login">Entrar</a>
</li>

<!-- DEPOIS -->
{% if user %}
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
            <i class="fas fa-user-circle"></i> {{ user.first_name }}
        </a>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="/dashboard">Dashboard</a></li>
            <li><a class="dropdown-item" href="/api-keys-page">API Keys</a></li>
            <li><a class="dropdown-item" href="/bots-page">Meus Bots</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item text-danger" href="/logout">Sair</a></li>
        </ul>
    </li>
{% else %}
    <li class="nav-item">
        <a class="nav-link" href="/login">Entrar</a>
    </li>
{% endif %}
```

### **3. Lógica de Upgrade de Planos**

**Arquivo:** `fastapi_app/templates/pricing.html` e `payment_choice.html`

**Lógica necessária:**

```python
# No backend (pages.py)
@router.get("/pricing")
async def pricing_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    user_plan = get_user_plan(request, db) if user else "guest"
    
    # Planos disponíveis baseado no plano atual
    available_plans = []
    
    if user_plan == "guest" or user_plan == "free":
        available_plans = ["pro", "premium"]
    elif user_plan == "pro":
        available_plans = ["premium"]
    elif user_plan == "premium":
        available_plans = []  # Nenhum upgrade disponível
    
    return templates.TemplateResponse("pricing.html", {
        "request": request,
        "user": user,
        "user_plan": user_plan,
        "available_plans": available_plans
    })
```

**No template:**

```html
<!-- Mostrar apenas planos disponíveis -->
{% if "pro" in available_plans %}
    <!-- Card Pro -->
{% endif %}

{% if "premium" in available_plans %}
    <!-- Card Premium -->
{% endif %}

{% if user_plan == "premium" %}
    <!-- Formulário de contato para plano enterprise -->
    <div class="card">
        <h4>Precisa de Mais?</h4>
        <p>Entre em contato para planos personalizados</p>
        <button>Falar com Vendas</button>
    </div>
{% endif %}
```

### **4. Textos de Upgrade**

**Mudar:**
- "Escolha Seu Plano" → "Upgrade Seu Plano"
- "Começar Grátis" → (esconder se já Free)

---

## 🔧 **PRÓXIMAS AÇÕES (ORDEM)**

### **Prioridade ALTA (Segurança):**

1. **Proteger páginas privadas** (15-20 min)
   - Aplicar `require_auth()` em todas rotas privadas
   - Aplicar `require_admin()` em `/admin-panel`
   - Redirecionar para login se não autenticado

### **Prioridade ALTA (UX):**

2. **Navbar dinâmica** (10 min)
   - Mostrar nome do usuário quando logado
   - Esconder "Entrar"
   - Dropdown com opções

3. **Lógica de planos** (20 min)
   - Pricing: Mostrar apenas upgrades disponíveis
   - Esconder downgrade
   - Formulário para Premium contact

### **Prioridade MÉDIA:**

4. **Testes completos** (30 min)
   - Testar fluxo completo
   - Testar proteções
   - Testar upgrades

---

## 📁 **ARQUIVOS QUE PRECISAM ALTERAÇÃO**

```
ALTA PRIORIDADE (Fazer AGORA):
✅ fastapi_app/models.py - CPF + Celular (FEITO)
✅ fastapi_app/schemas.py - Validação (FEITO)
✅ fastapi_app/templates/register.html - Campos (FEITO)
✅ fastapi_app/routers/pages.py - Processamento (FEITO)
✅ fastapi_app/utils/auth_pages.py - Auth helpers (FEITO)

⏳ fastapi_app/routers/pages.py - Aplicar proteção
⏳ fastapi_app/templates/base.html - Navbar dinâmica
⏳ fastapi_app/templates/pricing.html - Lógica upgrade
⏳ fastapi_app/templates/dashboard.html - Texto "Upgrade"
```

---

## 🎯 **ESTIMATIVA**

**Tempo para completar:** ~1 hora

**Breakdown:**
- Proteger rotas: 20 min
- Navbar dinâmica: 10 min
- Lógica de planos: 20 min
- Testes: 10 min

---

## 💡 **NOTAS IMPORTANTES**

### **Sobre Proteção de Rotas:**

**CRÍTICO:** Páginas sem proteção = **FALHA DE SEGURANÇA GRAVE!**

Qualquer pessoa pode acessar:
- `/dashboard` - Dados sensíveis
- `/api-keys-page` - Credenciais
- `/bots-page` - Configurações
- `/admin-panel` - Painel administrativo!

**Solução:** Aplicar `require_auth()` em TODAS essas rotas.

### **Sobre Cadastro Único:**

**Validações implementadas:**
- ✅ Email único (banco + constraint)
- ✅ CPF único (banco + constraint)
- ✅ Username único (baseado em email)

**Resultado:** Impossível duplicar cadastros!

### **Sobre Fluxo de Upgrade:**

**Regras:**
```
Free → Pode ver: Pro, Premium
Pro → Pode ver: Premium
Premium → Formulário de contato
```

**Sem downgrade:** Free e planos inferiores ficam escondidos.

---

## 🚀 **PRÓXIMO PASSO**

**Vou implementar AGORA:**

1. Proteção de rotas (CRÍTICO!)
2. Navbar dinâmica
3. Lógica de upgrade

**Tempo estimado:** 1 hora

**Após isso:** Sistema 100% seguro e com UX perfeita!

---

**Arquivo:** MELHORIAS_IMPLEMENTADAS_E_PENDENTES.md  
**Criado por:** Sistema de desenvolvimento  
**Última atualização:** 30/10/2025 08:00 AM













