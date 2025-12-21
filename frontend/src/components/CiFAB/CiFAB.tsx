/**
 * Global Ci Floating Action Button Component
 * Provides access to Ci overlay without changing navigation context
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import CiIcon from '../../assets/icon-ci.svg';
import './CiFAB.css';

interface CiFABProps {
  className?: string;
}

const CiFAB: React.FC<CiFABProps> = ({ className = '' }) => {
  const navigate = useNavigate();
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleOverlay = () => {
    setIsOverlayOpen(!isOverlayOpen);
  };

  const closeOverlay = () => {
    setIsOverlayOpen(false);
    setSearchQuery('');
  };

  useEffect(() => {
    if (isOverlayOpen) {
      // Fetch health status when overlay opens
      const fetchHealth = async () => {
        try {
          const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';
          const response = await fetch(`${API_BASE}/health`);
          const data = await response.json();
          setHealthStatus(data);
        } catch (error) {
          console.error('Failed to fetch health status:', error);
        }
      };
      fetchHealth();
    }
  }, [isOverlayOpen]);

  const modules = [
    { id: 'ci', name: 'Ci', path: '/ci', description: 'Центральне ядро', emoji: '⚙️' },
    { id: 'podija', name: 'ПоДія', path: '/podija', description: 'Події та сценарії', emoji: '🎯' },
    { id: 'nastrij', name: 'Настрій', path: '/nastrij', description: 'Емоційні стани', emoji: '😊' },
    { id: 'malya', name: 'Маля', path: '/malya', description: 'Ідеї та творчість', emoji: '💡' },
    { id: 'kazkar', name: 'Казкар', path: '/kazkar', description: 'Пам\'ять та історії', emoji: '📖' },
    { id: 'calendar', name: 'Календар', path: '/calendar', description: 'Час та планування', emoji: '📅' },
    { id: 'gallery', name: 'Галерея', path: '/gallery', description: 'Медіа-контент', emoji: '🖼️' },
  ];

  const handleNavigate = (path: string) => {
    navigate(path);
    closeOverlay();
  };

  const filteredModules = modules.filter(
    (module) =>
      module.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      module.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      {/* Floating Action Button */}
      <button
        className={`ci-fab ${className}`}
        onClick={toggleOverlay}
        aria-label="Open Ci central orchestration"
        title="Ci - Центральне ядро"
      >
        <img src={CiIcon} alt="Ci" className="ci-fab-icon" />
      </button>

      {/* Overlay */}
      {isOverlayOpen && (
        <div className="ci-overlay" onClick={closeOverlay}>
          <div className="ci-overlay-content" onClick={(e) => e.stopPropagation()}>
            <div className="ci-overlay-header">
              <h2>Ci — Центральне ядро</h2>
              <button
                className="ci-overlay-close"
                onClick={closeOverlay}
                aria-label="Close overlay"
              >
                ✕
              </button>
            </div>
            
            <div className="ci-overlay-body">
              <p className="ci-overlay-description">
                Центральна оркестрація системи Cimeika
              </p>

              {/* Quick Search */}
              <div className="ci-search" style={{ marginBottom: '1.5rem' }}>
                <input
                  type="text"
                  placeholder="🔍 Пошук модулів або команд..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '0.95rem',
                  }}
                />
              </div>

              {/* Module Navigation */}
              <div className="ci-modules" style={{ marginBottom: '1.5rem' }}>
                <h3>Навігація модулів</h3>
                <div style={{ display: 'grid', gap: '0.5rem' }}>
                  {filteredModules.map((module) => (
                    <button
                      key={module.id}
                      onClick={() => handleNavigate(module.path)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '0.75rem',
                        background: '#f8f9fa',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        transition: 'all 0.2s',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = '#e5e7eb';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = '#f8f9fa';
                      }}
                    >
                      <span style={{ fontSize: '1.5rem', marginRight: '0.75rem' }}>
                        {module.emoji}
                      </span>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 'bold' }}>{module.name}</div>
                        <div style={{ fontSize: '0.875rem', color: '#666' }}>
                          {module.description}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
              
              <div className="ci-actions">
                <h3>Швидкі дії</h3>
                <div className="ci-actions-grid">
                  <button className="ci-action-btn">
                    <span className="ci-action-icon">📝</span>
                    <span>Створити запис</span>
                  </button>
                  <button className="ci-action-btn">
                    <span className="ci-action-icon">📊</span>
                    <span>Статистика</span>
                  </button>
                  <button className="ci-action-btn">
                    <span className="ci-action-icon">⚙️</span>
                    <span>Налаштування</span>
                  </button>
                </div>
              </div>

              <div className="ci-status">
                <h3>Статус системи</h3>
                {healthStatus ? (
                  <div>
                    <div className="ci-status-indicator">
                      <span className="status-dot status-active"></span>
                      <span>
                        {healthStatus.status === 'healthy' || healthStatus.status === 'success'
                          ? 'Система активна'
                          : 'Система недоступна'}
                      </span>
                    </div>
                    {healthStatus.version && (
                      <div style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
                        Версія: {healthStatus.version}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="ci-status-indicator">
                    <span className="status-dot status-active"></span>
                    <span>Завантаження...</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default CiFAB;
