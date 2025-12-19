/**
 * Ci module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useCi } from '../hooks/useCi';

const CiView: React.FC = () => {
  const { status } = useCi();

  return (
    <div className="ci-view">
      <h1>Ci - Центральне ядро</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default CiView;
