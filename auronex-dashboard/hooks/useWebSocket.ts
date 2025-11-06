/**
 * Hook de WebSocket - DESABILITADO
 * Causa popup de autorização de rede local (ruim para confiança!)
 * Usar React Query com polling é suficiente
 */

import { useEffect, useState, useCallback } from 'react'
// import { io, Socket } from 'socket.io-client'  // ❌ REMOVIDO
import type { WebSocketMessage } from '@/types'

type Socket = any // Placeholder

interface UseWebSocketOptions {
  url?: string
  autoConnect?: boolean
  onMessage?: (message: WebSocketMessage) => void
  onConnect?: () => void
  onDisconnect?: () => void
  onError?: (error: Error) => void
}

/**
 * Hook para WebSocket (preços, trades, notificações)
 * ✅ Conexão automática
 * ✅ Reconexão automática
 * ✅ TypeScript
 */
export function useWebSocket(options: UseWebSocketOptions = {}) {
  const {
    url = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:8001',
    autoConnect = true,
    onMessage,
    onConnect,
    onDisconnect,
    onError,
  } = options

  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)

  useEffect(() => {
    // ❌ WebSocket DESABILITADO (causa popup de autorização!)
    // React Query com polling (1-5s) é suficiente para tempo real
    return
    
    /*
    if (!autoConnect) return

    // Conectar ao WebSocket
    const newSocket = io(url, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 10,
    })
    */

    // Event: Connect
    newSocket.on('connect', () => {
      console.log('[WebSocket] Connected')
      setIsConnected(true)
      onConnect?.()
    })

    // Event: Disconnect
    newSocket.on('disconnect', () => {
      console.log('[WebSocket] Disconnected')
      setIsConnected(false)
      onDisconnect?.()
    })

    // Event: Error
    newSocket.on('error', (error: Error) => {
      console.error('[WebSocket] Error:', error)
      onError?.(error)
    })

    // Event: Message (genérico)
    newSocket.on('message', (message: WebSocketMessage) => {
      setLastMessage(message)
      onMessage?.(message)
    })

    // Event: Preço atualizado
    newSocket.on('price_update', (data: any) => {
      const message: WebSocketMessage = {
        type: 'price_update',
        data,
        timestamp: Date.now(),
      }
      setLastMessage(message)
      onMessage?.(message)
    })

    // Event: Trade executado
    newSocket.on('trade_update', (data: any) => {
      const message: WebSocketMessage = {
        type: 'trade_update',
        data,
        timestamp: Date.now(),
      }
      setLastMessage(message)
      onMessage?.(message)
    })

    // Event: Status do bot mudou
    newSocket.on('bot_status', (data: any) => {
      const message: WebSocketMessage = {
        type: 'bot_status',
        data,
        timestamp: Date.now(),
      }
      setLastMessage(message)
      onMessage?.(message)
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [url, autoConnect, onMessage, onConnect, onDisconnect, onError])

  // Enviar mensagem
  const sendMessage = useCallback(
    (event: string, data: any) => {
      if (socket && isConnected) {
        socket.emit(event, data)
      } else {
        console.warn('[WebSocket] Cannot send message, not connected')
      }
    },
    [socket, isConnected]
  )

  // Conectar manualmente
  const connect = useCallback(() => {
    socket?.connect()
  }, [socket])

  // Desconectar manualmente
  const disconnect = useCallback(() => {
    socket?.disconnect()
  }, [socket])

  return {
    socket,
    isConnected,
    lastMessage,
    sendMessage,
    connect,
    disconnect,
  }
}

