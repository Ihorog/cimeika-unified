/**
 * NodeView Component
 * Displays a single Legend ci node with short/deep text layers
 */
import React, { useState } from 'react';
import './NodeView.css';

const NodeView = ({ node, onClose, onNavigate, connectedNodes = [] }) => {
  const [layerDepth, setLayerDepth] = useState('short');

  if (!node) return null;

  return (
    <div className="node-view-overlay" onClick={onClose}>
      <div className="node-view-container" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="node-view-header">
          <div className="node-view-icon">{node.icon}</div>
          <div className="node-view-header-text">
            <h2 className="node-view-title">{node.title}</h2>
            <div className="node-view-meta">
              <span>Вузол {node.id} з 20</span>
            </div>
          </div>
          <button className="node-view-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Layer Toggle */}
        <div className="node-view-layer-toggle">
          <button
            className={`layer-toggle-btn ${layerDepth === 'short' ? 'active' : ''}`}
            onClick={() => setLayerDepth('short')}
          >
            Короткий текст
          </button>
          <button
            className={`layer-toggle-btn ${layerDepth === 'deep' ? 'active' : ''}`}
            onClick={() => setLayerDepth('deep')}
          >
            Глибинний текст
          </button>
        </div>

        {/* Content */}
        <div className="node-view-content">
          {layerDepth === 'short' ? (
            <p className="node-view-short-text">{node.short_text}</p>
          ) : (
            <div className="node-view-deep-text">
              {node.deep_text.split('\n\n').map((paragraph, idx) => (
                <p key={idx}>{paragraph}</p>
              ))}
            </div>
          )}
        </div>

        {/* Tags */}
        {node.tags && node.tags.length > 0 && (
          <div className="node-view-tags">
            <span className="node-view-tags-label">🏷️ Теги:</span>
            <div className="node-view-tags-list">
              {node.tags.map((tag) => (
                <span key={tag} className="node-view-tag">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Visual Hint */}
        {node.visual_hint && (
          <div className="node-view-visual-hint">
            <strong>Візуальна підказка:</strong> {node.visual_hint}
          </div>
        )}

        {/* Connected Nodes */}
        {connectedNodes && connectedNodes.length > 0 && (
          <div className="node-view-connections">
            <h3 className="node-view-connections-title">Пов&apos;язані вузли</h3>
            <div className="node-view-connections-grid">
              {connectedNodes.map((conn) => (
                <button
                  key={conn.id}
                  className="node-view-connection-card"
                  onClick={() => onNavigate(conn)}
                >
                  <span className="node-view-connection-icon">{conn.icon}</span>
                  <span className="node-view-connection-title">{conn.title}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NodeView;
