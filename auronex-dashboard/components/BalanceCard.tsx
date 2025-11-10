'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Wallet } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'
import { cn } from '@/lib/utils'
import type { Balance } from '@/types'

interface BalanceCardProps {
  balance: Balance
  currency?: 'USD' | 'BRL'
  className?: string
}

/**
 * Card de Saldo
 * ✅ Mostra saldo total
 * ✅ Breakdown de moedas
 * ✅ Variação 24h
 */
export function BalanceCard({
  balance,
  currency = 'USD',
  className = '',
}: BalanceCardProps) {
  const [lucroTrades, setLucroTrades] = useState(0)
  
  // ✅ Buscar lucro dos trades
  useEffect(() => {
    fetch('/api/trades/stats', { credentials: 'include' })
      .then(r => r.json())
      .then(data => setLucroTrades(data.total_profit || 0))
      .catch(() => setLucroTrades(0))
  }, [balance])
  
  // ✅ Saldo Total = Exchange + Lucro Trades
  const saldoExchange = balance?.total_usd || 0
  const saldoComTrades = saldoExchange + lucroTrades
  
  const isPositive = lucroTrades >= 0
  const conversionRate = currency === 'BRL' ? 5.0 : 1.0
  const symbol = currency === 'BRL' ? 'R$' : '$'

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn('card card-glow p-6', className)}
    >
      {/* Animated glow */}
      <div className="absolute -top-24 -right-24 h-48 w-48 animate-pulse-glow rounded-full bg-accent-500/10 blur-3xl" />

      <div className="relative">
        {/* Header */}
        <div className="mb-4 flex items-center gap-2">
          <Wallet className="h-5 w-5 text-accent-500" />
          <h3 className="text-sm font-medium uppercase tracking-wider text-gray-400">
            Saldo Total
          </h3>
        </div>

        {/* Balance - COM LUCRO DOS TRADES! */}
        <div className="mb-4 flex items-baseline gap-3">
          <span className="text-5xl font-light text-white tabular-nums">
            {symbol}{' '}
            {(saldoComTrades * conversionRate).toLocaleString('en-US', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </span>

          {lucroTrades !== 0 && (
            <span
              className={cn(
                'flex items-center gap-1 text-sm font-medium',
                isPositive ? 'text-profit-500' : 'text-loss-500'
              )}
            >
              {isPositive ? (
                <TrendingUp className="h-4 w-4" />
              ) : (
                <TrendingDown className="h-4 w-4" />
              )}
              {Math.abs(lucroTrades * conversionRate).toFixed(2)}
            </span>
          )}
        </div>

        {/* Breakdown */}
        <div className="space-y-3 border-t border-white/5 pt-4">
          {/* USDT */}
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">USDT</span>
            <span className="font-medium text-white tabular-nums">
              {formatCurrency(balance.usdt * conversionRate, currency)}
            </span>
          </div>

          {/* BTC */}
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">BTC</span>
            <span className="font-medium text-white tabular-nums">
              {balance.btc.toFixed(8)} BTC
            </span>
          </div>

          {/* ETH */}
          {balance.eth > 0 && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">ETH</span>
              <span className="font-medium text-white tabular-nums">
                {balance.eth.toFixed(6)} ETH
              </span>
            </div>
          )}

          {/* BNB */}
          {balance.bnb > 0 && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">BNB</span>
              <span className="font-medium text-white tabular-nums">
                {balance.bnb.toFixed(4)} BNB
              </span>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  )
}

