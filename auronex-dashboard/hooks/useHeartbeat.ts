/**
 * Hook de Heartbeat
 * Envia sinal ao servidor a cada 30s
 * Se navegador fechar, servidor detecta e DESATIVA bots
 */

import { useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'

export function useHeartbeat() {
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) return

    // ✅ Enviar heartbeat a cada 30s (DESATIVADO - causava problemas)
    const interval = setInterval(async () => {
      try {
        // DESATIVADO TEMPORARIAMENTE
        // await fetch('/api/heartbeat', ...)
        console.log('[Heartbeat] Ping (desativado)')
      } catch (error) {
        console.error('[Heartbeat] Erro:', error)
      }
    }, 30000)  // 30 segundos

    // ✅ Ao fechar navegador (DESATIVADO - causava problemas de login)
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      // DESATIVADO TEMPORARIAMENTE
      // const xhr = new XMLHttpRequest()
      // xhr.open('POST', '/api/session/close', false)
      // xhr.send()
      console.log('[Heartbeat] Browser closing (auto-stop desativado)')
    }

    window.addEventListener('beforeunload', handleBeforeUnload)

    return () => {
      clearInterval(interval)
      window.removeEventListener('beforeunload', handleBeforeUnload)
    }
  }, [isAuthenticated])
}


