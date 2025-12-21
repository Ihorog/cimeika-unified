/**
 * Ci module UI components
 * Reusable UI components specific to Ci module
 */

import React from 'react';
import type { ModuleInfo, HealthStatus } from './types';

interface ModuleCardProps {
  module: ModuleInfo;
  onClick?: () => void;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({ module, onClick }) => {
  const statusEmoji = {
    in_development: '🟡',
    active: '🟢',
    maintenance: '🔴',
  };

  return (
    <div
      className="module-card"
      style={{
        background: '#f8f9fa',
        padding: '0.75rem',
        borderRadius: '6px',
        borderLeft: '3px solid #667eea',
        cursor: onClick ? 'pointer' : 'default',
      }}
      onClick={onClick}
    >
      <div>
        <strong>{module.name}</strong> — {module.description}
      </div>
      <span style={{ marginLeft: '1rem', color: '#666', fontSize: '0.9rem' }}>
        {statusEmoji[module.status]} {module.status}
      </span>
    </div>
  );
};

interface HealthCardProps {
  health: HealthStatus;
}

export const HealthCard: React.FC<HealthCardProps> = ({ health }) => {
  const isHealthy = health.status === 'healthy' || health.status === 'success';

  return (
    <div
      style={{
        background: '#f0f9ff',
        padding: '1rem',
        borderRadius: '8px',
        marginBottom: '1rem',
      }}
    >
      <p>
        <strong>Статус:</strong>{' '}
        {isHealthy ? '✅ Система працює' : '❌ Помилка'}
      </p>
      {health.canon_bundle_id && (
        <p>
          <strong>Canon Bundle ID:</strong> <code>{health.canon_bundle_id}</code>
        </p>
      )}
      {health.message && (
        <p>
          <strong>Повідомлення:</strong> {health.message}
        </p>
      )}
      {health.version && (
        <p>
          <strong>Версія:</strong> {health.version}
        </p>
      )}
    </div>
  );
};
