/**
 * Gallery module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useGallery } from '../hooks/useGallery';
import '../../../styles/moduleView.css';

const GalleryView: React.FC = () => {
  const { status } = useGallery();

  return (
    <div className="module-view gallery-view">
      <div className="module-view-header">
        <h1>Галерея — Медіа</h1>
        <p className="subtitle">Візуальний архів та медіа-контент</p>
        <span className="module-view-status">🟡 В розробці</span>
      </div>

      <div className="module-view-content">
        <h2>Про модуль</h2>
        <p>
          <strong>Галерея</strong> — це модуль для збереження та організації медіа-контенту.
          Фотографії, відео, аудіо та інші медіа-файли в єдиному організованому просторі.
        </p>

        <h2>Основні функції</h2>
        <ul className="features-list">
          <li>Збереження фото та відео</li>
          <li>Організація медіа-контенту</li>
          <li>Альбоми та колекції</li>
          <li>Теги та категорії</li>
          <li>Пошук по медіа</li>
          <li>Інтеграція з іншими модулями</li>
        </ul>

        <p><strong>Поточний статус:</strong> {status}</p>
      </div>
    </div>
  );
};

export default GalleryView;
