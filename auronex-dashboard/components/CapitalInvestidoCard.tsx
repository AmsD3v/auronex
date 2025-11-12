'use client'

import { useState, useEffect } from 'react'
import { useCotacao } from '@/hooks/useCotacao'
import { useTradingStore } from '@/stores/tradingStore'
import { formatCurrency } from '@/lib/utils'
import { TrendingUp } from 'lucide-react'
import type { Bot } from '@/types'

interface CapitalInvestidoCardProps {
  bots: Bot[]
  currency: 'USD' | 'BRL'
}

/**
 * Card: Capital Investido + Lucro Líquido
 * Soma capital de bots ATIVOS + mostra ganhos/perdas
 */
export function CapitalInvestidoCard({ bots, currency }: CapitalInvestidoCardProps) {
  const [lucroTotal, setLucroTotal] = useState(0)
  
  // ✅ Buscar lucro/perda total
  useEffect(() => {
    console.log('[CapitalCard] Buscando lucro...')
    fetch('/api/trades/stats', { credentials: 'include' })
      .then(r => {
        console.log('[CapitalCard] Stats response:', r.status)
        return r.json()
      })
      .then(data => {
        console.log('[CapitalCard] Stats data:', data)
        console.log('[CapitalCard] total_profit:', data.total_profit)
        setLucroTotal(data.total_profit || 0)
      })
      .catch(err => {
        console.error('[CapitalCard] Erro:', err)
        setLucroTotal(0)
      })
  }, [])
  
  // ✅ Somar capital APENAS dos bots ATIVOS
  const capitalInvestido = bots
    .filter(bot => bot.is_active)
    .reduce((sum, bot) => sum + (bot.capital || 0), 0)
  
  // ✅ Conversão com cotação REAL!
  const cotacaoReal = useCotacao()
  
  // DEBUG COMPLETO
  console.log('[CapitalCard] Cotação REAL:', cotacaoReal)
  console.log('[CapitalCard] Capital USD:', capitalInvestido)
  console.log('[CapitalCard] Lucro USD:', lucroTotal)
  console.log('[CapitalCard] Currency:', currency)
  
  // Número de bots ativos
  const botsAtivos = bots.filter(bot => bot.is_active).length
  
  return (
    <div className="card p-6">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-400">💰 Capital Investido</p>
          <p className="text-4xl font-light text-white mt-2">
            {formatCurrency(capitalInvestido, currency)}
          </p>
          <p className="mt-1 text-xs text-gray-500">
            {botsAtivos} bot{botsAtivos !== 1 ? 's' : ''} ativo{botsAtivos !== 1 ? 's' : ''}
          </p>
        </div>
        
        {/* Lucro Líquido - ✅ Mostra valor JÁ em BRL! */}
        <div className="text-right">
          <p className="text-xs text-gray-400 mb-1">Lucro Líquido</p>
          <p className={`text-2xl font-bold ${lucroTotal >= 0 ? 'text-profit-500' : 'text-loss-500'}`}>
            {lucroTotal >= 0 ? '+' : ''}{currency === 'BRL' ? 'R$' : '$'} {Math.abs(lucroTotal * cotacaoReal).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {lucroTotal >= 0 ? '📈' : '📉'} {capitalInvestido > 0 ? ((lucroTotal / capitalInvestido) * 100).toFixed(2) : '0.00'}%
          </p>
        </div>
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



