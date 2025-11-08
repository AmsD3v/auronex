/**
 * Hook de Tempo Real
 * Atualiza automaticamente dados do backend
 */

import { useQuery } from '@tanstack/react-query'
import { botsApi, exchangeApi, tradesApi, profileApi } from '@/lib/api'
import { useTradingStore } from '@/stores/tradingStore'
import { useAuthStore } from '@/stores/authStore'
import { REFETCH_INTERVALS } from '@/lib/constants'

/**
 * Hook principal para dados em tempo real
 * ✅ Atualiza automaticamente
 * ✅ Cache inteligente
 * ✅ Retry automático
 */
export function useRealtime() {
  const { setBots, setBalance, setLimits } = useTradingStore()
  const { isAuthenticated } = useAuthStore()

  // ========================================
  // BOTS - Atualiza a cada 5s
  // ========================================
  const {
    data: bots,
    isLoading: botsLoading,
    error: botsError,
    refetch: refetchBots,
  } = useQuery({
    queryKey: ['bots'],
    queryFn: async () => {
      const data = await botsApi.getAll()
      setBots(data)
      return data
    },
    refetchInterval: REFETCH_INTERVALS.FAST,
    staleTime: 0,
    enabled: isAuthenticated, // ✅ Só busca se autenticado!
  })

  // ========================================
  // BALANCE - Atualiza a cada 1s! ⚡
  // ========================================
  const {
    data: balance,
    isLoading: balanceLoading,
    error: balanceError,
  } = useQuery({
    queryKey: ['balance'],
    queryFn: async () => {
      const data = await exchangeApi.getBalance()
      setBalance(data)
      return data
    },
    refetchInterval: 3000, // ✅ 3 segundos (detecta trades rápido!)
    staleTime: 0,
    retry: 2,
    enabled: isAuthenticated,
    refetchOnWindowFocus: true  // ✅ Atualiza ao focar janela
  })

  // ========================================
  // TRADES HOJE - Atualiza a cada 5s
  // ========================================
  const {
    data: tradesData,
    isLoading: tradesLoading,
  } = useQuery({
    queryKey: ['trades-today'],
    queryFn: tradesApi.getToday,
    refetchInterval: 3000,  // ✅ 3s para detectar novos trades!
    staleTime: 0,
    enabled: isAuthenticated,
    refetchOnWindowFocus: true
  })

  // ========================================
  // STATS - Atualiza a cada 10s
  // ========================================
  const {
    data: stats,
    isLoading: statsLoading,
  } = useQuery({
    queryKey: ['trades-stats'],
    queryFn: tradesApi.getStats,
    refetchInterval: REFETCH_INTERVALS.NORMAL,
    staleTime: 0,
    enabled: isAuthenticated, // ✅ Só busca se autenticado!
  })

  // ========================================
  // LIMITES DO PLANO - Atualiza a cada 5s (detecta mudanças no admin!)
  // ========================================
  const {
    data: limits,
    isLoading: limitsLoading,
  } = useQuery({
    queryKey: ['profile-limits'],
    queryFn: async () => {
      const data = await profileApi.getLimits()
      setLimits(data)
      return data
    },
    refetchInterval: REFETCH_INTERVALS.FAST, // ✅ 5s para detectar mudanças rápido!
    refetchOnWindowFocus: true, // ✅ Refetch ao focar janela
    staleTime: 0,
    enabled: isAuthenticated, // ✅ Só busca se autenticado!
  })

  // ========================================
  // BOT MONITOR - Atualiza a cada 5s
  // ========================================
  const {
    data: monitor,
    isLoading: monitorLoading,
  } = useQuery({
    queryKey: ['bot-monitor'],
    queryFn: botsApi.getMonitor,
    refetchInterval: REFETCH_INTERVALS.FAST,
    staleTime: 0,
    enabled: isAuthenticated, // ✅ Só busca se autenticado!
  })

  return {
    // Bots
    bots: bots || [],
    botsLoading,
    botsError: botsError as Error | null,
    refetchBots,

    // Balance
    balance: balance || {
      usdt: 0,
      btc: 0,
      eth: 0,
      bnb: 0,
      total_usd: 0,
    },
    balanceLoading,
    balanceError: balanceError as Error | null,

    // Trades
    tradesCount: tradesData?.count || 0,
    trades: tradesData?.trades || [],
    tradesLoading,

    // Stats
    winRate: stats?.win_rate || 0,
    totalProfit: stats?.total_profit || 0,
    totalTrades: stats?.total_trades || 0,
    statsLoading,

    // Limits
    limits: limits || {
      plan: 'free',
      max_bots: 1,
      max_symbols_per_bot: 1,
      current_bots: 0,
      can_create_bot: true,
    },
    limitsLoading,

    // Monitor
    monitor: monitor || [],
    monitorLoading,

    // Loading geral
    isLoading: botsLoading || balanceLoading || tradesLoading || statsLoading || limitsLoading,
  }
}

