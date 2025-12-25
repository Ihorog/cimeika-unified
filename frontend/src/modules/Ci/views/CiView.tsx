/**
 * Ci module main view
 * UI orchestration without business logic
 */
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useCi } from '../hooks/useCi';
import { CANON_BUNDLE_ID } from '../../../app/canon';
import '../../../styles/moduleView.css';

interface HealthStatus {
  status?: string;
  canon_bundle_id?: string;
  message?: string;
}

const CiView: React.FC = () => {
  const { status } = useCi();
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [modulesStatus, setModulesStatus] = useState<any>(null);

  useEffect(() => {
    // Fetch health status
    const fetchHealth = async () => {
      try {
        const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        setHealthStatus(data);
      } catch (error) {
        console.error('Failed to fetch health status:', error);
      }
    };

    // Fetch modules status
    const fetchModules = async () => {
      try {
        const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';
        const response = await fetch(`${API_BASE}/api/v1/modules`);
        const data = await response.json();
        setModulesStatus(data);
      } catch (error) {
        console.error('Failed to fetch modules status:', error);
      }
    };

    fetchHealth();
    fetchModules();
  }, []);

  return (
    <div className="module-view ci-view">
      <div className="module-view-header">
        <h1>Ci — Центральне ядро</h1>
        <p className="subtitle">Оркестрація та координація всієї системи</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        {/* Legend ci Banner */}
        <div style={{ 
          background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
          border: '3px solid #f59e0b',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✨</div>
          <h2 style={{ color: '#92400e', margin: '0 0 0.5rem 0' }}>Легенда ci</h2>
          <p style={{ color: '#78350f', marginBottom: '1.5rem' }}>
            Інтерактивна модель еволюції знань і сенсів. 20 вузлів дослідження дуальності світобудови.
          </p>
          <Link 
            to="/ci/legend"
            style={{
              display: 'inline-block',
              background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
              color: 'white',
              padding: '0.75rem 2rem',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: 'bold',
              boxShadow: '0 4px 12px rgba(245, 158, 11, 0.4)',
              transition: 'all 0.2s ease'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 16px rgba(245, 158, 11, 0.5)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(245, 158, 11, 0.4)';
            }}
          >
            ⚡ Відкрити Легенду
          </Link>
        </div>

        {/* Chat Link */}
        <div style={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          border: '3px solid #5a67d8',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💬</div>
          <h2 style={{ color: 'white', margin: '0 0 0.5rem 0' }}>Чат з Ci</h2>
          <p style={{ color: 'rgba(255,255,255,0.9)', marginBottom: '1.5rem' }}>
            Інтелектуальний асистент з підтримкою GPT і голосового введення
          </p>
          <Link 
            to="/chat"
            style={{
              display: 'inline-block',
              background: 'white',
              color: '#5a67d8',
              padding: '0.75rem 2rem',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: 'bold',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
              transition: 'all 0.2s ease'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 16px rgba(0, 0, 0, 0.25)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
            }}
          >
            🗨️ Відкрити Чат
          </Link>
        </div>

        <h2>Про модуль</h2>
        <p>
          <strong>Ci</strong> (Сімейка) — це центральний модуль, який координує роботу всіх інших модулів системи.
          Він забезпечує комунікацію між модулями та управляє глобальним станом додатку.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Оркестрація взаємодії між модулями</li>
          <li>Управління глобальним контекстом</li>
          <li>Координація потоків даних</li>
          <li>Централізована обробка подій</li>
          <li>Моніторинг стану системи</li>
        </ul>

        <h2>Статус системи</h2>
        {healthStatus ? (
          <div style={{ background: '#f0f9ff', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
            <p><strong>Статус:</strong> {healthStatus.status === 'healthy' ? '✅ Система працює' : '❌ Помилка'}</p>
            <p><strong>Canon Bundle ID:</strong> <code>{healthStatus.canon_bundle_id || CANON_BUNDLE_ID}</code></p>
            {healthStatus.message && <p><strong>Повідомлення:</strong> {healthStatus.message}</p>}
          </div>
        ) : (
          <p>Завантаження статусу системи...</p>
        )}

        <h2>Модулі системи</h2>
        {modulesStatus ? (
          <div>
            <p style={{ marginBottom: '1rem' }}>
              <strong>Canon Bundle:</strong> <code>{modulesStatus.canon_bundle_id}</code>
            </p>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              {modulesStatus.modules?.map((module: any) => (
                <div key={module.id} style={{ 
                  background: '#f8f9fa', 
                  padding: '0.75rem', 
                  borderRadius: '6px',
                  borderLeft: '3px solid #667eea'
                }}>
                  <strong>{module.name}</strong> — {module.description}
                  <span style={{ marginLeft: '1rem', color: '#666', fontSize: '0.9rem' }}>
                    ({module.status})
                  </span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p>Завантаження інформації про модулі...</p>
        )}

        <p style={{ marginTop: '2rem' }}><strong>Поточний статус модуля:</strong> {status}</p>
      </div>
    </div>
  );
};

export default CiView;
