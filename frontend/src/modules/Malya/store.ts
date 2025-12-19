/**
 * Malya module store - State management
 */
import { create } from 'zustand';

interface MalyaState {
  status: string;
  setStatus: (status: string) => void;
}

export const useMalyaStore = create<MalyaState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
