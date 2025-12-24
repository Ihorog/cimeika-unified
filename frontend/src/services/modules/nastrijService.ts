/**
 * Nastrij Module API Service
 * Handles all API calls for Nastrij (Emotions) module
 */

import { apiClient } from '../api';

export interface NastrijEmotion {
  id: number;
  title: string;
  description: string;
  emotion_state?: string;
  intensity?: number;
  triggers?: string[];
  tags?: string[];
  time?: string;
  module?: string;
  source_trace?: string;
  canon_bundle_id?: string;
}

export interface NastrijEmotionCreate {
  title: string;
  description: string;
  emotion_state?: string;
  intensity?: number;
  triggers?: string[];
  tags?: string[];
}

export interface NastrijEmotionUpdate {
  title?: string;
  description?: string;
  emotion_state?: string;
  intensity?: number;
  triggers?: string[];
  tags?: string[];
}

const nastrijService = {
  /**
   * Get Nastrij module status
   */
  async getStatus() {
    const response = await apiClient.get('/api/v1/nastrij/');
    return response.data;
  },

  /**
   * Create a new emotion entry
   */
  async createEmotion(emotion: NastrijEmotionCreate): Promise<NastrijEmotion> {
    const response = await apiClient.post('/api/v1/nastrij/emotions', emotion);
    return response.data;
  },

  /**
   * Get all emotions with pagination
   */
  async getEmotions(params?: {
    skip?: number;
    limit?: number;
    emotion_state?: string;
  }): Promise<NastrijEmotion[]> {
    const response = await apiClient.get('/api/v1/nastrij/emotions', { params });
    return response.data;
  },

  /**
   * Get emotion by ID
   */
  async getEmotion(id: number): Promise<NastrijEmotion> {
    const response = await apiClient.get(`/api/v1/nastrij/emotions/${id}`);
    return response.data;
  },

  /**
   * Update emotion
   */
  async updateEmotion(id: number, updates: NastrijEmotionUpdate): Promise<NastrijEmotion> {
    const response = await apiClient.put(`/api/v1/nastrij/emotions/${id}`, updates);
    return response.data;
  },

  /**
   * Delete emotion
   */
  async deleteEmotion(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/nastrij/emotions/${id}`);
  },

  /**
   * Get recent emotions (last 10)
   */
  async getRecentEmotions(): Promise<NastrijEmotion[]> {
    return this.getEmotions({ limit: 10 });
  },
};

export default nastrijService;
