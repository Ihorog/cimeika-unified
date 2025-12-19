/**
 * Nastrij module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useNastrij } from '../hooks/useNastrij';

const NastrijView: React.FC = () => {
  const { status } = useNastrij();

  return (
    <div className="nastrij-view">
      <h1>Настрій - Емоції</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default NastrijView;
