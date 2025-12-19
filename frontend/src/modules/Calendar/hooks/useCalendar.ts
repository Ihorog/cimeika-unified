/**
 * useCalendar hook
 */
import { useEffect } from 'react';
import { useCalendarStore } from '../store';
import { calendarService } from '../service';

export const useCalendar = () => {
  const { status, setStatus } = useCalendarStore();

  useEffect(() => {
    calendarService.getStatus().then((data) => {
      setStatus(data.status);
    });
  }, [setStatus]);

  return { status };
};
