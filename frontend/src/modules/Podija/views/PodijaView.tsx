/**
 * Podija module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { usePodija } from '../hooks/usePodija';
import '../../../styles/moduleView.css';

const PodijaView: React.FC = () => {
  const { status } = usePodija();

  return (
    <div className="module-view podija-view">
      <div className="module-view-header">
        <h1>ПоДія — Події</h1>
        <p className="subtitle">Майбутнє, плани та сценарії</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        <h2>Про модуль</h2>
        <p>
          <strong>ПоДія</strong> — це модуль для планування та управління подіями.
          Створюйте, відстежуйте та аналізуйте майбутні події, плануйте сценарії розвитку подій.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Створення та управління подіями</li>
          <li>Планування майбутніх сценаріїв</li>
          <li>Відстеження етапів реалізації</li>
          <li>Інтеграція з календарем</li>
          <li>Нагадування про події</li>
          <li>Аналіз виконання планів</li>
        </ul>

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default PodijaView;
