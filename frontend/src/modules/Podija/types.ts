/**
 * Podija module types
 * Shared type definitions for Podija (Events) module
 */

export interface TimelineNode {
  id: string;
  title: string;
  description?: string;
  timestamp: string; // ISO 8601 datetime
  type: 'past' | 'present' | 'future';
  category: 'event' | 'milestone' | 'scenario';
  status: 'planned' | 'in_progress' | 'completed' | 'cancelled';
  tags?: string[];
  related_nodes?: string[];
}

export interface PodijaState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  timeline: TimelineNode[];
  selectedNode?: TimelineNode;
}

export interface CreateTimelineNodeRequest {
  title: string;
  description?: string;
  timestamp: string;
  type: 'past' | 'present' | 'future';
  category?: 'event' | 'milestone' | 'scenario';
  tags?: string[];
}
