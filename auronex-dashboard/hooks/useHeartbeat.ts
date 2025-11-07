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

    // ✅ Ao fechar navegador/aba
    const handleBeforeUnload = async () => {
      // Enviar sinal de logout
      try {
        await fetch('/api/session/close', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          keepalive: true,  // ✅ Garante que envia mesmo fechando
        })
      } catch (e) {
        // Ignorar erro (navegador está fechando)
      }
    }

    window.addEventListener('beforeunload', handleBeforeUnload)

    return () => {
      clearInterval(interval)
      window.removeEventListener('beforeunload', handleBeforeUnload)
    }
  }, [isAuthenticated])
}


