/**
 * Malya module API client
 * API functions for Malya (Ideas/Creativity) module
 */

import type { MalyaIdea, CreateIdeaRequest } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const malyaApi = {
  /**
   * Get all ideas
   */
  async getIdeas(): Promise<MalyaIdea[]> {
    const response = await fetch(`${API_BASE}/api/malya/ideas`);
    if (!response.ok) {
      throw new Error('Failed to fetch ideas');
    }
    const data = await response.json();
    return data.ideas || [];
  },

  /**
   * Create a new idea
   */
  async createIdea(idea: CreateIdeaRequest): Promise<MalyaIdea> {
    const response = await fetch(`${API_BASE}/api/malya/ideas`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(idea),
    });
    if (!response.ok) {
      throw new Error('Failed to create idea');
    }
    return response.json();
  },

  /**
   * Get idea by ID
   */
  async getIdea(id: string): Promise<MalyaIdea> {
    const response = await fetch(`${API_BASE}/api/malya/ideas/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch idea');
    }
    return response.json();
  },

  /**
   * Update idea
   */
  async updateIdea(id: string, idea: Partial<MalyaIdea>): Promise<MalyaIdea> {
    const response = await fetch(`${API_BASE}/api/malya/ideas/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(idea),
    });
    if (!response.ok) {
      throw new Error('Failed to update idea');
    }
    return response.json();
  },

  /**
   * Delete idea
   */
  async deleteIdea(id: string): Promise<void> {
    const response = await fetch(`${API_BASE}/api/malya/ideas/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete idea');
    }
  },
};
