/**
 * Hook para cotação USD/BRL em tempo real
 */
import { useQuery } from '@tanstack/react-query'

export function useCotacao() {
  const { data } = useQuery({
    queryKey: ['cotacao-usd-brl'],
    queryFn: async () => {
      const response = await fetch('/api/cotacao/usd-brl', { credentials: 'include' })
      const data = await response.json()
      console.log('[Cotacao] USD/BRL:', data.valor)
      return data
    },
    refetchInterval: 5 * 60 * 1000, // Atualiza a cada 5 min
    staleTime: 5 * 60 * 1000,
  })
  
  return data?.valor || 5.0  // Fallback 5.0 se não carregar
}

