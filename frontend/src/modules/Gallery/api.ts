/**
 * Gallery module API client
 * API functions for Gallery module
 */

import type { GalleryItem, CreateGalleryItemRequest } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const galleryApi = {
  /**
   * Get all gallery items
   */
  async getItems(): Promise<GalleryItem[]> {
    const response = await fetch(`${API_BASE}/api/gallery/items`);
    if (!response.ok) {
      throw new Error('Failed to fetch gallery items');
    }
    const data = await response.json();
    return data.items || [];
  },

  /**
   * Create a new gallery item
   */
  async createItem(item: CreateGalleryItemRequest): Promise<GalleryItem> {
    const response = await fetch(`${API_BASE}/api/gallery/items`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(item),
    });
    if (!response.ok) {
      throw new Error('Failed to create gallery item');
    }
    return response.json();
  },

  /**
   * Get gallery item by ID
   */
  async getItem(id: string): Promise<GalleryItem> {
    const response = await fetch(`${API_BASE}/api/gallery/items/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch gallery item');
    }
    return response.json();
  },

  /**
   * Delete gallery item
   */
  async deleteItem(id: string): Promise<void> {
    const response = await fetch(`${API_BASE}/api/gallery/items/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete gallery item');
    }
  },
};
