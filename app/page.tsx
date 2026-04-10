// CIMEIKA — Сі (головна сторінка)
import Link from 'next/link';

const modules = [
  { href: '/',         emoji: '⚙️',  name: 'Сі',        desc: 'Оркестрація та моніторинг системи'     },
  { href: '/kazkar',   emoji: '📖',  name: 'Казкар',    desc: 'Пам\'ять, легенди, наратив'             },
  { href: '/podija',   emoji: '📅',  name: 'ПоДія',     desc: 'Події, сценарії, тригери'               },
  { href: '/nastrij',  emoji: '💭',  name: 'Настрій',   desc: 'Відстеження емоційного стану'           },
  { href: '/malya',    emoji: '🎨',  name: 'Маля',      desc: 'Ідеї, творчість, варіативність'         },
  { href: '/kalendar', emoji: '⏰',  name: 'Календар',  desc: 'Час, ритми, вузлові точки'              },
  { href: '/gallery',  emoji: '🖼️',  name: 'Галерея',   desc: 'Медіа-архів, зображення, відео, аудіо' },
];

export default function HomePage() {
  return (
    <div className="page-home">
      <section className="hero">
        <p className="hero-eyebrow">Ласкаво просимо до Cimeika</p>
        <h1 className="hero-title">Екосистема творчості та управління</h1>
        <p className="hero-desc">
          Cimeika об&#39;єднує сім модулів для управління історіями, подіями,
          настроєм, ідеями та медіа в одній елегантній платформі.
        </p>
      </section>

      <section className="modules-grid">
        <h2 className="section-title">Модулі</h2>
        <div className="grid">
          {modules.map(({ href, emoji, name, desc }) => (
            <Link key={href} href={href} className="module-card">
              <span className="module-emoji">{emoji}</span>
              <h3 className="module-name">{name}</h3>
              <p className="module-desc">{desc}</p>
              <span className="module-link">Перейти до модуля →</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
