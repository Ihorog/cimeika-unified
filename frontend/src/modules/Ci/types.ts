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

// Participant API types
export interface ParticipantAction {
  type: 'suggest' | 'check' | 'patch';
  title: string;
  details: string;
}

export interface ParticipantMessageData {
  participant: string;
  message: string;
  severity: 'info' | 'warn' | 'error';
  outputs: {
    patch_unified_diff?: string | null;
    actions: ParticipantAction[];
  };
}
