'use client'

import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'
import { formatCurrency, formatPercent } from '@/lib/utils'
import { cn } from '@/lib/utils'

interface MetricsGridProps {
  totalBots: number
  activeBots: number
  balance: number
  tradesCount: number
  winRate: number
  currency?: 'USD' | 'BRL'
}

/**
 * Grid de Métricas Principais
 * ✅ 4 cards com animação
 * ✅ Hover effects
 * ✅ Formatação automática
 */
export function MetricsGrid({
  totalBots,
  activeBots,
  balance,
  tradesCount,
  winRate,
  currency = 'USD',
}: MetricsGridProps) {
  const metrics = [
    {
      label: 'Total de Bots',
      value: totalBots,
      subtitle: `${activeBots} ativos`,
      icon: '🤖',
      color: 'blue',
    },
    {
      label: 'Saldo Total',
      value: formatCurrency(balance, currency),
      subtitle: '+5.2%',
      icon: '💰',
      color: 'green',
      trending: true,
    },
    {
      label: 'Trades Hoje',
      value: tradesCount,
      subtitle: `${Math.floor(tradesCount / 2)} bots operando`,
      icon: '📈',
      color: 'purple',
    },
    {
      label: 'Taxa Sucesso',
      value: `${winRate.toFixed(1)}%`,
      subtitle: 'Win rate',
      icon: '✅',
      color: winRate >= 60 ? 'green' : 'red',
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric, index) => (
        <motion.div
          key={metric.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="metric"
        >
          <div className="flex items-start justify-between mb-4">
            <span className="text-4xl">{metric.icon}</span>
            {metric.trending && (
              <TrendingUp className="h-5 w-5 text-profit-500" />
            )}
          </div>

          <p className="metric-label">{metric.label}</p>

          <h3 className="metric-value">{metric.value}</h3>

          <p className="metric-subtitle">{metric.subtitle}</p>
        </motion.div>
      ))}
    </div>
  )
}

