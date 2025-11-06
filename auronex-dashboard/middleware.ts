import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Middleware do Next.js
 * Protege rotas que precisam de autenticação
 */
export function middleware(request: NextRequest) {
  // Rotas públicas (não precisam de auth)
  const publicPaths = ['/login', '/register', '/clear-cache.html']
  const path = request.nextUrl.pathname

  // Se é rota pública, deixar passar
  if (publicPaths.some(publicPath => path.startsWith(publicPath))) {
    return NextResponse.next()
  }

  // Para todas as outras rotas (incluindo /dashboard)
  // O próprio componente vai verificar autenticação
  // Middleware apenas passa adiante
  return NextResponse.next()
}

// Configurar quais rotas o middleware deve processar
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}

