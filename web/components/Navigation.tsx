// CIMEIKA — Navigation Component
// All labels in Ukrainian. Identifiers in English.

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const modules = [
  { href: '/',          emoji: '⚙️',  label: 'Сі'       },
  { href: '/kazkar',    emoji: '📖',  label: 'Казкар'   },
  { href: '/podija',    emoji: '📅',  label: 'ПоДія'    },
  { href: '/nastrij',   emoji: '💭',  label: 'Настрій'  },
  { href: '/malya',     emoji: '🎨',  label: 'Маля'     },
  { href: '/kalendar',  emoji: '⏰',  label: 'Календар' },
  { href: '/gallery',   emoji: '🖼️',  label: 'Галерея'  },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <header className="nav-shell">
      <div className="nav-brand">
        <span className="nav-brand-icon">⚙️</span>
        <span className="nav-brand-name">Cimeika</span>
        <span className="nav-brand-sub">Екосистема</span>
      </div>
      <nav className="nav-links">
        {modules.map(({ href, emoji, label }) => (
          <Link
            key={href}
            href={href}
            className={`nav-item ${pathname === href ? 'nav-item--active' : ''}`}
          >
            <span>{emoji}</span>
            <span>{label}</span>
          </Link>
        ))}
      </nav>
    </header>
  );
}
