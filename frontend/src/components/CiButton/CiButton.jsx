/**
 * Ci Button - Floating Action Button with Gesture Controls
 * Central interaction element with 4-axis swipe navigation
 */
import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGestureHandler } from './useGestureHandler';
import CimeikaLogo from '../../modules/image/cimeika-logo.svg';
import './CiButton.css';

const CiButton = () => {
  const navigate = useNavigate();
  const [swipeDirection, setSwipeDirection] = useState(null);
  const [isPressed, setIsPressed] = useState(false);

  // Handle swipe gestures
  const handleSwipe = useCallback((direction) => {
    // Show visual feedback
    setSwipeDirection(direction);

    // Navigate based on direction
    const routes = {
      up: '/podija',      // ПоДія - activation/launch/focus
      down: '/nastrij',   // Настрій - state/emotion/moment capture
      left: '/kazkar',    // Казкар - memory/history/experience
      right: '/malya',    // Маля - idea/variant/creation
    };

    if (routes[direction]) {
      navigate(routes[direction]);
    }

    // Clear visual feedback after animation
    setTimeout(() => {
      setSwipeDirection(null);
    }, 300);
  }, [navigate]);

  const { handleTouchStart, handleTouchMove, handleTouchEnd } = useGestureHandler(handleSwipe);

  // Handle click/tap - navigate to chat
  const handleClick = useCallback((e) => {
    // Only trigger if it was a tap (not a swipe)
    if (!swipeDirection) {
      navigate('/chat');
    }
  }, [navigate, swipeDirection]);

  // Handle mouse events for desktop
  const handleMouseDown = () => setIsPressed(true);
  const handleMouseUp = () => setIsPressed(false);
  const handleMouseLeave = () => setIsPressed(false);

  // Clear swipe direction indicator after animation
  useEffect(() => {
    if (swipeDirection) {
      const timer = setTimeout(() => setSwipeDirection(null), 300);
      return () => clearTimeout(timer);
    }
  }, [swipeDirection]);

  return (
    <div className="ci-button-container">
      {/* Swipe direction indicators */}
      {swipeDirection && (
        <div className={`swipe-indicator swipe-${swipeDirection}`}>
          {swipeDirection === 'up' && <span className="swipe-arrow">↑ ПоДія</span>}
          {swipeDirection === 'down' && <span className="swipe-arrow">↓ Настрій</span>}
          {swipeDirection === 'left' && <span className="swipe-arrow">← Казкар</span>}
          {swipeDirection === 'right' && <span className="swipe-arrow">→ Маля</span>}
        </div>
      )}

      <button
        className={`ci-button ${isPressed ? 'pressed' : ''} ${swipeDirection ? 'swiping' : ''}`}
        onClick={handleClick}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseLeave}
        aria-label="Ci - центральна кнопка навігації. Тап для чату, свайп для модулів"
        title="Ci: Тап → Чат | Свайп ↑→↓← для навігації"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            navigate('/chat');
          }
        }}
      >
        <img
          src={CimeikaLogo}
          alt="Cimeika Logo"
          className="ci-button-logo"
          draggable="false"
        />
      </button>

      {/* Hint for gestures (optional, can be shown on first visit) */}
      <div className="ci-button-hint" aria-hidden="true">
        <span className="hint-icon">⚡</span>
      </div>
    </div>
  );
};

export default CiButton;
