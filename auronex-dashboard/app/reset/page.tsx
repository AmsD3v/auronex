'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/authStore'

/**
 * Página de Reset
 * Limpa TUDO e volta para login
 */
export default function ResetPage() {
  const router = useRouter()
  const { logout } = useAuthStore()

  useEffect(() => {
    // Limpar TUDO
    logout()
    
    if (typeof window !== 'undefined') {
      localStorage.clear()
      sessionStorage.clear()
    }

    // Redirecionar após 1 segundo
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  }, [logout, router])

  return (
    <div className="flex min-h-screen items-center justify-center bg-dark-900">
      <div className="text-center">
        <div className="mb-4 h-16 w-16 animate-spin rounded-full border-4 border-accent-500/30 border-t-accent-500 mx-auto"></div>
        <p className="text-white text-xl mb-2">🧹 Limpando cache...</p>
        <p className="text-gray-400">Você será redirecionado para o login</p>
      </div>
    </div>
  )
}

