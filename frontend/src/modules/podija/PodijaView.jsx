import React, { useState, useEffect, useCallback } from 'react';
import { podijaService } from '../../services/modules';

const EMPTY_FORM = {
  title: '',
  description: '',
  event_date: '',
  event_type: 'personal',
  tags: ''
};

const EVENT_TYPES = [
  { value: 'personal', label: 'Особиста' },
  { value: 'work', label: 'Робота' },
  { value: 'family', label: 'Сім\'я' },
  { value: 'celebration', label: 'Свято' },
  { value: 'meeting', label: 'Зустріч' },
  { value: 'other', label: 'Інше' },
];

const STATUS_LABEL = {
  planned: 'Заплановано',
  done: 'Виконано',
  cancelled: 'Скасовано',
};

const PodijaView = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState('all'); // all, today, week
  const [modalOpen, setModalOpen] = useState(false);
  const [editEvent, setEditEvent] = useState(null); // null = create, object = edit
  const [form, setForm] = useState(EMPTY_FORM);

  const loadEvents = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let data;
      if (view === 'today') {
        data = await podijaService.getEventsToday();
      } else if (view === 'week') {
        data = await podijaService.getEventsWeek();
      } else {
        data = await podijaService.getEvents({ limit: 100 });
      }
      setEvents(data);
    } catch (err) {
      setError('Не вдалося завантажити події. Перевірте з\'єднання з backend.');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  }, [view]);

  useEffect(() => {
    loadEvents();
  }, [loadEvents]);

  const openCreate = () => {
    setEditEvent(null);
    setForm(EMPTY_FORM);
    setModalOpen(true);
  };

  const openEdit = (event) => {
    setEditEvent(event);
    setForm({
      title: event.title || '',
      description: event.description || '',
      event_date: event.event_date ? event.event_date.slice(0, 16) : '',
      event_type: event.event_type || 'personal',
      tags: (event.tags || []).join(', ')
    });
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setEditEvent(null);
    setForm(EMPTY_FORM);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const eventData = {
        title: form.title,
        description: form.description,
        event_date: form.event_date || undefined,
        event_type: form.event_type,
        tags: form.tags ? form.tags.split(',').map(t => t.trim()).filter(Boolean) : []
      };
      if (editEvent) {
        await podijaService.updateEvent(editEvent.id, eventData);
      } else {
        await podijaService.createEvent(eventData);
      }
      closeModal();
      loadEvents();
    } catch (err) {
      setError('Не вдалося зберегти подію: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDone = async (eventId) => {
    try {
      await podijaService.markDone(eventId);
      loadEvents();
    } catch (err) {
      setError('Не вдалося позначити подію як виконану');
    }
  };

  const handleCancel = async (eventId) => {
    try {
      await podijaService.markCancel(eventId);
      loadEvents();
    } catch (err) {
      setError('Не вдалося скасувати подію');
    }
  };

  const handleDelete = async (eventId) => {
    if (!window.confirm('Видалити подію?')) return;
    try {
      await podijaService.deleteEvent(eventId);
      loadEvents();
    } catch (err) {
      setError('Не вдалося видалити подію');
    }
  };

  return (
    <div className="module-view podija-view">
      <header className="module-header">
        <h1>ПоДія</h1>
        <p className="module-subtitle">Події, майбутнє, сценарії</p>
      </header>

      <main className="module-content">
        {error && (
          <div className="error-banner">{error}</div>
        )}

        <div className="module-toolbar">
          <div className="module-actions">
            <button className="btn-primary" onClick={openCreate}>+ Нова подія</button>
            <button className="btn-secondary" onClick={loadEvents} disabled={loading}>↻ Оновити</button>
          </div>
          <div className="view-mode-toggle">
            <button className={view === 'all' ? 'toggle-active' : 'toggle-btn'} onClick={() => setView('all')}>Всі</button>
            <button className={view === 'today' ? 'toggle-active' : 'toggle-btn'} onClick={() => setView('today')}>Сьогодні</button>
            <button className={view === 'week' ? 'toggle-active' : 'toggle-btn'} onClick={() => setView('week')}>Тиждень</button>
          </div>
        </div>

        {loading ? (
          <div className="loading-state">Завантаження...</div>
        ) : events.length === 0 ? (
          <div className="empty-state">
            <p>Немає подій</p>
            <p className="text-secondary">Створіть першу подію</p>
          </div>
        ) : (
          <div className="events-list">
            {events.map((event) => (
              <div
                key={event.id}
                className={`event-card ${event.status === 'done' ? 'completed' : ''} ${event.status === 'cancelled' ? 'cancelled' : ''}`}
              >
                <div className="event-header">
                  <h3>{event.title}</h3>
                  <span className={`status-badge status-${event.status || 'planned'}`}>
                    {STATUS_LABEL[event.status] || 'Невідомо'}
                  </span>
                </div>
                {event.description && (
                  <p className="event-description">{event.description}</p>
                )}
                <div className="event-meta">
                  {event.event_type && <span className="badge">{event.event_type}</span>}
                  {event.event_date && (
                    <span className="meta-item">📅 {new Date(event.event_date).toLocaleString('uk-UA')}</span>
                  )}
                </div>
                {event.tags && event.tags.length > 0 && (
                  <div className="event-tags">
                    {event.tags.map((tag, idx) => <span key={idx} className="tag">#{tag}</span>)}
                  </div>
                )}
                {event.status === 'planned' && (
                  <div className="event-actions">
                    <button className="btn-secondary" onClick={() => openEdit(event)}>✎ Редагувати</button>
                    <button className="btn-primary" onClick={() => handleDone(event.id)}>✓ Виконано</button>
                    <button className="btn-cancel" onClick={() => handleCancel(event.id)}>✕ Скасувати</button>
                    <button className="btn-delete" onClick={() => handleDelete(event.id)}>🗑</button>
                  </div>
                )}
                {event.status !== 'planned' && (
                  <div className="event-actions">
                    <button className="btn-delete" onClick={() => handleDelete(event.id)}>🗑 Видалити</button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>

      {modalOpen && (
        <div className="event-modal" onClick={(e) => e.target === e.currentTarget && closeModal()}>
          <div className="modal-content" style={{ maxWidth: '560px', padding: '2rem' }}>
            <button className="modal-close" onClick={closeModal}>×</button>
            <h2 style={{ marginBottom: '1.5rem' }}>{editEvent ? 'Редагувати подію' : 'Нова подія'}</h2>
            <form className="event-form" style={{ padding: 0, background: 'none', marginBottom: 0 }} onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Назва події *</label>
                <input
                  type="text"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  required
                  placeholder="Назва події"
                />
              </div>
              <div className="form-group">
                <label>Опис</label>
                <textarea
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  rows={3}
                  placeholder="Опишіть подію..."
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Дата події</label>
                  <input
                    type="datetime-local"
                    value={form.event_date}
                    onChange={(e) => setForm({ ...form, event_date: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Тип</label>
                  <select
                    value={form.event_type}
                    onChange={(e) => setForm({ ...form, event_type: e.target.value })}
                  >
                    {EVENT_TYPES.map(t => (
                      <option key={t.value} value={t.value}>{t.label}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label>Теги (через кому)</label>
                <input
                  type="text"
                  value={form.tags}
                  onChange={(e) => setForm({ ...form, tags: e.target.value })}
                  placeholder="важливо, термін, нагадати"
                />
              </div>
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                <button type="button" className="btn-secondary" onClick={closeModal}>Скасувати</button>
                <button type="submit" className="btn-primary">{editEvent ? 'Зберегти' : 'Створити'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PodijaView;
