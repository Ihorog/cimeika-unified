/**
 * Malya module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useMalya } from '../hooks/useMalya';
import '../../../styles/moduleView.css';

const MalyaView: React.FC = () => {
  const { status } = useMalya();

  return (
    <div className="module-view malya-view">
      <div className="module-view-header">
        <h1>Маля — Ідеї</h1>
        <p className="subtitle">Творчість та інновації</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        <h2>Про модуль</h2>
        <p>
          <strong>Маля</strong> — це модуль для збереження та розвитку ідей.
          Творчий простір для фіксації думок, розробки концепцій та інноваційних рішень.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Збереження та організація ідей</li>
          <li>Мозковий штурм та майнд-карти</li>
          <li>Розвиток концепцій</li>
          <li>Зв'язки між ідеями</li>
          <li>Креативні техніки</li>
          <li>Колаборативна робота над ідеями</li>
        </ul>

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default MalyaView;
