/**
 * Gallery module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useGallery } from '../hooks/useGallery';

const GalleryView: React.FC = () => {
  const { status } = useGallery();

  return (
    <div className="gallery-view">
      <h1>Галерея - Медіа</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default GalleryView;
