/**
 * Background Theme Context
 * Manages dynamic backgrounds based on module state
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './BackgroundTheme.css';

const BackgroundThemeContext = createContext();

export const useBackgroundTheme = () => {
  const context = useContext(BackgroundThemeContext);
  if (!context) {
    throw new Error('useBackgroundTheme must be used within BackgroundThemeProvider');
  }
  return context;
};

// Theme configuration per module
const THEME_CONFIG = {
  // Past/Memory - Dark, cold, low contrast
  kazkar: {
    type: 'dark',
    gradient: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
    textColor: '#c8c9d8',
    accentColor: '#4a90e2',
  },
  
  // Active/Present - Light, warm, high contrast
  podija: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    textColor: '#ffffff',
    accentColor: '#ffd700',
  },
  
  nastrij: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    textColor: '#ffffff',
    accentColor: '#43e97b',
  },
  
  malya: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    textColor: '#ffffff',
    accentColor: '#ffd700',
  },
  
  ci: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    textColor: '#ffffff',
    accentColor: '#f5f5f5',
  },
  
  chat: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    textColor: '#ffffff',
    accentColor: '#f5f5f5',
  },
  
  calendar: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #feca57 0%, #ff9ff3 100%)',
    textColor: '#ffffff',
    accentColor: '#4a90e2',
  },
  
  gallery: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)',
    textColor: '#ffffff',
    accentColor: '#4a90e2',
  },
  
  // Default/Welcome
  default: {
    type: 'light',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    textColor: '#ffffff',
    accentColor: '#f5f5f5',
  },
};

export const BackgroundThemeProvider = ({ children }) => {
  const location = useLocation();
  const [currentTheme, setCurrentTheme] = useState(THEME_CONFIG.default);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    // Extract module name from path
    const pathParts = location.pathname.split('/').filter(Boolean);
    const moduleName = pathParts[0] || 'default';
    
    const newTheme = THEME_CONFIG[moduleName] || THEME_CONFIG.default;
    
    if (newTheme !== currentTheme) {
      setIsTransitioning(true);
      
      // Apply theme after transition starts
      setTimeout(() => {
        setCurrentTheme(newTheme);
      }, 50);
      
      // End transition
      setTimeout(() => {
        setIsTransitioning(false);
      }, 600);
    }
  }, [location.pathname]);

  return (
    <BackgroundThemeContext.Provider value={{ currentTheme, isTransitioning }}>
      <div 
        className={`app-background ${currentTheme.type} ${isTransitioning ? 'transitioning' : ''}`}
        style={{
          '--theme-gradient': currentTheme.gradient,
          '--theme-text-color': currentTheme.textColor,
          '--theme-accent-color': currentTheme.accentColor,
        }}
      >
        {children}
      </div>
    </BackgroundThemeContext.Provider>
  );
};
