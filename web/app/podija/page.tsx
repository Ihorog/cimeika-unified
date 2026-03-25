'use client';
import { useState } from 'react';

export default function PodiyaPage() {
  const [events, setEvents] = useState<{ id: number; title: string; date: string }[]>([]);
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');

  const add = () => {
    if (!title.trim()) return;
    setEvents(e => [{ id: Date.now(), title, date }, ...e]);
    setTitle(''); setDate(''); setOpen(false);
  };

  return (
    <div className="page-module">
      <div className="module-header">
        <div>
          <h1>ПоДія</h1>
          <p className="module-subtitle">Події та тригери екосистеми</p>
        </div>
        <button className="btn-primary" onClick={() => setOpen(true)}>+ Нова подія</button>
      </div>
      {open && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Нова подія</h2>
            <input className="input" placeholder="Назва події" value={title} onChange={e => setTitle(e.target.value)} />
            <input className="input" type="date" value={date} onChange={e => setDate(e.target.value)} />
            <div className="modal-actions">
              <button className="btn-ghost" onClick={() => setOpen(false)}>Скасувати</button>
              <button className="btn-primary" onClick={add}>Зберегти</button>
            </div>
          </div>
        </div>
      )}
      {events.length === 0
        ? <p className="empty-state">Ще немає жодної події.</p>
        : <div className="card-list">{events.map(e => <div key={e.id} className="card"><h3>{e.title}</h3>{e.date && <p className="text-muted">{e.date}</p>}</div>)}</div>}
    </div>
  );
}
