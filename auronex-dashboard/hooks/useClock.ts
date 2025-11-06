/**
 * Hook de Relógio
 * Atualiza a cada 1 segundo
 */

import { useState, useEffect } from 'react'

/**
 * Hook para relógio em tempo real
 * ✅ Atualiza TODO segundo!
 * ✅ Formato customizável
 */
export function useClock(format: 'time' | 'datetime' | 'full' = 'time') {
  const [time, setTime] = useState<string>('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()

      switch (format) {
        case 'time':
          setTime(now.toLocaleTimeString('pt-BR'))
          break
        case 'datetime':
          setTime(
            now.toLocaleString('pt-BR', {
              dateStyle: 'short',
              timeStyle: 'short',
            })
          )
          break
        case 'full':
          setTime(
            now.toLocaleString('pt-BR', {
              dateStyle: 'long',
              timeStyle: 'medium',
            })
          )
          break
      }
    }

    // Atualizar imediatamente
    updateTime()

    // ✅ Atualizar a cada 1 segundo!
    const interval = setInterval(updateTime, 1000)

    return () => clearInterval(interval)
  }, [format])

  return time
}

