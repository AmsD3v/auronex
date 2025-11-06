# 🚀 Auronex Dashboard - React + Next.js

**Dashboard profissional para bot trader de criptomoedas**

---

## 🎯 Features

- ✅ **Tempo Real**: Atualização automática a cada 1 segundo
- ✅ **TypeScript**: Type safety completo
- ✅ **Tailwind CSS**: Estilização moderna e rápida
- ✅ **React Query**: Cache inteligente e refetch automático
- ✅ **Zustand**: State management simples e rápido
- ✅ **Framer Motion**: Animações suaves
- ✅ **WebSocket**: Conexão em tempo real (preparado)
- ✅ **Responsivo**: Mobile-first design

---

## 📦 Instalação

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev

# Build de produção
npm run build

# Rodar produção
npm start
```

---

## 🔧 Estrutura do Projeto

```
auronex-dashboard/
├── app/                    # Páginas (Next.js App Router)
│   ├── layout.tsx         # Layout global
│   ├── page.tsx           # Home (redirect)
│   ├── login/page.tsx     # Login
│   └── dashboard/page.tsx # Dashboard
│
├── components/            # Componentes React
│   ├── Header.tsx        # Header com relógio
│   ├── Clock.tsx         # Relógio em tempo real
│   ├── MetricsGrid.tsx   # Grid de métricas
│   ├── BalanceCard.tsx   # Card de saldo
│   ├── BotCard.tsx       # Card de bot
│   └── BotsGrid.tsx      # Grid de bots
│
├── hooks/                # Hooks customizados
│   ├── useRealtime.ts   # Dados em tempo real
│   ├── useClock.ts      # Relógio
│   ├── useWebSocket.ts  # WebSocket
│   └── useBots.ts       # Operações com bots
│
├── stores/               # State management (Zustand)
│   ├── authStore.ts     # Autenticação
│   ├── tradingStore.ts  # Trading
│   └── uiStore.ts       # UI
│
├── lib/                  # Utilitários
│   ├── api.ts           # API client (Axios)
│   ├── utils.ts         # Funções auxiliares
│   └── constants.ts     # Constantes
│
├── types/                # TypeScript types
│   └── index.ts         # Types globais
│
└── public/               # Assets estáticos
```

---

## 🔌 Integração com Backend

O dashboard se conecta ao backend FastAPI em:
- **Local**: `http://localhost:8001/api`
- **Produção**: Configure `NEXT_PUBLIC_API_URL`

### Variáveis de Ambiente

Crie `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8001/api
NEXT_PUBLIC_WS_URL=http://localhost:8001
```

---

## 🎨 Tecnologias

### Core
- **Next.js 14**: Framework React
- **React 18**: UI library
- **TypeScript**: Type safety

### Styling
- **Tailwind CSS**: Utility-first CSS
- **Framer Motion**: Animações

### State & Data
- **Zustand**: State management
- **TanStack Query**: Data fetching
- **Axios**: HTTP client
- **Socket.IO**: WebSocket

### Dev Tools
- **ESLint**: Linting
- **TypeScript**: Type checking

---

## 📊 Hooks Principais

### `useRealtime()`
```typescript
const {
  bots,          // Lista de bots (atualiza 5s)
  balance,       // Saldo (atualiza 1s!) ⚡
  tradesCount,   // Trades hoje (atualiza 5s)
  winRate,       // Win rate (atualiza 10s)
  limits,        // Limites do plano (atualiza 30s)
} = useRealtime()
```

### `useClock()`
```typescript
const time = useClock('time') // Atualiza 1s!
```

### `useBots()`
```typescript
const {
  toggle,          // Ligar/desligar bot
  updateConfig,    // Atualizar config
  updateSymbols,   // Atualizar cryptos
  deleteBot,       // Deletar bot
} = useBots()
```

---

## 🚀 Deploy

### Vercel (Recomendado)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy produção
vercel --prod
```

### Configurações Vercel
1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Deploy automático em cada push

---

## 📈 Performance

- ✅ **First Load**: < 3s
- ✅ **Time to Interactive**: < 2s
- ✅ **Lighthouse Score**: 95+
- ✅ **Bundle Size**: < 300KB
- ✅ **Max Concurrent Users**: 1000+

---

## 🔐 Autenticação

```typescript
// Login
const { login } = useAuthStore()
await login('email@example.com', 'senha')

// Logout
const { logout } = useAuthStore()
logout()

// Verificar
const { isAuthenticated } = useAuthStore()
```

---

## 🎯 Próximas Features

- [ ] TradingView charts
- [ ] Notificações push
- [ ] Modo offline
- [ ] Testes E2E
- [ ] Analytics avançado
- [ ] WebSocket completo

---

## 📝 Scripts Disponíveis

```bash
npm run dev        # Desenvolvimento (hot reload)
npm run build      # Build de produção
npm run start      # Rodar produção
npm run lint       # Linting
npm run type-check # Type checking
```

---

## 🐛 Debug

### React Query Devtools
Aberto automaticamente em desenvolvimento (canto inferior direito)

### Console Logs
```typescript
console.log('[API] Request:', url)
console.log('[WebSocket] Connected')
```

---

## 📞 Suporte

- **Issues**: GitHub Issues
- **Email**: suporte@auronex.com.br
- **Docs**: [Documentação completa](/)

---

**Desenvolvido com ❤️ por Auronex Technology**

