import type { Metadata } from 'next';
import { Navigation } from '@/components/Navigation';
import './globals.css';
import './styles/modules.css';

export const metadata: Metadata = {
  title: 'Cimeika',
  description: 'Екосистема творчості та управління',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uk">
      <body>
        <Navigation />
        <main className="main-content">{children}</main>
        <footer className="footer">
          Cimeika © 2026 · Екосистема творчості та управління контентом
        </footer>
      </body>
    </html>
  );
}
