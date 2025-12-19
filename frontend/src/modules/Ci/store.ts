/**
 * Ci module store - State management
 */
import { create } from 'zustand';

interface CiState {
  status: string;
  setStatus: (status: string) => void;
}

export const useCiStore = create<CiState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
