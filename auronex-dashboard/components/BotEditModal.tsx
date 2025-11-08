'use client'

import { useState, useEffect } from 'react'
import { createPortal } from 'react-dom'
import { X, Loader2 } from 'lucide-react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { botsApi, exchangeApi } from '@/lib/api'
import { toast } from 'sonner'
import { motion, AnimatePresence } from 'framer-motion'
import { EXCHANGES, TIMEFRAMES, STRATEGIES } from '@/lib/constants'
import { useTradingStore } from '@/stores/tradingStore'
import type { Bot } from '@/types'

interface BotEditModalProps {
  isOpen: boolean
  onClose: () => void
  bot: Bot
}

/**
 * Modal de Edição de Bot - ENTERPRISE
 * ✅ Editar exchange
 * ✅ Editar múltiplas cryptos
 * ✅ Editar estratégia, timeframe, etc
 * ✅ Validação completa
 */
export function BotEditModal({ isOpen, onClose, bot }: BotEditModalProps) {
  const queryClient = useQueryClient()
  const { limits, currency } = useTradingStore()
  const [mounted, setMounted] = useState(false)
  
  // ✅ Conversão
  const COTACAO = 5.0
  const toMoeda = (usd: number) => currency === 'BRL' ? usd * COTACAO : usd
  const toUSD = (valor: number) => currency === 'BRL' ? valor / COTACAO : valor
  const simbolo = currency === 'BRL' ? 'R$' : '$'
  
  // ✅ Saldo da exchange
  const [saldoExchange, setSaldoExchange] = useState<number>(0)
  const [carregandoSaldo, setCarregandoSaldo] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // Form state - inicializa com dados do bot
  const [name, setName] = useState(bot.name)
  const [exchange, setExchange] = useState(bot.exchange)
  const [symbols, setSymbols] = useState<string[]>(bot.symbols || [])
  const [strategy, setStrategy] = useState(bot.strategy)
  const [timeframe, setTimeframe] = useState(bot.timeframe)
  const [capital, setCapital] = useState(bot.capital)
  const [stopLoss, setStopLoss] = useState(bot.stop_loss_percent)
  const [takeProfit, setTakeProfit] = useState(bot.take_profit_percent)
  const [isTestnet, setIsTestnet] = useState(bot.is_testnet ?? true)
  const [searchTerm, setSearchTerm] = useState('')  // ✅ Busca de cryptos
  const [botSpeed, setBotSpeed] = useState<'ultra' | 'hunter' | 'scalper'>('ultra')  // ✅ NOVO: Velocidade

  // ✅ Buscar saldo quando exchange mudar
  useEffect(() => {
    if (isOpen && exchange) {
      setCarregandoSaldo(true)
      exchangeApi.getBalance(exchange.toLowerCase())
        .then(balance => {
          setSaldoExchange(balance.total_usd || 0)
          setCarregandoSaldo(false)
        })
        .catch(() => {
          setSaldoExchange(0)
          setCarregandoSaldo(false)
        })
    }
  }, [isOpen, exchange])

  // Resetar form quando bot mudar
  useEffect(() => {
    if (bot) {
      setName(bot.name)
      setExchange(bot.exchange)
      setSymbols(bot.symbols || [])
      setStrategy(bot.strategy)
      setTimeframe(bot.timeframe)
      // ✅ Converter capital USD → moeda selecionada
      setCapital(toMoeda(bot.capital))
      setStopLoss(bot.stop_loss_percent)
      setTakeProfit(bot.take_profit_percent)
      setIsTestnet(bot.is_testnet ?? true)
      
      // ✅ NOVO: Detectar velocidade baseado em configuração
      const speed = (bot as any).analysis_interval || 5
      if (speed <= 1) setBotSpeed('scalper')
      else if (speed <= 3) setBotSpeed('hunter')
      else setBotSpeed('ultra')
    }
  }, [bot])

  // Buscar símbolos disponíveis da exchange selecionada
  const { data: availableSymbols, isLoading: loadingSymbols } = useQuery({
    queryKey: ['symbols', exchange],
    queryFn: () => exchangeApi.getSymbols(exchange),
    enabled: isOpen && !!exchange,
  })

  // Mutation para atualizar bot
  const updateBotMutation = useMutation({
    mutationFn: (data: Partial<Bot>) => botsApi.update(bot.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      toast.success('Bot atualizado com sucesso!')
      onClose()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Erro ao atualizar bot')
    },
  })

  // Limites por plano
  const maxSymbols = limits?.max_symbols_per_bot || 1

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validações
    if (!name.trim()) {
      toast.error('Nome é obrigatório')
      return
    }

    if (symbols.length === 0) {
      toast.error('Selecione pelo menos 1 criptomoeda')
      return
    }

    if (symbols.length > maxSymbols) {
      toast.error(`Máximo de ${maxSymbols} criptomoedas no plano ${limits?.plan.toUpperCase()}`)
      return
    }

    if (capital <= 0) {
      toast.error('Capital deve ser maior que zero')
      return
    }

    // ✅ VALIDAÇÃO (apenas se saldo > 0, senão testnet pode estar offline)
    if (saldoExchange > 0) {
      const capitalUSD = toUSD(capital)
      
      if (capitalUSD > saldoExchange) {
        const saldoMoeda = toMoeda(saldoExchange)
        toast.error(
          `🚫 Capital maior que saldo!\n\n` +
          `Saldo ${exchange.toUpperCase()}: ${simbolo} ${saldoMoeda.toFixed(2)}\n` +
          `Você quer: ${simbolo} ${capital.toFixed(2)}`,
          { duration: 8000 }
        )
        return
      }
    } else {
      // Testnet offline - permitir mas avisar
      console.warn(`[${exchange}] Testnet offline - validação ignorada`)
    }

    // ✅ Converter velocidade
    const speedMap = { ultra: 5, hunter: 3, scalper: 1 }
    const analysisInterval = speedMap[botSpeed]

    // ✅ Converter capital para USD antes de salvar!
    const capitalUSD = toUSD(capital)

    // Atualizar bot
    updateBotMutation.mutate({
      name: name.trim(),
      exchange,
      symbols,
      strategy,
      timeframe,
      capital: capitalUSD,  // ✅ Sempre envia USD para backend
      stop_loss_percent: stopLoss,
      take_profit_percent: takeProfit,
      is_testnet: isTestnet,
      analysis_interval: analysisInterval,
      hunter_mode: botSpeed !== 'ultra',
    })
  }

  // Handle symbol toggle
  const toggleSymbol = (symbol: string) => {
    if (symbols.includes(symbol)) {
      setSymbols(symbols.filter((s) => s !== symbol))
    } else {
      if (symbols.length >= maxSymbols) {
        toast.warning(`Limite de ${maxSymbols} cryptos atingido (Plano ${limits?.plan.toUpperCase()})`)
        return
      }
      setSymbols([...symbols, symbol])
    }
  }

  // Filtrar cryptos pela busca
  const filteredSymbols = availableSymbols?.filter((symbol) =>
    symbol.toLowerCase().includes(searchTerm.toLowerCase())
  ) || []

  if (!isOpen || !mounted) return null

  // ✅ PORTAL - Renderiza no body (fora de containers!)
  return createPortal(
    <AnimatePresence>
      <div 
        role="dialog"
        aria-modal="true"
        className="fixed inset-0 z-[99999] flex items-center justify-center p-4"
        style={{ zIndex: 99999, position: 'fixed' }}
      >
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="modal-backdrop absolute inset-0 bg-black/90 backdrop-blur-md"
          style={{ zIndex: 99998, position: 'fixed' }}
        />

        {/* Modal - ENTERPRISE (altura maior, sempre visível) */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative w-full max-w-4xl h-[95vh] overflow-hidden"
          style={{ zIndex: 99999 }}
        >
          <div className="card h-full flex flex-col p-8">
            {/* Header */}
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-white">
                  Editar Bot
                </h2>
                <p className="mt-1 text-sm text-gray-400">
                  Configure as definições do bot de trading
                </p>
              </div>

              <button
                onClick={onClose}
                className="rounded-lg p-2 text-gray-400 hover:bg-dark-700 hover:text-white transition-colors"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Form - Scrollable com botões fixos no fim */}
            <form onSubmit={handleSubmit} className="flex flex-col flex-1 overflow-hidden">
              <div className="flex-1 overflow-y-auto space-y-6 pr-2">
              {/* Nome */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Nome do Bot *
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Ex: Bot Trader 1"
                  className="input"
                  required
                />
              </div>

              {/* Exchange */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Exchange *
                </label>
                <select
                  value={exchange}
                  onChange={(e) => {
                    setExchange(e.target.value)
                    setSymbols([]) // Limpar símbolos ao mudar exchange
                  }}
                  className="input"
                  required
                >
                  {EXCHANGES.map((ex) => (
                    <option key={ex.value} value={ex.value}>
                      {ex.label}
                    </option>
                  ))}
                </select>
                <p className="mt-1 text-xs text-gray-500">
                  ⚠️ Ao mudar a exchange, as criptomoedas serão resetadas
                </p>
              </div>

              {/* Criptomoedas */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Criptomoedas * ({symbols.length}/{maxSymbols})
                </label>
                
                {loadingSymbols ? (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="h-6 w-6 animate-spin text-accent-500" />
                    <span className="ml-2 text-sm text-gray-400">
                      Carregando cryptos de {exchange}...
                    </span>
                  </div>
                ) : (
                  <div className="rounded-xl border border-dark-600 bg-dark-800 p-4">
                    {/* Busca de cryptos - ENTERPRISE! */}
                    <div className="mb-3">
                      <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="🔍 Buscar criptomoeda... (ex: BTC, ETH, SOL)"
                        className="input text-sm"
                      />
                    </div>

                    <div className="mb-3 flex items-center justify-between">
                      <span className="text-sm text-gray-400">
                        {filteredSymbols.length} de {availableSymbols?.length || 0} em {exchange.toUpperCase()}
                      </span>
                      {symbols.length >= maxSymbols && (
                        <span className="text-xs text-yellow-500">
                          Limite atingido ({symbols.length}/{maxSymbols})
                        </span>
                      )}
                    </div>

                    <div className="grid grid-cols-4 gap-2 max-h-64 overflow-y-auto">
                      {filteredSymbols.length === 0 ? (
                        <div className="col-span-4 py-8 text-center text-sm text-gray-500">
                          {searchTerm ? `Nenhuma crypto encontrada para &quot;${searchTerm}&quot;` : 'Nenhuma crypto disponível'}
                        </div>
                      ) : (
                        filteredSymbols.map((symbol) => (
                          <button
                            key={symbol}
                            type="button"
                            onClick={() => toggleSymbol(symbol)}
                            className={`
                              rounded-lg px-3 py-2 text-sm font-medium transition-all
                              ${
                                symbols.includes(symbol)
                                  ? 'bg-accent-500 text-white shadow-lg shadow-accent-500/50'
                                  : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
                              }
                            `}
                          >
                            {symbol.replace('/USDT', '').replace('/BTC', '').replace('/BRL', '')}
                          </button>
                        ))
                      )}
                    </div>

                    {/* Info helper */}
                    {searchTerm && filteredSymbols.length > 0 && (
                      <p className="mt-2 text-xs text-gray-500">
                        ✅ {filteredSymbols.length} resultados para &quot;{searchTerm}&quot;
                      </p>
                    )}
                  </div>
                )}
              </div>

              {/* VELOCIDADE DO BOT - NOVO! ⭐ */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  ⚡ Velocidade do Bot *
                </label>
                <div className="grid grid-cols-3 gap-3">
                  <button
                    type="button"
                    onClick={() => setBotSpeed('ultra')}
                    className={`
                      rounded-lg border px-4 py-3 text-sm font-medium transition-all
                      ${botSpeed === 'ultra' 
                        ? 'border-accent-500 bg-accent-500/20 text-accent-500 shadow-lg shadow-accent-500/30' 
                        : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-accent-500/50 hover:text-white'
                      }
                    `}
                  >
                    <div className="text-center">
                      <div className="text-lg mb-1">📈</div>
                      <div className="font-semibold">Ultra Rápido</div>
                      <div className="text-xs opacity-75">5s · Balanceado</div>
                    </div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setBotSpeed('hunter')}
                    className={`
                      rounded-lg border px-4 py-3 text-sm font-medium transition-all
                      ${botSpeed === 'hunter' 
                        ? 'border-yellow-500 bg-yellow-500/20 text-yellow-500 shadow-lg shadow-yellow-500/30' 
                        : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-yellow-500/50 hover:text-white'
                      }
                    `}
                  >
                    <div className="text-center">
                      <div className="text-lg mb-1">🎯</div>
                      <div className="font-semibold">Caçador</div>
                      <div className="text-xs opacity-75">3s · Agressivo</div>
                    </div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setBotSpeed('scalper')}
                    className={`
                      rounded-lg border px-4 py-3 text-sm font-medium transition-all
                      ${botSpeed === 'scalper' 
                        ? 'border-red-500 bg-red-500/20 text-red-500 shadow-lg shadow-red-500/30' 
                        : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-red-500/50 hover:text-white'
                      }
                    `}
                  >
                    <div className="text-center">
                      <div className="text-lg mb-1">⚡</div>
                      <div className="font-semibold">Scalper</div>
                      <div className="text-xs opacity-75">1s · Ultra</div>
                    </div>
                  </button>
                </div>
                <p className="mt-2 text-xs text-gray-500">
                  {botSpeed === 'ultra' && '✅ Recomendado para iniciantes · 10-20 trades/dia · Win rate 60-65%'}
                  {botSpeed === 'hunter' && '🎯 Caça micro oscilações · 20-40 trades/dia · Win rate 65-70%'}
                  {botSpeed === 'scalper' && '⚡ Máxima velocidade · 50-100+ trades/dia · Win rate 60-65%'}
                </p>
              </div>

              {/* Estratégia e Timeframe */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Estratégia *
                  </label>
                  <select
                    value={strategy}
                    onChange={(e) => setStrategy(e.target.value)}
                    className="input"
                    required
                  >
                    {STRATEGIES.map((s) => (
                      <option key={s.value} value={s.value}>
                        {s.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Timeframe *
                  </label>
                  <select
                    value={timeframe}
                    onChange={(e) => setTimeframe(e.target.value)}
                    className="input"
                    required
                  >
                    {TIMEFRAMES.map((tf) => (
                      <option key={tf.value} value={tf.value}>
                        {tf.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Capital */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Capital ({currency}) *
                </label>
                <input
                  type="number"
                  value={capital}
                  onChange={(e) => setCapital(Number(e.target.value))}
                  min="1"
                  step="0.01"
                  className="input"
                  required
                />
              </div>

              {/* Stop Loss e Take Profit */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Stop Loss (%) *
                  </label>
                  <input
                    type="number"
                    value={stopLoss}
                    onChange={(e) => setStopLoss(Number(e.target.value))}
                    min="0.1"
                    max="50"
                    step="0.1"
                    className="input"
                    required
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Take Profit (%) *
                  </label>
                  <input
                    type="number"
                    value={takeProfit}
                    onChange={(e) => setTakeProfit(Number(e.target.value))}
                    min="0.1"
                    max="100"
                    step="0.1"
                    className="input"
                    required
                  />
                </div>
              </div>

              {/* Testnet */}
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="testnet-edit"
                  checked={isTestnet}
                  onChange={(e) => setIsTestnet(e.target.checked)}
                  className="h-4 w-4 rounded border-dark-600 bg-dark-800 text-accent-500 focus:ring-2 focus:ring-accent-500 focus:ring-offset-0"
                />
                <label htmlFor="testnet-edit" className="text-sm text-gray-300">
                  Usar Testnet (recomendado para testes)
                </label>
              </div>
              </div>

              {/* Buttons - FIXO NO FIM (sempre visível!) */}
              <div className="flex gap-3 pt-6 border-t border-white/10 mt-6">
                <button
                  type="button"
                  onClick={onClose}
                  className="btn-secondary flex-1"
                  disabled={updateBotMutation.isPending}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                  disabled={updateBotMutation.isPending}
                >
                  {updateBotMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Salvando...
                    </>
                  ) : (
                    'Salvar Alterações'
                  )}
                </button>
              </div>
            </form>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>,
    document.body  // ✅ PORTAL - Renderiza no body, não no container!
  )
}

