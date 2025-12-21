/**
 * Nastrij module types
 * Shared type definitions for Nastrij (Mood/Emotions) module
 */

export interface NastrijState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  current_mood?: MoodEntry;
  mood_history: MoodEntry[];
}

export interface MoodEntry {
  id: string;
  mood: string; // e.g., "happy", "sad", "anxious", "calm"
  intensity: number; // 1-10 scale
  notes?: string;
  timestamp: string; // ISO 8601 datetime
  tags?: string[];
  context?: Record<string, any>;
}

export interface CreateMoodEntryRequest {
  mood: string;
  intensity: number;
  notes?: string;
  tags?: string[];
}

export interface MoodAnalytics {
  average_intensity: number;
  most_common_mood: string;
  mood_distribution: Record<string, number>;
  trend: 'improving' | 'stable' | 'declining';
}
