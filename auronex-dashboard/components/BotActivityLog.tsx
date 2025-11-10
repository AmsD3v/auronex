'use client'

import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { Activity, TrendingUp, TrendingDown, Clock } from 'lucide-react'

interface BotActivity {
  id: number
  bot_id: number
  bot_name: string
  timestamp: string
  action: 'analyzing' | 'buy' | 'sell' | 'hold' | 'stop_loss' | 'take_profit'
  symbol: string
  price?: number
  quantity?: number
  profit?: number
  reason?: string
}

export function BotActivityLog() {
  const [activities, setActivities] = useState<BotActivity[]>([])

  // ✅ Buscar atividades REAIS dos bots
  useEffect(() => {
    const loadActivities = async () => {
      try {
        const response = await fetch('/api/bot-activity/recent', { credentials: 'include' })
        if (response.ok) {
          const data = await response.json()
          setActivities(data)
        }
      } catch (error) {
        console.error('Erro ao carregar atividades:', error)
      }
    }
    
    loadActivities()
    
    // Atualizar a cada 5s
    const interval = setInterval(loadActivities, 5000)
    return () => clearInterval(interval)
  }, [])

  // Mock para exibir quando não houver dados
  const mockActivities: BotActivity[] = [
    {
      id: 1,
      bot_id: 38,
      bot_name: 'Bot Binance',
      timestamp: new Date().toISOString(),
      action: 'analyzing',
      symbol: 'SOL/USDT',
      reason: 'Procurando oportunidades...'
    },
    {
      id: 2,
      bot_id: 38,
      bot_name: 'Bot Binance',
      timestamp: new Date(Date.now() - 30000).toISOString(),
      action: 'hold',
      symbol: 'PEPE/USDT',
      price: 0.00000850,
      reason: 'RSI neutro (55), aguardando'
    },
  ]

  // Mock removido - usa dados reais agora!

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'buy': return '🟢'
      case 'sell': return '🔴'
      case 'analyzing': return '🔍'
      case 'hold': return '⏸️'
      case 'stop_loss': return '🛑'
      case 'take_profit': return '🎯'
      default: return '📊'
    }
  }

  const getActionColor = (action: string) => {
    switch (action) {
      case 'buy': return 'text-profit-500'
      case 'sell': return 'text-loss-500'
      case 'analyzing': return 'text-blue-500'
      case 'hold': return 'text-gray-500'
      case 'stop_loss': return 'text-red-500'
      case 'take_profit': return 'text-green-500'
      default: return 'text-gray-400'
    }
  }

  const getActionText = (action: string) => {
    const map: Record<string, string> = {
      analyzing: 'Analisando',
      buy: 'Comprando',
      sell: 'Vendendo',
      hold: 'Aguardando',
      stop_loss: 'Stop Loss',
      take_profit: 'Take Profit'
    }
    return map[action] || action
  }

  return (
    <div className="card p-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold text-white mb-1">
            📊 Atividade dos Bots
          </h3>
          <p className="text-sm text-gray-400">
            Acompanhe o que seus bots estão fazendo em tempo real
          </p>
        </div>
        <Activity className="h-6 w-6 text-accent-500 animate-pulse" />
      </div>

      {/* Lista de atividades */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        <AnimatePresence mode="popLayout">
          {activities.length > 0 ? activities.map((activity) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="flex items-start gap-3 p-3 rounded-lg bg-dark-800/50 border border-white/5 hover:border-accent-500/30 transition-all"
            >
              {/* Icon */}
              <div className="text-2xl flex-shrink-0">
                {getActionIcon(activity.action)}
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-sm font-semibold ${getActionColor(activity.action)}`}>
                    {getActionText(activity.action)}
                  </span>
                  <span className="text-xs text-gray-500">•</span>
                  <span className="text-xs text-gray-400">{activity.symbol}</span>
                </div>

                <p className="text-xs text-gray-500 mb-1">
                  {activity.bot_name}
                </p>

                {activity.reason && (
                  <p className="text-xs text-gray-400">
                    {activity.reason}
                  </p>
                )}

                {activity.price && (
                  <p className="text-xs text-white mt-1">
                    Preço: ${activity.price.toFixed(activity.price < 1 ? 8 : 2)}
                  </p>
                )}

                {activity.profit !== undefined && (
                  <div className="flex items-center gap-1 mt-1">
                    {activity.profit >= 0 ? (
                      <>
                        <TrendingUp className="h-3 w-3 text-profit-500" />
                        <span className="text-xs font-semibold text-profit-500">
                          +${activity.profit.toFixed(2)}
                        </span>
                      </>
                    ) : (
                      <>
                        <TrendingDown className="h-3 w-3 text-loss-500" />
                        <span className="text-xs font-semibold text-loss-500">
                          ${activity.profit.toFixed(2)}
                        </span>
                      </>
                    )}
                  </div>
                )}
              </div>

              {/* Timestamp */}
              <div className="text-right flex-shrink-0">
                <div className="flex items-center gap-1 text-xs text-gray-500">
                  <Clock className="h-3 w-3" />
                  {new Date(activity.timestamp).toLocaleTimeString('pt-BR', {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                  })}
                </div>
              </div>
            </motion.div>
          )) : (
            <div className="text-center py-8">
              <p className="text-gray-500">Nenhuma atividade ainda</p>
              <p className="text-xs text-gray-600 mt-1">Ative um bot para ver atividades</p>
            </div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <div className="mt-4 pt-4 border-t border-white/5">
        <p className="text-xs text-gray-500 text-center">
          ⚡ Atualizado em tempo real
        </p>
      </div>
    </div>
  )
}



