/**
 * Voice integration hook for Android WebView
 * Handles voice text input and TTS output
 */
import { useEffect, useCallback } from 'react';

interface AndroidBridge {
  startVoice: () => void;
  speak: (text: string) => void;
  enableOverlay: () => void;
  disableOverlay: () => void;
}

declare global {
  interface Window {
    Android?: AndroidBridge;
    onVoiceText?: (text: string) => void;
  }
}

interface UseVoiceIntegrationOptions {
  onVoiceText?: (text: string) => void;
  onError?: (error: Error) => void;
}

export const useVoiceIntegration = (options: UseVoiceIntegrationOptions = {}) => {
  const { onVoiceText, onError } = options;

  // Check if running in Android WebView
  const isAndroid = typeof window !== 'undefined' && !!window.Android;

  // Setup voice text handler
  useEffect(() => {
    if (onVoiceText) {
      // Save previous handler if it exists
      const previousHandler = window.onVoiceText;
      window.onVoiceText = onVoiceText;

      return () => {
        // Restore previous handler or delete
        if (previousHandler) {
          window.onVoiceText = previousHandler;
        } else {
          delete window.onVoiceText;
        }
      };
    }
  }, [onVoiceText]);

  // Start voice recognition
  const startVoice = useCallback(() => {
    if (!isAndroid) {
      onError?.(new Error('Voice recognition is only available in Android app'));
      return;
    }

    try {
      window.Android?.startVoice();
    } catch (error) {
      onError?.(error as Error);
    }
  }, [isAndroid, onError]);

  // Speak text using TTS
  const speak = useCallback((text: string) => {
    if (!isAndroid) {
      if (process.env.NODE_ENV === 'development') {
        console.log('TTS not available (not in Android app)');
      }
      return;
    }

    try {
      window.Android?.speak(text);
    } catch (error) {
      onError?.(error as Error);
    }
  }, [isAndroid, onError]);

  // Enable overlay button
  const enableOverlay = useCallback(() => {
    if (!isAndroid) {
      onError?.(new Error('Overlay is only available in Android app'));
      return;
    }

    try {
      window.Android?.enableOverlay();
    } catch (error) {
      onError?.(error as Error);
    }
  }, [isAndroid, onError]);

  // Disable overlay button
  const disableOverlay = useCallback(() => {
    if (!isAndroid) {
      return;
    }

    try {
      window.Android?.disableOverlay();
    } catch (error) {
      onError?.(error as Error);
    }
  }, [isAndroid, onError]);

  return {
    isAndroid,
    startVoice,
    speak,
    enableOverlay,
    disableOverlay,
  };
};

export default useVoiceIntegration;
