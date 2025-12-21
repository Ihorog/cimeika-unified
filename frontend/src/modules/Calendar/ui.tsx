/**
 * Calendar module UI components
 * Reusable UI components specific to Calendar module
 */

import React from 'react';
import type { CalendarEvent } from './types';

interface EventCardProps {
  event: CalendarEvent;
  onClick?: () => void;
}

export const EventCard: React.FC<EventCardProps> = ({ event, onClick }) => {
  const typeEmoji = {
    event: '📅',
    task: '✓',
    reminder: '🔔',
  };

  const statusColor = {
    pending: '#fbbf24',
    completed: '#10b981',
    cancelled: '#ef4444',
  };

  return (
    <div
      style={{
        background: '#fff',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: `4px solid ${statusColor[event.status]}`,
        cursor: onClick ? 'pointer' : 'default',
        marginBottom: '0.5rem',
      }}
      onClick={onClick}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>
          {typeEmoji[event.type]}
        </span>
        <strong>{event.title}</strong>
      </div>
      {event.description && <p style={{ color: '#666' }}>{event.description}</p>}
      <div style={{ fontSize: '0.875rem', color: '#888', marginTop: '0.5rem' }}>
        <div>Початок: {new Date(event.start).toLocaleString('uk-UA')}</div>
        <div>Кінець: {new Date(event.end).toLocaleString('uk-UA')}</div>
      </div>
      {event.tags && event.tags.length > 0 && (
        <div style={{ marginTop: '0.5rem' }}>
          {event.tags.map((tag) => (
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
