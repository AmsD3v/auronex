/**
 * Hook de WebSocket - DESABILITADO
 * Causa popup de autorização de rede local (ruim para confiança!)
 * Usar React Query com polling é suficiente
 */

import { useCallback } from 'react'
import type { WebSocketMessage } from '@/types'

interface UseWebSocketOptions {
  url?: string
  autoConnect?: boolean
  onMessage?: (message: WebSocketMessage) => void
  onConnect?: () => void
  onDisconnect?: () => void
  onError?: (error: Error) => void
}

/**
 * Hook para WebSocket - DESABILITADO
 * Retorna apenas stub (não faz nada)
 * Sistema usa React Query para tempo real
 */
export function useWebSocket(_options: UseWebSocketOptions = {}) {
  // ❌ WebSocket DESABILITADO (causava popup de autorização!)
  // Sistema usa React Query com polling (1-5s)
  // Performance é excelente e SEM popup!

  // Stub functions (não fazem nada)
  const sendMessage = useCallback(() => {
    console.warn('[WebSocket] Desabilitado - use React Query')
  }, [])

  const connect = useCallback(() => {
    console.warn('[WebSocket] Desabilitado - use React Query')
  }, [])

  const disconnect = useCallback(() => {
    console.warn('[WebSocket] Desabilitado - use React Query')
  }, [])

  // Retornar stub (compatível com código existente)
  return {
    socket: null,
    isConnected: false,
    lastMessage: null,
    sendMessage,
    connect,
    disconnect,
  }
}
