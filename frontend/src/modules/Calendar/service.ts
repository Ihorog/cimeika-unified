/**
 * Calendar module service - API and data layer
 * Implements ServiceInterface
 */

import type { ServiceInterface, ApiResponse } from '../../../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const calendarService: ServiceInterface = {
  async getStatus(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/v1/calendar`);
      const data = await response.json();
      return {
        status: 'success',
        data
      };
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  },
  
  async process(data: any): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/v1/calendar/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      return {
        status: 'success',
        data: result
      };
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  },
  
  validate(data: any): boolean {
    return typeof data === 'object' && data !== null;
  }
};
