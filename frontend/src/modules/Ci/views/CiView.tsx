/**
 * Ci module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useCi } from '../hooks/useCi';
import '../../../styles/moduleView.css';

const CiView: React.FC = () => {
  const { status } = useCi();

  return (
    <div className="module-view ci-view">
      <div className="module-view-header">
        <h1>Ci — Центральне ядро</h1>
        <p className="subtitle">Оркестрація та координація всієї системи</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
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

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default CiView;
