/**
 * usePodija hook
 */
import { useEffect } from 'react';
import { usePodijaStore } from '../store';
import { podijaService } from '../service';

export const usePodija = () => {
  const { status, setStatus } = usePodijaStore();

  useEffect(() => {
    podijaService.getStatus().then((data) => {
      setStatus(data.status);
    });
  }, [setStatus]);

  return { status };
};
