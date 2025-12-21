/**
 * Malya module types
 * Shared type definitions for Malya (Ideas/Creativity) module
 */

export interface MalyaIdea {
  id: string;
  title: string;
  description: string;
  category: 'innovation' | 'creative' | 'improvement' | 'experiment';
  status: 'draft' | 'active' | 'completed' | 'archived';
  priority: 'low' | 'medium' | 'high';
  tags?: string[];
  created_at: string;
  updated_at: string;
  related_modules?: string[];
}

export interface MalyaState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  ideas: MalyaIdea[];
  selectedIdea?: MalyaIdea;
}

export interface CreateIdeaRequest {
  title: string;
  description: string;
  category?: 'innovation' | 'creative' | 'improvement' | 'experiment';
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
}
