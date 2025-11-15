/**
 * Cache Buster - Elimina problemas de cache
 * ✅ Limpa cache no login
 * ✅ Força reload quando necessário
 * ✅ Versioning automático
 */

export const CacheBuster = {
  /**
   * Limpar TODO o cache do navegador
   */
  clearAll() {
    // 1. LocalStorage
    localStorage.clear()
    
    // 2. SessionStorage
    sessionStorage.clear()
    
    // 3. Cookies (se houver)
    document.cookie.split(";").forEach((c) => {
      document.cookie = c
        .replace(/^ +/, "")
        .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/")
    })
    
    // 4. Cache API (Service Worker)
    if ('caches' in window) {
      caches.keys().then((names) => {
        names.forEach((name) => {
          caches.delete(name)
        })
      })
    }
    
    console.log('✅ Cache completamente limpo!')
  },

  /**
   * Limpar apenas dados de autenticação
   */
  clearAuth() {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    localStorage.removeItem('auth-storage')
    
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')
    
    console.log('✅ Cache de auth limpo!')
  },

  /**
   * Forçar reload da página sem cache
   */
  hardReload() {
    // Limpar cache
    this.clearAll()
    
    // Adicionar timestamp à URL para forçar reload
    const url = new URL(window.location.href)
    url.searchParams.set('_nocache', Date.now().toString())
    
    // Reload sem cache
    window.location.href = url.toString()
  },

  /**
   * Limpar cache e fazer logout
   */
  clearAndLogout() {
    this.clearAll()
    window.location.href = '/login'
  },

  /**
   * Verificar versão e forçar reload se mudou
   */
  checkVersion(currentVersion: string) {
    const storedVersion = localStorage.getItem('app_version')
    
    if (storedVersion && storedVersion !== currentVersion) {
      console.log(`🔄 Nova versão detectada: ${storedVersion} → ${currentVersion}`)
      console.log('🔄 Forçando reload sem cache...')
      
      // Limpar cache
      this.clearAll()
      
      // Salvar nova versão
      localStorage.setItem('app_version', currentVersion)
      
      // Reload
      window.location.reload()
    } else {
      localStorage.setItem('app_version', currentVersion)
    }
  },

  /**
   * Adicionar timestamp a URLs para cache busting
   */
  bustUrl(url: string): string {
    const separator = url.includes('?') ? '&' : '?'
    return `${url}${separator}_t=${Date.now()}`
  }
}

/**
 * Hook para usar cache buster
 */
export function useCacheBuster() {
  return CacheBuster
}




