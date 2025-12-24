import React, { useState } from 'react';
import { ciService } from '../services/modules';
import './CiOverlay.css';

const CiOverlay = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await ciService.quickCapture(input);
      setResponse(result);
      setInput('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to capture. Backend might be offline.');
      console.error('Ci capture error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setIsOpen(false);
    setResponse(null);
    setError(null);
  };

  return (
    <>
      {/* Floating Ci Button */}
      <button 
        className="ci-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open Ci Assistant"
        title="Ci - Центральне ядро"
      >
        <span className="ci-icon">Ci</span>
      </button>

      {/* Overlay Drawer */}
      {isOpen && (
        <div className="ci-overlay">
          <div className="ci-overlay-header">
            <h2>Ci Assistant</h2>
            <button 
              className="ci-close"
              onClick={handleClose}
              aria-label="Close"
            >
              ×
            </button>
          </div>
          <div className="ci-overlay-content">
            <div className="ci-input-section">
              <form onSubmit={handleSubmit}>
                <textarea
                  className="ci-input"
                  placeholder="Що на серці? Розкажіть Ci..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  rows={3}
                  disabled={loading}
                />
                <button 
                  type="submit" 
                  className="ci-submit"
                  disabled={loading || !input.trim()}
                >
                  {loading ? 'Обробка...' : 'Захопити'}
                </button>
              </form>

              {error && (
                <div className="ci-error">
                  <strong>Помилка:</strong> {error}
                </div>
              )}

              {response && (
                <div className="ci-response">
                  <h3>Відповідь Ci</h3>
                  <div className="ci-response-section">
                    <strong>ID події:</strong> {response.event_id}
                  </div>
                  
                  {response.classification && (
                    <div className="ci-response-section">
                      <strong>Класифікація:</strong>
                      <ul>
                        {response.classification.emotion_state && (
                          <li>Емоційний стан: {response.classification.emotion_state}</li>
                        )}
                        {response.classification.intent && (
                          <li>Намір: {response.classification.intent}</li>
                        )}
                        {response.classification.module_suggestion && (
                          <li>Рекомендований модуль: {response.classification.module_suggestion}</li>
                        )}
                        {response.classification.tags?.length > 0 && (
                          <li>Теги: {response.classification.tags.join(', ')}</li>
                        )}
                      </ul>
                    </div>
                  )}

                  {response.time_position && (
                    <div className="ci-response-section">
                      <strong>Час:</strong> {response.time_position.readable}
                    </div>
                  )}

                  {response.seo_context && (
                    <div className="ci-response-section">
                      <strong>SEO контекст:</strong> {response.seo_context.url}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="ci-info">
              <p className="ci-note">
                <strong>CANON v1.0.0:</strong> ci.capture() - Єдина точка входу
              </p>
              <p className="ci-note">
                Без логіну, stateless дія, випромінює подію
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Backdrop */}
      {isOpen && (
        <div 
          className="ci-backdrop"
          onClick={handleClose}
        />
      )}
    </>
  );
};

export default CiOverlay;
