/**
 * Ci module API client
 * API functions for Ci module
 */

import type { CiState, CiChatMessage, CiChatResponse, HealthStatus } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const ciApi = {
  /**
   * Get Ci module state
   */
  async getState(): Promise<CiState> {
    const response = await fetch(`${API_BASE}/api/ci/state`);
    if (!response.ok) {
      throw new Error('Failed to fetch Ci state');
    }
    return response.json();
  },

  /**
   * Get health status
   */
  async getHealth(): Promise<HealthStatus> {
    const response = await fetch(`${API_BASE}/health`);
    if (!response.ok) {
      throw new Error('Failed to fetch health status');
    }
    return response.json();
  },

  /**
   * Send chat message to Ci
   */
  async chat(message: CiChatMessage): Promise<CiChatResponse> {
    const response = await fetch(`${API_BASE}/api/ci/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message),
    });
    if (!response.ok) {
      throw new Error('Failed to send chat message');
    }
    return response.json();
  },
};
