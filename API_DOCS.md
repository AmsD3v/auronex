# 📡 ROBOTRADER SaaS - DOCUMENTAÇÃO DA API

**Base URL:** `https://robotrader-saas.herokuapp.com/api`

---

## **AUTENTICAÇÃO**

### **Registro**
```http
POST /auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "senha_segura_123",
  "first_name": "João",
  "last_name": "Silva"
}
```

**Response:**
```json
{
  "message": "Usuário criado com sucesso!",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### **Login**
```http
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "senha_segura_123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "email": "user@example.com",
    "first_name": "João"
  }
}
```

---

### **Refresh Token**
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## **PERFIL DO USUÁRIO**

### **Ver Perfil**
```http
GET /profile/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "email": "user@example.com",
  "plan": "pro",
  "created_at": "2025-01-27T10:00:00Z"
}
```

---

## **API KEYS (CORRETORAS)**

### **Listar API Keys**
```http
GET /api-keys/
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "exchange": "binance",
    "api_key_masked": "***ABCD",
    "is_testnet": true,
    "is_active": true,
    "created_at": "2025-01-27T10:00:00Z"
  }
]
```

---

### **Adicionar API Key**
```http
POST /api-keys/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "exchange": "binance",
  "api_key": "sua_api_key_aqui",
  "secret_key": "sua_secret_key_aqui",
  "is_testnet": true
}
```

**Response:**
```json
{
  "id": 1,
  "exchange": "binance",
  "api_key_masked": "***ABCD",
  "is_testnet": true,
  "is_active": true,
  "created_at": "2025-01-27T10:00:00Z"
}
```

---

### **Deletar API Key**
```http
DELETE /api-keys/{id}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

---

## **BOTS**

### **Listar Bots**
```http
GET /bots/
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Meu Bot Agressivo",
    "exchange": "binance",
    "symbols": ["BTCUSDT", "ETHUSDT"],
    "capital": "1000.00",
    "strategy": "mean_reversion",
    "timeframe": "15m",
    "stop_loss_percent": "1.500",
    "take_profit_percent": "3.000",
    "is_active": true,
    "created_at": "2025-01-27T10:00:00Z"
  }
]
```

---

### **Criar Bot**
```http
POST /bots/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Meu Bot Scalper",
  "exchange": "binance",
  "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
  "capital": "500.00",
  "strategy": "mean_reversion",
  "timeframe": "5m",
  "stop_loss_percent": "1.0",
  "take_profit_percent": "2.0"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Meu Bot Scalper",
  "exchange": "binance",
  "symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
  "capital": "500.00",
  "strategy": "mean_reversion",
  "timeframe": "5m",
  "stop_loss_percent": "1.000",
  "take_profit_percent": "2.000",
  "is_active": false,
  "created_at": "2025-01-27T11:00:00Z"
}
```

---

### **Iniciar Bot**
```http
POST /bots/{id}/start/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "message": "Bot iniciado!"
}
```

---

### **Parar Bot**
```http
POST /bots/{id}/stop/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "message": "Bot parado!"
}
```

---

### **Atualizar Bot**
```http
PATCH /bots/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "capital": "1500.00",
  "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Meu Bot Agressivo",
  "exchange": "binance",
  "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
  "capital": "1500.00",
  ...
}
```

---

### **Deletar Bot**
```http
DELETE /bots/{id}/
Authorization: Bearer {access_token}
```

**Response:** `204 No Content`

---

## **TRADES**

### **Listar Trades**
```http
GET /trades/
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "symbol_display": "BTCUSDT",
    "side": "buy",
    "entry_price": "42500.00",
    "exit_price": "43200.00",
    "quantity": "0.01",
    "profit_loss": "7.00",
    "profit_loss_percent": "1.65",
    "entry_time": "2025-01-27T10:00:00Z",
    "exit_time": "2025-01-27T10:15:00Z",
    "status": "closed"
  },
  {
    "id": 2,
    "symbol_display": "ETHUSDT",
    "side": "buy",
    "entry_price": "2250.00",
    "exit_price": null,
    "quantity": "0.1",
    "profit_loss": null,
    "profit_loss_percent": null,
    "entry_time": "2025-01-27T11:00:00Z",
    "exit_time": null,
    "status": "open"
  }
]
```

---

### **Ver Trade Individual**
```http
GET /trades/{id}/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "symbol_display": "BTCUSDT",
  "side": "buy",
  "entry_price": "42500.00",
  "exit_price": "43200.00",
  "quantity": "0.01",
  "profit_loss": "7.00",
  "profit_loss_percent": "1.65",
  "entry_time": "2025-01-27T10:00:00Z",
  "exit_time": "2025-01-27T10:15:00Z",
  "status": "closed"
}
```

---

## **CÓDIGOS DE STATUS**

| Código | Significado |
|--------|-------------|
| 200 | OK |
| 201 | Criado |
| 204 | Sem conteúdo (delete) |
| 400 | Bad Request (dados inválidos) |
| 401 | Não autorizado (token inválido) |
| 403 | Proibido (sem permissão) |
| 404 | Não encontrado |
| 500 | Erro interno |

---

## **ERROS**

**Formato de erro:**
```json
{
  "error": "Mensagem descritiva do erro",
  "detail": {
    "campo": ["Descrição do problema"]
  }
}
```

**Exemplos:**

```json
// Token expirado
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}

// Dados inválidos
{
  "email": ["Este campo é obrigatório."],
  "password": ["Senha muito curta."]
}
```

---

## **RATE LIMITING**

```
Free: 60 requests/minuto
Pro: 300 requests/minuto
Premium: Ilimitado
```

**Header de resposta:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1234567890
```

---

## **EXEMPLOS EM CÓDIGO**

### **Python (requests)**
```python
import requests

BASE_URL = "https://robotrader-saas.herokuapp.com/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "email": "user@example.com",
    "password": "senha123"
})
token = response.json()["access"]

# Criar bot
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/bots/", 
    headers=headers,
    json={
        "name": "Meu Bot",
        "exchange": "binance",
        "symbols": ["BTCUSDT"],
        "capital": "1000"
    }
)
bot = response.json()
print(bot)
```

### **JavaScript (fetch)**
```javascript
const BASE_URL = "https://robotrader-saas.herokuapp.com/api";

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'senha123'
  })
});
const { access } = await loginResponse.json();

// Listar bots
const botsResponse = await fetch(`${BASE_URL}/bots/`, {
  headers: { 'Authorization': `Bearer ${access}` }
});
const bots = await botsResponse.json();
console.log(bots);
```

---

## **WEBHOOKS (FUTURO)**

**Receber notificações de trades:**

```http
POST https://seu-site.com/webhook
Content-Type: application/json

{
  "event": "trade.closed",
  "data": {
    "trade_id": 123,
    "symbol": "BTCUSDT",
    "profit_loss": "7.00"
  }
}
```

---

**API completa e documentada!** 🚀

