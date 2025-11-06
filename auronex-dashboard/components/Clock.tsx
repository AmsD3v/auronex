'use client'

import { useClock } from '@/hooks/useClock'
import { motion } from 'framer-motion'

interface ClockProps {
  format?: 'time' | 'datetime' | 'full'
  className?: string
}

/**
 * Componente de Relógio
 * ✅ Atualiza TODO segundo!
 * ✅ Formato customizável
 */
export function Clock({ format = 'time', className = '' }: ClockProps) {
  const time = useClock(format)

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`text-right ${className}`}
    >
      <div className="tabular-nums text-3xl font-light text-white">
        {time}
      </div>
      <div className="mt-1 text-xs text-gray-400">
        Atualiza a cada 1s
      </div>
    </motion.div>
  )
}

