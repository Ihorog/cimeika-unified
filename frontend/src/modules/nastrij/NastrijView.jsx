import React, { useState, useEffect } from 'react';
import { nastrijService } from '../../services/modules';

const NastrijView = () => {
  const [emotions, setEmotions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all'); // all, happy, sad, neutral, etc.
  const [newEmotion, setNewEmotion] = useState({
    emotion_state: '',
    intensity: 5,
    context: '',
    triggers: '',
    notes: '',
    tags: ''
  });

  // Emotion states with icons and colors
  const emotionStates = [
    { value: 'щасливий', label: 'Щасливий', icon: '😊', color: '#FFD700' },
    { value: 'сумний', label: 'Сумний', icon: '😢', color: '#4169E1' },
    { value: 'спокійний', label: 'Спокійний', icon: '😌', color: '#90EE90' },
    { value: 'тривожний', label: 'Тривожний', icon: '😰', color: '#FFA500' },
    { value: 'злий', label: 'Злий', icon: '😠', color: '#FF4444' },
    { value: 'натхненний', label: 'Натхненний', icon: '✨', color: '#9370DB' },
    { value: 'втомлений', label: 'Втомлений', icon: '😴', color: '#778899' },
    { value: 'енергійний', label: 'Енергійний', icon: '⚡', color: '#FF6347' },
    { value: 'задумливий', label: 'Задумливий', icon: '🤔', color: '#87CEEB' },
    { value: 'вдячний', label: 'Вдячний', icon: '🙏', color: '#DDA0DD' }
  ];

  useEffect(() => {
    loadEmotions();
  }, [filter]);

  const loadEmotions = async () => {
    setLoading(true);
    setError(null);
    try {
      let params = { limit: 50 };
      if (filter !== 'all') {
        params.emotion_state = filter;
      }
      
      const data = await nastrijService.getEmotions(params);
      setEmotions(data);
    } catch (err) {
      setError('Не вдалося завантажити емоційні стани. Перевірте з\'єднання з backend.');
      console.error('Error loading emotions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const emotionData = {
        emotion_state: newEmotion.emotion_state,
        intensity: parseFloat(newEmotion.intensity),
        context: newEmotion.context,
        triggers: newEmotion.triggers ? newEmotion.triggers.split(',').map(t => t.trim()) : [],
        notes: newEmotion.notes,
        tags: newEmotion.tags ? newEmotion.tags.split(',').map(t => t.trim()) : []
      };
      
      await nastrijService.createEmotion(emotionData);
      setNewEmotion({
        emotion_state: '',
        intensity: 5,
        context: '',
        triggers: '',
        notes: '',
        tags: ''
      });
      setShowForm(false);
      loadEmotions();
    } catch (err) {
      setError('Не вдалося створити емоційний запис: ' + (err.response?.data?.detail || err.message));
      console.error('Error creating emotion:', err);
    }
  };

  const getEmotionIcon = (state) => {
    const emotion = emotionStates.find(e => e.value === state);
    return emotion ? emotion.icon : '💭';
  };

  const getEmotionColor = (state) => {
    const emotion = emotionStates.find(e => e.value === state);
    return emotion ? emotion.color : '#999';
  };

  return (
    <div className="module-view nastrij-view">
      <header className="module-header">
        <h1>Настрій</h1>
        <p className="module-subtitle">Емоційні стани, контекст</p>
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
              {showForm ? 'Скасувати' : '💭 Записати емоцію'}
            </button>
            <button 
              className="btn-secondary"
              onClick={loadEmotions}
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
              Всі ({emotions.length})
            </button>
            {emotionStates.slice(0, 6).map((emotion) => (
              <button 
                key={emotion.value}
                className={filter === emotion.value ? 'filter-active' : 'filter-btn'}
                onClick={() => setFilter(emotion.value)}
                title={emotion.label}
              >
                {emotion.icon}
              </button>
            ))}
          </div>
        </div>

        {showForm && (
          <form className="emotion-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Емоційний стан *</label>
              <select
                value={newEmotion.emotion_state}
                onChange={(e) => setNewEmotion({...newEmotion, emotion_state: e.target.value})}
                required
              >
                <option value="">Оберіть стан</option>
                {emotionStates.map((emotion) => (
                  <option key={emotion.value} value={emotion.value}>
                    {emotion.icon} {emotion.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Інтенсивність: {newEmotion.intensity}/10</label>
              <input
                type="range"
                min="1"
                max="10"
                value={newEmotion.intensity}
                onChange={(e) => setNewEmotion({...newEmotion, intensity: e.target.value})}
                className="intensity-slider"
              />
              <div className="intensity-labels">
                <span>Слабо</span>
                <span>Помірно</span>
                <span>Сильно</span>
              </div>
            </div>

            <div className="form-group">
              <label>Контекст</label>
              <textarea
                value={newEmotion.context}
                onChange={(e) => setNewEmotion({...newEmotion, context: e.target.value})}
                rows={3}
                placeholder="Що відбувається? В якій ситуації ви це відчуваєте?"
              />
            </div>

            <div className="form-group">
              <label>Тригери (через кому)</label>
              <input
                type="text"
                value={newEmotion.triggers}
                onChange={(e) => setNewEmotion({...newEmotion, triggers: e.target.value})}
                placeholder="робота, люди, погода"
              />
            </div>

            <div className="form-group">
              <label>Примітки</label>
              <textarea
                value={newEmotion.notes}
                onChange={(e) => setNewEmotion({...newEmotion, notes: e.target.value})}
                rows={2}
                placeholder="Додаткові деталі або роздуми..."
              />
            </div>

            <div className="form-group">
              <label>Теги (через кому)</label>
              <input
                type="text"
                value={newEmotion.tags}
                onChange={(e) => setNewEmotion({...newEmotion, tags: e.target.value})}
                placeholder="настрій, день, відчуття"
              />
            </div>

            <button type="submit" className="btn-primary">
              Зберегти емоцію
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading-state">
            Завантаження...
          </div>
        ) : emotions.length === 0 ? (
          <div className="empty-state">
            <p>💭 Немає записів</p>
            <p className="text-secondary">Запишіть ваш перший емоційний стан</p>
          </div>
        ) : (
          <div className="emotions-grid">
            {emotions.map((emotion) => (
              <div 
                key={emotion.id} 
                className="emotion-card"
                style={{ borderLeftColor: getEmotionColor(emotion.emotion_state) }}
              >
                <div className="emotion-header">
                  <div className="emotion-icon-large">
                    {getEmotionIcon(emotion.emotion_state)}
                  </div>
                  <div className="emotion-title">
                    <h3>{emotion.emotion_state}</h3>
                    {emotion.intensity && (
                      <div className="emotion-intensity">
                        <div className="intensity-bar">
                          <div 
                            className="intensity-fill" 
                            style={{ 
                              width: `${emotion.intensity * 10}%`,
                              backgroundColor: getEmotionColor(emotion.emotion_state)
                            }}
                          />
                        </div>
                        <span className="intensity-value">{emotion.intensity}/10</span>
                      </div>
                    )}
                  </div>
                </div>

                {emotion.context && (
                  <p className="emotion-context">{emotion.context}</p>
                )}

                {emotion.triggers && emotion.triggers.length > 0 && (
                  <div className="emotion-triggers">
                    <strong>Тригери:</strong>
                    {emotion.triggers.map((trigger, idx) => (
                      <span key={idx} className="trigger-badge">⚡ {trigger}</span>
                    ))}
                  </div>
                )}

                {emotion.notes && (
                  <p className="emotion-notes">
                    <strong>Примітки:</strong> {emotion.notes}
                  </p>
                )}

                <div className="emotion-meta">
                  {emotion.time && (
                    <span className="meta-item">
                      🕐 {new Date(emotion.time).toLocaleString('uk-UA')}
                    </span>
                  )}
                </div>

                {emotion.tags && emotion.tags.length > 0 && (
                  <div className="emotion-tags">
                    {emotion.tags.map((tag, idx) => (
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

export default NastrijView;
