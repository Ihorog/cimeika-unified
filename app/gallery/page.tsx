'use client';
import { useState, useRef } from 'react';

type MediaType = 'all' | 'image' | 'video' | 'audio';
type MediaItem = { id: number; name: string; type: 'image' | 'video' | 'audio'; url: string };
const TYPE_LABELS: Record<MediaType, string> = { all: 'Все', image: 'Зображення', video: 'Відео', audio: 'Аудіо' };

export default function GalleryPage() {
  const [filter, setFilter] = useState<MediaType>('all');
  const [items, setItems] = useState<MediaItem[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const newItems: MediaItem[] = files.map(f => ({
      id: Date.now() + Math.random(), name: f.name, url: URL.createObjectURL(f),
      type: f.type.startsWith('image') ? 'image' : f.type.startsWith('video') ? 'video' : 'audio'
    }));
    setItems(i => [...i, ...newItems]);
  };

  const visible = items.filter(i => filter === 'all' || i.type === filter);

  return (
    <div className="page-module">
      <div className="module-header">
        <div>
          <h1>Галерея</h1>
          <p className="module-subtitle">Медіа ресурси та творчі роботи</p>
        </div>
        <button className="btn-primary" onClick={() => inputRef.current?.click()}>↑ Завантажити</button>
        <input ref={inputRef} type="file" multiple accept="image/*,video/*,audio/*" style={{ display: 'none' }} onChange={handleUpload} />
      </div>
      <div className="filter-tabs">
        {(Object.keys(TYPE_LABELS) as MediaType[]).map(t => (
          <button key={t} className={`filter-tab${filter === t ? ' filter-tab--active' : ''}`} onClick={() => setFilter(t)}>{TYPE_LABELS[t]}</button>
        ))}
      </div>
      {visible.length === 0
        ? <p className="empty-state">Немає медіа-файлів у цій категорії.</p>
        : <div className="gallery-grid">{visible.map(item => (
            <div key={item.id} className="gallery-item">
              {item.type === 'image' && <img src={item.url} alt={item.name} />}
              {item.type === 'video' && <video src={item.url} controls />}
              {item.type === 'audio' && <div className="audio-item"><span>🎵</span><audio src={item.url} controls /><p>{item.name}</p></div>}
            </div>
          ))}</div>}
    </div>
  );
}
