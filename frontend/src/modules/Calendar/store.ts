/**
 * Calendar module store - State management
 */
import { create } from 'zustand';

interface CalendarState {
  status: string;
  setStatus: (status: string) => void;
}

export const useCalendarStore = create<CalendarState>((set) => ({
  status: 'idle',
  setStatus: (status) => set({ status }),
}));
