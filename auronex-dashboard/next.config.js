/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output standalone para deploy otimizado
  output: 'standalone',
  
  // Compressão
  compress: true,
  
  // Headers de segurança E anti-cache
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          // Segurança
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          }
        ]
      },
      {
        // ✅ ANTI-CACHE para páginas dinâmicas
        source: '/((?!_next/static|_next/image|favicon.ico).*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
          },
          {
            key: 'Pragma',
            value: 'no-cache'
          },
          {
            key: 'Expires',
            value: '0'
          }
        ]
      }
    ]
  },

  // Rewrites para API (proxy reverso) - SEMPRE localhost em dev
  async rewrites() {
    // ✅ Em dev, SEMPRE localhost (ignorar env)
    const isDev = process.env.NODE_ENV !== 'production'
    const baseUrl = isDev ? 'http://localhost:8001' : (process.env.NEXT_PUBLIC_API_URL || 'https://auronex.com.br')
    
    console.log('[Next Config] Rewrites para:', baseUrl)
    
    return [
      {
        source: '/api/:path*',
        destination: `${baseUrl}/api/:path*`
      }
    ]
  },

  // Otimizações de imagem
  images: {
    domains: ['auronex.com.br', 'app.auronex.com.br'],
    formats: ['image/avif', 'image/webp'],
  },

  // React Strict Mode
  reactStrictMode: true,

  // Desativar x-powered-by
  poweredByHeader: false,
}

module.exports = nextConfig
