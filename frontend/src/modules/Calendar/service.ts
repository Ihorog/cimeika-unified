/**
 * Calendar module service - API and data layer
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const calendarService = {
  async getStatus() {
    const response = await fetch(`${API_BASE}/api/v1/calendar`);
    return response.json();
  }
};
