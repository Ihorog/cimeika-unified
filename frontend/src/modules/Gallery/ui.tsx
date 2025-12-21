/**
 * Gallery module UI components
 * Reusable UI components specific to Gallery module
 */

import React from 'react';
import type { GalleryItem } from './types';

interface GalleryItemCardProps {
  item: GalleryItem;
  onClick?: () => void;
}

export const GalleryItemCard: React.FC<GalleryItemCardProps> = ({ item, onClick }) => {
  const typeEmoji = {
    image: '🖼️',
    video: '🎥',
    audio: '🎵',
    document: '📄',
  };

  return (
    <div
      style={{
        background: '#fff',
        padding: '1rem',
        borderRadius: '8px',
        cursor: onClick ? 'pointer' : 'default',
        marginBottom: '0.5rem',
        border: '1px solid #e5e7eb',
      }}
      onClick={onClick}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>
          {typeEmoji[item.type]}
        </span>
        <strong>{item.title}</strong>
      </div>
      {item.description && <p style={{ color: '#666', marginBottom: '0.5rem' }}>{item.description}</p>}
      {item.thumbnail_url && (
        <img
          src={item.thumbnail_url}
          alt={item.title}
          style={{ width: '100%', borderRadius: '4px', marginBottom: '0.5rem' }}
        />
      )}
      <div style={{ fontSize: '0.875rem', color: '#888' }}>
        Створено: {new Date(item.created_at).toLocaleDateString('uk-UA')}
      </div>
      {item.tags && item.tags.length > 0 && (
        <div style={{ marginTop: '0.5rem' }}>
          {item.tags.map((tag) => (
            <span
              key={tag}
              style={{
                display: 'inline-block',
                background: '#e5e7eb',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontSize: '0.75rem',
                marginRight: '0.25rem',
              }}
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};
