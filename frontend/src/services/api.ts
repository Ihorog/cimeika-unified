/**
 * API Configuration and Base Service
 */

import axios from 'axios';

// API Base URL from environment variable
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'CIMEIKA';

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Health Check Service
 */
export const healthService = {
  /**
   * Check backend health
   */
  async checkBackend() {
    try {
      const response = await apiClient.get('/health');
      return {
        status: 'healthy',
        data: response.data,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.response?.data?.message || error.message || 'Backend connection failed',
        timestamp: new Date().toISOString(),
      };
    }
  },

  /**
   * Get modules list
   */
  async getModules() {
    try {
      const response = await apiClient.get('/api/v1/modules');
      return {
        status: 'success',
        modules: response.data.modules,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.response?.data?.message || error.message || 'Failed to fetch modules',
        timestamp: new Date().toISOString(),
      };
    }
  },

  /**
   * Check frontend health
   */
  async checkFrontend() {
    return {
      status: 'healthy',
      name: APP_NAME,
      version: '0.1.0',
      apiUrl: API_BASE_URL,
      timestamp: new Date().toISOString(),
      environment: import.meta.env.MODE,
    };
  },

  /**
   * Comprehensive health check
   */
  async checkAll() {
    const [frontend, backend, modules] = await Promise.all([
      this.checkFrontend(),
      this.checkBackend(),
      this.getModules(),
    ]);

    const allHealthy = 
      frontend.status === 'healthy' &&
      backend.status === 'healthy' &&
      modules.status === 'success';

    return {
      overall: allHealthy ? 'healthy' : 'degraded',
      frontend,
      backend,
      modules,
      timestamp: new Date().toISOString(),
    };
  },
};

export default apiClient;
