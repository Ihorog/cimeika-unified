/**
 * Podija module store - State management
 */
import { create } from 'zustand';

interface PodijaState {
  status: string;
  setStatus: (status: string) => void;
}

export const usePodijaStore = create<PodijaState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
