/**
 * TypeScript types para toda aplicação
 */

// ========================================
// USER & AUTH
// ========================================

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  subscription?: Subscription
  created_at: string
}

export interface Subscription {
  id: number
  plan: 'free' | 'pro' | 'premium'
  status: 'active' | 'cancelled' | 'expired'
  expires_at: string | null
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// ========================================
// BOT
// ========================================

export interface Bot {
  id: number
  name: string
  exchange: string
  symbols: string[]
  strategy: string
  timeframe: string
  capital: number
  stop_loss_percent: number
  take_profit_percent: number
  is_active: boolean
  is_testnet: boolean
  created_at: string
  updated_at: string
  user_id: number
  // ✅ NOVO: Velocidade do bot
  analysis_interval?: number
  hunter_mode?: boolean
}

export interface BotConfig {
  strategy?: string
  timeframe?: string
  stop_loss_percent?: number
  take_profit_percent?: number
  modo_cacador?: boolean
}

export interface BotMonitor {
  bot_id: number
  bot_name: string
  is_active: boolean
  last_check: string
  total_trades: number
  profit_loss: number
  status: 'running' | 'paused' | 'error'
}

// ========================================
// EXCHANGE & BALANCE
// ========================================

export interface Balance {
  usdt: number
  btc: number
  eth: number
  bnb: number
  total_usd: number
  change_24h?: number
}

export interface Ticker {
  symbol: string
  last: number
  bid: number
  ask: number
  high: number
  low: number
  volume: number
  change: number
  changePercent: number
  timestamp: number
}

export interface OHLCV {
  timestamp: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}

// ========================================
// TRADE
// ========================================

export interface Trade {
  id: number
  user_id: number
  bot_id: number
  symbol: string
  side: 'buy' | 'sell'
  entry_price: number
  exit_price: number | null
  quantity: number
  entry_time: string
  exit_time: string | null
  profit_loss: number | null
  profit_loss_percent: number | null
  signal_confidence: number
  signal_reason: string
  status: 'open' | 'closed'
}

export interface TradeStats {
  total_trades: number
  open_trades: number
  closed_trades: number
  profitable_trades: number
  losing_trades: number
  win_rate: number
  total_profit: number
  total_loss: number
  net_profit: number
  average_profit: number
  average_loss: number
  best_trade: number
  worst_trade: number
}

// ========================================
// API KEY
// ========================================

export interface APIKey {
  id: number
  exchange: string
  label: string
  is_testnet: boolean
  is_active: boolean
  created_at: string
}

export interface APIKeyDecrypted extends APIKey {
  api_key: string
  secret: string
}

// ========================================
// TOP 5
// ========================================

export interface Top5Item {
  rank: number
  symbol: string
  name: string
  price: number
  change_24h: number
  volume_24h: number
  market_cap?: number
}

// ========================================
// PORTFOLIO
// ========================================

export interface PortfolioItem {
  symbol: string
  quantity: number
  entry_price: number
  current_price: number
  value_usd: number
  profit_loss: number
  profit_loss_percent: number
  allocation_percent: number
}

export interface Portfolio {
  total_value: number
  total_invested: number
  total_profit_loss: number
  total_profit_loss_percent: number
  items: PortfolioItem[]
}

// ========================================
// PROFILE LIMITS
// ========================================

export interface ProfileLimits {
  plan: 'free' | 'pro' | 'premium'
  max_bots: number
  max_symbols_per_bot: number
  current_bots: number
  can_create_bot: boolean
}

// ========================================
// NOTIFICATION
// ========================================

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: Date
  read: boolean
}

// ========================================
// WEBSOCKET
// ========================================

export interface WebSocketMessage {
  type: 'price_update' | 'trade_update' | 'bot_status' | 'notification'
  data: any
  timestamp: number
}

// ========================================
// CHART
// ========================================

export interface ChartData {
  labels: string[]
  datasets: {
    label: string
    data: number[]
    borderColor?: string
    backgroundColor?: string
  }[]
}

