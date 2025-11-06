'use client'

import { Clock } from './Clock'
import { useAuthStore } from '@/stores/authStore'
import { useTradingStore } from '@/stores/tradingStore'
import { Menu, X, LogOut } from 'lucide-react'
import { useUIStore } from '@/stores/uiStore'
import { motion } from 'framer-motion'

/**
 * Header do Dashboard
 * ✅ Logo + Título
 * ✅ Relógio em tempo real
 * ✅ User info + Logout
 */
export function Header() {
  const { user, logout } = useAuthStore()
  const { currency } = useTradingStore()
  const { sidebarOpen, toggleSidebar } = useUIStore()

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky top-0 z-50 border-b border-white/5 bg-dark-800/50 backdrop-blur-xl"
    >
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left: Logo + Title */}
        <div className="flex items-center gap-4">
          {/* Menu toggle (mobile) */}
          <button
            onClick={toggleSidebar}
            className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-dark-700 hover:text-white lg:hidden"
          >
            {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>

          <div>
            <h1 className="text-2xl font-light text-white">
              Auronex Trading
            </h1>
            <p className="text-sm text-gray-400">
              Real-time trading platform
            </p>
          </div>
        </div>

        {/* Right: Clock + User */}
        <div className="flex items-center gap-6">
          {/* Clock */}
          <Clock />

          {/* User info */}
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-white">
                {user?.first_name || user?.email}
              </p>
              <p className="text-xs text-gray-400">
                {user?.subscription?.plan?.toUpperCase() || 'FREE'}
                {' · '}
                {currency}
              </p>
            </div>

            {/* Logout button */}
            <button
              onClick={handleLogout}
              className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-loss-500/20 hover:text-loss-500"
              title="Sair"
            >
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </motion.header>
  )
}

