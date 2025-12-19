/**
 * Malya module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useMalya } from '../hooks/useMalya';

const MalyaView: React.FC = () => {
  const { status } = useMalya();

  return (
    <div className="malya-view">
      <h1>Маля - Ідеї</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default MalyaView;
