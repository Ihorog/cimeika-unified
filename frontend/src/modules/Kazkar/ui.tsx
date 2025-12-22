/**
 * Kazkar module UI components
 * Reusable UI components specific to Kazkar (Memory/Stories) module
 */

import React from 'react';
import type { KazkarEntry } from './types';

interface KazkarEntryCardProps {
  entry: KazkarEntry;
  onClick?: () => void;
}

export const KazkarEntryCard: React.FC<KazkarEntryCardProps> = ({ entry, onClick }) => {
  const typeEmoji = {
    story: '📖',
    memory: '💭',
    legend: '⚡',
    fact: '📌',
  };

  const typeColor = {
    story: '#8b5cf6',
    memory: '#3b82f6',
    legend: '#f59e0b',
    fact: '#10b981',
  };

  const typeLabel = {
    story: 'Історія',
    memory: 'Спогад',
    legend: 'Легенда',
    fact: 'Факт',
  };

  const storyType = entry.story_type || 'memory';

  return (
    <div
      style={{
        background: '#fff',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: `4px solid ${typeColor[storyType]}`,
        cursor: onClick ? 'pointer' : 'default',
        marginBottom: '0.5rem',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      }}
      onClick={onClick}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>
          {typeEmoji[storyType]}
        </span>
        <strong>{entry.title}</strong>
      </div>
      <p style={{ color: '#666', marginBottom: '0.5rem', lineHeight: '1.5' }}>
        {entry.content.length > 200 ? `${entry.content.substring(0, 200)}...` : entry.content}
      </p>
      <div style={{ fontSize: '0.875rem', color: '#888' }}>
        <div>Тип: {typeLabel[storyType]}</div>
        {entry.location && <div>Місце: {entry.location}</div>}
        {entry.participants && entry.participants.length > 0 && (
          <div>Учасники: {entry.participants.join(', ')}</div>
        )}
        <div>Час: {new Date(entry.time).toLocaleDateString('uk-UA')}</div>
      </div>
      {entry.tags && entry.tags.length > 0 && (
        <div style={{ marginTop: '0.5rem' }}>
          {entry.tags.map((tag) => (
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
