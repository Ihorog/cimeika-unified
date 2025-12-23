/**
 * Legend viewer component - displays full legend with rich formatting
 */
import React from 'react';
import type { KazkarEntry } from '../types';

interface LegendViewerProps {
  legend: KazkarEntry;
  onClose: () => void;
}

export const LegendViewer: React.FC<LegendViewerProps> = ({ legend, onClose }) => {
  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '2rem',
        overflow: 'auto',
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: '12px',
          maxWidth: '900px',
          width: '100%',
          maxHeight: '90vh',
          overflow: 'auto',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          style={{
            background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            color: '#fff',
            padding: '2rem',
            borderRadius: '12px 12px 0 0',
            position: 'relative',
          }}
        >
          <button
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '1rem',
              right: '1rem',
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              borderRadius: '50%',
              width: '40px',
              height: '40px',
              fontSize: '1.5rem',
              color: '#fff',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            ×
          </button>
          <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>⚡</div>
          <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>
            {legend.title}
          </h1>
          <div style={{ marginTop: '1rem', opacity: 0.9, fontSize: '0.95rem' }}>
            {legend.location && (
              <div style={{ marginBottom: '0.5rem' }}>
                📍 <strong>Місце:</strong> {legend.location}
              </div>
            )}
            {legend.participants && legend.participants.length > 0 && (
              <div style={{ marginBottom: '0.5rem' }}>
                👥 <strong>Учасники:</strong> {legend.participants.join(', ')}
              </div>
            )}
            <div>
              🕐 <strong>Створено:</strong> {new Date(legend.time).toLocaleDateString('uk-UA', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </div>
          </div>
        </div>

        {/* Content */}
        <div style={{ padding: '2rem' }}>
          <div
            style={{
              lineHeight: '1.8',
              fontSize: '1.1rem',
              color: '#374151',
              whiteSpace: 'pre-wrap',
            }}
          >
            {legend.content}
          </div>

          {/* Tags */}
          {legend.tags && legend.tags.length > 0 && (
            <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '2px solid #e5e7eb' }}>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                🏷️ Теги:
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {legend.tags.map((tag) => (
                  <span
                    key={tag}
                    style={{
                      background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
                      color: '#92400e',
                      padding: '0.5rem 1rem',
                      borderRadius: '20px',
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      border: '1px solid #fbbf24',
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Metadata */}
          <div
            style={{
              marginTop: '2rem',
              paddingTop: '2rem',
              borderTop: '2px solid #e5e7eb',
              fontSize: '0.875rem',
              color: '#6b7280',
            }}
          >
            <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '0.5rem' }}>
              <div><strong>ID:</strong></div>
              <div>{legend.id}</div>
              <div><strong>Модуль:</strong></div>
              <div>{legend.module}</div>
              <div><strong>Canon Bundle:</strong></div>
              <div style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{legend.canon_bundle_id}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
