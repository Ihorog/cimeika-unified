import React, { useState } from 'react';
import { ciService } from '../../services/modules';
import { useNavigate } from 'react-router-dom';

const CiView = () => {
  const navigate = useNavigate();
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleCapture = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await ciService.quickCapture(input);
      setResponse(result);
      // Auto-scroll to response
      setTimeout(() => {
        document.querySelector('.ci-response')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      setError('Не вдалося обробити запит. Перевірте підключення до backend.');
      console.error('Ci capture error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleModuleNavigation = (modulePath) => {
    navigate(modulePath);
  };

  const modules = [
    { 
      name: 'Казкар', 
      path: '/app/kazkar', 
      icon: '📖', 
      description: 'Пам\'ять, історії, легенди',
      color: '#7B2CBF'
    },
    { 
      name: 'Подія', 
      path: '/app/podija', 
      icon: '🎯', 
      description: 'Події, майбутнє, сценарії',
      color: '#F72585'
    },
    { 
      name: 'Настрій', 
      path: '/app/nastrij', 
      icon: '💭', 
      description: 'Емоційні стани',
      color: '#4361EE'
    },
    { 
      name: 'Маля', 
      path: '/app/malya', 
      icon: '💡', 
      description: 'Ідеї та творчість',
      color: '#F9C74F'
    },
    { 
      name: 'Календар', 
      path: '/app/calendar', 
      icon: '📅', 
      description: 'Час та планування',
      color: '#90BE6D'
    },
    { 
      name: 'Галерея', 
      path: '/app/gallery', 
      icon: '🖼️', 
      description: 'Візуальний архів',
      color: '#F94144'
    },
  ];

  return (
    <div className="module-view ci-view">
      <header className="module-header ci-hero">
        <h1>Ci</h1>
        <p className="module-subtitle">Центральне ядро · Точка входу в систему</p>
        <p className="ci-tagline">
          &quot;Дійсність перша, дія перед поясненням&quot; — CANON v1.0.0
        </p>
      </header>
      
      <main className="module-content">
        {/* Main Capture Interface */}
        <section className="ci-capture-section">
          <h2 className="section-title">ci.capture() — Захопіть момент</h2>
          <form onSubmit={handleCapture} className="ci-main-form">
            <textarea
              className="ci-main-input"
              placeholder="Що на думці? Що відбувається? Розкажіть Ci..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              rows={4}
              disabled={loading}
            />
            <button 
              type="submit" 
              className="btn-primary btn-large"
              disabled={loading || !input.trim()}
            >
              {loading ? '⏳ Обробка...' : '✨ Захопити'}
            </button>
          </form>

          {error && (
            <div className="error-banner">
              {error}
            </div>
          )}

          {response && (
            <div className="ci-response ci-main-response">
              <h3>📊 Результат аналізу</h3>
              <div className="response-grid">
                <div className="response-card">
                  <strong>ID події:</strong>
                  <code>{response.event_id}</code>
                </div>
                
                {response.classification?.emotion_state && (
                  <div className="response-card">
                    <strong>Емоційний стан:</strong>
                    <span className="highlight">{response.classification.emotion_state}</span>
                  </div>
                )}

                {response.classification?.intent && (
                  <div className="response-card">
                    <strong>Намір:</strong>
                    <span className="highlight">{response.classification.intent}</span>
                  </div>
                )}

                {response.classification?.module_suggestion && (
                  <div className="response-card">
                    <strong>Рекомендований модуль:</strong>
                    <span className="highlight">{response.classification.module_suggestion}</span>
                  </div>
                )}

                {response.time_position && (
                  <div className="response-card">
                    <strong>Час:</strong>
                    <span>{response.time_position.readable}</span>
                  </div>
                )}

                {response.classification?.tags?.length > 0 && (
                  <div className="response-card full-width">
                    <strong>Теги:</strong>
                    <div className="tag-list">
                      {response.classification.tags.map((tag, idx) => (
                        <span key={idx} className="tag">{tag}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {response.classification?.module_suggestion && (
                <button 
                  className="btn-secondary"
                  onClick={() => handleModuleNavigation(`/${response.classification.module_suggestion.toLowerCase()}`)}
                >
                  Перейти до модуля →
                </button>
              )}
            </div>
          )}
        </section>

        {/* Modules Navigation */}
        <section className="ci-modules-section">
          <h2 className="section-title">Сім модулів · Сім інструментів</h2>
          <div className="modules-grid">
            {modules.map((module) => (
              <div 
                key={module.path}
                className="module-card"
                onClick={() => handleModuleNavigation(module.path)}
                style={{ borderLeftColor: module.color }}
              >
                <div className="module-icon">{module.icon}</div>
                <h3>{module.name}</h3>
                <p>{module.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Quick Info */}
        <section className="ci-info-section">
          <div className="info-card">
            <h3>🎯 Принципи Ci</h3>
            <ul>
              <li>Дійсність перша — фіксуй як є</li>
              <li>Дія перед поясненням — робити, не планувати</li>
              <li>≤5 секунд до першої дії</li>
              <li>Без логіну, stateless</li>
              <li>Емісія подій, не збереження</li>
            </ul>
          </div>
          <div className="info-card">
            <h3>📖 Легенди Ci</h3>
            <p>Ci народився з необхідності пам&apos;ятати важливе в потоці життя.</p>
            <button 
              className="btn-secondary"
              onClick={() => navigate('/app/legends')}
            >
              Читати легенди →
            </button>
          </div>
        </section>
      </main>
    </div>
  );
};

export default CiView;
