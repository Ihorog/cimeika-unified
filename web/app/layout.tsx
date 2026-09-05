import type { Metadata } from 'next'
import { SiteChrome } from '@/components/SiteChrome'
import './globals.css'
import './styles/modules.css'

export const metadata: Metadata = {
  title: 'Cimeika',
  description: 'Екосистема творчості та управління',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uk">
      <body>
        <SiteChrome>{children}</SiteChrome>
      </body>
    </html>
  )
}
