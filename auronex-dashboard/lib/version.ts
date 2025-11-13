/**
 * Versão do sistema
 * Atualizada automaticamente via GitHub Actions ou script
 */

export const VERSION = '1.0.02b'
export const BUILD_DATE = '2025-11-12'
export const ENVIRONMENT = process.env.NODE_ENV || 'development'

export function getFullVersion() {
  return `v${VERSION} (${ENVIRONMENT})`
}

export function getBuildInfo() {
  return {
    version: VERSION,
    buildDate: BUILD_DATE,
    environment: ENVIRONMENT,
    platform: 'React + Next.js + FastAPI'
  }
}

