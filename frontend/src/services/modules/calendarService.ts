/**
 * Calendar Module API Service
 * Handles all API calls for Calendar module
 */

import { apiClient } from '../api';

export interface CalendarEntry {
  id: number;
  title: string;
  description: string;
  scheduled_at?: string;
  is_recurring?: boolean;
  recurrence_pattern?: string;
  tags?: string[];
  time?: string;
  module?: string;
  source_trace?: string;
  canon_bundle_id?: string;
}

export interface CalendarEntryCreate {
  title: string;
  description: string;
  scheduled_at?: string;
  is_recurring?: boolean;
  recurrence_pattern?: string;
  tags?: string[];
}

export interface CalendarEntryUpdate {
  title?: string;
  description?: string;
  scheduled_at?: string;
  is_recurring?: boolean;
  recurrence_pattern?: string;
  tags?: string[];
}

const calendarService = {
  /**
   * Get Calendar module status
   */
  async getStatus() {
    const response = await apiClient.get('/api/v1/calendar/');
    return response.data;
  },

  /**
   * Create a new calendar entry
   */
  async createEntry(entry: CalendarEntryCreate): Promise<CalendarEntry> {
    const response = await apiClient.post('/api/v1/calendar/entries', entry);
    return response.data;
  },

  /**
   * Get all entries with pagination
   */
  async getEntries(params?: {
    skip?: number;
    limit?: number;
    is_recurring?: boolean;
  }): Promise<CalendarEntry[]> {
    const response = await apiClient.get('/api/v1/calendar/entries', { params });
    return response.data;
  },

  /**
   * Get entry by ID
   */
  async getEntry(id: number): Promise<CalendarEntry> {
    const response = await apiClient.get(`/api/v1/calendar/entries/${id}`);
    return response.data;
  },

  /**
   * Update entry
   */
  async updateEntry(id: number, updates: CalendarEntryUpdate): Promise<CalendarEntry> {
    const response = await apiClient.put(`/api/v1/calendar/entries/${id}`, updates);
    return response.data;
  },

  /**
   * Delete entry
   */
  async deleteEntry(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/calendar/entries/${id}`);
  },

  /**
   * Get today's entries
   */
  async getTodayEntries(): Promise<CalendarEntry[]> {
    const today = new Date().toISOString().split('T')[0];
    return this.getEntries({ limit: 100 });
  },

  /**
   * Get recurring entries
   */
  async getRecurringEntries(): Promise<CalendarEntry[]> {
    return this.getEntries({ is_recurring: true });
  },
};

export default calendarService;
