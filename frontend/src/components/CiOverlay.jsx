import React, { useState } from 'react';
import './CiOverlay.css';

const CiOverlay = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating Ci Button */}
      <button 
        className="ci-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open Ci Assistant"
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
              onClick={() => setIsOpen(false)}
            >
              ×
            </button>
          </div>
          <div className="ci-overlay-content">
            <div className="ci-placeholder">
              <p>Text and voice interaction placeholder</p>
              <p className="ci-note">AI integration pending</p>
            </div>
          </div>
        </div>
      )}

      {/* Backdrop */}
      {isOpen && (
        <div 
          className="ci-backdrop"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
};

export default CiOverlay;
