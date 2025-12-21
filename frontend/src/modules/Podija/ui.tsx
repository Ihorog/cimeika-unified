/**
 * Podija module UI components
 * Reusable UI components specific to Podija (Events) module
 */

import React from 'react';
import type { TimelineNode } from './types';

interface TimelineNodeCardProps {
  node: TimelineNode;
  onClick?: () => void;
}

export const TimelineNodeCard: React.FC<TimelineNodeCardProps> = ({ node, onClick }) => {
  const typeColor = {
    past: '#94a3b8',
    present: '#3b82f6',
    future: '#8b5cf6',
  };

  const categoryEmoji = {
    event: '📅',
    milestone: '🏆',
    scenario: '🎯',
  };

  const statusEmoji = {
    planned: '📋',
    in_progress: '⚡',
    completed: '✅',
    cancelled: '❌',
  };

  return (
    <div
      style={{
        background: '#fff',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: `4px solid ${typeColor[node.type]}`,
        cursor: onClick ? 'pointer' : 'default',
        marginBottom: '0.5rem',
      }}
      onClick={onClick}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>
          {categoryEmoji[node.category]}
        </span>
        <strong>{node.title}</strong>
        <span style={{ marginLeft: 'auto', fontSize: '1.2rem' }}>
          {statusEmoji[node.status]}
        </span>
      </div>
      {node.description && <p style={{ color: '#666', marginBottom: '0.5rem' }}>{node.description}</p>}
      <div style={{ fontSize: '0.875rem', color: '#888' }}>
        <div>Час: {new Date(node.timestamp).toLocaleString('uk-UA')}</div>
        <div>Тип: {node.type === 'past' ? 'Минуле' : node.type === 'present' ? 'Теперішнє' : 'Майбутнє'}</div>
      </div>
      {node.tags && node.tags.length > 0 && (
        <div style={{ marginTop: '0.5rem' }}>
          {node.tags.map((tag) => (
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
