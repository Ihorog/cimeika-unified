/**
 * Podija module API client
 * API functions for Podija (Events) module
 */

import type { TimelineNode, CreateTimelineNodeRequest } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const podijaApi = {
  /**
   * Get timeline nodes
   */
  async getTimeline(): Promise<TimelineNode[]> {
    const response = await fetch(`${API_BASE}/api/podija/timeline`);
    if (!response.ok) {
      throw new Error('Failed to fetch timeline');
    }
    const data = await response.json();
    return data.timeline || [];
  },

  /**
   * Create a new timeline node
   */
  async createNode(node: CreateTimelineNodeRequest): Promise<TimelineNode> {
    const response = await fetch(`${API_BASE}/api/podija/timeline`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(node),
    });
    if (!response.ok) {
      throw new Error('Failed to create timeline node');
    }
    return response.json();
  },

  /**
   * Get timeline node by ID
   */
  async getNode(id: string): Promise<TimelineNode> {
    const response = await fetch(`${API_BASE}/api/podija/timeline/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch timeline node');
    }
    return response.json();
  },

  /**
   * Update timeline node
   */
  async updateNode(id: string, node: Partial<TimelineNode>): Promise<TimelineNode> {
    const response = await fetch(`${API_BASE}/api/podija/timeline/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(node),
    });
    if (!response.ok) {
      throw new Error('Failed to update timeline node');
    }
    return response.json();
  },
};
