/**
 * Hugging Face Participant API Client
 * Implements "Ci Participant Protocol v1"
 */

export interface ParticipantMessageInput {
  text: string;
  artifacts?: Array<{
    name: string;
    content_base64: string;
  }>;
  metadata?: {
    source: 'ci' | 'ci-cd' | 'user';
    repo?: string;
    run_id?: string;
    pr?: number;
  };
}

export interface ParticipantMessageRequest {
  conversation_id: string;
  mode: 'analysis' | 'autofix' | 'logger';
  topic?: string;
  input: ParticipantMessageInput;
}

export interface ParticipantAction {
  type: 'suggest' | 'check' | 'patch';
  title: string;
  details: string;
}

export interface ParticipantMessageResponse {
  participant: string;
  message: string;
  severity: 'info' | 'warn' | 'error';
  outputs: {
    patch_unified_diff?: string | null;
    actions: ParticipantAction[];
  };
}

export interface ParticipantHealthResponse {
  status: string;
}

export interface ParticipantReadyResponse {
  status: string;
  env?: Record<string, any>;
}

/**
 * Participant API Client
 */
export class ParticipantClient {
  private apiUrl: string;
  private apiKey?: string;

  constructor(apiUrl?: string, apiKey?: string) {
    this.apiUrl = apiUrl || import.meta.env.VITE_PARTICIPANT_API_URL || 'https://ihorog-cimeika-api.hf.space';
    this.apiKey = apiKey || import.meta.env.VITE_PARTICIPANT_API_KEY;
  }

  /**
   * Get headers for API requests
   */
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.apiKey) {
      headers['X-API-KEY'] = this.apiKey;
    }

    return headers;
  }

  /**
   * Send a message to the participant API
   */
  async sendMessage(request: ParticipantMessageRequest): Promise<ParticipantMessageResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/api/participant/message`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('API authentication failed');
        }
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Participant API error:', error);
      throw error;
    }
  }

  /**
   * Check API health
   */
  async checkHealth(): Promise<ParticipantHealthResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/health`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Health check failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  /**
   * Check API readiness
   */
  async checkReady(): Promise<ParticipantReadyResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/ready`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Ready check failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Ready check error:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const participantClient = new ParticipantClient();

export default participantClient;
