/**
 * useGallery hook
 */
import { useEffect } from 'react';
import { useGalleryStore } from '../store';
import { galleryService } from '../service';

export const useGallery = () => {
  const { status, setStatus } = useGalleryStore();

  useEffect(() => {
    galleryService.getStatus()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((error) => {
        console.error('Failed to fetch Gallery status:', error);
        setStatus('error');
      });
  }, [setStatus]);

  return { status };
};
