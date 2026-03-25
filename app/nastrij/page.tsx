'use client';
import { useState } from 'react';

const MOODS = [
  { id: 'joy',    emoji: '✨', label: 'Радість'  },
  { id: 'calm',   emoji: '🌊', label: 'Спокій'   },
  { id: 'focus',  emoji: '🎯', label: 'Фокус'    },
  { id: 'sad',    emoji: '🌧️', label: 'Смуток'   },
  { id: 'energy', emoji: '⚡', label: 'Енергія'  },
];

export default function NastrijPage() {
  const [active, setActive] = useState<string | null>(null);
  return (
    <div className="page-module">
      <div className="module-header">
        <div>
          <h1>Настрій</h1>
          <p className="module-subtitle">Відстеження емоційного стану</p>
        </div>
      </div>
      <div className="mood-grid">
        {MOODS.map(m => (
          <button key={m.id} className={`mood-card ${active === m.id ? 'mood-card--active' : ''}`} onClick={() => setActive(m.id)}>
            <span className="mood-emoji">{m.emoji}</span>
            <span className="mood-label">{m.label}</span>
          </button>
        ))}
      </div>
      {active && <p className="mood-selected">Поточний стан: <strong>{MOODS.find(m => m.id === active)?.label}</strong></p>}
    </div>
  );
}
