/**
 * Auth Store - Zustand
 * Gerencia autenticação do usuário
 */

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { authApi } from '@/lib/api'
import type { User } from '@/types'

interface AuthState {
  // State
  token: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  setUser: (user: User) => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Login
      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null })

        try {
          const data = await authApi.login(email, password)

      // ✅ Salvar e garantir que persiste
      set({
        token: data.access_token,
        user: data.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      })
      
      // ✅ LOG completo para debug
      console.log('[Auth] Login OK!')
      console.log('[Auth] Token:', data.access_token?.substring(0, 20))
      console.log('[Auth] User completo:', data.user)
      console.log('[Auth] first_name:', data.user?.first_name)
      console.log('[Auth] email:', data.user?.email)

      return true
        } catch (error: any) {
          const errorMessage =
            error.response?.data?.detail ||
            error.message ||
            'Erro ao fazer login'

          set({
            token: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          })

          return false
        }
      },

      // Logout
      logout: () => {
        authApi.logout()
        set({
          token: null,
          user: null,
          isAuthenticated: false,
          error: null,
        })
      },

      // Set user
      setUser: (user: User) => {
        set({ user })
      },

      // Clear error
      clearError: () => {
        set({ error: null })
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        // ✅ SÓ marca autenticado se TEM token E user
        isAuthenticated: state.token && state.user ? state.isAuthenticated : false,
      }),
      // ✅ Validar ao carregar do localStorage
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Se não tem token OU não tem user, limpar
          if (!state.token || !state.user) {
            state.token = null
            state.user = null
            state.isAuthenticated = false
          }
        }
      },
    }
  )
)

