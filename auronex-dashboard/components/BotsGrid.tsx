'use client'

import { useState } from 'react'
import { BotCard } from './BotCard'
import { BotCreateModal } from './BotCreateModal'
import { Plus } from 'lucide-react'
import type { Bot } from '@/types'

interface BotsGridProps {
  bots: Bot[]
  className?: string
}

/**
 * Grid de Bots
 * ✅ Lista todos os bots
 * ✅ Botão para criar novo (modal integrado!)
 * ✅ Cada bot com exchange diferente
 */
export function BotsGrid({ bots, className = '' }: BotsGridProps) {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)

  if (bots.length === 0) {
    return (
      <>
        <div className={`card p-12 text-center ${className}`}>
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-accent-500/10">
            <Plus className="h-8 w-8 text-accent-500" />
          </div>
          <h3 className="mb-2 text-lg font-semibold text-white">
            Nenhum bot configurado
          </h3>
          <p className="mb-6 text-gray-400">
            Crie seu primeiro bot para começar a operar
          </p>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="btn-primary inline-flex items-center gap-2"
          >
            <Plus className="h-5 w-5" />
            Criar Bot Agora
          </button>
        </div>

        {/* Modal de criação */}
        <BotCreateModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
        />
      </>
    )
  }

  return (
    <>
      <div className={className}>
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-white">Seus Bots</h2>
            <p className="mt-1 text-sm text-gray-400">
              {bots.length} bot{bots.length !== 1 ? 's' : ''} configurado{bots.length !== 1 ? 's' : ''}
            </p>
          </div>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="btn-secondary inline-flex items-center gap-2 py-2 text-sm"
          >
            <Plus className="h-4 w-4" />
            Novo Bot
          </button>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {bots.map((bot, index) => (
            <BotCard key={bot.id} bot={bot} index={index} />
          ))}
        </div>
      </div>

      {/* Modal de criação */}
      <BotCreateModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
    </>
  )
}

