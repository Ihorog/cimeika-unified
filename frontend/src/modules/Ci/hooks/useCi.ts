/**
 * useCi hook
 */
import { useEffect } from 'react';
import { useCiStore } from '../store';
import { ciService } from '../service';

export const useCi = () => {
  const { status, setStatus } = useCiStore();

  useEffect(() => {
    ciService.getStatus().then((data) => {
      setStatus(data.status);
    });
  }, [setStatus]);

  return { status };
};
