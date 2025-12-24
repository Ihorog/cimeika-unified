/**
 * Gallery Module API Service
 * Handles all API calls for Gallery (Media) module
 */

import { apiClient } from '../api';

export interface GalleryItem {
  id: number;
  title: string;
  description: string;
  media_type?: string;
  url?: string;
  thumbnail_url?: string;
  metadata?: Record<string, any>;
  tags?: string[];
  time?: string;
  module?: string;
  source_trace?: string;
  canon_bundle_id?: string;
}

export interface GalleryItemCreate {
  title: string;
  description: string;
  media_type?: string;
  url?: string;
  thumbnail_url?: string;
  metadata?: Record<string, any>;
  tags?: string[];
}

export interface GalleryItemUpdate {
  title?: string;
  description?: string;
  media_type?: string;
  url?: string;
  thumbnail_url?: string;
  metadata?: Record<string, any>;
  tags?: string[];
}

const galleryService = {
  /**
   * Get Gallery module status
   */
  async getStatus() {
    const response = await apiClient.get('/api/v1/gallery/');
    return response.data;
  },

  /**
   * Create a new gallery item
   */
  async createItem(item: GalleryItemCreate): Promise<GalleryItem> {
    const response = await apiClient.post('/api/v1/gallery/items', item);
    return response.data;
  },

  /**
   * Get all items with pagination
   */
  async getItems(params?: {
    skip?: number;
    limit?: number;
    media_type?: string;
  }): Promise<GalleryItem[]> {
    const response = await apiClient.get('/api/v1/gallery/items', { params });
    return response.data;
  },

  /**
   * Get item by ID
   */
  async getItem(id: number): Promise<GalleryItem> {
    const response = await apiClient.get(`/api/v1/gallery/items/${id}`);
    return response.data;
  },

  /**
   * Update item
   */
  async updateItem(id: number, updates: GalleryItemUpdate): Promise<GalleryItem> {
    const response = await apiClient.put(`/api/v1/gallery/items/${id}`, updates);
    return response.data;
  },

  /**
   * Delete item
   */
  async deleteItem(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/gallery/items/${id}`);
  },

  /**
   * Get items by media type
   */
  async getItemsByType(mediaType: string): Promise<GalleryItem[]> {
    return this.getItems({ media_type: mediaType });
  },

  /**
   * Get recent items
   */
  async getRecentItems(limit: number = 20): Promise<GalleryItem[]> {
    return this.getItems({ limit });
  },
};

export default galleryService;
