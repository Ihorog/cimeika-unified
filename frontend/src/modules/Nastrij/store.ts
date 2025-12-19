/**
 * Nastrij module store - State management
 */
import { create } from 'zustand';

interface NastrijState {
  status: string;
  setStatus: (status: string) => void;
}

export const useNastrijStore = create<NastrijState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
