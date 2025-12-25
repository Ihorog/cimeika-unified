/**
 * LegendScene.tsx
 * Immersive legend display with animations and sense nodes
 */
import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import LegendRitualMode from './LegendRitualMode';
import useKazkarRealtime from '../hooks/useKazkarRealtime';

export interface LegendSceneProps {
  title: string;
  content: string;
  senses: { symbol: string; label: string }[];
  onPlayVoice?: () => void;
}

const LegendScene: React.FC<LegendSceneProps> = ({
  title,
  content,
  senses,
  onPlayVoice,
}) => {
  const [isRitualMode, setIsRitualMode] = useState(false);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const [volume, setVolume] = useState(0.5); // 50% default volume
  const [showVolumeControl, setShowVolumeControl] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // WebSocket connection for real-time updates
  const { lastEvent, status: wsStatus, isConnected } = useKazkarRealtime({
    debug: false,
  });

  // Initialize ambient audio
  useEffect(() => {
    const audio = new Audio('/audio/kazkar_ambient.mp3');
    audio.loop = true;
    audio.volume = volume;
    audioRef.current = audio;

    // Handle loading errors gracefully
    audio.addEventListener('error', () => {
      console.log('[LegendScene] Ambient audio not available, continuing without audio');
    });

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  // Update volume when changed
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  // Handle real-time events
  useEffect(() => {
    if (lastEvent) {
      console.log('[LegendScene] Received WebSocket event:', lastEvent);
      // Handle legend_sense_activated or other events
      if (lastEvent.event === 'legend_sense_activated') {
        // Could trigger visual effects or animations here
      }
    }
  }, [lastEvent]);

  // Toggle ambient audio playback
  const toggleAudio = () => {
    if (audioRef.current) {
      if (isAudioPlaying) {
        audioRef.current.pause();
        setIsAudioPlaying(false);
      } else {
        audioRef.current.play().catch(error => {
          console.log('[LegendScene] Audio play prevented:', error);
        });
        setIsAudioPlaying(true);
      }
    }
  };

  if (isRitualMode) {
    return <LegendRitualMode onReturn={() => setIsRitualMode(false)} />;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(to bottom, #000000, #0f172a, #312e81)',
        color: '#e0e7ff',
        padding: '2rem',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      {/* Main content container */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        style={{
          maxWidth: '900px',
          width: '100%',
          background: 'rgba(30, 27, 75, 0.6)',
          backdropFilter: 'blur(12px)',
          borderRadius: '32px',
          padding: '3rem',
          boxShadow: '0 20px 60px rgba(99, 102, 241, 0.4), 0 0 100px rgba(139, 92, 246, 0.2)',
          border: '1px solid rgba(139, 92, 246, 0.3)',
        }}
      >
        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
          style={{
            fontSize: '3rem',
            fontWeight: 'bold',
            marginBottom: '2rem',
            background: 'linear-gradient(135deg, #818cf8, #c4b5fd)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            lineHeight: '1.2',
          }}
        >
          {title}
        </motion.h1>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7, duration: 0.8 }}
          style={{
            fontSize: '1.25rem',
            lineHeight: '1.8',
            marginBottom: '3rem',
            color: '#c7d2fe',
            whiteSpace: 'pre-wrap',
          }}
        >
          {content}
        </motion.div>

        {/* Sense nodes */}
        {senses && senses.length > 0 && (
          <div style={{ marginBottom: '2rem' }}>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.5 }}
              style={{
                fontSize: '0.875rem',
                color: '#a5b4fc',
                marginBottom: '1rem',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              Відчуття
            </motion.div>
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '1rem',
              }}
            >
              {senses.map((sense, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{
                    delay: 1.1 + index * 0.1,
                    duration: 0.4,
                    type: 'spring',
                    stiffness: 200,
                  }}
                  style={{
                    background: 'rgba(99, 102, 241, 0.2)',
                    border: '1px solid rgba(139, 92, 246, 0.5)',
                    borderRadius: '20px',
                    padding: '0.75rem 1.5rem',
                    fontSize: '1rem',
                    color: '#e0e7ff',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)',
                    cursor: 'default',
                  }}
                >
                  <span style={{ fontSize: '1.5rem' }}>{sense.symbol}</span>
                  <span>{sense.label}</span>
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* Controls */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 0.5 }}
          style={{
            display: 'flex',
            gap: '1rem',
            flexWrap: 'wrap',
            marginTop: '2rem',
          }}
        >
          {onPlayVoice && (
            <button
              onClick={onPlayVoice}
              style={{
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                border: 'none',
                borderRadius: '12px',
                padding: '1rem 2rem',
                fontSize: '1rem',
                fontWeight: '600',
                color: '#ffffff',
                cursor: 'pointer',
                boxShadow: '0 8px 20px rgba(99, 102, 241, 0.4)',
                transition: 'transform 0.2s, box-shadow 0.2s',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow =
                  '0 12px 28px rgba(99, 102, 241, 0.5)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow =
                  '0 8px 20px rgba(99, 102, 241, 0.4)';
              }}
              aria-label="Озвучити легенду"
            >
              <span aria-hidden="true">▶️</span>
              <span>Озвучити</span>
            </button>
          )}

          <button
            onClick={() => setIsRitualMode(true)}
            style={{
              background: 'rgba(79, 70, 229, 0.2)',
              border: '1px solid rgba(139, 92, 246, 0.5)',
              borderRadius: '12px',
              padding: '1rem 2rem',
              fontSize: '1rem',
              fontWeight: '600',
              color: '#c7d2fe',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)',
              transition: 'transform 0.2s, background 0.2s',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.background = 'rgba(79, 70, 229, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.background = 'rgba(79, 70, 229, 0.2)';
            }}
            aria-label="Увійти в режим ритуалу"
          >
            <span aria-hidden="true">🌗</span>
            <span>Режим Ритуалу</span>
          </button>
        </motion.div>
      </motion.div>

      {/* Audio controls (fixed position) */}
      <div
        style={{
          position: 'fixed',
          bottom: '2rem',
          right: '2rem',
          zIndex: 1000,
        }}
      >
        {/* WebSocket status indicator */}
        {isConnected && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            style={{
              position: 'absolute',
              top: '-10px',
              right: '-10px',
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              background: '#10b981',
              boxShadow: '0 0 10px rgba(16, 185, 129, 0.5)',
            }}
            title="Connected to real-time updates"
          />
        )}

        {/* Main audio button */}
        <button
          onClick={toggleAudio}
          onMouseEnter={() => setShowVolumeControl(true)}
          style={{
            background: 'rgba(30, 27, 75, 0.9)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(139, 92, 246, 0.3)',
            borderRadius: '50%',
            width: '56px',
            height: '56px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(99, 102, 241, 0.4)',
            transition: 'transform 0.2s, box-shadow 0.2s',
            fontSize: '1.5rem',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.1)';
            e.currentTarget.style.boxShadow = '0 6px 16px rgba(99, 102, 241, 0.6)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(99, 102, 241, 0.4)';
            setShowVolumeControl(false);
          }}
          aria-label={isAudioPlaying ? 'Pause ambient audio' : 'Play ambient audio'}
        >
          <span aria-hidden="true">{isAudioPlaying ? '🔊' : '🔇'}</span>
        </button>

        {/* Volume slider */}
        {showVolumeControl && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            style={{
              position: 'absolute',
              bottom: '0',
              right: '70px',
              background: 'rgba(30, 27, 75, 0.95)',
              backdropFilter: 'blur(12px)',
              border: '1px solid rgba(139, 92, 246, 0.3)',
              borderRadius: '28px',
              padding: '0.75rem 1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              boxShadow: '0 4px 12px rgba(99, 102, 241, 0.4)',
            }}
            onMouseEnter={() => setShowVolumeControl(true)}
            onMouseLeave={() => setShowVolumeControl(false)}
          >
            <span style={{ fontSize: '0.875rem', color: '#a5b4fc' }}>Гучність</span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={volume}
              onChange={(e) => setVolume(parseFloat(e.target.value))}
              style={{
                width: '120px',
                height: '4px',
                borderRadius: '2px',
                background: `linear-gradient(to right, #6366f1 0%, #6366f1 ${volume * 100}%, rgba(139, 92, 246, 0.3) ${volume * 100}%, rgba(139, 92, 246, 0.3) 100%)`,
                outline: 'none',
                cursor: 'pointer',
              }}
              aria-label="Volume control"
            />
            <span style={{ fontSize: '0.875rem', color: '#e0e7ff', minWidth: '35px' }}>
              {Math.round(volume * 100)}%
            </span>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default LegendScene;
