import React, { useState, useEffect } from 'react';
import { calendarService } from '../../services/modules';

const CalendarView = () => {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all'); // all, today, upcoming, recurring
  const [viewMode, setViewMode] = useState('list'); // list, calendar
  const [newEntry, setNewEntry] = useState({
    title: '',
    description: '',
    scheduled_at: '',
    end_time: '',
    entry_type: 'event',
    is_recurring: false,
    recurrence_pattern: '',
    location: '',
    participants: '',
    tags: ''
  });

  useEffect(() => {
    loadEntries();
  }, [filter]);

  const loadEntries = async () => {
    setLoading(true);
    setError(null);
    try {
      let data;
      if (filter === 'today') {
        data = await calendarService.getTodayEntries();
      } else if (filter === 'recurring') {
        data = await calendarService.getRecurringEntries();
      } else if (filter === 'upcoming') {
        data = await calendarService.getEntries({ limit: 50 });
        // Filter upcoming entries (future dates)
        const now = new Date();
        data = data.filter(entry => entry.scheduled_at && new Date(entry.scheduled_at) > now);
      } else {
        data = await calendarService.getEntries({ limit: 50 });
      }
      setEntries(data);
    } catch (err) {
      setError('Не вдалося завантажити записи календаря. Перевірте з\'єднання з backend.');
      console.error('Error loading calendar entries:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const entryData = {
        title: newEntry.title,
        description: newEntry.description,
        scheduled_at: newEntry.scheduled_at || undefined,
        end_time: newEntry.end_time || undefined,
        entry_type: newEntry.entry_type,
        is_recurring: newEntry.is_recurring,
        recurrence_pattern: newEntry.is_recurring && newEntry.recurrence_pattern ? 
          { pattern: newEntry.recurrence_pattern } : undefined,
        location: newEntry.location || undefined,
        participants: newEntry.participants ? newEntry.participants.split(',').map(p => p.trim()) : undefined,
        tags: newEntry.tags ? newEntry.tags.split(',').map(t => t.trim()) : []
      };
      
      await calendarService.createEntry(entryData);
      setNewEntry({
        title: '',
        description: '',
        scheduled_at: '',
        end_time: '',
        entry_type: 'event',
        is_recurring: false,
        recurrence_pattern: '',
        location: '',
        participants: '',
        tags: ''
      });
      setShowForm(false);
      loadEntries();
    } catch (err) {
      setError('Не вдалося створити запис: ' + (err.response?.data?.detail || err.message));
      console.error('Error creating entry:', err);
    }
  };

  const formatDateTime = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleString('uk-UA', {
      day: 'numeric',
      month: 'long',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const isToday = (dateStr) => {
    if (!dateStr) return false;
    const date = new Date(dateStr);
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isPast = (dateStr) => {
    if (!dateStr) return false;
    return new Date(dateStr) < new Date();
  };

  const getEntryIcon = (type) => {
    const icons = {
      event: '📅',
      meeting: '👥',
      deadline: '⏰',
      reminder: '🔔',
      task: '✓',
      appointment: '🏥',
      birthday: '🎂',
      holiday: '🎉'
    };
    return icons[type] || '📌';
  };

  const groupEntriesByDate = (entries) => {
    const grouped = {};
    entries.forEach(entry => {
      if (!entry.scheduled_at) {
        const key = 'Без дати';
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(entry);
        return;
      }
      const date = new Date(entry.scheduled_at);
      const key = date.toLocaleDateString('uk-UA', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(entry);
    });
    return grouped;
  };

  return (
    <div className="module-view calendar-view">
      <header className="module-header">
        <h1>Календар</h1>
        <p className="module-subtitle">Час, ритми, планування</p>
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
              {showForm ? 'Скасувати' : '+ Новий запис'}
            </button>
            <button 
              className="btn-secondary"
              onClick={loadEntries}
              disabled={loading}
            >
              ↻ Оновити
            </button>
          </div>

          <div className="view-mode-toggle">
            <button
              className={viewMode === 'list' ? 'toggle-active' : 'toggle-btn'}
              onClick={() => setViewMode('list')}
            >
              📋 Список
            </button>
            <button
              className={viewMode === 'calendar' ? 'toggle-active' : 'toggle-btn'}
              onClick={() => setViewMode('calendar')}
            >
              📅 Календар
            </button>
          </div>

          <div className="filter-buttons">
            <button 
              className={filter === 'all' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('all')}
            >
              Всі ({entries.length})
            </button>
            <button 
              className={filter === 'today' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('today')}
            >
              Сьогодні
            </button>
            <button 
              className={filter === 'upcoming' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('upcoming')}
            >
              Майбутні
            </button>
            <button 
              className={filter === 'recurring' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('recurring')}
            >
              🔄 Повторювані
            </button>
          </div>
        </div>

        {showForm && (
          <form className="calendar-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Назва *</label>
              <input
                type="text"
                value={newEntry.title}
                onChange={(e) => setNewEntry({...newEntry, title: e.target.value})}
                required
                placeholder="Назва події або завдання"
              />
            </div>

            <div className="form-group">
              <label>Опис</label>
              <textarea
                value={newEntry.description}
                onChange={(e) => setNewEntry({...newEntry, description: e.target.value})}
                rows={3}
                placeholder="Детальний опис..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Початок *</label>
                <input
                  type="datetime-local"
                  value={newEntry.scheduled_at}
                  onChange={(e) => setNewEntry({...newEntry, scheduled_at: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Кінець</label>
                <input
                  type="datetime-local"
                  value={newEntry.end_time}
                  onChange={(e) => setNewEntry({...newEntry, end_time: e.target.value})}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Тип</label>
                <select
                  value={newEntry.entry_type}
                  onChange={(e) => setNewEntry({...newEntry, entry_type: e.target.value})}
                >
                  <option value="event">Подія</option>
                  <option value="meeting">Зустріч</option>
                  <option value="deadline">Дедлайн</option>
                  <option value="reminder">Нагадування</option>
                  <option value="task">Завдання</option>
                  <option value="appointment">Прийом</option>
                  <option value="birthday">День народження</option>
                  <option value="holiday">Свято</option>
                </select>
              </div>

              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={newEntry.is_recurring}
                    onChange={(e) => setNewEntry({...newEntry, is_recurring: e.target.checked})}
                  />
                  {' '}Повторюваний
                </label>
              </div>
            </div>

            {newEntry.is_recurring && (
              <div className="form-group">
                <label>Шаблон повторення</label>
                <select
                  value={newEntry.recurrence_pattern}
                  onChange={(e) => setNewEntry({...newEntry, recurrence_pattern: e.target.value})}
                >
                  <option value="">Оберіть...</option>
                  <option value="daily">Щодня</option>
                  <option value="weekly">Щотижня</option>
                  <option value="monthly">Щомісяця</option>
                  <option value="yearly">Щороку</option>
                </select>
              </div>
            )}

            <div className="form-group">
              <label>Місце</label>
              <input
                type="text"
                value={newEntry.location}
                onChange={(e) => setNewEntry({...newEntry, location: e.target.value})}
                placeholder="Адреса або назва місця"
              />
            </div>

            <div className="form-group">
              <label>Учасники (через кому)</label>
              <input
                type="text"
                value={newEntry.participants}
                onChange={(e) => setNewEntry({...newEntry, participants: e.target.value})}
                placeholder="Іван, Марія, Петро"
              />
            </div>

            <div className="form-group">
              <label>Теги (через кому)</label>
              <input
                type="text"
                value={newEntry.tags}
                onChange={(e) => setNewEntry({...newEntry, tags: e.target.value})}
                placeholder="робота, важливо, особисте"
              />
            </div>

            <button type="submit" className="btn-primary">
              Створити запис
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading-state">
            Завантаження...
          </div>
        ) : entries.length === 0 ? (
          <div className="empty-state">
            <p>📅 Немає записів</p>
            <p className="text-secondary">Додайте перший запис у календар</p>
          </div>
        ) : viewMode === 'list' ? (
          <div className="calendar-list">
            {Object.entries(groupEntriesByDate(entries)).map(([date, dateEntries]) => (
              <div key={date} className="calendar-date-group">
                <h3 className="date-header">{date}</h3>
                <div className="entries-list">
                  {dateEntries.map((entry) => (
                    <div 
                      key={entry.id} 
                      className={`calendar-entry-card ${isPast(entry.scheduled_at) ? 'past' : ''} ${isToday(entry.scheduled_at) ? 'today' : ''}`}
                    >
                      <div className="entry-icon">
                        {getEntryIcon(entry.entry_type)}
                        {entry.is_recurring && <span className="recurring-badge">🔄</span>}
                      </div>
                      <div className="entry-content">
                        <h4>{entry.title}</h4>
                        {entry.description && (
                          <p className="entry-description">{entry.description}</p>
                        )}
                        <div className="entry-details">
                          {entry.scheduled_at && (
                            <span className="detail-item">
                              🕐 {formatDateTime(entry.scheduled_at)}
                              {entry.end_time && ` - ${new Date(entry.end_time).toLocaleTimeString('uk-UA', {hour: '2-digit', minute: '2-digit'})}`}
                            </span>
                          )}
                          {entry.location && (
                            <span className="detail-item">📍 {entry.location}</span>
                          )}
                          {entry.participants && entry.participants.length > 0 && (
                            <span className="detail-item">
                              👥 {entry.participants.join(', ')}
                            </span>
                          )}
                        </div>
                        {entry.tags && entry.tags.length > 0 && (
                          <div className="entry-tags">
                            {entry.tags.map((tag, idx) => (
                              <span key={idx} className="tag">#{tag}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="calendar-grid">
            <p className="info-message">🚧 Візуальний календар в розробці. Наразі використовуйте режим списку.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default CalendarView;
