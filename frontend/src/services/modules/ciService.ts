/**
 * Ci Module API Service
 * Handles all API calls for Ci module
 */

import { apiClient } from '../api';

export interface CiCaptureRequest {
  type: 'text' | 'voice' | 'gesture' | 'intent';
  content: string;
  metadata?: Record<string, any>;
}

export interface CiCaptureResponse {
  event_id: string;
  classification: {
    emotion_state?: string;
    intent?: string;
    module_suggestion?: string;
    tags: string[];
  };
  time_position: {
    iso: string;
    readable: string;
  };
  related_traces: string[];
  seo_context?: {
    lang: string;
    state: string;
    intent: string;
    url: string;
  };
}

export interface CiStatus {
  module: string;
  name: string;
  description: string;
  status: string;
}

const ciService = {
  /**
   * Get Ci module status
   */
  async getStatus(): Promise<CiStatus> {
    const response = await apiClient.get('/api/v1/ci/');
    return response.data;
  },

  /**
   * CANON v1.0.0: ci.capture() - Main entry point action
   * Stateless, no login required
   */
  async capture(request: CiCaptureRequest): Promise<CiCaptureResponse> {
    const response = await apiClient.post('/api/v1/ci/capture', request);
    return response.data;
  },

  /**
   * Quick capture with just text
   */
  async quickCapture(text: string): Promise<CiCaptureResponse> {
    return this.capture({
      type: 'text',
      content: text,
    });
  },

  /**
   * Get Legend Ci metadata
   */
  async getLegendMetadata(): Promise<any> {
    const response = await apiClient.get('/api/v1/ci/legend/metadata');
    return response.data;
  },

  /**
   * Get all Legend Ci nodes
   */
  async getLegendNodes(): Promise<any[]> {
    const response = await apiClient.get('/api/v1/ci/legend/nodes');
    return response.data;
  },

  /**
   * Get specific Legend Ci node by ID
   */
  async getLegendNode(nodeId: string): Promise<any> {
    const response = await apiClient.get(`/api/v1/ci/legend/nodes/${nodeId}`);
    return response.data;
  },

  /**
   * Get Duality Legend (15 nodes)
   */
  async getDualityLegend(): Promise<any> {
    const response = await apiClient.get('/api/v1/ci/legend/duality');
    return response.data;
  },
};

export default ciService;
