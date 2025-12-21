/**
 * Kazkar module API client
 * API functions for Kazkar (Memory/Stories) module
 */

import type { KazkarEntry, CreateKazkarEntryRequest, KazkarLibrary } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const kazkarApi = {
  /**
   * Get library overview
   */
  async getLibrary(): Promise<KazkarLibrary> {
    const response = await fetch(`${API_BASE}/api/kazkar/library`);
    if (!response.ok) {
      throw new Error('Failed to fetch Kazkar library');
    }
    return response.json();
  },

  /**
   * Get all entries
   */
  async getEntries(): Promise<KazkarEntry[]> {
    const response = await fetch(`${API_BASE}/api/kazkar/entries`);
    if (!response.ok) {
      throw new Error('Failed to fetch Kazkar entries');
    }
    const data = await response.json();
    return data.entries || [];
  },

  /**
   * Create a new entry
   */
  async createEntry(entry: CreateKazkarEntryRequest): Promise<KazkarEntry> {
    const response = await fetch(`${API_BASE}/api/kazkar/entries`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(entry),
    });
    if (!response.ok) {
      throw new Error('Failed to create Kazkar entry');
    }
    return response.json();
  },

  /**
   * Get entry by ID
   */
  async getEntry(id: string): Promise<KazkarEntry> {
    const response = await fetch(`${API_BASE}/api/kazkar/entries/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch Kazkar entry');
    }
    return response.json();
  },

  /**
   * Update entry
   */
  async updateEntry(id: string, entry: Partial<KazkarEntry>): Promise<KazkarEntry> {
    const response = await fetch(`${API_BASE}/api/kazkar/entries/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(entry),
    });
    if (!response.ok) {
      throw new Error('Failed to update Kazkar entry');
    }
    return response.json();
  },

  /**
   * Delete entry
   */
  async deleteEntry(id: string): Promise<void> {
    const response = await fetch(`${API_BASE}/api/kazkar/entries/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete Kazkar entry');
    }
  },
};
