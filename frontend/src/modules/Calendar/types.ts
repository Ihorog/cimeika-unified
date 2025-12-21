/**
 * Calendar module types
 * Shared type definitions for Calendar module
 */

export interface CalendarEvent {
  id: string;
  title: string;
  description?: string;
  start: string; // ISO 8601 datetime
  end: string; // ISO 8601 datetime
  type: 'event' | 'task' | 'reminder';
  status: 'pending' | 'completed' | 'cancelled';
  tags?: string[];
  related_modules?: string[];
}

export interface CalendarState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  events: CalendarEvent[];
  selectedDate?: string;
}

export interface CreateEventRequest {
  title: string;
  description?: string;
  start: string;
  end: string;
  type?: 'event' | 'task' | 'reminder';
  tags?: string[];
}
