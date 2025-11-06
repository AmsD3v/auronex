'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Play, Pause, Settings, Trash2 } from 'lucide-react'
import { useBots } from '@/hooks/useBots'
import { formatCurrency } from '@/lib/utils'
import { cn } from '@/lib/utils'
import { BotEditModal } from './BotEditModal'
import type { Bot } from '@/types'

interface BotCardProps {
  bot: Bot
  index: number
}

/**
 * Card de Bot Individual
 * ✅ Toggle (ligar/desligar)
 * ✅ Informações do bot
 * ✅ Ações (editar, deletar)
 */
export function BotCard({ bot, index }: BotCardProps) {
  const { toggle, isToggling, deleteBot, isDeleting } = useBots()
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)

  const handleToggle = () => {
    toggle({ id: bot.id, is_active: !bot.is_active })
  }

  const handleDelete = () => {
    if (confirm(`Deletar bot "${bot.name}"?`)) {
      deleteBot(bot.id)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="card p-6"
    >
      {/* Header */}
      <div className="mb-4 flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white">{bot.name}</h3>
          <div className="mt-1 flex items-center gap-2">
            <span className="badge badge-info text-xs">
              🏦 {bot.exchange.toUpperCase()}
            </span>
            <span className="text-xs text-gray-500">·</span>
            <span className="text-xs text-gray-400">{bot.strategy}</span>
          </div>
        </div>

        {/* Toggle button */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={cn(
            'rounded-lg p-2 transition-colors',
            bot.is_active
              ? 'bg-profit-500/20 text-profit-500 hover:bg-profit-500/30'
              : 'bg-gray-500/20 text-gray-400 hover:bg-gray-500/30'
          )}
          title={bot.is_active ? 'Parar bot' : 'Iniciar bot'}
        >
          {bot.is_active ? (
            <Pause className="h-5 w-5" />
          ) : (
            <Play className="h-5 w-5" />
          )}
        </button>
      </div>

      {/* Info */}
      <div className="mb-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Capital</span>
          <span className="font-medium text-white">
            {formatCurrency(bot.capital)}
          </span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Timeframe</span>
          <span className="font-medium text-white">{bot.timeframe}</span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Stop Loss</span>
          <span className="font-medium text-white">
            {bot.stop_loss_percent}%
          </span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Take Profit</span>
          <span className="font-medium text-white">
            {bot.take_profit_percent}%
          </span>
        </div>
      </div>

      {/* Symbols */}
      {bot.symbols && bot.symbols.length > 0 && (
        <div className="mb-4">
          <p className="mb-2 text-xs font-medium uppercase tracking-wider text-gray-400">
            Criptomoedas ({bot.symbols.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {bot.symbols.slice(0, 5).map((symbol) => (
              <span
                key={symbol}
                className="badge badge-info text-xs"
              >
                {symbol.replace('/USDT', '').replace('/BRL', '').replace('/BTC', '')}
              </span>
            ))}
            {bot.symbols.length > 5 && (
              <span className="badge bg-gray-500/20 text-gray-400 text-xs">
                +{bot.symbols.length - 5}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Status indicator */}
      <div className="mb-4 flex items-center gap-2">
        <div
          className={cn(
            'h-2 w-2 rounded-full',
            bot.is_active ? 'bg-profit-500 animate-pulse' : 'bg-gray-500'
          )}
        />
        <span className="text-sm text-gray-400">
          {bot.is_active ? 'Ativo' : 'Pausado'}
        </span>
        {bot.is_testnet && (
          <span className="badge badge-warning ml-auto">Testnet</span>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-2 border-t border-white/5 pt-4">
        <button
          onClick={() => setIsEditModalOpen(true)}
          className="btn-secondary flex-1 py-2 text-sm"
          title="Configurações"
        >
          <Settings className="mr-1 inline-block h-4 w-4" />
          Config
        </button>

        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="btn-secondary py-2 text-sm text-loss-500 hover:bg-loss-500/20"
          title="Deletar bot"
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </div>

      {/* Modal de Edição */}
      <BotEditModal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        bot={bot}
      />
    </motion.div>
  )
}

