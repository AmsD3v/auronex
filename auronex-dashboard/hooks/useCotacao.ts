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
      console.log('[Cotacao] USD/BRL atualizada:', data.valor)
      return data
    },
    refetchInterval: 5 * 60 * 1000, // Atualiza a cada 5 min
    staleTime: 0,  // ✅ Sempre refetch
    refetchOnMount: true,
    refetchOnWindowFocus: true,
  })
  
  return data?.valor || 5.30  // ✅ Fallback 5.30 (valor real médio)
}

