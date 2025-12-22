/**
 * Module Status Dashboard Component
 * Example component demonstrating module orchestrator usage
 */

import React from 'react';
import { useModulesStatus, useModulesMetadata } from '../hooks/useModules';

const ModuleStatusDashboard: React.FC = () => {
  const { statuses, loading, error } = useModulesStatus();
  const metadata = useModulesMetadata();

  if (loading) {
    return (
      <div className="p-4">
        <p>Loading module statuses...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-red-600">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Cimeika Modules Status</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {Object.entries(statuses).map(([name, status]) => {
          const meta = metadata[name];
          const statusColor = 
            status.status === 'active' ? 'bg-green-100 border-green-400' :
            status.status === 'inactive' ? 'bg-yellow-100 border-yellow-400' :
            'bg-red-100 border-red-400';

          return (
            <div 
              key={name}
              className={`border-2 rounded-lg p-4 ${statusColor}`}
            >
              <h3 className="text-lg font-semibold capitalize mb-2">
                {name}
              </h3>
              
              {meta && (
                <p className="text-sm text-gray-600 mb-2">
                  {meta.description}
                </p>
              )}
              
              <div className="text-sm space-y-1">
                <p>
                  <span className="font-medium">Status:</span>{' '}
                  <span className="capitalize">{status.status}</span>
                </p>
                <p>
                  <span className="font-medium">Initialized:</span>{' '}
                  {status.initialized ? 'Yes' : 'No'}
                </p>
                {meta && (
                  <p>
                    <span className="font-medium">Version:</span>{' '}
                    {meta.version}
                  </p>
                )}
              </div>
              
              {status.error && (
                <p className="text-sm text-red-600 mt-2">
                  Error: {status.error}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ModuleStatusDashboard;
