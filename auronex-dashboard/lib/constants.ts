/**
 * Constantes da aplicação
 */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api'

export const REFETCH_INTERVALS = {
  REALTIME: 1000,      // 1 segundo
  FAST: 5000,          // 5 segundos
  NORMAL: 10000,       // 10 segundos
  SLOW: 30000,         // 30 segundos
} as const

export const TRADING_PROFILES = {
  HEDGE_FUND: {
    name: '🏦 Hedge Fund',
    dashboardInterval: 30,
    botInterval: 60,
    strategy: 'trend_following',
    description: 'Conservador, análises longas'
  },
  DAY_TRADER: {
    name: '📈 Day Trader',
    dashboardInterval: 5,
    botInterval: 3,
    strategy: 'mean_reversion',
    description: 'Balanceado, operações diárias'
  },
  SCALPER: {
    name: '⚡ Scalper',
    dashboardInterval: 3,
    botInterval: 1,
    strategy: 'scalping',
    description: 'Agressivo, operações rápidas'
  },
  ULTRA: {
    name: '🚀 Ultra',
    dashboardInterval: 1,
    botInterval: 1,
    strategy: 'trend_following',
    description: 'Ultra agressivo, máxima velocidade'
  },
} as const

export const EXCHANGES = [
  // Internacionais - Principais
  { value: 'binance', label: 'Binance', icon: '🟡' },
  { value: 'bybit', label: 'Bybit', icon: '🟠' },
  { value: 'okx', label: 'OKX', icon: '⚫' },
  { value: 'kucoin', label: 'KuCoin', icon: '🟢' },
  { value: 'gateio', label: 'Gate.io', icon: '🔵' },
  { value: 'mexc', label: 'MEXC', icon: '🔴' },
  { value: 'bitget', label: 'Bitget', icon: '🟣' },
  { value: 'huobi', label: 'Huobi', icon: '🟢' },
  { value: 'kraken', label: 'Kraken', icon: '🔵' },
  { value: 'coinbase', label: 'Coinbase', icon: '🔵' },
  // Brasileiras
  { value: 'mercadobitcoin', label: 'Mercado Bitcoin', icon: '🇧🇷' },
  { value: 'foxbit', label: 'Foxbit', icon: '🇧🇷' },
  { value: 'novadax', label: 'NovaDAX', icon: '🇧🇷' },
  { value: 'brasilbitcoin', label: 'Brasil Bitcoin', icon: '🇧🇷' },
] as const

export const PLANS = {
  FREE: {
    name: 'Free',
    max_bots: 1,
    max_symbols: 1,
    features: ['1 Bot', '1 Crypto', 'Testnet', '7 dias trial'],
  },
  PRO: {
    name: 'Pro',
    max_bots: 3,
    max_symbols: 5,
    features: ['3 Bots', '5 Cryptos', 'Produção', 'Suporte prioritário'],
  },
  PREMIUM: {
    name: 'Premium',
    max_bots: 10,
    max_symbols: 20,
    features: ['10 Bots', '20 Cryptos', 'API dedicada', 'Suporte 24/7', 'Analytics avançado'],
  },
} as const

export const TIMEFRAMES = [
  { value: '1m', label: '1 minuto' },
  { value: '5m', label: '5 minutos' },
  { value: '15m', label: '15 minutos' },
  { value: '1h', label: '1 hora' },
  { value: '4h', label: '4 horas' },
  { value: '1d', label: '1 dia' },
] as const

export const STRATEGIES = [
  { value: 'trend_following', label: 'Trend Following', description: 'Segue tendências de mercado' },
  { value: 'mean_reversion', label: 'Mean Reversion', description: 'Reversão à média' },
  { value: 'scalping', label: 'Scalping', description: 'Operações rápidas' },
  { value: 'arbitrage', label: 'Arbitrage', description: 'Arbitragem entre exchanges' },
] as const

