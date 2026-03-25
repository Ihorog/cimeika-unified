'use client';
import { useState } from 'react';

export default function KazkarPage() {
  const [stories, setStories] = useState<{ id: number; title: string; body: string }[]>([]);
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const add = () => {
    if (!title.trim()) return;
    setStories(s => [{ id: Date.now(), title, body }, ...s]);
    setTitle(''); setBody(''); setOpen(false);
  };

  return (
    <div className="page-module">
      <div className="module-header">
        <div>
          <h1>Казкар</h1>
          <p className="module-subtitle">Історії та наратив екосистеми Cimeika</p>
        </div>
        <button className="btn-primary" onClick={() => setOpen(true)}>+ Нова історія</button>
      </div>
      {open && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Нова історія</h2>
            <input className="input" placeholder="Назва" value={title} onChange={e => setTitle(e.target.value)} />
            <textarea className="textarea" placeholder="Текст..." value={body} onChange={e => setBody(e.target.value)} rows={5} />
            <div className="modal-actions">
              <button className="btn-ghost" onClick={() => setOpen(false)}>Скасувати</button>
              <button className="btn-primary" onClick={add}>Зберегти</button>
            </div>
          </div>
        </div>
      )}
      {stories.length === 0
        ? <p className="empty-state">Ще немає жодної історії. Створіть першу.</p>
        : <div className="card-list">{stories.map(s => <div key={s.id} className="card"><h3>{s.title}</h3>{s.body && <p>{s.body}</p>}</div>)}</div>}
    </div>
  );
}
