/**
 * Kazkar module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useKazkar } from '../hooks/useKazkar';

const KazkarView: React.FC = () => {
  const { status } = useKazkar();

  return (
    <div className="kazkar-view">
      <h1>Казкар - Пам'ять</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default KazkarView;
