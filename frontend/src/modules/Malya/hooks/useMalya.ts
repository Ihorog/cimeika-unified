/**
 * useMalya hook
 */
import { useEffect } from 'react';
import { useMalyaStore } from '../store';
import { malyaService } from '../service';

export const useMalya = () => {
  const { status, setStatus } = useMalyaStore();

  useEffect(() => {
    malyaService.getStatus()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((error) => {
        console.error('Failed to fetch Malya status:', error);
        setStatus('error');
      });
  }, [setStatus]);

  return { status };
};
