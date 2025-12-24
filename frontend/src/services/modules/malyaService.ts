/**
 * Malya Module API Service
 * Handles all API calls for Malya (Ideas) module
 */

import { apiClient } from '../api';

export interface MalyaIdea {
  id: number;
  title: string;
  description: string;
  idea_type?: string;
  status?: string;
  related_ideas?: number[];
  tags?: string[];
  time?: string;
  module?: string;
  source_trace?: string;
  canon_bundle_id?: string;
}

export interface MalyaIdeaCreate {
  title: string;
  description: string;
  idea_type?: string;
  status?: string;
  related_ideas?: number[];
  tags?: string[];
}

export interface MalyaIdeaUpdate {
  title?: string;
  description?: string;
  idea_type?: string;
  status?: string;
  related_ideas?: number[];
  tags?: string[];
}

const malyaService = {
  /**
   * Get Malya module status
   */
  async getStatus() {
    const response = await apiClient.get('/api/v1/malya/');
    return response.data;
  },

  /**
   * Create a new idea
   */
  async createIdea(idea: MalyaIdeaCreate): Promise<MalyaIdea> {
    const response = await apiClient.post('/api/v1/malya/ideas', idea);
    return response.data;
  },

  /**
   * Get all ideas with pagination
   */
  async getIdeas(params?: {
    skip?: number;
    limit?: number;
    idea_type?: string;
    status?: string;
  }): Promise<MalyaIdea[]> {
    const response = await apiClient.get('/api/v1/malya/ideas', { params });
    return response.data;
  },

  /**
   * Get idea by ID
   */
  async getIdea(id: number): Promise<MalyaIdea> {
    const response = await apiClient.get(`/api/v1/malya/ideas/${id}`);
    return response.data;
  },

  /**
   * Update idea
   */
  async updateIdea(id: number, updates: MalyaIdeaUpdate): Promise<MalyaIdea> {
    const response = await apiClient.put(`/api/v1/malya/ideas/${id}`, updates);
    return response.data;
  },

  /**
   * Delete idea
   */
  async deleteIdea(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/malya/ideas/${id}`);
  },

  /**
   * Get ideas by status
   */
  async getIdeasByStatus(status: string): Promise<MalyaIdea[]> {
    return this.getIdeas({ status });
  },

  /**
   * Get active ideas (not archived/completed)
   */
  async getActiveIdeas(): Promise<MalyaIdea[]> {
    return this.getIdeas({ status: 'active' });
  },
};

export default malyaService;
