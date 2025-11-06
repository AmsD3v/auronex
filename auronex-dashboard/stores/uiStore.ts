/**
 * UI Store - Zustand
 * Gerencia estado da interface (sidebar, modals, etc)
 */

import { create } from 'zustand'

interface UIState {
  // State
  sidebarOpen: boolean
  theme: 'dark' | 'light'
  notifications: Notification[]
  isLoading: boolean
  
  // Actions
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  setTheme: (theme: 'dark' | 'light') => void
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void
  removeNotification: (id: string) => void
  clearNotifications: () => void
  setLoading: (loading: boolean) => void
}

interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: Date
}

export const useUIStore = create<UIState>((set) => ({
  // Initial state
  sidebarOpen: true,
  theme: 'dark',
  notifications: [],
  isLoading: false,

  // Toggle sidebar
  toggleSidebar: () =>
    set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  // Set sidebar open
  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  // Set theme
  setTheme: (theme) => set({ theme }),

  // Add notification
  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        {
          ...notification,
          id: Math.random().toString(36).substring(7),
          timestamp: new Date(),
        },
      ],
    })),

  // Remove notification
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),

  // Clear notifications
  clearNotifications: () => set({ notifications: [] }),

  // Set loading
  setLoading: (loading) => set({ isLoading: loading }),
}))

