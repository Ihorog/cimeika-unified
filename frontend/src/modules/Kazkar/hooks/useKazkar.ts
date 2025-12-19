/**
 * useKazkar hook
 */
import { useEffect } from 'react';
import { useKazkarStore } from '../store';
import { kazkarService } from '../service';

export const useKazkar = () => {
  const { status, setStatus } = useKazkarStore();

  useEffect(() => {
    kazkarService.getStatus().then((data) => {
      setStatus(data.status);
    });
  }, [setStatus]);

  return { status };
};
