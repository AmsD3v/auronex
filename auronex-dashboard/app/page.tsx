import { redirect } from 'next/navigation'

/**
 * Home page - Redireciona para login
 */
export default function HomePage() {
  // Redirect para login
  redirect('/login')
}

