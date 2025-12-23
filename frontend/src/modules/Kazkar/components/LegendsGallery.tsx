/**
 * Legends gallery component - displays legends in a beautiful grid
 */
import React, { useState } from 'react';
import type { KazkarEntry } from '../types';
import { LegendViewer } from './LegendViewer';

interface LegendsGalleryProps {
  legends: KazkarEntry[];
  loading?: boolean;
}

export const LegendsGallery: React.FC<LegendsGalleryProps> = ({ legends, loading }) => {
  const [selectedLegend, setSelectedLegend] = useState<KazkarEntry | null>(null);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem', color: '#666' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚡</div>
        <p>Завантаження легенд...</p>
      </div>
    );
  }

  if (legends.length === 0) {
    return (
      <div
        style={{
          textAlign: 'center',
          padding: '3rem',
          background: '#f9fafb',
          borderRadius: '12px',
          border: '2px dashed #d1d5db',
        }}
      >
        <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>⚡</div>
        <h3 style={{ color: '#6b7280', marginBottom: '0.5rem' }}>Ще немає легенд</h3>
        <p style={{ color: '#9ca3af' }}>Створіть першу легенду Ci!</p>
      </div>
    );
  }

  return (
    <>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '1.5rem',
        }}
      >
        {legends.map((legend) => (
          <div
            key={legend.id}
            onClick={() => setSelectedLegend(legend)}
            style={{
              background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
              borderRadius: '12px',
              padding: '1.5rem',
              cursor: 'pointer',
              border: '2px solid #fbbf24',
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.07)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 12px 24px rgba(0, 0, 0, 0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.07)';
            }}
          >
            {/* Icon and Title */}
            <div style={{ display: 'flex', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div style={{ fontSize: '2.5rem', marginRight: '0.75rem', flexShrink: 0 }}>⚡</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <h3
                  style={{
                    margin: 0,
                    fontSize: '1.25rem',
                    fontWeight: 'bold',
                    color: '#92400e',
                    lineHeight: '1.3',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}
                >
                  {legend.title}
                </h3>
              </div>
            </div>

            {/* Content Preview */}
            <p
              style={{
                color: '#78350f',
                fontSize: '0.95rem',
                lineHeight: '1.6',
                marginBottom: '1rem',
                display: '-webkit-box',
                WebkitLineClamp: 4,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
              }}
            >
              {legend.content}
            </p>

            {/* Metadata */}
            <div style={{ fontSize: '0.875rem', color: '#92400e', marginBottom: '1rem' }}>
              {legend.participants && legend.participants.length > 0 && (
                <div style={{ marginBottom: '0.25rem' }}>
                  👥 {legend.participants.join(', ')}
                </div>
              )}
              {legend.location && (
                <div style={{ marginBottom: '0.25rem' }}>
                  📍 {legend.location}
                </div>
              )}
            </div>

            {/* Tags Preview */}
            {legend.tags && legend.tags.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
                {legend.tags.slice(0, 3).map((tag) => (
                  <span
                    key={tag}
                    style={{
                      background: '#fbbf24',
                      color: '#78350f',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '12px',
                      fontSize: '0.75rem',
                      fontWeight: '500',
                    }}
                  >
                    {tag}
                  </span>
                ))}
                {legend.tags.length > 3 && (
                  <span
                    style={{
                      color: '#92400e',
                      padding: '0.25rem 0.5rem',
                      fontSize: '0.75rem',
                    }}
                  >
                    +{legend.tags.length - 3}
                  </span>
                )}
              </div>
            )}

            {/* Read More Indicator */}
            <div
              style={{
                marginTop: '1rem',
                paddingTop: '1rem',
                borderTop: '1px solid #fbbf24',
                textAlign: 'center',
                color: '#92400e',
                fontSize: '0.875rem',
                fontWeight: '600',
              }}
            >
              Читати повністю →
            </div>
          </div>
        ))}
      </div>

      {/* Legend Viewer Modal */}
      {selectedLegend && (
        <LegendViewer
          legend={selectedLegend}
          onClose={() => setSelectedLegend(null)}
        />
      )}
    </>
  );
};
