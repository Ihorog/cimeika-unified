/**
 * Nastrij module API client
 * API functions for Nastrij (Mood/Emotions) module
 */

import type { NastrijState, MoodEntry, CreateMoodEntryRequest, MoodAnalytics } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const nastrijApi = {
  /**
   * Get current mood state
   */
  async getState(): Promise<NastrijState> {
    const response = await fetch(`${API_BASE}/api/nastrij/state`);
    if (!response.ok) {
      throw new Error('Failed to fetch Nastrij state');
    }
    return response.json();
  },

  /**
   * Get mood history
   */
  async getMoodHistory(): Promise<MoodEntry[]> {
    const response = await fetch(`${API_BASE}/api/nastrij/mood-history`);
    if (!response.ok) {
      throw new Error('Failed to fetch mood history');
    }
    const data = await response.json();
    return data.history || [];
  },

  /**
   * Create a new mood entry
   */
  async createMoodEntry(entry: CreateMoodEntryRequest): Promise<MoodEntry> {
    const response = await fetch(`${API_BASE}/api/nastrij/mood`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(entry),
    });
    if (!response.ok) {
      throw new Error('Failed to create mood entry');
    }
    return response.json();
  },

  /**
   * Get mood analytics
   */
  async getAnalytics(): Promise<MoodAnalytics> {
    const response = await fetch(`${API_BASE}/api/nastrij/analytics`);
    if (!response.ok) {
      throw new Error('Failed to fetch mood analytics');
    }
    return response.json();
  },
};
