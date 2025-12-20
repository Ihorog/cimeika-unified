/**
 * Global Ci Floating Action Button Component
 * Provides access to Ci overlay without changing navigation context
 */
import React, { useState } from 'react';
import './CiFAB.css';

interface CiFABProps {
  className?: string;
}

const CiFAB: React.FC<CiFABProps> = ({ className = '' }) => {
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);

  const toggleOverlay = () => {
    setIsOverlayOpen(!isOverlayOpen);
  };

  const closeOverlay = () => {
    setIsOverlayOpen(false);
  };

  return (
    <>
      {/* Floating Action Button */}
      <button
        className={`ci-fab ${className}`}
        onClick={toggleOverlay}
        aria-label="Open Ci central orchestration"
        title="Ci - Центральне ядро"
      >
        <span className="ci-fab-icon">Ci</span>
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
              
              <div className="ci-actions">
                <h3>Швидкі дії</h3>
                <div className="ci-actions-grid">
                  <button className="ci-action-btn">
                    <span className="ci-action-icon">📝</span>
                    <span>Створити запис</span>
                  </button>
                  <button className="ci-action-btn">
                    <span className="ci-action-icon">🔍</span>
                    <span>Пошук</span>
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
                <div className="ci-status-indicator">
                  <span className="status-dot status-active"></span>
                  <span>Система активна</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default CiFAB;
