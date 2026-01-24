import React, { useState, useEffect } from 'react';
import { galleryService } from '../../services/modules';

const GalleryView = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all'); // all, image, video, audio, document
  const [selectedItem, setSelectedItem] = useState(null);
  const [newItem, setNewItem] = useState({
    title: '',
    description: '',
    media_type: 'image',
    url: '',
    thumbnail_url: '',
    mime_type: '',
    tags: ''
  });

  useEffect(() => {
    loadItems();
  }, [filter]);

  const loadItems = async () => {
    setLoading(true);
    setError(null);
    try {
      let data;
      if (filter === 'all') {
        data = await galleryService.getRecentItems(50);
      } else {
        data = await galleryService.getItemsByType(filter);
      }
      setItems(data);
    } catch (err) {
      setError('Не вдалося завантажити елементи галереї. Перевірте з\'єднання з backend.');
      console.error('Error loading gallery items:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const itemData = {
        title: newItem.title,
        description: newItem.description,
        media_type: newItem.media_type,
        url: newItem.url,
        thumbnail_url: newItem.thumbnail_url || undefined,
        mime_type: newItem.mime_type || undefined,
        tags: newItem.tags ? newItem.tags.split(',').map(t => t.trim()) : []
      };
      
      await galleryService.createItem(itemData);
      setNewItem({
        title: '',
        description: '',
        media_type: 'image',
        url: '',
        thumbnail_url: '',
        mime_type: '',
        tags: ''
      });
      setShowForm(false);
      loadItems();
    } catch (err) {
      setError('Не вдалося створити елемент: ' + (err.response?.data?.detail || err.message));
      console.error('Error creating item:', err);
    }
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
  };

  const closeModal = () => {
    setSelectedItem(null);
  };

  const getMediaIcon = (type) => {
    const icons = {
      image: '🖼️',
      video: '🎬',
      audio: '🎵',
      document: '📄',
      other: '📎'
    };
    return icons[type] || icons.other;
  };

  const getMimeTypeIcon = (mimeType) => {
    if (!mimeType) return '📎';
    if (mimeType.startsWith('image/')) return '🖼️';
    if (mimeType.startsWith('video/')) return '🎬';
    if (mimeType.startsWith('audio/')) return '🎵';
    if (mimeType.includes('pdf')) return '📕';
    if (mimeType.includes('word') || mimeType.includes('document')) return '📘';
    if (mimeType.includes('sheet') || mimeType.includes('excel')) return '📊';
    if (mimeType.includes('presentation') || mimeType.includes('powerpoint')) return '📙';
    return '📎';
  };

  const isImageUrl = (url) => {
    if (!url) return false;
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'];
    return imageExtensions.some(ext => url.toLowerCase().endsWith(ext));
  };

  const isVideoUrl = (url) => {
    if (!url) return false;
    const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi'];
    return videoExtensions.some(ext => url.toLowerCase().endsWith(ext));
  };

  return (
    <div className="module-view gallery-view">
      <header className="module-header">
        <h1>Галерея</h1>
        <p className="module-subtitle">Візуальний архів, медіа</p>
      </header>
      
      <main className="module-content">
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <div className="module-toolbar">
          <div className="module-actions">
            <button 
              className="btn-primary"
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? 'Скасувати' : '+ Додати медіа'}
            </button>
            <button 
              className="btn-secondary"
              onClick={loadItems}
              disabled={loading}
            >
              ↻ Оновити
            </button>
          </div>

          <div className="filter-buttons">
            <button 
              className={filter === 'all' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('all')}
            >
              Всі ({items.length})
            </button>
            <button 
              className={filter === 'image' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('image')}
              title="Зображення"
            >
              🖼️
            </button>
            <button 
              className={filter === 'video' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('video')}
              title="Відео"
            >
              🎬
            </button>
            <button 
              className={filter === 'audio' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('audio')}
              title="Аудіо"
            >
              🎵
            </button>
            <button 
              className={filter === 'document' ? 'filter-active' : 'filter-btn'}
              onClick={() => setFilter('document')}
              title="Документи"
            >
              📄
            </button>
          </div>
        </div>

        {showForm && (
          <form className="gallery-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Назва *</label>
              <input
                type="text"
                value={newItem.title}
                onChange={(e) => setNewItem({...newItem, title: e.target.value})}
                required
                placeholder="Назва файлу або медіа"
              />
            </div>

            <div className="form-group">
              <label>Опис</label>
              <textarea
                value={newItem.description}
                onChange={(e) => setNewItem({...newItem, description: e.target.value})}
                rows={3}
                placeholder="Опис медіа-елементу..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Тип медіа *</label>
                <select
                  value={newItem.media_type}
                  onChange={(e) => setNewItem({...newItem, media_type: e.target.value})}
                  required
                >
                  <option value="image">Зображення</option>
                  <option value="video">Відео</option>
                  <option value="audio">Аудіо</option>
                  <option value="document">Документ</option>
                  <option value="other">Інше</option>
                </select>
              </div>

              <div className="form-group">
                <label>MIME тип</label>
                <input
                  type="text"
                  value={newItem.mime_type}
                  onChange={(e) => setNewItem({...newItem, mime_type: e.target.value})}
                  placeholder="image/jpeg, video/mp4, etc."
                />
              </div>
            </div>

            <div className="form-group">
              <label>URL медіа *</label>
              <input
                type="url"
                value={newItem.url}
                onChange={(e) => setNewItem({...newItem, url: e.target.value})}
                required
                placeholder="https://example.com/image.jpg"
              />
              <small className="form-help">
                💡 Посилання на зображення, відео або інший файл
              </small>
            </div>

            <div className="form-group">
              <label>URL превʼю (опціонально)</label>
              <input
                type="url"
                value={newItem.thumbnail_url}
                onChange={(e) => setNewItem({...newItem, thumbnail_url: e.target.value})}
                placeholder="https://example.com/thumbnail.jpg"
              />
            </div>

            <div className="form-group">
              <label>Теги (через кому)</label>
              <input
                type="text"
                value={newItem.tags}
                onChange={(e) => setNewItem({...newItem, tags: e.target.value})}
                placeholder="фото, подорож, спогади"
              />
            </div>

            <button type="submit" className="btn-primary">
              Додати до галереї
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading-state">
            Завантаження...
          </div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <p>🖼️ Галерея порожня</p>
            <p className="text-secondary">Додайте перший медіа-елемент</p>
          </div>
        ) : (
          <div className="gallery-grid">
            {items.map((item) => (
              <div 
                key={item.id} 
                className="gallery-item-card"
                onClick={() => handleItemClick(item)}
              >
                <div className="gallery-item-preview">
                  {item.thumbnail_url && isImageUrl(item.thumbnail_url) ? (
                    <img 
                      src={item.thumbnail_url} 
                      alt={item.title}
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                  ) : item.url && isImageUrl(item.url) ? (
                    <img 
                      src={item.url} 
                      alt={item.title}
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div className="gallery-item-placeholder" style={{ display: (item.thumbnail_url || item.url) && (isImageUrl(item.thumbnail_url) || isImageUrl(item.url)) ? 'none' : 'flex' }}>
                    <span className="placeholder-icon">
                      {item.mime_type ? getMimeTypeIcon(item.mime_type) : getMediaIcon(item.media_type)}
                    </span>
                  </div>
                  <div className="gallery-item-overlay">
                    <span className="overlay-icon">👁️</span>
                  </div>
                </div>
                <div className="gallery-item-info">
                  <h4>{item.title}</h4>
                  {item.description && (
                    <p className="item-description">{item.description.substring(0, 60)}{item.description.length > 60 ? '...' : ''}</p>
                  )}
                  <div className="item-meta">
                    <span className="meta-badge">
                      {getMediaIcon(item.media_type)} {item.media_type}
                    </span>
                    {item.time && (
                      <span className="meta-time">
                        {new Date(item.time).toLocaleDateString('uk-UA')}
                      </span>
                    )}
                  </div>
                  {item.tags && item.tags.length > 0 && (
                    <div className="item-tags">
                      {item.tags.slice(0, 3).map((tag, idx) => (
                        <span key={idx} className="tag">#{tag}</span>
                      ))}
                      {item.tags.length > 3 && <span className="tag">+{item.tags.length - 3}</span>}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal for viewing full item */}
        {selectedItem && (
          <div className="gallery-modal" onClick={closeModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={closeModal}>✕</button>
              
              <div className="modal-media">
                {selectedItem.url && isImageUrl(selectedItem.url) ? (
                  <img src={selectedItem.url} alt={selectedItem.title} />
                ) : selectedItem.url && isVideoUrl(selectedItem.url) ? (
                  <video controls src={selectedItem.url}>
                    Ваш браузер не підтримує відео.
                  </video>
                ) : (
                  <div className="modal-placeholder">
                    <span className="placeholder-icon-large">
                      {selectedItem.mime_type ? getMimeTypeIcon(selectedItem.mime_type) : getMediaIcon(selectedItem.media_type)}
                    </span>
                    <a href={selectedItem.url} target="_blank" rel="noopener noreferrer" className="btn-primary">
                      Відкрити файл ↗
                    </a>
                  </div>
                )}
              </div>

              <div className="modal-details">
                <h2>{selectedItem.title}</h2>
                {selectedItem.description && (
                  <p className="modal-description">{selectedItem.description}</p>
                )}
                
                <div className="modal-metadata">
                  <div className="metadata-item">
                    <strong>Тип:</strong> {getMediaIcon(selectedItem.media_type)} {selectedItem.media_type}
                  </div>
                  {selectedItem.mime_type && (
                    <div className="metadata-item">
                      <strong>MIME:</strong> {selectedItem.mime_type}
                    </div>
                  )}
                  {selectedItem.time && (
                    <div className="metadata-item">
                      <strong>Дата:</strong> {new Date(selectedItem.time).toLocaleString('uk-UA')}
                    </div>
                  )}
                  {selectedItem.url && (
                    <div className="metadata-item">
                      <strong>URL:</strong>{' '}
                      <a href={selectedItem.url} target="_blank" rel="noopener noreferrer">
                        Відкрити ↗
                      </a>
                    </div>
                  )}
                </div>

                {selectedItem.tags && selectedItem.tags.length > 0 && (
                  <div className="modal-tags">
                    {selectedItem.tags.map((tag, idx) => (
                      <span key={idx} className="tag">#{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default GalleryView;
