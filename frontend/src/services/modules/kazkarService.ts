/**
 * Kazkar Module API Service
 * Handles all API calls for Kazkar (Memory) module
 */

import { apiClient } from '../api';

export interface KazkarStory {
  id: number;
  title: string;
  content: string;
  story_type?: string;
  participants?: string[];
  location?: string;
  tags?: string[];
  time?: string;
  module?: string;
  source_trace?: string;
  canon_bundle_id?: string;
}

export interface KazkarStoryCreate {
  title: string;
  content: string;
  story_type?: string;
  participants?: string[];
  location?: string;
  tags?: string[];
}

export interface KazkarStoryUpdate {
  title?: string;
  content?: string;
  story_type?: string;
  participants?: string[];
  location?: string;
  tags?: string[];
}

export interface KazkarStats {
  total_stories: number;
  by_type: Record<string, number>;
}

const kazkarService = {
  /**
   * Get Kazkar module status
   */
  async getStatus() {
    const response = await apiClient.get('/api/v1/kazkar/');
    return response.data;
  },

  /**
   * Get stories statistics
   */
  async getStats(): Promise<KazkarStats> {
    const response = await apiClient.get('/api/v1/kazkar/stats');
    return response.data;
  },

  /**
   * Create a new story
   */
  async createStory(story: KazkarStoryCreate): Promise<KazkarStory> {
    const response = await apiClient.post('/api/v1/kazkar/stories', story);
    return response.data;
  },

  /**
   * Get all stories with pagination
   */
  async getStories(params?: {
    skip?: number;
    limit?: number;
    story_type?: string;
  }): Promise<KazkarStory[]> {
    const response = await apiClient.get('/api/v1/kazkar/stories', { params });
    return response.data;
  },

  /**
   * Get story by ID
   */
  async getStory(id: number): Promise<KazkarStory> {
    const response = await apiClient.get(`/api/v1/kazkar/stories/${id}`);
    return response.data;
  },

  /**
   * Update story
   */
  async updateStory(id: number, updates: KazkarStoryUpdate): Promise<KazkarStory> {
    const response = await apiClient.put(`/api/v1/kazkar/stories/${id}`, updates);
    return response.data;
  },

  /**
   * Delete story
   */
  async deleteStory(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/kazkar/stories/${id}`);
  },
};

export default kazkarService;
