/**
 * Podija module service - API and data layer
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const podijaService = {
  async getStatus() {
    const response = await fetch(`${API_BASE}/api/v1/podija`);
    return response.json();
  }
};
