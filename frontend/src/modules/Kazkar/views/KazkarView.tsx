/**
 * Kazkar module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useKazkar } from '../hooks/useKazkar';
import '../../../styles/moduleView.css';

const KazkarView: React.FC = () => {
  const { status } = useKazkar();

  return (
    <div className="module-view kazkar-view">
      <div className="module-view-header">
        <h1>Казкар — Пам'ять</h1>
        <p className="subtitle">Історії, спогади та легенди</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        <h2>Про модуль</h2>
        <p>
          <strong>Казкар</strong> — це модуль для збереження та організації спогадів, історій та легенд.
          Тут можна зберігати важливі моменти життя, сімейні історії та створювати власні оповіді.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Збереження спогадів та історій</li>
          <li>Організація сімейних легенд</li>
          <li>Створення хронології подій</li>
          <li>Прив'язка медіа до спогадів</li>
          <li>Теги та категоризація</li>
          <li>Пошук по архіву спогадів</li>
        </ul>

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default KazkarView;
