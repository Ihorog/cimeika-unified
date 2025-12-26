import React, { useState, useEffect } from 'react';
import { kazkarService } from '../../services/modules';

const KazkarView = () => {
  const [stories, setStories] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [newStory, setNewStory] = useState({
    title: '',
    content: '',
    story_type: 'memory',
    participants: '',
    location: '',
    tags: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [storiesData, statsData] = await Promise.all([
        kazkarService.getStories({ limit: 20 }),
        kazkarService.getStats()
      ]);
      setStories(storiesData);
      setStats(statsData);
    } catch (err) {
      setError('Не вдалося завантажити дані. Перевірте з\'єднання з backend.');
      console.error('Error loading Kazkar data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const storyData = {
        title: newStory.title,
        content: newStory.content,
        story_type: newStory.story_type,
        participants: newStory.participants ? newStory.participants.split(',').map(p => p.trim()) : [],
        location: newStory.location || undefined,
        tags: newStory.tags ? newStory.tags.split(',').map(t => t.trim()) : []
      };
      
      await kazkarService.createStory(storyData);
      setNewStory({
        title: '',
        content: '',
        story_type: 'memory',
        participants: '',
        location: '',
        tags: ''
      });
      setShowForm(false);
      loadData();
    } catch (err) {
      setError('Не вдалося створити історію: ' + (err.response?.data?.detail || err.message));
      console.error('Error creating story:', err);
    }
  };

  return (
    <div className="module-view kazkar-view">
      <header className="module-header">
        <h1>Казкар</h1>
        <p className="module-subtitle">Пам&apos;ять, історії, легенди</p>
      </header>
      
      <main className="module-content">
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {stats && (
          <div className="stats-card">
            <h3>Статистика</h3>
            <p>Всього історій: <strong>{stats.total_stories}</strong></p>
            {stats.by_type && Object.keys(stats.by_type).length > 0 && (
              <div className="stats-breakdown">
                {Object.entries(stats.by_type).map(([type, count]) => (
                  <span key={type} className="stat-badge">
                    {type}: {count}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="module-actions">
          <button 
            className="btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Скасувати' : '+ Нова історія'}
          </button>
          <button 
            className="btn-secondary"
            onClick={loadData}
            disabled={loading}
          >
            ↻ Оновити
          </button>
        </div>

        {showForm && (
          <form className="story-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Назва *</label>
              <input
                type="text"
                value={newStory.title}
                onChange={(e) => setNewStory({...newStory, title: e.target.value})}
                required
                placeholder="Назва історії"
              />
            </div>

            <div className="form-group">
              <label>Зміст *</label>
              <textarea
                value={newStory.content}
                onChange={(e) => setNewStory({...newStory, content: e.target.value})}
                required
                rows={5}
                placeholder="Розкажіть вашу історію..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Тип історії</label>
                <select
                  value={newStory.story_type}
                  onChange={(e) => setNewStory({...newStory, story_type: e.target.value})}
                >
                  <option value="memory">Спогад</option>
                  <option value="legend">Легенда</option>
                  <option value="story">Історія</option>
                  <option value="event">Подія</option>
                </select>
              </div>

              <div className="form-group">
                <label>Місце</label>
                <input
                  type="text"
                  value={newStory.location}
                  onChange={(e) => setNewStory({...newStory, location: e.target.value})}
                  placeholder="Де це відбулося?"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Учасники (через кому)</label>
              <input
                type="text"
                value={newStory.participants}
                onChange={(e) => setNewStory({...newStory, participants: e.target.value})}
                placeholder="Ім'я1, Ім'я2, ..."
              />
            </div>

            <div className="form-group">
              <label>Теги (через кому)</label>
              <input
                type="text"
                value={newStory.tags}
                onChange={(e) => setNewStory({...newStory, tags: e.target.value})}
                placeholder="сім'я, подорож, свято"
              />
            </div>

            <button type="submit" className="btn-primary">
              Зберегти історію
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading-state">
            Завантаження...
          </div>
        ) : stories.length === 0 ? (
          <div className="empty-state">
            <p>Поки що немає історій</p>
            <p className="text-secondary">Створіть першу історію для Казкара</p>
          </div>
        ) : (
          <div className="stories-grid">
            {stories.map((story) => (
              <div key={story.id} className="story-card">
                <h3>{story.title}</h3>
                <p className="story-content">{story.content}</p>
                <div className="story-meta">
                  {story.story_type && (
                    <span className="badge">{story.story_type}</span>
                  )}
                  {story.location && (
                    <span className="meta-item">📍 {story.location}</span>
                  )}
                  {story.participants && story.participants.length > 0 && (
                    <span className="meta-item">👥 {story.participants.join(', ')}</span>
                  )}
                </div>
                {story.tags && story.tags.length > 0 && (
                  <div className="story-tags">
                    {story.tags.map((tag, idx) => (
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

export default KazkarView;
