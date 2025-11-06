import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Toaster } from 'sonner'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Auronex · Trading Platform',
  description: 'Professional trading bot platform - Trade cryptocurrencies automatically',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" className={inter.className}>
      <body suppressHydrationWarning>
        <Providers>
          {children}
          <Toaster 
            position="top-right"
            richColors
            closeButton
          />
        </Providers>
      </body>
    </html>
  )
}
