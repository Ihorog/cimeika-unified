import React, { useEffect, useRef, useState } from 'react';

const AudioLayer = ({ enabled = true, volume = 0.3 }) => {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [fadeInterval, setFadeInterval] = useState(null);

  useEffect(() => {
    // Note: In a real implementation, you would load an actual audio file
    // For now, this is a placeholder that handles the audio logic
    
    if (enabled && !isPlaying) {
      fadeIn();
    } else if (!enabled && isPlaying) {
      fadeOut();
    }
  }, [enabled]);

  const fadeIn = () => {
    if (audioRef.current && audioRef.current.src) {
      audioRef.current.volume = 0;
      audioRef.current.play().then(() => {
        setIsPlaying(true);
        
        // Gradual fade in
        let currentVolume = 0;
        const targetVolume = volume;
        const step = targetVolume / 30; // 30 steps
        
        const interval = setInterval(() => {
          currentVolume += step;
          if (currentVolume >= targetVolume) {
            currentVolume = targetVolume;
            clearInterval(interval);
          }
          if (audioRef.current) {
            audioRef.current.volume = currentVolume;
          }
        }, 100);
        
        setFadeInterval(interval);
      }).catch(err => {
        console.log('Audio autoplay prevented:', err);
      });
    }
  };

  const fadeOut = () => {
    if (audioRef.current && fadeInterval) {
      clearInterval(fadeInterval);
      
      let currentVolume = audioRef.current.volume;
      const step = currentVolume / 20; // 20 steps
      
      const interval = setInterval(() => {
        currentVolume -= step;
        if (currentVolume <= 0) {
          currentVolume = 0;
          clearInterval(interval);
          if (audioRef.current) {
            audioRef.current.pause();
            setIsPlaying(false);
          }
        }
        if (audioRef.current) {
          audioRef.current.volume = currentVolume;
        }
      }, 100);
    }
  };

  useEffect(() => {
    return () => {
      if (fadeInterval) {
        clearInterval(fadeInterval);
      }
      if (audioRef.current) {
        audioRef.current.pause();
      }
    };
  }, [fadeInterval]);

  return (
    <audio 
      ref={audioRef} 
      loop 
      preload="auto"
    >
      {/* 
        In a real implementation, add source to ambient audio:
        <source src="/assets/3d/ambient_cimeika.mp3" type="audio/mpeg" />
      */}
    </audio>
  );
};

export default AudioLayer;
