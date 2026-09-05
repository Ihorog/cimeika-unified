'use client'

import { usePathname } from 'next/navigation'
import { Navigation } from '@/components/Navigation'

export function SiteChrome({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  if (pathname === '/') {
    return <>{children}</>
  }

  return (
    <>
      <Navigation />
      <main className="main-content">{children}</main>
      <footer className="footer">
        Cimeika © 2026 · Екосистема творчості та управління контентом
      </footer>
    </>
  )
}
