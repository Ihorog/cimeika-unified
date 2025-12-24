/**
 * Legend ci API Service
 * Handles all API calls for Legend ci interactive system
 */

const API_BASE = '/api/ci';

export const legendCiApi = {
  // Get legend metadata and structure
  async getMetadata() {
    const response = await fetch(`${API_BASE}/legend`);
    if (!response.ok) throw new Error('Failed to fetch legend metadata');
    return response.json();
  },

  // Get all nodes or filtered by tags
  async getNodes(tags = null) {
    const url = tags
      ? `${API_BASE}/legend/nodes?tags=${tags}`
      : `${API_BASE}/legend/nodes`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch legend nodes');
    return response.json();
  },

  // Get specific node by ID
  async getNode(nodeId) {
    const response = await fetch(`${API_BASE}/legend/nodes/${nodeId}`);
    if (!response.ok) throw new Error(`Failed to fetch node ${nodeId}`);
    return response.json();
  },

  // Get complete duality legend
  async getDualityLegend() {
    const response = await fetch(`${API_BASE}/legend/duality`);
    if (!response.ok) throw new Error('Failed to fetch duality legend');
    return response.json();
  },

  // Get specific duality section
  async getDualitySection(sectionId) {
    const response = await fetch(`${API_BASE}/legend/duality/sections/${sectionId}`);
    if (!response.ok) throw new Error(`Failed to fetch section ${sectionId}`);
    return response.json();
  },

  // Get symbolic library
  async getSymbols() {
    const response = await fetch(`${API_BASE}/legend/symbols`);
    if (!response.ok) throw new Error('Failed to fetch symbols');
    return response.json();
  },

  // Get navigation options from current node
  async getNavigation(currentNodeId, state = 'overview') {
    const response = await fetch(
      `${API_BASE}/legend/navigation/${currentNodeId}?state=${state}`
    );
    if (!response.ok) throw new Error('Failed to fetch navigation options');
    return response.json();
  }
};
