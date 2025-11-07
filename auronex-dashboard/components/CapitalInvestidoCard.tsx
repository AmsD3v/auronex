'use client'

import { useTradingStore } from '@/stores/tradingStore'
import { formatCurrency } from '@/lib/utils'
import { TrendingUp } from 'lucide-react'
import type { Bot } from '@/types'

interface CapitalInvestidoCardProps {
  bots: Bot[]
  currency: 'USD' | 'BRL'
}

/**
 * Card: Capital Investido
 * Soma capital de TODOS os bots ATIVOS
 */
export function CapitalInvestidoCard({ bots, currency }: CapitalInvestidoCardProps) {
  // ✅ Somar capital APENAS dos bots ATIVOS
  const capitalInvestido = bots
    .filter(bot => bot.is_active)
    .reduce((sum, bot) => sum + (bot.capital || 0), 0)
  
  // Número de bots ativos
  const botsAtivos = bots.filter(bot => bot.is_active).length
  
  return (
    <div className="card p-6">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-gray-400">💰 Capital Investido</p>
        <TrendingUp className="h-5 w-5 text-accent-500" />
      </div>

      {/* Valor total investido */}
      <div className="mb-6">
        <p className="text-4xl font-light text-white">
          {formatCurrency(capitalInvestido, currency)}
        </p>
        <p className="mt-1 text-xs text-gray-500">
          {botsAtivos} bot{botsAtivos !== 1 ? 's' : ''} ativo{botsAtivos !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Detalhes por bot ativo */}
      {bots.filter(bot => bot.is_active).length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-medium uppercase tracking-wider text-gray-400 mb-3">
            Alocação por Bot
          </p>
          {bots
            .filter(bot => bot.is_active)
            .map(bot => (
              <div key={bot.id} className="flex justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-accent-500 animate-pulse"></div>
                  <span className="text-gray-300">{bot.name}</span>
                  <span className="text-xs text-gray-500">({bot.exchange.toUpperCase()})</span>
                </div>
                <span className="font-medium text-white">
                  {formatCurrency(bot.capital || 0, currency)}
                </span>
              </div>
            ))}
        </div>
      )}

      {/* Se nenhum bot ativo */}
      {bots.filter(bot => bot.is_active).length === 0 && (
        <div className="text-center py-4">
          <p className="text-sm text-gray-500">
            Nenhum bot ativo
          </p>
          <p className="text-xs text-gray-600 mt-1">
            Ative um bot para começar a investir
          </p>
        </div>
      )}
    </div>
  )
}


