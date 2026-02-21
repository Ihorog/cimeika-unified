/**
 * Podija Module API Service
 * Handles all API calls for Podija (Events) module
 */

import { apiClient } from '../api';

export interface PodijaEvent {
  id: number;
  title: string;
  description: string;
  event_date?: string;
  event_type?: string;
  is_completed?: boolean;
  status?: string;
  tags?: string[];
  time?: string;
  module?: string;
  source_trace?: string;
  canon_bundle_id?: string;
}

export interface PodijaEventCreate {
  title: string;
  description: string;
  event_date?: string;
  event_type?: string;
  is_completed?: boolean;
  tags?: string[];
}

export interface PodijaEventUpdate {
  title?: string;
  description?: string;
  event_date?: string;
  event_type?: string;
  is_completed?: boolean;
  tags?: string[];
}

const podijaService = {
  /**
   * Get Podija module status
   */
  async getStatus() {
    const response = await apiClient.get('/api/v1/podija/');
    return response.data;
  },

  /**
   * Create a new event
   */
  async createEvent(event: PodijaEventCreate): Promise<PodijaEvent> {
    const response = await apiClient.post('/api/v1/podija/events', event);
    return response.data;
  },

  /**
   * Get all events with pagination
   */
  async getEvents(params?: {
    skip?: number;
    limit?: number;
    event_type?: string;
    is_completed?: boolean;
  }): Promise<PodijaEvent[]> {
    const response = await apiClient.get('/api/v1/podija/events', { params });
    return response.data;
  },

  /**
   * Get event by ID
   */
  async getEvent(id: number): Promise<PodijaEvent> {
    const response = await apiClient.get(`/api/v1/podija/events/${id}`);
    return response.data;
  },

  /**
   * Update event
   */
  async updateEvent(id: number, updates: PodijaEventUpdate): Promise<PodijaEvent> {
    const response = await apiClient.put(`/api/v1/podija/events/${id}`, updates);
    return response.data;
  },

  /**
   * Delete event
   */
  async deleteEvent(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/podija/events/${id}`);
  },

  /**
   * Mark event as completed
   */
  async completeEvent(id: number): Promise<PodijaEvent> {
    return this.updateEvent(id, { is_completed: true });
  },

  /**
   * Get upcoming events
   */
  async getUpcomingEvents(limit: number = 10): Promise<PodijaEvent[]> {
    return this.getEvents({ is_completed: false, limit });
  },

  /**
   * Get events scheduled for today
   */
  async getEventsToday(): Promise<PodijaEvent[]> {
    const response = await apiClient.get('/api/v1/podija/events/today');
    return response.data;
  },

  /**
   * Get events scheduled for the current week
   */
  async getEventsWeek(): Promise<PodijaEvent[]> {
    const response = await apiClient.get('/api/v1/podija/events/week');
    return response.data;
  },

  /**
   * Mark event as done
   */
  async markDone(id: number): Promise<PodijaEvent> {
    const response = await apiClient.post(`/api/v1/podija/events/${id}/done`);
    return response.data;
  },

  /**
   * Cancel an event
   */
  async markCancel(id: number): Promise<PodijaEvent> {
    const response = await apiClient.post(`/api/v1/podija/events/${id}/cancel`);
    return response.data;
  },
};

export default podijaService;
