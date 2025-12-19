/**
 * useKazkar hook
 */
import { useEffect } from 'react';
import { useKazkarStore } from '../store';
import { kazkarService } from '../service';

export const useKazkar = () => {
  const { status, setStatus } = useKazkarStore();

  useEffect(() => {
    kazkarService.getStatus()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((error) => {
        console.error('Failed to fetch Kazkar status:', error);
        setStatus('error');
      });
  }, [setStatus]);

  return { status };
};
