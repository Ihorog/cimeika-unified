/**
 * Podija module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { usePodija } from '../hooks/usePodija';

const PodijaView: React.FC = () => {
  const { status } = usePodija();

  return (
    <div className="podija-view">
      <h1>Подія - Події</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default PodijaView;
