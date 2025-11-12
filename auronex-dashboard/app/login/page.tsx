'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/authStore'
import { motion } from 'framer-motion'
import { LogIn, Mail, Lock, Loader2 } from 'lucide-react'
import { toast } from 'sonner'

/**
 * Página de Login
 * ✅ Formulário profissional
 * ✅ Validação
 * ✅ Loading states
 * ✅ Animações suaves
 */
export default function LoginPage() {
  const router = useRouter()
  const { login, isAuthenticated, isLoading, error, clearError } = useAuthStore()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // Limpar localStorage ao carregar (evita loops)
  useEffect(() => {
    // Se tem isAuthenticated mas não tem token válido, limpar
    const authData = localStorage.getItem('auth-storage')
    if (authData) {
      try {
        const { state } = JSON.parse(authData)
        if (!state.token || !state.user) {
          // Dados inválidos, limpar
          localStorage.removeItem('auth-storage')
          window.location.reload()
        }
      } catch {
        localStorage.removeItem('auth-storage')
      }
    }
  }, [])

  // Redirecionar se já está autenticado
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/')  // ✅ Raiz (não /dashboard)
    }
  }, [isAuthenticated, router])

  // Limpar erro ao mudar campos
  useEffect(() => {
    if (error) {
      clearError()
    }
  }, [email, password, error, clearError])

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validação básica
    if (!email || !password) {
      toast.error('Preencha email e senha!')
      return
    }

    // Validar formato email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      toast.error('Email inválido!')
      return
    }

    // Fazer login
    console.log('[Login Page] Tentando login...')
    const success = await login(email, password)
    console.log('[Login Page] Resultado:', success)

    if (success) {
      console.log('[Login Page] Sucesso! Redirecionando...')
      toast.success('Login realizado com sucesso!')
      // ✅ Aguardar localStorage salvar
      await new Promise(resolve => setTimeout(resolve, 300))
      router.push('/')
    } else {
      console.log('[Login Page] FALHA! Mostrando erro...')
      toast.error('❌ Email ou senha incorretos!', {
        duration: 5000,
        position: 'top-center'
      })
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-dark-900">
      {/* Background gradient animado */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 h-80 w-80 animate-pulse-slow rounded-full bg-primary-500/10 blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 h-80 w-80 animate-pulse-slow rounded-full bg-accent-500/10 blur-3xl" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Login container */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-md px-6"
      >
        {/* Logo e título */}
        <div className="mb-8 text-center">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-2 text-5xl font-light text-white"
          >
            Auronex
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-gray-400"
          >
            Trading Platform · By Auronex Technology
          </motion.p>
        </div>

        {/* Card de login */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="card card-glow p-8"
        >
          <h2 className="mb-6 text-2xl font-semibold text-white">
            Fazer login
          </h2>

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label htmlFor="email" className="mb-2 block text-sm font-medium text-gray-300">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500" />
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="seu@email.com"
                  className="input pl-10"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            {/* Senha */}
            <div>
              <label htmlFor="password" className="mb-2 block text-sm font-medium text-gray-300">
                Senha
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500" />
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="input pl-10"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            {/* Lembrar-me */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  className="h-4 w-4 rounded border-gray-600 bg-dark-700 text-accent-500 focus:ring-2 focus:ring-accent-500/50"
                />
                <span className="text-sm text-gray-400">Lembrar-me</span>
              </label>
              <a
                href="#"
                className="text-sm text-accent-500 hover:text-accent-400 transition-colors"
              >
                Esqueceu a senha?
              </a>
            </div>

            {/* Botão submit */}
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Entrando...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <LogIn className="h-5 w-5" />
                  Entrar
                </span>
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center gap-4">
            <div className="h-px flex-1 bg-white/10"></div>
            <span className="text-xs text-gray-500">OU</span>
            <div className="h-px flex-1 bg-white/10"></div>
          </div>

          {/* Link para registro */}
          <div className="text-center text-sm text-gray-400">
            Ainda não tem conta?{' '}
            <a
              href="/register"
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-accent-500 hover:text-accent-400 transition-colors"
            >
              Criar conta
            </a>
          </div>
        </motion.div>

        {/* Links úteis */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-6 text-center"
        >
          <div className="flex items-center justify-center gap-6 text-sm text-gray-500">
            <a href="#" className="hover:text-gray-400 transition-colors">
              Termos
            </a>
            <span>•</span>
            <a href="#" className="hover:text-gray-400 transition-colors">
              Privacidade
            </a>
            <span>•</span>
            <a
              href="/admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gray-400 transition-colors"
            >
              Admin
            </a>
          </div>
        </motion.div>
      </motion.div>
    </div>
  )
}

