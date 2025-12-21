/**
 * Kazkar module types
 * Shared type definitions for Kazkar (Memory/Stories) module
 */

export interface KazkarEntry {
  id: string;
  title: string;
  content: string;
  type: 'story' | 'memory' | 'legend' | 'fact';
  timestamp: string; // ISO 8601 datetime when the memory occurred
  created_at: string; // ISO 8601 datetime when entry was created
  updated_at: string;
  tags?: string[];
  related_entries?: string[];
  attachments?: string[];
}

export interface KazkarState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  entries: KazkarEntry[];
  selectedEntry?: KazkarEntry;
}

export interface CreateKazkarEntryRequest {
  title: string;
  content: string;
  type: 'story' | 'memory' | 'legend' | 'fact';
  timestamp: string;
  tags?: string[];
}

export interface KazkarLibrary {
  total_entries: number;
  entries_by_type: Record<string, number>;
  recent_entries: KazkarEntry[];
}
