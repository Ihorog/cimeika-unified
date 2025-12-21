/**
 * Gallery module types
 * Shared type definitions for Gallery module
 */

export interface GalleryItem {
  id: string;
  title: string;
  description?: string;
  type: 'image' | 'video' | 'audio' | 'document';
  url: string;
  thumbnail_url?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
  metadata?: Record<string, any>;
}

export interface GalleryState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  items: GalleryItem[];
  selectedItem?: GalleryItem;
}

export interface CreateGalleryItemRequest {
  title: string;
  description?: string;
  type: 'image' | 'video' | 'audio' | 'document';
  url: string;
  tags?: string[];
}
