/**
 * Kazkar module API client
 * API functions for Kazkar (Memory/Stories) module
 */

import type { KazkarEntry, CreateKazkarEntryRequest } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const kazkarApi = {
  /**
   * Get library overview (stats)
   */
  async getStats(): Promise<{ total_stories: number; by_type: Record<string, number> }> {
    const response = await fetch(`${API_BASE}/api/v1/kazkar/stats`);
    if (!response.ok) {
      throw new Error('Failed to fetch Kazkar stats');
    }
    return response.json();
  },

  /**
   * Get all stories with optional type filter
   */
  async getStories(storyType?: string): Promise<KazkarEntry[]> {
    const url = new URL(`${API_BASE}/api/v1/kazkar/stories`);
    if (storyType) {
      url.searchParams.append('story_type', storyType);
    }
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error('Failed to fetch Kazkar stories');
    }
    return response.json();
  },

  /**
   * Get only legends
   */
  async getLegends(): Promise<KazkarEntry[]> {
    const response = await fetch(`${API_BASE}/api/v1/kazkar/legends`);
    if (!response.ok) {
      throw new Error('Failed to fetch legends');
    }
    return response.json();
  },

  /**
   * Create a new story
   */
  async createStory(story: CreateKazkarEntryRequest): Promise<KazkarEntry> {
    const response = await fetch(`${API_BASE}/api/v1/kazkar/stories`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(story),
    });
    if (!response.ok) {
      throw new Error('Failed to create story');
    }
    return response.json();
  },

  /**
   * Get story by ID
   */
  async getStory(id: number): Promise<KazkarEntry> {
    const response = await fetch(`${API_BASE}/api/v1/kazkar/stories/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch story');
    }
    return response.json();
  },

  /**
   * Update story
   */
  async updateStory(id: number, story: Partial<KazkarEntry>): Promise<KazkarEntry> {
    const response = await fetch(`${API_BASE}/api/v1/kazkar/stories/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(story),
    });
    if (!response.ok) {
      throw new Error('Failed to update story');
    }
    return response.json();
  },

  /**
   * Delete story
   */
  async deleteStory(id: number): Promise<void> {
    const response = await fetch(`${API_BASE}/api/v1/kazkar/stories/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete story');
    }
  },
};
