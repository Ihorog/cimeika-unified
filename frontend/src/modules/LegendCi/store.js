/**
 * Legend ci State Store
 * Manages the state of the interactive Legend ci system using Zustand
 */
import { create } from 'zustand';

const useLegendCiStore = create((set, get) => ({
  // Navigation state
  currentNode: null,
  visitedNodes: [],
  userState: 'overview', // 'overview' | 'immersion' | 'integration'
  
  // Data
  nodes: [],
  metadata: null,
  symbols: null,
  
  // View preferences
  layerDepth: 'short', // 'short' | 'deep'
  visualMode: 'radial', // 'radial' | 'linear' | 'network'
  
  // Loading states
  loading: false,
  error: null,
  
  // Actions
  setCurrentNode: (node) => set({ currentNode: node }),
  
  visitNode: (nodeId) => set((state) => {
    if (!state.visitedNodes.includes(nodeId)) {
      return { visitedNodes: [...state.visitedNodes, nodeId] };
    }
    return state;
  }),
  
  setUserState: (newState) => set({ userState: newState }),
  
  setLayerDepth: (depth) => set({ layerDepth: depth }),
  
  setVisualMode: (mode) => set({ visualMode: mode }),
  
  setNodes: (nodes) => set({ nodes }),
  
  setMetadata: (metadata) => set({ metadata }),
  
  setSymbols: (symbols) => set({ symbols }),
  
  setLoading: (loading) => set({ loading }),
  
  setError: (error) => set({ error }),
  
  // Computed getters
  getNodeById: (id) => {
    const { nodes } = get();
    return nodes.find(node => node.id === id);
  },
  
  getConnectedNodes: (nodeId) => {
    const { nodes } = get();
    const node = nodes.find(n => n.id === nodeId);
    if (!node) return [];
    
    return (node.connections || []).map(connId =>
      nodes.find(n => n.id === connId)
    ).filter(Boolean);
  },
  
  getProgress: () => {
    const { nodes, visitedNodes } = get();
    if (!nodes.length) return 0;
    return Math.round((visitedNodes.length / nodes.length) * 100);
  },
  
  // Reset
  reset: () => set({
    currentNode: null,
    visitedNodes: [],
    userState: 'overview',
    layerDepth: 'short',
    visualMode: 'radial',
    error: null
  })
}));

export default useLegendCiStore;
