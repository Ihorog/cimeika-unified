/**
 * Welcome Page - Вітальна сторінка Cimeika
 * Beautiful landing page with gradient background
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import CimeikaLogo from '../modules/image/cimeika-logo.svg';
import './WelcomePage.css';

export default function WelcomePage() {
  const navigate = useNavigate();

  const modules = [
    { 
      id: 'ci', 
      name: 'Ci', 
      icon: '⚙️', 
      description: 'Центральне ядро системи',
      color: '#667eea',
      path: '/ci'
    },
    { 
      id: 'podija', 
      name: 'ПоДія', 
      icon: '🎯', 
      description: 'Події та активації',
      color: '#f093fb',
      path: '/podija'
    },
    { 
      id: 'nastrij', 
      name: 'Настрій', 
      icon: '😊', 
      description: 'Емоційні стани',
      color: '#4facfe',
      path: '/nastrij'
    },
    { 
      id: 'malya', 
      name: 'Маля', 
      icon: '💡', 
      description: 'Ідеї та творчість',
      color: '#43e97b',
      path: '/malya'
    },
    { 
      id: 'kazkar', 
      name: 'Казкар', 
      icon: '📖', 
      description: 'Пам\'ять та історії',
      color: '#fa709a',
      path: '/kazkar'
    },
    { 
      id: 'calendar', 
      name: 'Календар', 
      icon: '📅', 
      description: 'Час та планування',
      color: '#feca57',
      path: '/calendar'
    },
    { 
      id: 'gallery', 
      name: 'Галерея', 
      icon: '🖼️', 
      description: 'Медіа-контент',
      color: '#ff6b6b',
      path: '/gallery'
    },
  ];

  return (
    <div className="welcome-page">
      {/* Animated background */}
      <div className="welcome-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      {/* Content */}
      <div className="welcome-content">
        {/* Hero Section */}
        <div className="welcome-hero">
          <div className="welcome-logo-container">
            <img src={CimeikaLogo} alt="Cimeika" className="welcome-logo" />
          </div>
          <h1 className="welcome-title">
            Вітаємо в <span className="gradient-text">Cimeika</span>
          </h1>
          <p className="welcome-subtitle">
            Інтелектуальна система для організації життя
          </p>
          <button 
            className="welcome-cta"
            onClick={() => navigate('/chat')}
          >
            <span>Розпочати з чату</span>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>

        {/* Modules Grid */}
        <div className="welcome-modules">
          <h2 className="modules-title">Модулі системи</h2>
          <div className="modules-grid">
            {modules.map((module) => (
              <div
                key={module.id}
                className="module-card"
                onClick={() => navigate(module.path)}
                style={{ '--module-color': module.color }}
              >
                <div className="module-icon">{module.icon}</div>
                <h3 className="module-name">{module.name}</h3>
                <p className="module-description">{module.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="welcome-features">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI-асистент</h3>
            <p>Розумний чат з GPT для швидкої допомоги</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Жестове керування</h3>
            <p>Швидка навігація свайпами</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>7 модулів</h3>
            <p>Повний контроль над життям</p>
          </div>
        </div>

        {/* Footer */}
        <footer className="welcome-footer">
          <p>Створено з ❤️ для організації життя</p>
          <div className="footer-links">
            <button onClick={() => navigate('/home')}>Старий інтерфейс</button>
            <button onClick={() => navigate('/health')}>Статус системи</button>
          </div>
        </footer>
      </div>
    </div>
  );
}
