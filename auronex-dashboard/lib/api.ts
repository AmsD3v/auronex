/**
 * API Client - Axios
 * Comunicação com backend FastAPI
 */

import axios, { AxiosError, AxiosRequestConfig } from 'axios'
import type {
  LoginResponse,
  User,
  Bot,
  BotConfig,
  BotMonitor,
  Balance,
  Ticker,
  OHLCV,
  Trade,
  TradeStats,
  APIKey,
  APIKeyDecrypted,
  ProfileLimits,
} from '@/types'

// ✅ LOCAL: http://localhost:8001 → PRODUÇÃO: https://auronex.com.br
const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
const API_BASE_URL = `${BASE}/api`

// Criar instância axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token automaticamente
api.interceptors.request.use(
  (config) => {
    // Buscar token do localStorage
    if (typeof window !== 'undefined') {
      const authData = localStorage.getItem('auth-storage')
      if (authData) {
        try {
          const { state } = JSON.parse(authData)
          if (state?.token) {
            config.headers.Authorization = `Bearer ${state.token}`
          }
        } catch (error) {
          console.error('Error parsing auth data:', error)
        }
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Log de erro
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
    })
    
    // Token inválido - logout APENAS se for endpoint de auth
    if (error.response?.status === 401 && error.config?.url?.includes('/auth')) {
      if (typeof window !== 'undefined') {
        console.warn('Token inválido detectado no endpoint de auth - fazendo logout')
        localStorage.removeItem('auth-storage')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// ========================================
// AUTH API
// ========================================

export const authApi = {
  /**
   * Login do usuário
   */
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/login', {  // ✅ CORRIGIDO!
      email,
      password,
    })
    return response.data
  },

  /**
   * Logout (apenas limpa localStorage)
   */
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-storage')
    }
  },

  /**
   * Verificar se token é válido
   */
  verifyToken: async (): Promise<boolean> => {
    try {
      await api.get('/auth/me')
      return true
    } catch {
      return false
    }
  },
}

// ========================================
// BOTS API
// ========================================

export const botsApi = {
  /**
   * Buscar todos os bots do usuário
   */
  getAll: async (): Promise<Bot[]> => {
    const response = await api.get<{ bots: Bot[]; total: number } | Bot[]>('/bots/')
    // ✅ Aceitar ambos formatos
    if (Array.isArray(response.data)) {
      return response.data
    }
    return response.data.bots || []
  },

  /**
   * Buscar um bot específico
   */
  getOne: async (id: number): Promise<Bot> => {
    const response = await api.get<Bot>(`/bots/${id}`)
    return response.data
  },

  /**
   * Criar novo bot
   */
  create: async (data: Partial<Bot>): Promise<Bot> => {
    const response = await api.post<Bot>('/bots/', data)
    return response.data
  },

  /**
   * Atualizar bot - USA PATCH (FastAPI aceita agora)
   */
  update: async (id: number, data: Partial<Bot>): Promise<Bot> => {
    const response = await api.patch<Bot>(`/bots/${id}/`, data)  // ✅ COM / no fim!
    return response.data
  },

  /**
   * Deletar bot
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/bots/${id}`)
  },

  /**
   * Toggle bot (ligar/desligar)
   */
  toggle: async (id: number, is_active: boolean): Promise<Bot> => {
    const response = await api.patch<Bot>(`/bots/${id}/toggle`, {
      is_active,
    })
    return response.data
  },

  /**
   * Atualizar configuração do bot
   */
  updateConfig: async (id: number, config: BotConfig): Promise<Bot> => {
    const response = await api.patch<Bot>(`/bots/${id}/config`, config)
    return response.data
  },

  /**
   * Atualizar símbolos do bot
   */
  updateSymbols: async (id: number, symbols: string[]): Promise<Bot> => {
    const response = await api.patch<Bot>(`/bots/${id}/symbols`, {
      symbols,
    })
    return response.data
  },

  /**
   * Iniciar todos os bots
   */
  startAll: async (): Promise<void> => {
    await api.post('/bots/start-all')
  },

  /**
   * Parar todos os bots
   */
  stopAll: async (): Promise<void> => {
    await api.post('/bots/stop-all')
  },

  /**
   * Monitor de bots
   */
  getMonitor: async (): Promise<BotMonitor[]> => {
    const response = await api.get<{ bots: BotMonitor[] }>('/bot-monitor/all')
    return response.data.bots || []
  },
}

