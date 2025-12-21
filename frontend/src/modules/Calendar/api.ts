/**
 * Calendar module API client
 * API functions for Calendar module
 */

import type { CalendarEvent, CreateEventRequest } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const calendarApi = {
  /**
   * Get all calendar events
   */
  async getEvents(): Promise<CalendarEvent[]> {
    const response = await fetch(`${API_BASE}/api/calendar/events`);
    if (!response.ok) {
      throw new Error('Failed to fetch calendar events');
    }
    const data = await response.json();
    return data.events || [];
  },

  /**
   * Create a new calendar event
   */
  async createEvent(event: CreateEventRequest): Promise<CalendarEvent> {
    const response = await fetch(`${API_BASE}/api/calendar/events`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event),
    });
    if (!response.ok) {
      throw new Error('Failed to create calendar event');
    }
    return response.json();
  },

  /**
   * Get event by ID
   */
  async getEvent(id: string): Promise<CalendarEvent> {
    const response = await fetch(`${API_BASE}/api/calendar/events/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch calendar event');
    }
    return response.json();
  },

  /**
   * Update calendar event
   */
  async updateEvent(id: string, event: Partial<CalendarEvent>): Promise<CalendarEvent> {
    const response = await fetch(`${API_BASE}/api/calendar/events/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event),
    });
    if (!response.ok) {
      throw new Error('Failed to update calendar event');
    }
    return response.json();
  },

  /**
   * Delete calendar event
   */
  async deleteEvent(id: string): Promise<void> {
    const response = await fetch(`${API_BASE}/api/calendar/events/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete calendar event');
    }
  },
};
