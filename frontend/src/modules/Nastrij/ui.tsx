/**
 * Nastrij module UI components
 * Reusable UI components specific to Nastrij (Mood/Emotions) module
 */

import React from 'react';
import type { MoodEntry } from './types';

interface MoodEntryCardProps {
  entry: MoodEntry;
  onClick?: () => void;
}

export const MoodEntryCard: React.FC<MoodEntryCardProps> = ({ entry, onClick }) => {
  const moodEmoji: Record<string, string> = {
    happy: '😊',
    sad: '😢',
    anxious: '😰',
    calm: '😌',
    angry: '😠',
    excited: '🤩',
    tired: '😴',
    neutral: '😐',
  };

  const getIntensityColor = (intensity: number): string => {
    if (intensity <= 3) return '#10b981';
    if (intensity <= 6) return '#fbbf24';
    return '#ef4444';
  };

  return (
    <div
      style={{
        background: '#fff',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: `4px solid ${getIntensityColor(entry.intensity)}`,
        cursor: onClick ? 'pointer' : 'default',
        marginBottom: '0.5rem',
      }}
      onClick={onClick}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '2rem', marginRight: '0.5rem' }}>
          {moodEmoji[entry.mood.toLowerCase()] || '😐'}
        </span>
        <div>
          <strong style={{ textTransform: 'capitalize' }}>{entry.mood}</strong>
          <div style={{ fontSize: '0.875rem', color: '#888' }}>
            Інтенсивність: {entry.intensity}/10
          </div>
        </div>
      </div>
      {entry.notes && <p style={{ color: '#666', marginBottom: '0.5rem' }}>{entry.notes}</p>}
      <div style={{ fontSize: '0.875rem', color: '#888' }}>
        {new Date(entry.timestamp).toLocaleString('uk-UA')}
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
