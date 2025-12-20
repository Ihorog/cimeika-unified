import { useState, useEffect } from 'react';
import { healthService } from '../services/api';

function HealthCheckPage() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkHealth();
    // Auto-refresh every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await healthService.checkAll();
      setHealthData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'success':
        return 'text-green-600';
      case 'unhealthy':
      case 'error':
        return 'text-red-600';
      case 'degraded':
        return 'text-yellow-600';
      default:
        return 'text-gray-600';
    }
  };

  const getStatusBadge = (status) => {
    const baseClasses = 'px-3 py-1 rounded-full text-sm font-semibold';
    switch (status) {
      case 'healthy':
      case 'success':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'unhealthy':
      case 'error':
        return `${baseClasses} bg-red-100 text-red-800`;
      case 'degraded':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  if (loading && !healthData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Перевірка стану системи...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            CIMEIKA Health Check
          </h1>
          <p className="text-gray-600">Перевірка стану розгортання системи</p>
          {healthData && (
            <div className="mt-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-gray-700 font-semibold">Загальний статус:</span>
                <span className={getStatusBadge(healthData.overall)}>
                  {healthData.overall === 'healthy' ? '✅ HEALTHY' : 
                   healthData.overall === 'degraded' ? '⚠️ DEGRADED' : '❌ UNHEALTHY'}
                </span>
              </div>
              <button
                onClick={checkHealth}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Перевірка...' : '🔄 Оновити'}
              </button>
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">❌ Помилка: {error}</p>
          </div>
        )}

        {healthData && (
          <div className="space-y-6">
            {/* Frontend Status */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">🎨</span>
                Frontend Status
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-600 text-sm">Status</p>
                  <p className={`font-semibold ${getStatusColor(healthData.frontend.status)}`}>
                    {healthData.frontend.status}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm">Name</p>
                  <p className="font-semibold text-gray-800">{healthData.frontend.name}</p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm">Version</p>
                  <p className="font-semibold text-gray-800">{healthData.frontend.version}</p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm">Environment</p>
                  <p className="font-semibold text-gray-800">{healthData.frontend.environment}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-gray-600 text-sm">API URL</p>
                  <p className="font-mono text-sm text-blue-600 break-all">
                    {healthData.frontend.apiUrl}
                  </p>
                </div>
              </div>
            </div>

            {/* Backend Status */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">⚙️</span>
                Backend Status
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-600 text-sm">Status</p>
                  <p className={`font-semibold ${getStatusColor(healthData.backend.status)}`}>
                    {healthData.backend.status}
                  </p>
                </div>
                {healthData.backend.data && (
                  <>
                    <div>
                      <p className="text-gray-600 text-sm">Message</p>
                      <p className="font-semibold text-gray-800">
                        {healthData.backend.data.message}
                      </p>
                    </div>
                  </>
                )}
                {healthData.backend.error && (
                  <div className="col-span-2">
                    <p className="text-gray-600 text-sm">Error</p>
                    <p className="font-mono text-sm text-red-600">{healthData.backend.error}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Modules Status */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">📦</span>
                Modules Status
              </h2>
              <div className="mb-4">
                <p className="text-gray-600 text-sm">Status</p>
                <p className={`font-semibold ${getStatusColor(healthData.modules.status)}`}>
                  {healthData.modules.status}
                </p>
              </div>
              {healthData.modules.modules && (
                <div className="space-y-3">
                  <p className="text-gray-600 text-sm font-semibold">
                    Available Modules ({healthData.modules.modules.length})
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {healthData.modules.modules.map((module) => (
                      <div
                        key={module.id}
                        className="border border-gray-200 rounded-md p-3 hover:border-blue-300 transition-colors"
                      >
                        <p className="font-semibold text-gray-800">{module.name}</p>
                        <p className="text-sm text-gray-600">{module.description}</p>
                        <span className="inline-block mt-2 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded">
                          {module.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {healthData.modules.error && (
                <div className="mt-4">
                  <p className="text-gray-600 text-sm">Error</p>
                  <p className="font-mono text-sm text-red-600">{healthData.modules.error}</p>
                </div>
              )}
            </div>

            {/* Timestamp */}
            <div className="text-center text-sm text-gray-500">
              Last updated: {new Date(healthData.timestamp).toLocaleString('uk-UA')}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default HealthCheckPage;
