/**
 * Ci module types
 * Shared type definitions for Ci module
 */

export interface CiState {
  status: 'idle' | 'loading' | 'ready' | 'error';
  modules: ModuleInfo[];
  health?: HealthStatus;
}

export interface ModuleInfo {
  id: string;
  name: string;
  description: string;
  status: 'in_development' | 'active' | 'maintenance';
}

export interface HealthStatus {
  status: string;
  message: string;
  timestamp: string;
  version?: string;
  canon_bundle_id?: string;
}

export interface CiChatMessage {
  message: string;
  context?: Record<string, any>;
}

export interface CiChatResponse {
  reply: string;
  timestamp: string;
  context?: Record<string, any>;
}
