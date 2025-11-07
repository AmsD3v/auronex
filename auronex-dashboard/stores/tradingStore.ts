/**
 * Trading Store - Zustand
 * Gerencia estado dos bots e trading
 */

import { create } from 'zustand'
import type { Bot, Balance, ProfileLimits } from '@/types'

interface TradingState {
  // State
  bots: Bot[]
  selectedBot: Bot | null
  balance: Balance | null
  limits: ProfileLimits | null
  currency: 'USD' | 'BRL'
  selectedSymbols: string[]

  // Actions
  setBots: (bots: Bot[]) => void
  addBot: (bot: Bot) => void
  updateBot: (id: number, updates: Partial<Bot>) => void
  removeBot: (id: number) => void
  setSelectedBot: (bot: Bot | null) => void
  toggleBot: (id: number) => void
  setBalance: (balance: Balance) => void
  setLimits: (limits: ProfileLimits) => void
  setCurrency: (currency: 'USD' | 'BRL') => void
  setSelectedSymbols: (symbols: string[]) => void
  addSymbol: (symbol: string) => void
  removeSymbol: (symbol: string) => void
}

export const useTradingStore = create<TradingState>((set) => ({
  // Initial state
  bots: [],
  selectedBot: null,
  balance: null,
  limits: null,
  currency: 'BRL',  // ✅ Padrão BRL
  selectedSymbols: [],

  // Set bots
  setBots: (bots) => set({ bots }),

  // Add bot
  addBot: (bot) =>
    set((state) => ({
      bots: [...state.bots, bot],
    })),

  // Update bot
  updateBot: (id, updates) =>
    set((state) => ({
      bots: state.bots.map((bot) =>
        bot.id === id ? { ...bot, ...updates } : bot
      ),
      selectedBot:
        state.selectedBot?.id === id
          ? { ...state.selectedBot, ...updates }
          : state.selectedBot,
    })),

  // Remove bot
  removeBot: (id) =>
    set((state) => ({
      bots: state.bots.filter((bot) => bot.id !== id),
      selectedBot: state.selectedBot?.id === id ? null : state.selectedBot,
    })),

  // Set selected bot
  setSelectedBot: (bot) => set({ selectedBot: bot }),

  // Toggle bot
  toggleBot: (id) =>
    set((state) => ({
      bots: state.bots.map((bot) =>
        bot.id === id ? { ...bot, is_active: !bot.is_active } : bot
      ),
    })),

  // Set balance
  setBalance: (balance) => set({ balance }),

  // Set limits
  setLimits: (limits) => set({ limits }),

  // Set currency
  setCurrency: (currency) => set({ currency }),

  // Set selected symbols
  setSelectedSymbols: (symbols) => set({ selectedSymbols: symbols }),

  // Add symbol
  addSymbol: (symbol) =>
    set((state) => ({
      selectedSymbols: [...state.selectedSymbols, symbol],
    })),

  // Remove symbol
  removeSymbol: (symbol) =>
    set((state) => ({
      selectedSymbols: state.selectedSymbols.filter((s) => s !== symbol),
    })),
}))