// ========================================
// EXCHANGE API
// ========================================

export const exchangeApi = {
  /**
   * Buscar saldo da exchange
   */
  getBalance: async (): Promise<Balance> => {
    const response = await api.get<Balance>('/exchange/balance')
    return response.data
  },

  /**
   * Buscar ticker de um símbolo
   */
  getTicker: async (symbol: string): Promise<Ticker> => {
    const response = await api.get<Ticker>('/exchange/ticker', {
      params: { symbol },
    })
    return response.data
  },

  /**
   * Buscar dados OHLCV (candlesticks)
   */
  getOHLCV: async (
    symbol: string,
    timeframe: string = '1h',
    limit: number = 100
  ): Promise<OHLCV[]> => {
    const response = await api.get<OHLCV[]>('/exchange/ohlcv', {
      params: { symbol, timeframe, limit },
    })
    return response.data
  },

  /**
   * Buscar todos os símbolos disponíveis
   */
  getSymbols: async (exchange: string = 'binance'): Promise<string[]> => {
    const response = await api.get<string[]>('/exchange/symbols', {
      params: { exchange },
    })
    return response.data
  },
}

// ========================================
// TRADES API
// ========================================

export const tradesApi = {
  /**
   * Buscar trades de hoje
   */
  getToday: async (): Promise<{ count: number; trades: Trade[] }> => {
    const response = await api.get<{ count: number; trades: Trade[] }>(
      '/trades/today'
    )
    return response.data
  },

  /**
   * Buscar estatísticas de trades
   */
  getStats: async (): Promise<TradeStats> => {
    const response = await api.get<TradeStats>('/trades/stats')
    return response.data
  },

  /**
   * Buscar histórico de trades
   */
  getHistory: async (limit: number = 50): Promise<Trade[]> => {
    const response = await api.get<Trade[]>('/trades/history', {
      params: { limit },
    })
    return response.data
  },

  /**
   * Buscar trades de um bot específico
   */
  getByBot: async (botId: number, limit: number = 50): Promise<Trade[]> => {
    const response = await api.get<Trade[]>(`/trades/bot/${botId}`, {
      params: { limit },
    })
    return response.data
  },
}

// ========================================
// API KEYS API
// ========================================

export const apiKeysApi = {
  /**
   * Buscar todas as API Keys do usuário
   */
  getAll: async (): Promise<APIKey[]> => {
    const response = await api.get<APIKey[]>('/api-keys/')
    return response.data
  },

  /**
   * Criar nova API Key
   */
  create: async (data: {
    exchange: string
    api_key: string
    secret: string
    label?: string
    is_testnet: boolean
  }): Promise<APIKey> => {
    const response = await api.post<APIKey>('/api-keys/', data)
    return response.data
  },

  /**
   * Deletar API Key
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api-keys/${id}`)
  },

  /**
   * Descriptografar API Key (admin only)
   */
  decrypt: async (id: number): Promise<APIKeyDecrypted> => {
    const response = await api.get<APIKeyDecrypted>(`/api-keys/${id}/decrypt`)
    return response.data
  },
}

// ========================================
// PROFILE API
// ========================================

export const profileApi = {
  /**
   * Buscar limites do plano do usuário
   */
  getLimits: async (): Promise<ProfileLimits> => {
    const response = await api.get<ProfileLimits>('/profile/limits/')
    return response.data
  },
}

// Exportar instância axios para uso direto se necessário
export default api

