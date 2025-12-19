/**
 * Gallery module store - State management
 */
import { create } from 'zustand';

interface GalleryState {
  status: string;
  setStatus: (status: string) => void;
}

export const useGalleryStore = create<GalleryState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
