'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/authStore'
import { useTradingStore } from '@/stores/tradingStore'
import { useRealtime } from '@/hooks/useRealtime'
import { useHeartbeat } from '@/hooks/useHeartbeat'
import { Clock } from '@/components/Clock'
import { MetricsGrid } from '@/components/MetricsGrid'
import { BalanceCard } from '@/components/BalanceCard'
import { CapitalInvestidoCard } from '@/components/CapitalInvestidoCard'
import { BotsGrid } from '@/components/BotsGrid'
import { BotActivityLog } from '@/components/BotActivityLog'
import { Top5Performance } from '@/components/Top5Performance'
import { ThemeToggle } from '@/components/ThemeToggle'
import { LogOut, RefreshCw } from 'lucide-react'

/**
 * Dashboard Principal - COM TEMPO REAL
 * ✅ Atualiza automaticamente
 * ✅ Métricas em tempo real
 * ✅ SEM loops!
 */
export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, user, logout } = useAuthStore()
  const { currency } = useTradingStore()
  
  const [mounted, setMounted] = useState(false)
  
  // ✅ Heartbeat - Detecta quando fecha navegador
  useHeartbeat()
  
  // ✅ Hook de tempo real - Atualiza automaticamente!
  const {
    bots,
    balance,
    tradesCount,
    winRate,
    limits,
    isLoading,
    botsError,
    balanceError,
  } = useRealtime()

  // Evitar hidratação SSR
  useEffect(() => {
    setMounted(true)
  }, [])

  // Verificar autenticação APENAS uma vez
  useEffect(() => {
    if (mounted && !isAuthenticated) {
      console.log('[Dashboard] Não autenticado, redirecionando para login')
      router.push('/login')
    }
  }, [mounted, isAuthenticated, router])

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  // Não renderizar nada até montar
  if (!mounted) {
    return null
  }

  // Se não autenticado, não mostrar nada (vai redirecionar)
  if (!isAuthenticated) {
    return null
  }

  // Dashboard renderizado - VERSÃO SIMPLIFICADA
  return (
    <div className="min-h-screen bg-dark-900">
      {/* Header Simplificado */}
      <header className="sticky top-0 z-50 border-b border-white/5 bg-dark-800/50 backdrop-blur-xl">
        <div className="flex items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-2xl font-light text-white">Auronex Trading</h1>
            <p className="text-sm text-gray-400">Real-time trading platform</p>
          </div>

          <div className="flex items-center gap-6">
            {/* Clock */}
            <Clock />

            {/* User info */}
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-sm font-medium text-white">
                  {user?.first_name || user?.email || 'Usuário'}
                </p>
                <div className="flex items-center gap-2">
                  <p className="text-xs text-gray-400">
                    {user?.subscription?.plan?.toUpperCase() || 'FREE'}
                  </p>
                  {/* Seletor BRL/USD */}
                  <select
                    value={currency}
                    onChange={(e) => useTradingStore.setState({ currency: e.target.value as 'USD' | 'BRL' })}
                    className="text-xs bg-dark-700 text-gray-400 border border-white/10 rounded px-2 py-0.5"
                  >
                    <option value="BRL">BRL</option>
                    <option value="USD">USD</option>
                  </select>
                </div>
              </div>

              {/* Logout button */}
              <button
                onClick={handleLogout}
                className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-red-500/20 hover:text-red-500"
                title="Sair"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-6 py-8 relative">
        {/* Welcome message */}
        <div className="mb-8">
          <h2 className="text-3xl font-light text-white">
            Bem-vindo, {user?.first_name || 'Trader'}! 👋
          </h2>
          <p className="mt-2 text-gray-400 flex items-center gap-2">
            Acompanhe seus bots e trades em tempo real
            {isLoading && (
              <RefreshCw className="h-4 w-4 animate-spin text-accent-500" />
            )}
          </p>
        </div>

        {/* Avisos de erro (se houver) */}
        {botsError && (
          <div className="mb-6 rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-4">
            <p className="text-sm text-yellow-500">
              ⚠️ Erro ao buscar bots. Crie seu primeiro bot em:{' '}
              <a href="/bots-page" target="_blank" className="underline font-semibold">
                Gerenciar Bots
              </a>
            </p>
          </div>
        )}
        
        {balanceError && (
          <div className="mb-6 rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-4">
            <p className="text-sm text-yellow-500">
              ⚠️ Erro ao buscar saldo. Configure uma API Key em:{' '}
              <a href="/api-keys-page" target="_blank" className="underline font-semibold">
                API Keys
              </a>
            </p>
          </div>
        )}

        {/* Plan info */}
        {limits && (
          <div className="mb-6 rounded-xl border border-accent-500/30 bg-accent-500/10 p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-accent-500 font-semibold mb-1">
                  📊 Plano: {limits.plan.toUpperCase()}
                </p>
                <p className="text-xs text-gray-400">
                  {limits.current_bots} de {limits.max_bots} bots · {limits.max_symbols_per_bot} cryptos por bot
                </p>
              </div>
              <div>
                {bots.length >= limits.max_bots ? (
                  <p className="text-xs text-yellow-500">
                    ⚠️ Limite de bots atingido
                  </p>
                ) : (
                  <p className="text-xs text-accent-500 font-semibold">
                    Bots utilizados {bots.length}/{limits.max_bots}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Metrics Grid - TEMPO REAL! */}
        <MetricsGrid
          totalBots={(bots || []).length}
          activeBots={(bots || []).filter((bot) => bot.is_active).length}
          balance={balance?.total_usd || 0}
          tradesCount={tradesCount}
          winRate={winRate}
          currency={currency}
        />

        {/* Balance Card + Info */}
        <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Capital Investido (soma dos bots ativos) */}
          <div>
            <CapitalInvestidoCard bots={bots || []} currency={currency} />
          </div>

          {/* Status do Sistema */}
          <div>
            <div className="card p-6">
              <h3 className="text-xl font-semibold text-white mb-4">
                📊 Status do Sistema
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>
                    <p className="text-gray-300">Frontend React</p>
                  </div>
                  <span className="text-green-500 font-semibold text-sm">Rodando</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>
                    <p className="text-gray-300">Backend FastAPI</p>
                  </div>
                  <span className="text-green-500 font-semibold text-sm">Conectado</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`h-3 w-3 rounded-full ${isLoading ? 'bg-yellow-500' : 'bg-green-500 animate-pulse'}`}></div>
                    <p className="text-gray-300">Tempo Real</p>
                  </div>
                  <span className={`font-semibold text-sm ${isLoading ? 'text-yellow-500' : 'text-green-500'}`}>
                    {isLoading ? 'Carregando...' : 'Ativo'}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full bg-accent-500"></div>
                    <p className="text-gray-300">Atualização</p>
                  </div>
                  <span className="text-accent-500 font-semibold text-sm">1 segundo</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bots Grid - TEMPO REAL! */}
        <div className="mt-8">
          <BotsGrid bots={bots || []} />
        </div>

        {/* Top 5 Performance */}
        <div className="mt-8">
          <Top5Performance />
        </div>

        {/* Atividade dos Bots em Tempo Real - DEPOIS do Top 5 */}
        <div className="mt-8">
          <BotActivityLog />
        </div>

        {/* Links úteis */}
        <div className="mt-8 card p-6">
          <h3 className="text-xl font-semibold text-white mb-4">🔗 Links Rápidos</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a
              href="/bots-page"
              target="_blank"
              rel="noopener noreferrer"
              className="block p-4 rounded-xl bg-dark-700/50 hover:bg-dark-700 transition-all border border-white/10 hover:border-accent-500/50 hover:-translate-y-0.5"
            >
              <p className="text-white font-semibold mb-1">🤖 Gerenciar Bots</p>
              <p className="text-sm text-gray-400">Criar e configurar bots de trading</p>
            </a>
            
            <a
              href="/api-keys-page"
              target="_blank"
              rel="noopener noreferrer"
              className="block p-4 rounded-xl bg-dark-700/50 hover:bg-dark-700 transition-all border border-white/10 hover:border-accent-500/50 hover:-translate-y-0.5"
            >
              <p className="text-white font-semibold mb-1">🔑 API Keys</p>
              <p className="text-sm text-gray-400">Conectar suas exchanges</p>
            </a>
            
            <a
              href="/admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="block p-4 rounded-xl bg-dark-700/50 hover:bg-dark-700 transition-all border border-white/10 hover:border-accent-500/50 hover:-translate-y-0.5"
            >
              <p className="text-white font-semibold mb-1">👨‍💼 Admin Panel</p>
              <p className="text-sm text-gray-400">Painel administrativo</p>
            </a>
            
            <a
              href="/api/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="block p-4 rounded-xl bg-dark-700/50 hover:bg-dark-700 transition-all border border-white/10 hover:border-accent-500/50 hover:-translate-y-0.5"
            >
              <p className="text-white font-semibold mb-1">📚 API Docs</p>
              <p className="text-sm text-gray-400">Documentação da API FastAPI</p>
            </a>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 border-t border-white/5 pt-8 text-center text-sm text-gray-500">
          <p>Auronex Trading Platform · React + Next.js · v1.0.0</p>
        </footer>
      </main>
    </div>
  )
}

