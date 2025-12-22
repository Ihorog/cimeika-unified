/**
 * Custom hook for gesture detection (swipe directions)
 * Handles touch events to detect 4-directional swipes
 */
import { useRef, useCallback } from 'react';

// Gesture configuration constants
const GESTURE_CONFIG = {
  SWIPE_THRESHOLD: 50, // Minimum distance in pixels to be considered a swipe
  SWIPE_VELOCITY_THRESHOLD: 0.3, // Minimum velocity (px/ms)
};

export const useGestureHandler = (onSwipe) => {
  const touchStartRef = useRef(null);
  const touchEndRef = useRef(null);

  const handleTouchStart = useCallback((e) => {
    const touch = e.touches[0];
    touchStartRef.current = {
      x: touch.clientX,
      y: touch.clientY,
      time: Date.now(),
    };
    touchEndRef.current = null;
  }, []);

  const handleTouchMove = useCallback((e) => {
    const touch = e.touches[0];
    touchEndRef.current = {
      x: touch.clientX,
      y: touch.clientY,
      time: Date.now(),
    };
  }, []);

  const handleTouchEnd = useCallback(() => {
    if (!touchStartRef.current || !touchEndRef.current) {
      return;
    }

    const start = touchStartRef.current;
    const end = touchEndRef.current;

    const deltaX = end.x - start.x;
    const deltaY = end.y - start.y;
    const deltaTime = end.time - start.time;

    const absX = Math.abs(deltaX);
    const absY = Math.abs(deltaY);

    // Check if movement is significant enough
    if (absX < GESTURE_CONFIG.SWIPE_THRESHOLD && absY < GESTURE_CONFIG.SWIPE_THRESHOLD) {
      return;
    }

    // Calculate velocity
    const velocity = Math.max(absX, absY) / deltaTime;

    // Ensure minimum velocity
    if (velocity < GESTURE_CONFIG.SWIPE_VELOCITY_THRESHOLD) {
      return;
    }

    // Determine direction (prioritize the axis with larger movement)
    let direction = null;

    if (absX > absY) {
      // Horizontal swipe
      direction = deltaX > 0 ? 'right' : 'left';
    } else {
      // Vertical swipe
      direction = deltaY > 0 ? 'down' : 'up';
    }

    if (direction && onSwipe) {
      onSwipe(direction);
    }

    // Reset
    touchStartRef.current = null;
    touchEndRef.current = null;
  }, [onSwipe]);

  return {
    handleTouchStart,
    handleTouchMove,
    handleTouchEnd,
  };
};

export default useGestureHandler;
