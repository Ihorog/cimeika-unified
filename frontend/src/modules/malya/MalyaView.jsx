import React, { useState, useEffect } from 'react';
import { malyaService } from '../../services/modules';

const MalyaView = () => {
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all'); // all, active, archived
  const [newIdea, setNewIdea] = useState({
    title: '',
    description: '',
    idea_type: 'personal',
    status: 'active',
    tags: ''
  });

  useEffect(() => {
    loadIdeas();
  }, [filter]);

  const loadIdeas = async () => {
    setLoading(true);
    setError(null);
    try {
      let params = { limit: 50 };
      if (filter !== 'all') {
        params.status = filter;
      }
      
      const data = await malyaService.getIdeas(params);
      setIdeas(data);
    } catch (err) {
      setError('Не вдалося завантажити ідеї. Перевірте з\'єднання з backend.');
      console.error('Error loading ideas:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const ideaData = {
        title: newIdea.title,
        description: newIdea.description,
        idea_type: newIdea.idea_type,
        status: newIdea.status,
        tags: newIdea.tags ? newIdea.tags.split(',').map(t => t.trim()) : []
      };
      
      await malyaService.createIdea(ideaData);
      setNewIdea({
        title: '',
        description: '',
        idea_type: 'personal',
        status: 'active',
        tags: ''
      });
      setShowForm(false);
      loadIdeas();
    } catch (err) {
      setError('Не вдалося створити ідею: ' + (err.response?.data?.detail || err.message));
      console.error('Error creating idea:', err);
    }
  };

  return (
    <div className="module-view malya-view">
      <header className="module-header">
        <h1>Маля</h1>
        <p className="module-subtitle">Ідеї, творчість, інновації</p>
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
              {showForm ? 'Скасувати' : '💡 Нова ідея'}
            </button>
            <button 
              className="btn-secondary"
              onClick={loadIdeas}
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
              Всі ({ideas.length})
            </button>
            <button 
              className={filter === 'active' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('active')}
            >
              Активні
            </button>
            <button 
              className={filter === 'archived' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('archived')}
            >
              Архівні
            </button>
          </div>
        </div>

        {showForm && (
          <form className="idea-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Назва ідеї *</label>
              <input
                type="text"
                value={newIdea.title}
                onChange={(e) => setNewIdea({...newIdea, title: e.target.value})}
                required
                placeholder="Коротка назва ідеї"
              />
            </div>

            <div className="form-group">
              <label>Опис *</label>
              <textarea
                value={newIdea.description}
                onChange={(e) => setNewIdea({...newIdea, description: e.target.value})}
                required
                rows={5}
                placeholder="Детально опишіть вашу ідею..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Тип ідеї</label>
                <select
                  value={newIdea.idea_type}
                  onChange={(e) => setNewIdea({...newIdea, idea_type: e.target.value})}
                >
                  <option value="personal">Особиста</option>
                  <option value="project">Проєкт</option>
                  <option value="business">Бізнес</option>
                  <option value="creative">Творча</option>
                  <option value="improvement">Покращення</option>
                  <option value="invention">Винахід</option>
                </select>
              </div>

              <div className="form-group">
                <label>Статус</label>
                <select
                  value={newIdea.status}
                  onChange={(e) => setNewIdea({...newIdea, status: e.target.value})}
                >
                  <option value="active">Активна</option>
                  <option value="in_progress">В процесі</option>
                  <option value="completed">Реалізована</option>
                  <option value="archived">Архівна</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Теги (через кому)</label>
              <input
                type="text"
                value={newIdea.tags}
                onChange={(e) => setNewIdea({...newIdea, tags: e.target.value})}
                placeholder="інновація, технологія, стартап"
              />
            </div>

            <button type="submit" className="btn-primary">
              Зберегти ідею
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading-state">
            Завантаження...
          </div>
        ) : ideas.length === 0 ? (
          <div className="empty-state">
            <p>💡 Немає ідей</p>
            <p className="text-secondary">Запишіть вашу першу ідею в Маля</p>
          </div>
        ) : (
          <div className="ideas-grid">
            {ideas.map((idea) => (
              <div key={idea.id} className="idea-card">
                <div className="idea-icon">💡</div>
                <h3>{idea.title}</h3>
                <p className="idea-description">{idea.description}</p>
                <div className="idea-meta">
                  {idea.idea_type && (
                    <span className="badge">{idea.idea_type}</span>
                  )}
                  {idea.status && (
                    <span className={`status-badge status-${idea.status}`}>
                      {idea.status}
                    </span>
                  )}
                </div>
                {idea.tags && idea.tags.length > 0 && (
                  <div className="idea-tags">
                    {idea.tags.map((tag, idx) => (
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

export default MalyaView;
