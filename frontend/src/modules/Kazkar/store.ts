/**
 * Kazkar module store - State management
 */
import { create } from 'zustand';

interface KazkarState {
  status: string;
  setStatus: (status: string) => void;
}

export const useKazkarStore = create<KazkarState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
