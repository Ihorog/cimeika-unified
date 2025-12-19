/**
 * useNastrij hook
 */
import { useEffect } from 'react';
import { useNastrijStore } from '../store';
import { nastrijService } from '../service';

export const useNastrij = () => {
  const { status, setStatus } = useNastrijStore();

  useEffect(() => {
    nastrijService.getStatus()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((error) => {
        console.error('Failed to fetch Nastrij status:', error);
        setStatus('error');
      });
  }, [setStatus]);

  return { status };
};
