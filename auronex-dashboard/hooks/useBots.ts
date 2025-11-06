/**
 * Hook de Bots
 * Operações com bots (toggle, update, etc)
 */

import { useMutation, useQueryClient } from '@tanstack/react-query'
import { botsApi } from '@/lib/api'
import { useTradingStore } from '@/stores/tradingStore'
import { toast } from 'sonner'
import type { Bot, BotConfig } from '@/types'

/**
 * Hook para operações com bots
 * ✅ Toggle (ligar/desligar)
 * ✅ Update config
 * ✅ Update symbols
 * ✅ Delete
 * ✅ Invalidação automática de cache
 */
export function useBots() {
  const queryClient = useQueryClient()
  const { updateBot, removeBot } = useTradingStore()

  // ========================================
  // TOGGLE BOT (Ligar/Desligar)
  // ========================================
  const toggleMutation = useMutation({
    mutationFn: ({ id, is_active }: { id: number; is_active: boolean }) =>
      botsApi.toggle(id, is_active),
    onMutate: async ({ id, is_active }) => {
      // Otimistic update
      updateBot(id, { is_active })
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      toast.success(`Bot ${data.is_active ? 'iniciado' : 'parado'}!`)
    },
    onError: (error: any) => {
      toast.error(`Erro: ${error.response?.data?.detail || error.message}`)
      queryClient.invalidateQueries({ queryKey: ['bots'] })
    },
  })

  // ========================================
  // UPDATE CONFIG
  // ========================================
  const updateConfigMutation = useMutation({
    mutationFn: ({ id, config }: { id: number; config: BotConfig }) =>
      botsApi.updateConfig(id, config),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      updateBot(data.id, data)
      toast.success('Configuração atualizada!')
    },
    onError: (error: any) => {
      toast.error(`Erro: ${error.response?.data?.detail || error.message}`)
    },
  })

  // ========================================
  // UPDATE SYMBOLS
  // ========================================
  const updateSymbolsMutation = useMutation({
    mutationFn: ({ id, symbols }: { id: number; symbols: string[] }) =>
      botsApi.updateSymbols(id, symbols),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      updateBot(data.id, data)
      toast.success('Criptomoedas atualizadas!')
    },
    onError: (error: any) => {
      toast.error(`Erro: ${error.response?.data?.detail || error.message}`)
    },
  })

  // ========================================
  // DELETE BOT
  // ========================================
  const deleteMutation = useMutation({
    mutationFn: (id: number) => botsApi.delete(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      removeBot(id)
      toast.success('Bot deletado!')
    },
    onError: (error: any) => {
      toast.error(`Erro: ${error.response?.data?.detail || error.message}`)
    },
  })

  // ========================================
  // CREATE BOT
  // ========================================
  const createMutation = useMutation({
    mutationFn: (data: Partial<Bot>) => botsApi.create(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      toast.success('Bot criado!')
    },
    onError: (error: any) => {
      toast.error(`Erro: ${error.response?.data?.detail || error.message}`)
    },
  })

  return {
    // Toggle
    toggle: toggleMutation.mutate,
    isToggling: toggleMutation.isPending,

    // Update config
    updateConfig: updateConfigMutation.mutate,
    isUpdatingConfig: updateConfigMutation.isPending,

    // Update symbols
    updateSymbols: updateSymbolsMutation.mutate,
    isUpdatingSymbols: updateSymbolsMutation.isPending,

    // Delete
    deleteBot: deleteMutation.mutate,
    isDeleting: deleteMutation.isPending,

    // Create
    createBot: createMutation.mutate,
    isCreating: createMutation.isPending,
  }
}

