/**
 * LegendPage.tsx
 * Page component that fetches and displays a legend by ID
 */
import React, { useState, useEffect } from 'react';
import LegendScene from './LegendScene';
import type { KazkarEntry } from '../types';

interface LegendPageProps {
  legendId: string;
}

/**
 * Fetch a legend by ID from the backend API
 */
async function fetchLegendById(id: string): Promise<KazkarEntry> {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const res = await fetch(`${apiUrl}/api/v1/kazkar/stories/${id}`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch legend: ${res.statusText}`);
  }
  
  return await res.json();
}

/**
 * Play voice for the given text using TTS API
 */
function playVoice(text: string): void {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const audio = new Audio(`${apiUrl}/api/tts?text=${encodeURIComponent(text)}`);
  audio.play().catch((error) => {
    console.error('Failed to play voice:', error);
    // Fallback: inform user that TTS is not available
    alert('Озвучування недоступне в цей момент');
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
        const data = await fetchLegendById(legendId);
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
