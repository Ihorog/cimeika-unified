import React, { createContext, useContext, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const ThemeContext = createContext();

// Module → Theme mapping (deterministic)
const THEME_MAP = {
  '/kazkar': 'night',
  '/ci': 'day',
  '/podija': 'day',
  '/nastrij': 'day',
  '/malya': 'day',
  '/calendar': 'day',
  '/gallery': 'day',
};

export const ThemeProvider = ({ children }) => {
  const location = useLocation();
  const [theme, setTheme] = useState('day');

  useEffect(() => {
    // Determine theme from current route
    const currentPath = location.pathname;
    const matchedTheme = THEME_MAP[currentPath] || 'day';
    
    setTheme(matchedTheme);
    
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', matchedTheme);
  }, [location]);

  return (
    <ThemeContext.Provider value={{ theme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
