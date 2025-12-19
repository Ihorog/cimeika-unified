/**
 * Home Page - Main landing page displaying all modules
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const [modules, setModules] = useState([]);
  const [status, setStatus] = useState('loading');

  useEffect(() => {
    // Fetch modules from backend
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
    fetch(`${apiUrl}/api/v1/modules`)
      .then(res => res.json())
      .then(data => {
        setModules(data.modules);
        setStatus('success');
      })
      .catch(err => {
        console.error('Failed to fetch modules:', err);
        setStatus('error');
        // Fallback to static data if backend is not available
        setModules([
          { id: 'ci', name: 'Ci', description: 'Центральне ядро, оркестрація' },
          { id: 'kazkar', name: 'Казкар', description: 'Пам\'ять, історії, легенди' },
          { id: 'podiya', name: 'ПоДія', description: 'Події, майбутнє, сценарії' },
          { id: 'nastriy', name: 'Настрій', description: 'Емоційні стани, контекст' },
          { id: 'malya', name: 'Маля', description: 'Ідеї, творчість, інновації' },
          { id: 'galereya', name: 'Галерея', description: 'Візуальний архів, медіа' },
          { id: 'kalendar', name: 'Календар', description: 'Час, ритми, планування' },
        ]);
      });
  }, []);

  const getModulePath = (moduleId) => {
    const pathMap = {
      'ci': '/ci',
      'kazkar': '/kazkar',
      'podiya': '/podija',
      'nastriy': '/nastrij',
      'malya': '/malya',
      'galereya': '/gallery',
      'kalendar': '/calendar',
    };
    return pathMap[moduleId] || `/${moduleId}`;
  };

  return (
    <div className="home-page">
      <section className="hero-section">
        <h1>Вітаємо в CIMEIKA</h1>
        <p className="hero-subtitle">
          Інтегрована платформа для управління життям через 7 взаємопов'язаних модулів
        </p>
        <p className="hero-description">
          Система, що допомагає людям організовувати пам'ять, емоції, події, ідеї, час та простір в єдиному просторі
        </p>
      </section>

      <section className="modules-section">
        <h2>Модулі системи</h2>
        
        {status === 'loading' && (
          <div className="loading">
            <p>Завантаження модулів...</p>
          </div>
        )}

        {status === 'success' && (
          <div className="modules-grid">
            {modules.map(module => (
              <Link 
                key={module.id} 
                to={getModulePath(module.id)} 
                className="module-card"
              >
                <div className="module-header">
                  <h3>{module.name}</h3>
                  <span className="module-icon">→</span>
                </div>
                <p className="module-description">{module.description}</p>
                <span className="module-status">🟡 В розробці</span>
              </Link>
            ))}
          </div>
        )}
      </section>

      <section className="info-section">
        <div className="info-card">
          <h3>🎯 Про проєкт</h3>
          <p>
            <strong>Cimeika</strong> (українською: Сімейка/Сім'я) — це екосистема, 
            що допомагає організовувати різні аспекти життя в одному місці.
          </p>
        </div>
        <div className="info-card">
          <h3>🏗️ Архітектура</h3>
          <p>
            Побудовано на React 18, TypeScript, Zustand для стану, 
            з FastAPI backend та PostgreSQL базою даних.
          </p>
        </div>
        <div className="info-card">
          <h3>🌍 Мультимовність</h3>
          <p>
            Основна мова — українська. Підтримка автоматичної 
            мультимовності для розширення аудиторії.
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
