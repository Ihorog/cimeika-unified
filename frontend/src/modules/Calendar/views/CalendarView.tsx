/**
 * Calendar module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useCalendar } from '../hooks/useCalendar';
import '../../../styles/moduleView.css';

const CalendarView: React.FC = () => {
  const { status } = useCalendar();

  return (
    <div className="module-view calendar-view">
      <div className="module-view-header">
        <h1>Календар — Час</h1>
        <p className="subtitle">Управління часом, ритми та планування</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        <h2>Про модуль</h2>
        <p>
          <strong>Календар</strong> — це модуль для управління часом та планування.
          Організуйте свій час, відстежуйте ритми життя та плануйте майбутнє.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Планування подій та завдань</li>
          <li>Відстеження життєвих ритмів</li>
          <li>Інтеграція з модулем ПоДія</li>
          <li>Нагадування та сповіщення</li>
          <li>Різні види календарів</li>
          <li>Аналітика використання часу</li>
        </ul>

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default CalendarView;
