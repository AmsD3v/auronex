'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, TrendingUp, TrendingDown, Calendar, Download } from 'lucide-react'
import { useTradingStore } from '@/stores/tradingStore'
import { useCotacao } from '@/hooks/useCotacao'

interface Trade {
  id: number
  symbol: string
  entry_price: number
  exit_price: number
  quantity: number
  profit_loss: number
  entry_time: string
  exit_time: string
  status: string
}

interface TradesHistoryModalProps {
  isOpen: boolean
  onClose: () => void
}

export function TradesHistoryModal({ isOpen, onClose }: TradesHistoryModalProps) {
  const [trades, setTrades] = useState<Trade[]>([])
  const [loading, setLoading] = useState(false)
  const { currency } = useTradingStore()
  
  useEffect(() => {
    if (isOpen) {
      loadTrades()
    }
  }, [isOpen])
  
  const loadTrades = async () => {
    setLoading(true)
    try {
      // Buscar trades do MÊS atual
      const response = await fetch('/api/trades/month', { credentials: 'include' })
      if (response.ok) {
        const data = await response.json()
        setTrades(data.trades || [])
      }
    } catch (error) {
      console.error('Erro ao carregar trades:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const cotacaoReal = useCotacao()
  const cotacao = currency === 'BRL' ? cotacaoReal : 1.0
  const symbol = currency === 'BRL' ? 'R$' : '$'
  
  if (!isOpen) return null
  
  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="card w-full max-w-4xl max-h-[80vh] overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-white/10 p-6">
            <div className="flex items-center gap-3">
              <Calendar className="h-6 w-6 text-accent-500" />
              <h2 className="text-2xl font-semibold text-white">
                📊 Trades do Mês
              </h2>
            </div>
            <button
              onClick={onClose}
              className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-white/10 hover:text-white"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          
          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[60vh]">
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-accent-500 border-r-transparent"></div>
                <p className="mt-4 text-gray-400">Carregando...</p>
              </div>
            ) : trades.length > 0 ? (
              <div className="space-y-3">
                {trades.map((trade) => (
                  <motion.div
                    key={trade.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="rounded-lg border border-white/10 bg-dark-800/50 p-4"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-lg font-semibold text-white">{trade.symbol}</p>
                        <p className="text-xs text-gray-500">
                          {new Date(trade.entry_time).toLocaleString('pt-BR')}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className={`text-xl font-bold ${trade.profit_loss >= 0 ? 'text-profit-500' : 'text-loss-500'}`}>
                          {trade.profit_loss >= 0 ? '+' : ''}{symbol} {Math.abs(trade.profit_loss * cotacao).toFixed(2)}
                        </p>
                        <p className="text-xs text-gray-500">{trade.status}</p>
                      </div>
                    </div>
                    <div className="mt-3 grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Entrada</p>
                        <p className="text-white">${trade.entry_price.toFixed(8)}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Saída</p>
                        <p className="text-white">${trade.exit_price?.toFixed(8) || '-'}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Quantidade</p>
                        <p className="text-white">{trade.quantity.toFixed(8)}</p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-400">Nenhum trade este mês</p>
              </div>
            )}
          </div>
          
          {/* Footer */}
          <div className="border-t border-white/10 p-4 flex justify-between items-center">
            <p className="text-sm text-gray-400">
              Total: {trades.length} trades
            </p>
            <button className="btn-secondary text-sm">
              <Download className="h-4 w-4 mr-2" />
              Exportar CSV
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}

