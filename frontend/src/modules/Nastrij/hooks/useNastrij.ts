/**
 * useNastrij hook
 */
import { useEffect } from 'react';
import { useNastrijStore } from '../store';
import { nastrijService } from '../service';

export const useNastrij = () => {
  const { status, setStatus } = useNastrijStore();

  useEffect(() => {
    nastrijService.getStatus().then((data) => {
      setStatus(data.status);
    });
  }, [setStatus]);

  return { status };
};
