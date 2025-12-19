/**
 * Ci module service - API and data layer
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const ciService = {
  async getStatus() {
    const response = await fetch(`${API_BASE}/api/v1/ci`);
    return response.json();
  }
};
