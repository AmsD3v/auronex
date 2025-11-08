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

    // ✅ Enviar heartbeat a cada 30s
    const interval = setInterval(async () => {
      try {
        await fetch('/api/heartbeat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        })
      } catch (error) {
        console.error('[Heartbeat] Erro:', error)
      }
    }, 30000)  // 30 segundos

    // ✅ Ao fechar navegador/aba - CRÍTICO!
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      // Enviar sinal SÍNCRONO para garantir execução
      const xhr = new XMLHttpRequest()
      xhr.open('POST', `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/session/close`, false)  // false = síncrono!
      xhr.setRequestHeader('Content-Type', 'application/json')
      xhr.withCredentials = true
      
      try {
        xhr.send()
        console.log('[Heartbeat] Session closed on exit')
      } catch (e) {
        console.error('[Heartbeat] Failed to close session:', e)
      }
    }

    window.addEventListener('beforeunload', handleBeforeUnload)
    window.addEventListener('unload', handleBeforeUnload)  // Backup

    return () => {
      clearInterval(interval)
      window.removeEventListener('beforeunload', handleBeforeUnload)
    }
  }, [isAuthenticated])
}


