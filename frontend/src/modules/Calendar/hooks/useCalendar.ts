/**
 * useCalendar hook
 */
import { useEffect } from 'react';
import { useCalendarStore } from '../store';
import { calendarService } from '../service';

export const useCalendar = () => {
  const { status, setStatus } = useCalendarStore();

  useEffect(() => {
    calendarService.getStatus()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((error) => {
        console.error('Failed to fetch Calendar status:', error);
        setStatus('error');
      });
  }, [setStatus]);

  return { status };
};
