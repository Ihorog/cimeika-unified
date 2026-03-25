'use client';
import { useState } from 'react';

export default function MalyaPage() {
  const [ideas, setIdeas] = useState<{ id: number; text: string }[]>([]);
  const [text, setText] = useState('');
  const add = () => { if (!text.trim()) return; setIdeas(i => [{ id: Date.now(), text }, ...i]); setText(''); };

  return (
    <div className="page-module">
      <div className="module-header">
        <div>
          <h1>Маля</h1>
          <p className="module-subtitle">Ідеї та творчість</p>
        </div>
      </div>
      <div className="idea-input-row">
        <input className="input" placeholder="Нова ідея..." value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && add()} />
        <button className="btn-primary" onClick={add}>Додати</button>
      </div>
      {ideas.length === 0
        ? <p className="empty-state">Ще немає ідей. Почніть думати вголос.</p>
        : <div className="card-list">{ideas.map(i => <div key={i.id} className="card"><p>{i.text}</p></div>)}</div>}
    </div>
  );
}
