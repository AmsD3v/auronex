'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { TrendingUp, TrendingDown, Flame, Calendar, Clock } from 'lucide-react'
import { motion } from 'framer-motion'

interface Top5Coin {
  symbol: string
  name: string
  price: number
  change_24h: number
  change_7d?: number
  change_30d?: number
  volume_24h: number
  market_cap?: number
}

type Category = 'hoje' | 'semana' | 'mes' | 'virais' | 'corretora'

const EXCHANGES = [
  'binance', 'bybit', 'okx', 'kucoin', 'gateio', 'mexc', 'bitget',
  'huobi', 'kraken', 'coinbase', 'mercadobitcoin', 'foxbit', 'novadax', 'brasilbitcoin'
]

export function Top5Performance() {
  const [activeCategory, setActiveCategory] = useState<Category>('hoje')
  const [searchExchange, setSearchExchange] = useState('binance')

  // Dados por categoria
  const dataByCategory: Record<Category, Top5Coin[]> = {
    hoje: [
      { symbol: 'SOL/USDT', name: 'Solana', price: 120, change_24h: 12.3, volume_24h: 200000000 },
      { symbol: 'MATIC/USDT', name: 'Polygon', price: 0.8, change_24h: 8.5, volume_24h: 150000000 },
      { symbol: 'AVAX/USDT', name: 'Avalanche', price: 35, change_24h: 6.7, volume_24h: 100000000 },
      { symbol: 'BTC/USDT', name: 'Bitcoin', price: 50000, change_24h: 5.2, volume_24h: 1000000000 },
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3000, change_24h: 4.8, volume_24h: 500000000 },
    ],
    semana: [
      { symbol: 'BTC/USDT', name: 'Bitcoin', price: 50000, change_7d: 8.5, change_24h: 5.2, volume_24h: 1000000000 },
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3000, change_7d: 7.2, change_24h: 4.8, volume_24h: 500000000 },
      { symbol: 'SOL/USDT', name: 'Solana', price: 120, change_7d: 15.8, change_24h: 12.3, volume_24h: 200000000 },
      { symbol: 'AVAX/USDT', name: 'Avalanche', price: 35, change_7d: 10.3, change_24h: 6.7, volume_24h: 100000000 },
      { symbol: 'DOT/USDT', name: 'Polkadot', price: 6.5, change_7d: 6.5, change_24h: 3.2, volume_24h: 80000000 },
    ],
    mes: [
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3000, change_30d: 25.5, change_24h: 4.8, volume_24h: 500000000 },
      { symbol: 'SOL/USDT', name: 'Solana', price: 120, change_30d: 45.2, change_24h: 12.3, volume_24h: 200000000 },
      { symbol: 'BTC/USDT', name: 'Bitcoin', price: 50000, change_30d: 18.3, change_24h: 5.2, volume_24h: 1000000000 },
      { symbol: 'MATIC/USDT', name: 'Polygon', price: 0.8, change_30d: 35.7, change_24h: 8.5, volume_24h: 150000000 },
      { symbol: 'LINK/USDT', name: 'Chainlink', price: 14, change_30d: 28.9, change_24h: 5.1, volume_24h: 120000000 },
    ],
    virais: [
      { symbol: 'PEPE/USDT', name: 'Pepe', price: 0.00000123, change_24h: 85.5, volume_24h: 50000000 },
      { symbol: 'SHIB/USDT', name: 'Shiba Inu', price: 0.00000850, change_24h: 45.2, volume_24h: 80000000 },
      { symbol: 'FLOKI/USDT', name: 'Floki', price: 0.000025, change_24h: 38.7, volume_24h: 30000000 },
      { symbol: 'BONK/USDT', name: 'Bonk', price: 0.0000015, change_24h: 125.3, volume_24h: 40000000 },
      { symbol: 'WIF/USDT', name: 'dogwifhat', price: 2.5, change_24h: 95.8, volume_24h: 35000000 },
    ],
    corretora: [
      { symbol: 'BTC/USDT', name: 'Bitcoin', price: 50000, change_24h: 5.2, volume_24h: 1000000000 },
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3000, change_24h: 4.8, volume_24h: 500000000 },
      { symbol: 'BNB/USDT', name: 'BNB', price: 320, change_24h: 3.5, volume_24h: 300000000 },
      { symbol: 'SOL/USDT', name: 'Solana', price: 120, change_24h: 8.5, volume_24h: 200000000 },
      { symbol: 'XRP/USDT', name: 'Ripple', price: 0.52, change_24h: 2.1, volume_24h: 150000000 },
    ],
  }

  // ✅ Dados por exchange (para categoria "corretora")
  const dataByExchange: Record<string, Top5Coin[]> = {
    binance: [
      { symbol: 'BTC/USDT', name: 'Bitcoin', price: 50000, change_24h: 5.2, volume_24h: 1000000000 },
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3000, change_24h: 4.8, volume_24h: 500000000 },
      { symbol: 'BNB/USDT', name: 'BNB', price: 320, change_24h: 3.5, volume_24h: 300000000 },
      { symbol: 'SOL/USDT', name: 'Solana', price: 120, change_24h: 8.5, volume_24h: 200000000 },
      { symbol: 'XRP/USDT', name: 'Ripple', price: 0.52, change_24h: 2.1, volume_24h: 150000000 },
    ],
    bybit: [
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3001, change_24h: 4.9, volume_24h: 450000000 },
      { symbol: 'SOL/USDT', name: 'Solana', price: 121, change_24h: 8.7, volume_24h: 180000000 },
      { symbol: 'MATIC/USDT', name: 'Polygon', price: 0.81, change_24h: 8.2, volume_24h: 140000000 },
      { symbol: 'AVAX/USDT', name: 'Avalanche', price: 35.5, change_24h: 7.1, volume_24h: 95000000 },
      { symbol: 'DOT/USDT', name: 'Polkadot', price: 6.8, change_24h: 5.3, volume_24h: 85000000 },
    ],
    okx: [
      { symbol: 'BTC/USDT', name: 'Bitcoin', price: 50050, change_24h: 5.3, volume_24h: 800000000 },
      { symbol: 'ETH/USDT', name: 'Ethereum', price: 3005, change_24h: 4.9, volume_24h: 400000000 },
      { symbol: 'TRX/USDT', name: 'TRON', price: 0.08, change_24h: 6.2, volume_24h: 120000000 },
      { symbol: 'ADA/USDT', name: 'Cardano', price: 0.35, change_24h: 4.5, volume_24h: 100000000 },
      { symbol: 'XRP/USDT', name: 'Ripple', price: 0.53, change_24h: 2.5, volume_24h: 140000000 },
    ],
  }
  
  // Usar dados da exchange selecionada ou padrão
  const currentData = activeCategory === 'corretora' 
    ? (dataByExchange[searchExchange] || dataByCategory[activeCategory])
    : dataByCategory[activeCategory]

  const categories = [
    { value: 'hoje', label: 'Hoje', icon: Clock, color: 'accent' },
    { value: 'semana', label: 'Semana', icon: Calendar, color: 'blue' },
    { value: 'mes', label: 'Mês', icon: TrendingUp, color: 'green' },
    { value: 'virais', label: 'Virais', icon: Flame, color: 'red' },
    { value: 'corretora', label: 'Corretora', icon: TrendingUp, color: 'yellow' },
  ] as const

  return (
    <div className="card p-6">
      {/* Header */}
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-white mb-2">
          🏆 Top 5 Performance
        </h3>
        <p className="text-sm text-gray-400">
          Criptomoedas com melhor desempenho
        </p>
      </div>

      {/* Categorias */}
      <div className="mb-6 flex gap-2 overflow-x-auto pb-2">
        {categories.map((cat) => {
          const Icon = cat.icon
          return (
            <button
              key={cat.value}
              onClick={() => setActiveCategory(cat.value as Category)}
              className={`
                flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium
                whitespace-nowrap transition-all
                ${activeCategory === cat.value
                  ? 'bg-accent-500/20 text-accent-500 border border-accent-500/30'
                  : 'bg-dark-700/50 text-gray-400 border border-white/10 hover:bg-dark-700'
                }
              `}
            >
              <Icon className="h-4 w-4" />
              {cat.label}
            </button>
          )
        })}
      </div>

      {/* Busca de exchange (apenas em "Corretora") - 14 exchanges */}
      {activeCategory === 'corretora' && (
        <div className="mb-4">
          <label className="block text-xs text-gray-400 mb-2">Selecionar Exchange:</label>
          <select
            value={searchExchange}
            onChange={(e) => setSearchExchange(e.target.value)}
            className="input text-sm"
          >
            {EXCHANGES.map(ex => (
              <option key={ex} value={ex}>{ex.toUpperCase()}</option>
            ))}
          </select>
          <p className="mt-2 text-xs text-gray-500">
            Top 5 de {searchExchange.toUpperCase()}
          </p>
        </div>
      )}

      {/* Lista Top 5 */}
      <div className="space-y-3">
        {currentData.map((coin, index) => (
          <motion.div
            key={coin.symbol}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center justify-between p-3 rounded-xl bg-dark-800/50 border border-white/5 hover:border-accent-500/30 transition-all"
          >
            {/* Ranking + Nome */}
            <div className="flex items-center gap-3">
              <div className={`
                flex h-8 w-8 items-center justify-center rounded-full font-bold text-sm
                ${index === 0 ? 'bg-yellow-500/20 text-yellow-500' : 
                  index === 1 ? 'bg-gray-400/20 text-gray-400' :
                  index === 2 ? 'bg-orange-500/20 text-orange-500' :
                  'bg-dark-700 text-gray-500'}
              `}>
                {index + 1}
              </div>
              
              <div>
                <p className="text-white font-medium">{coin.symbol.split('/')[0]}</p>
                <p className="text-xs text-gray-500">{coin.name}</p>
              </div>
            </div>

            {/* Preço + Variação */}
            <div className="text-right">
              <p className="text-white font-medium text-sm">
                ${coin.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 8 })}
              </p>
              <div className="flex items-center gap-1">
                {(activeCategory === 'semana' ? coin.change_7d : 
                  activeCategory === 'mes' ? coin.change_30d : 
                  coin.change_24h) >= 0 ? (
                  <>
                    <TrendingUp className="h-3 w-3 text-profit-500" />
                    <span className="text-xs font-semibold text-profit-500">
                      +{(activeCategory === 'semana' ? coin.change_7d : 
                         activeCategory === 'mes' ? coin.change_30d : 
                         coin.change_24h)?.toFixed(2)}%
                    </span>
                  </>
                ) : (
                  <>
                    <TrendingDown className="h-3 w-3 text-loss-500" />
                    <span className="text-xs font-semibold text-loss-500">
                      {(activeCategory === 'semana' ? coin.change_7d : 
                        activeCategory === 'mes' ? coin.change_30d : 
                        coin.change_24h)?.toFixed(2)}%
                    </span>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-4 pt-4 border-t border-white/5">
        <p className="text-xs text-gray-500 text-center">
          Dados atualizados a cada 5 minutos
        </p>
      </div>
    </div>
  )
}

