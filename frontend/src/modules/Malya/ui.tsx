/**
 * Malya module UI components
 * Reusable UI components specific to Malya (Ideas/Creativity) module
 */

import React from 'react';
import type { MalyaIdea } from './types';

interface IdeaCardProps {
  idea: MalyaIdea;
  onClick?: () => void;
}

export const IdeaCard: React.FC<IdeaCardProps> = ({ idea, onClick }) => {
  const categoryEmoji = {
    innovation: '💡',
    creative: '🎨',
    improvement: '🔧',
    experiment: '🧪',
  };

  const priorityColor = {
    low: '#94a3b8',
    medium: '#fbbf24',
    high: '#ef4444',
  };

  const statusColor = {
    draft: '#9ca3af',
    active: '#3b82f6',
    completed: '#10b981',
    archived: '#64748b',
  };

  return (
    <div
      style={{
        background: '#fff',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: `4px solid ${priorityColor[idea.priority]}`,
        cursor: onClick ? 'pointer' : 'default',
        marginBottom: '0.5rem',
      }}
      onClick={onClick}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>
          {categoryEmoji[idea.category]}
        </span>
        <strong>{idea.title}</strong>
        <span
          style={{
            marginLeft: 'auto',
            padding: '0.25rem 0.5rem',
            borderRadius: '4px',
            background: statusColor[idea.status],
            color: '#fff',
            fontSize: '0.75rem',
          }}
        >
          {idea.status}
        </span>
      </div>
      <p style={{ color: '#666', marginBottom: '0.5rem' }}>{idea.description}</p>
      <div style={{ fontSize: '0.875rem', color: '#888' }}>
        <div>Пріоритет: {idea.priority}</div>
        <div>Категорія: {idea.category}</div>
      </div>
      {idea.tags && idea.tags.length > 0 && (
        <div style={{ marginTop: '0.5rem' }}>
          {idea.tags.map((tag) => (
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
