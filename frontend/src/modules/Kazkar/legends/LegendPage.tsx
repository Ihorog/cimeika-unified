/**
 * LegendPage.tsx
 * Page component that fetches and displays a legend by ID
 */
import React, { useState, useEffect } from 'react';
import LegendScene from './LegendScene';
import { kazkarApi } from '../api';
import type { KazkarEntry } from '../types';

interface LegendPageProps {
  legendId: string | number;
}

/**
 * Play voice for the given text using TTS API
 */
function playVoice(text: string): void {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
  const audio = new Audio(`${apiUrl}/api/tts?text=${encodeURIComponent(text)}`);
  audio.play().catch((error) => {
    console.error('Failed to play voice:', error);
    // Note: In production, this should use a toast notification
    // For now, silently fail to avoid disrupting the user experience
  });
}

const LegendPage: React.FC<LegendPageProps> = ({ legendId }) => {
  const [legend, setLegend] = useState<KazkarEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadLegend = async () => {
      try {
        setLoading(true);
        setError(null);
        // Convert to number if string
        const id = typeof legendId === 'string' ? parseInt(legendId, 10) : legendId;
        const data = await kazkarApi.getStory(id);
        setLegend(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
        console.error('Error fetching legend:', err);
      } finally {
        setLoading(false);
      }
    };

    loadLegend();
  }, [legendId]);

  if (loading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          background: 'linear-gradient(to bottom, #000000, #0f172a, #312e81)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#e0e7ff',
          fontSize: '1.5rem',
          fontWeight: '300',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <div
            style={{
              marginBottom: '1rem',
              fontSize: '3rem',
            }}
          >
            ✦
          </div>
          <div>Завантаження легенди...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        style={{
          minHeight: '100vh',
          background: 'linear-gradient(to bottom, #000000, #0f172a, #312e81)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#fca5a5',
          fontSize: '1.25rem',
          padding: '2rem',
        }}
      >
        <div style={{ textAlign: 'center', maxWidth: '600px' }}>
          <div
            style={{
              marginBottom: '1rem',
              fontSize: '3rem',
            }}
          >
            ⚠️
          </div>
          <div>Помилка завантаження легенди</div>
          <div style={{ fontSize: '1rem', marginTop: '1rem', opacity: 0.8 }}>
            {error}
          </div>
        </div>
      </div>
    );
  }

  if (!legend) {
    return (
      <div
        style={{
          minHeight: '100vh',
          background: 'linear-gradient(to bottom, #000000, #0f172a, #312e81)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#e0e7ff',
          fontSize: '1.25rem',
        }}
      >
        Легенду не знайдено
      </div>
    );
  }

  // Extract sense nodes from tags if available
  const senses = legend.tags
    ? legend.tags.map((tag) => ({
        symbol: '✦',
        label: tag,
      }))
    : [];

  // Create voice playback handler
  const handlePlayVoice = () => {
    const fullText = `${legend.title}. ${legend.content}`;
    playVoice(fullText);
  };

  return (
    <LegendScene
      title={legend.title}
      content={legend.content}
      senses={senses}
      onPlayVoice={handlePlayVoice}
    />
  );
};

export default LegendPage;
