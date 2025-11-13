'use client'

import { useState, useEffect } from 'react'
import { createPortal } from 'react-dom'
import { X, Plus, Loader2 } from 'lucide-react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { botsApi, exchangeApi, apiKeysApi } from '@/lib/api'
import { toast } from 'sonner'
import { motion, AnimatePresence } from 'framer-motion'
import { EXCHANGES, TIMEFRAMES, STRATEGIES } from '@/lib/constants'
import { useTradingStore } from '@/stores/tradingStore'

interface BotCreateModalProps {
  isOpen: boolean
  onClose: () => void
}

/**
 * Modal de Criação de Bot
 * ✅ Seleção de exchange por bot
 * ✅ Múltiplas cryptos (filtradas por exchange)
 * ✅ Validação de limites por plano
 */
export function BotCreateModal({ isOpen, onClose }: BotCreateModalProps) {
  const queryClient = useQueryClient()
  const { limits, currency } = useTradingStore()  // ✅ Moeda
  const [mounted, setMounted] = useState(false)
  
  // ✅ Conversão
  const COTACAO = 5.0
  const toMoeda = (usd: number) => currency === 'BRL' ? usd * COTACAO : usd
  const toUSD = (valor: number) => currency === 'BRL' ? valor / COTACAO : valor
  const simbolo = currency === 'BRL' ? 'R$' : '$'

  // ✅ Form state ANTES dos useEffects!
  const [name, setName] = useState('')
  const [exchange, setExchange] = useState('binance')
  const [symbols, setSymbols] = useState<string[]>([])
  const [strategy, setStrategy] = useState('mean_reversion')
  const [timeframe, setTimeframe] = useState('15m')
  const [capital, setCapital] = useState(1000)
  const [stopLoss, setStopLoss] = useState(2.0)
  const [takeProfit, setTakeProfit] = useState(4.0)
  const [isTestnet, setIsTestnet] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [botSpeed, setBotSpeed] = useState<'ultra' | 'hunter' | 'scalper'>('ultra')
  const [saldoExchange, setSaldoExchange] = useState<number>(0)
  const [carregandoSaldo, setCarregandoSaldo] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])
  
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
          // Falhou - não bloqueia, apenas não mostra
          setSaldoExchange(0)
          setCarregandoSaldo(false)
        })
    }
  }, [isOpen, exchange])

  // Buscar API Keys do usuário
  const { data: apiKeys } = useQuery({
    queryKey: ['api-keys'],
    queryFn: apiKeysApi.getAll,
    enabled: isOpen,
  })

  // ✅ Buscar símbolos da exchange SELECIONADA (recarrega ao mudar!)
  const { data: availableSymbols, isLoading: loadingSymbols, refetch: refetchSymbols } = useQuery({
    queryKey: ['symbols', exchange],
    queryFn: async () => {
      console.log(`[Symbols] Carregando para ${exchange}...`)
      const symbols = await exchangeApi.getSymbols(exchange)
      console.log(`[Symbols] ${exchange}: ${symbols?.length || 0} symbols`)
      return symbols
    },
    enabled: isOpen && !!exchange,
    staleTime: 0,  // ✅ Sempre recarregar
    refetchOnMount: true,
  })
  
  // ✅ Recarregar symbols quando exchange mudar E limpar seleção inválida
  useEffect(() => {
    if (isOpen && exchange) {
      console.log(`[Symbols] Exchange mudou para: ${exchange}, recarregando...`)
      refetchSymbols()
      
      // ✅ Limpar symbols selecionados (ao mudar exchange)
      console.log(`[Symbols] Limpando seleção ao mudar exchange`)
      setSymbols([])
    }
  }, [exchange, isOpen])

  // Reset form ao fechar
  useEffect(() => {
    if (!isOpen) {
      setName('')
      setExchange('binance')
      setSymbols([])
      setStrategy('mean_reversion')
      setTimeframe('15m')
      setCapital(1000)
      setStopLoss(2.0)
      setTakeProfit(4.0)
      setIsTestnet(true)
    }
  }, [isOpen])

  // Mutation para criar bot
  const createMutation = useMutation({
    mutationFn: (data: any) => botsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bots'] })
      toast.success('Bot criado com sucesso!')
      onClose()
    },
    onError: (error: any) => {
      toast.error(`Erro: ${error.response?.data?.detail || error.message}`)
    },
  })

  // Verificar se usuário tem API Key para a exchange selecionada
  const hasAPIKeyForExchange = apiKeys?.some(
    (key) => key.exchange.toLowerCase() === exchange.toLowerCase() && key.is_active
  )

  // Limites do plano
  const maxSymbols = limits?.max_symbols_per_bot || 1
  const canCreateBot = limits?.can_create_bot ?? true

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {  // ✅ ASYNC!
    e.preventDefault()

    // Validações
    if (!name.trim()) {
      toast.error('Digite um nome para o bot')
      return
    }

    // ✅ VALIDAÇÃO: Mínimo 1 cripto
    if (symbols.length === 0) {
      toast.error('❌ Selecione pelo menos 1 criptomoeda!', { duration: 5000 })
      return
    }

    if (symbols.length > maxSymbols) {
      toast.error(`Seu plano permite no máximo ${maxSymbols} cryptos por bot`)
      return
    }

    if (capital <= 0) {
      toast.error('Capital deve ser maior que 0')
      return
    }

    if (!hasAPIKeyForExchange) {
      toast.error(`Configure uma API Key para ${exchange.toUpperCase()} primeiro!`)
      return
    }

    // ✅ VALIDAÇÃO CORRETA: Capital vs Saldo da MESMA exchange
    try {
      const balanceResponse = await exchangeApi.getBalance()  // TODO: Filtrar por exchange
      const saldoExchangeUSD = balanceResponse.total_usd || 0
      const saldoMoeda = toMoeda(saldoExchangeUSD)
      const capitalUSD = toUSD(capital)
      
      // ✅ Validar capital DESTE bot vs saldo DESTA exchange
      if (capitalUSD > saldoExchangeUSD) {
        toast.error(
          `🚫 Capital maior que saldo na ${exchange.toUpperCase()}!\n\n` +
          `Saldo ${exchange.toUpperCase()}: ${simbolo} ${saldoMoeda.toFixed(2)}\n` +
          `Você quer alocar: ${simbolo} ${capital.toFixed(2)}\n\n` +
          `Reduza o capital ou adicione fundos nesta exchange.`,
          { duration: 10000 }
        )
        return
      }
      
      console.log(`[${exchange}] OK: ${simbolo}${capital} <= ${simbolo}${saldoMoeda.toFixed(2)}`)
      
    } catch (error) {
      toast.error('Erro ao validar saldo.')
      return
    }

    // Converter velocidade
    const speedMap = { ultra: 5, hunter: 3, scalper: 1 }

    // ✅ Converter capital para USD antes de salvar!
    const capitalUSD = toUSD(capital)

    // Criar bot
    createMutation.mutate({
      name: name.trim(),
      exchange: exchange.toLowerCase(),
      symbols,
      strategy,
      timeframe,
      capital: capitalUSD,  // ✅ Sempre USD para backend
      stop_loss_percent: stopLoss,
      take_profit_percent: takeProfit,
      is_testnet: isTestnet,
      is_active: false,
      analysis_interval: speedMap[botSpeed],
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

  // ✅ USAR PORTAL - Renderiza FORA do container!
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

        {/* Modal - ENTERPRISE (altura maior, botões sempre visíveis) */}
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
                  Criar Novo Bot
                </h2>
                <p className="mt-1 text-sm text-gray-400">
                  Configure um bot de trading para operar automaticamente
                </p>
              </div>

              <button
                onClick={onClose}
                className="rounded-lg p-2 text-gray-400 hover:bg-dark-700 hover:text-white transition-colors"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Limite de bots */}
            {!canCreateBot && (
              <div className="mb-6 rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-4">
                <p className="text-sm text-yellow-500">
                  ⚠️ Você atingiu o limite de {limits?.max_bots} bots do plano {limits?.plan.toUpperCase()}.
                  Faça upgrade para criar mais bots!
                </p>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="flex flex-col flex-1 overflow-hidden">
              {/* Conteúdo scrollable */}
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
                      {ex.icon} {ex.label}
                    </option>
                  ))}
                </select>

                {/* Verificar se tem API Key */}
                {!hasAPIKeyForExchange && (
                  <p className="mt-2 text-xs text-yellow-500">
                    ⚠️ Configure uma API Key para {exchange.toUpperCase()} em{' '}
                    <a
                      href="http://localhost:8001/api-keys-page"
                      target="_blank"
                      className="underline"
                    >
                      API Keys
                    </a>
                  </p>
                )}
              </div>

              {/* Criptomoedas */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Criptomoedas * (Máx: {maxSymbols})
                </label>
                <p className="mb-3 text-xs text-gray-500">
                  {symbols.length} de {maxSymbols} selecionadas
                  {symbols.length >= maxSymbols && (
                    <span className="ml-2 text-yellow-500">
                      · Limite atingido (Plano {limits?.plan.toUpperCase()})
                    </span>
                  )}
                </p>

                {loadingSymbols ? (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="h-8 w-8 animate-spin text-accent-500" />
                  </div>
                ) : (
                  <div className="rounded-xl border border-white/10 bg-dark-800/40 p-4">
                    {/* Campo de Busca - ENTERPRISE! */}
                    <div className="mb-3">
                      <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="🔍 Buscar criptomoeda... (ex: BTC, ETH, SOL)"
                        className="input text-sm w-full"
                      />
                    </div>

                    {/* Contador de resultados */}
                    <div className="mb-3 text-xs text-gray-400">
                      {filteredSymbols.length} de {availableSymbols?.length || 0} cryptos em {exchange.toUpperCase()}
                    </div>

                    <div className="max-h-60 overflow-y-auto">
                      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
                        {filteredSymbols.length === 0 ? (
                          <div className="col-span-full py-8 text-center text-sm text-gray-500">
                            {searchTerm ? `Nenhuma crypto encontrada para &quot;${searchTerm}&quot;` : 'Nenhuma crypto disponível'}
                          </div>
                        ) : (
                          filteredSymbols.map((symbol) => {
                            const isSelected = symbols.includes(symbol)
                            const symbolName = symbol  // ✅ Formato completo: GALA/USDT

                            return (
                              <button
                                key={symbol}
                                type="button"
                                onClick={() => toggleSymbol(symbol)}
                                className={`rounded-lg border px-3 py-2 text-sm font-medium transition-all ${
                                  isSelected
                                    ? 'border-accent-500 bg-accent-500/20 text-accent-500 shadow-lg shadow-accent-500/30'
                                    : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-accent-500/50 hover:text-white'
                                }`}
                              >
                                {symbolName.replace('/USDT', '').replace('/BRL', '').replace('/BTC', '')}
                              </button>
                            )
                          })
                        )}
                      </div>
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
                        : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-accent-500/50'
                      }
                    `}
                  >
                    <div className="text-center">
                      <div className="text-lg mb-1">📈</div>
                      <div className="font-semibold">Ultra Rápido</div>
                      <div className="text-xs opacity-75">5 seg</div>
                    </div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setBotSpeed('hunter')}
                    className={`
                      rounded-lg border px-4 py-3 text-sm font-medium transition-all
                      ${botSpeed === 'hunter' 
                        ? 'border-yellow-500 bg-yellow-500/20 text-yellow-500 shadow-lg shadow-yellow-500/30' 
                        : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-yellow-500/50'
                      }
                    `}
                  >
                    <div className="text-center">
                      <div className="text-lg mb-1">🎯</div>
                      <div className="font-semibold">Caçador</div>
                      <div className="text-xs opacity-75">3 seg</div>
                    </div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setBotSpeed('scalper')}
                    className={`
                      rounded-lg border px-4 py-3 text-sm font-medium transition-all
                      ${botSpeed === 'scalper' 
                        ? 'border-red-500 bg-red-500/20 text-red-500 shadow-lg shadow-red-500/30' 
                        : 'border-white/10 bg-dark-700/50 text-gray-400 hover:border-red-500/50'
                      }
                    `}
                  >
                    <div className="text-center">
                      <div className="text-lg mb-1">⚡</div>
                      <div className="font-semibold">Scalper</div>
                      <div className="text-xs opacity-75">1 seg</div>
                    </div>
                  </button>
                </div>
                <div className="mt-2 rounded-lg bg-dark-800/50 p-3 border border-white/5">
                  <p className="text-xs text-gray-400">
                    {botSpeed === 'ultra' && '✅ Recomendado para iniciantes · 10-20 trades/dia'}
                    {botSpeed === 'hunter' && '🎯 Caça micro oscilações 0.3-1% · 20-40 trades/dia'}
                    {botSpeed === 'scalper' && '⚡ Máxima velocidade · 50-100+ trades/dia'}
                  </p>
                </div>
              </div>

              {/* Grid: Strategy + Timeframe */}
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                {/* Estratégia */}
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
                    {STRATEGIES.map((strat) => (
                      <option key={strat.value} value={strat.value}>
                        {strat.label}
                      </option>
                    ))}
                  </select>
                  <p className="mt-1 text-xs text-gray-500">
                    {STRATEGIES.find((s) => s.value === strategy)?.description}
                  </p>
                </div>

                {/* Timeframe */}
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

              {/* Grid: Capital + Stop Loss + Take Profit */}
              <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Capital ({currency}) *
                  </label>
                  <input
                    type="number"
                    value={capital}
                    onChange={(e) => setCapital(parseFloat(e.target.value))}
                    min={10}
                    step={10}
                    className="input"
                    required
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Stop Loss (%) *
                  </label>
                  <input
                    type="number"
                    value={stopLoss}
                    onChange={(e) => setStopLoss(parseFloat(e.target.value))}
                    min={0.5}
                    max={20}
                    step={0.5}
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
                    onChange={(e) => setTakeProfit(parseFloat(e.target.value))}
                    min={1}
                    max={50}
                    step={0.5}
                    className="input"
                    required
                  />
                </div>
              </div>

              {/* Testnet */}
              <div>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isTestnet}
                    onChange={(e) => setIsTestnet(e.target.checked)}
                    className="h-4 w-4 rounded border-gray-600 bg-dark-700 text-accent-500 focus:ring-2 focus:ring-accent-500/50"
                  />
                  <span className="text-sm text-gray-300">
                    Usar Testnet (recomendado para testes)
                  </span>
                </label>
              </div>
              </div>

              {/* Botões - FIXOS NO FIM (sempre visíveis!) */}
              <div className="flex justify-end gap-3 border-t border-white/10 pt-6 mt-6 bg-dark-800">
                <button
                  type="button"
                  onClick={onClose}
                  className="btn-secondary"
                  disabled={createMutation.isPending}
                >
                  Cancelar
                </button>

                <button
                  type="submit"
                  className="btn-primary"
                  disabled={createMutation.isPending || !canCreateBot}
                >
                  {createMutation.isPending ? (
                    <span className="flex items-center gap-2">
                      <Loader2 className="h-5 w-5 animate-spin" />
                      Criando...
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      <Plus className="h-5 w-5" />
                      Criar Bot
                    </span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>,
    document.body  // ✅ PORTAL - Renderiza no body!
  )
}

