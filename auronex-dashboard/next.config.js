/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output standalone para deploy otimizado
  output: 'standalone',
  
  // Compressão
  compress: true,
  
  // Headers de segurança
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
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
      }
    ]
  },

  // Rewrites para API (proxy reverso)
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api'
    const baseUrl = apiUrl.replace('/api', '')
    
    return [
      {
        source: '/api/:path*',
        destination: `${baseUrl}/:path*`
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
