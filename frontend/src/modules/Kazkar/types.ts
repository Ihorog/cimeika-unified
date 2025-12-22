/**
 * Kazkar module types
 * Shared type definitions for Kazkar (Memory/Stories) module
 */

export interface KazkarEntry {
  id: number;
  title: string;
  content: string;
  story_type: 'story' | 'memory' | 'legend' | 'fact' | null;
  participants?: string[];
  location?: string;
  time: string; // ISO 8601 datetime
  tags: string[];
  source_trace?: string;
  module: string;
  canon_bundle_id: string;
}

export interface KazkarState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  stories: KazkarEntry[];
  selectedStory?: KazkarEntry;
  filterType?: 'story' | 'memory' | 'legend' | 'fact' | 'all';
}

export interface CreateKazkarEntryRequest {
  title: string;
  content: string;
  story_type?: 'story' | 'memory' | 'legend' | 'fact';
  participants?: string[];
  location?: string;
  tags?: string[];
  source_trace?: string;
}

export interface KazkarStats {
  total_stories: number;
  by_type: Record<string, number>;
}
