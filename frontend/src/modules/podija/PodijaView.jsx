import React, { useState, useEffect } from 'react';
import { podijaService } from '../../services/modules';

const PodijaView = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all'); // all, upcoming, completed
  const [newEvent, setNewEvent] = useState({
    title: '',
    description: '',
    event_date: '',
    event_type: 'personal',
    tags: ''
  });

  useEffect(() => {
    loadEvents();
  }, [filter]);

  const loadEvents = async () => {
    setLoading(true);
    setError(null);
    try {
      let params = { limit: 50 };
      if (filter === 'upcoming') {
        params.is_completed = false;
      } else if (filter === 'completed') {
        params.is_completed = true;
      }
      
      const data = await podijaService.getEvents(params);
      setEvents(data);
    } catch (err) {
      setError('Не вдалося завантажити події. Перевірте з\'єднання з backend.');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const eventData = {
        title: newEvent.title,
        description: newEvent.description,
        event_date: newEvent.event_date || undefined,
        event_type: newEvent.event_type,
        is_completed: false,
        tags: newEvent.tags ? newEvent.tags.split(',').map(t => t.trim()) : []
      };
      
      await podijaService.createEvent(eventData);
      setNewEvent({
        title: '',
        description: '',
        event_date: '',
        event_type: 'personal',
        tags: ''
      });
      setShowForm(false);
      loadEvents();
    } catch (err) {
      setError('Не вдалося створити подію: ' + (err.response?.data?.detail || err.message));
      console.error('Error creating event:', err);
    }
  };

  const handleToggleComplete = async (eventId, currentStatus) => {
    try {
      await podijaService.updateEvent(eventId, { is_completed: !currentStatus });
      loadEvents();
    } catch (err) {
      setError('Не вдалося оновити подію');
      console.error('Error updating event:', err);
    }
  };

  return (
    <div className="module-view podija-view">
      <header className="module-header">
        <h1>Подія</h1>
        <p className="module-subtitle">Події, майбутнє, сценарії</p>
      </header>
      
      <main className="module-content">
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <div className="module-toolbar">
          <div className="module-actions">
            <button 
              className="btn-primary"
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? 'Скасувати' : '+ Нова подія'}
            </button>
            <button 
              className="btn-secondary"
              onClick={loadEvents}
              disabled={loading}
            >
              ↻ Оновити
            </button>
          </div>

          <div className="filter-buttons">
            <button 
              className={filter === 'all' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('all')}
            >
              Всі ({events.length})
            </button>
            <button 
              className={filter === 'upcoming' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('upcoming')}
            >
              Майбутні
            </button>
            <button 
              className={filter === 'completed' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('completed')}
            >
              Завершені
            </button>
          </div>
        </div>

        {showForm && (
          <form className="event-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Назва події *</label>
              <input
                type="text"
                value={newEvent.title}
                onChange={(e) => setNewEvent({...newEvent, title: e.target.value})}
                required
                placeholder="Назва події"
              />
            </div>

            <div className="form-group">
              <label>Опис *</label>
              <textarea
                value={newEvent.description}
                onChange={(e) => setNewEvent({...newEvent, description: e.target.value})}
                required
                rows={4}
                placeholder="Опишіть подію..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Дата події</label>
                <input
                  type="datetime-local"
                  value={newEvent.event_date}
                  onChange={(e) => setNewEvent({...newEvent, event_date: e.target.value})}
                />
              </div>

              <div className="form-group">
                <label>Тип</label>
                <select
                  value={newEvent.event_type}
                  onChange={(e) => setNewEvent({...newEvent, event_type: e.target.value})}
                >
                  <option value="personal">Особиста</option>
                  <option value="work">Робота</option>
                  <option value="family">Сім'я</option>
                  <option value="celebration">Свято</option>
                  <option value="meeting">Зустріч</option>
                  <option value="other">Інше</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Теги (через кому)</label>
              <input
                type="text"
                value={newEvent.tags}
                onChange={(e) => setNewEvent({...newEvent, tags: e.target.value})}
                placeholder="важливо, термін, нагадати"
              />
            </div>

            <button type="submit" className="btn-primary">
              Створити подію
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading-state">
            Завантаження...
          </div>
        ) : events.length === 0 ? (
          <div className="empty-state">
            <p>Немає подій</p>
            <p className="text-secondary">Створіть першу подію</p>
          </div>
        ) : (
          <div className="events-list">
            {events.map((event) => (
              <div key={event.id} className={`event-card ${event.is_completed ? 'completed' : ''}`}>
                <div className="event-header">
                  <h3>{event.title}</h3>
                  <button
                    className="checkbox-btn"
                    onClick={() => handleToggleComplete(event.id, event.is_completed)}
                    title={event.is_completed ? 'Позначити як незавершену' : 'Позначити як завершену'}
                  >
                    {event.is_completed ? '✓' : '○'}
                  </button>
                </div>
                <p className="event-description">{event.description}</p>
                <div className="event-meta">
                  {event.event_type && (
                    <span className="badge">{event.event_type}</span>
                  )}
                  {event.event_date && (
                    <span className="meta-item">
                      📅 {new Date(event.event_date).toLocaleString('uk-UA')}
                    </span>
                  )}
                </div>
                {event.tags && event.tags.length > 0 && (
                  <div className="event-tags">
                    {event.tags.map((tag, idx) => (
                      <span key={idx} className="tag">#{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default PodijaView;
