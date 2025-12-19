/**
 * Nastrij module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useNastrij } from '../hooks/useNastrij';
import '../../../styles/moduleView.css';

const NastrijView: React.FC = () => {
  const { status } = useNastrij();

  return (
    <div className="module-view nastrij-view">
      <div className="module-view-header">
        <h1>Настрій — Емоції</h1>
        <p className="subtitle">Емоційні стани та контекст</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        <h2>Про модуль</h2>
        <p>
          <strong>Настрій</strong> — це модуль для відстеження та аналізу емоційних станів.
          Допомагає зрозуміти свої емоції, відстежувати настрій та знаходити шляхи до гармонії.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Трекінг емоційних станів</li>
          <li>Журнал настрою</li>
          <li>Аналіз емоційних патернів</li>
          <li>Контекстуальні нотатки</li>
          <li>Візуалізація емоційної динаміки</li>
          <li>Рекомендації для покращення настрою</li>
        </ul>

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default NastrijView;
