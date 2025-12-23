/**
 * Ci Legends View - dedicated interface for browsing Ci Legends
 */
import React, { useEffect, useState } from 'react';
import { kazkarApi } from '../api';
import type { KazkarEntry } from '../types';
import { LegendsGallery } from '../components/LegendsGallery';
import { LegendForm } from '../components/LegendForm';

const CiLegendsView: React.FC = () => {
  const [legends, setLegends] = useState<KazkarEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  useEffect(() => {
    loadLegends();
  }, []);

  const loadLegends = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await kazkarApi.getLegends();
      setLegends(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load legends');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSuccess = () => {
    setShowCreateForm(false);
    loadLegends();
  };

  // Get all unique tags from legends
  const allTags = Array.from(
    new Set(legends.flatMap((legend) => legend.tags || []))
  ).sort();

  // Filter legends based on search and tags
  const filteredLegends = legends.filter((legend) => {
    const matchesSearch = searchQuery
      ? legend.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        legend.content.toLowerCase().includes(searchQuery.toLowerCase())
      : true;

    const matchesTags =
      selectedTags.length === 0 ||
      selectedTags.some((tag) => legend.tags?.includes(tag));

    return matchesSearch && matchesTags;
  });

  if (showCreateForm) {
    return (
      <div className="module-view kazkar-legends-view">
        <div className="module-view-header">
          <h1>⚡ Легенди Ci</h1>
          <p className="subtitle">Створення нової легенди</p>
        </div>
        <div className="module-view-content">
          <LegendForm
            onSuccess={handleCreateSuccess}
            onCancel={() => setShowCreateForm(false)}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="module-view kazkar-legends-view">
      {/* Hero Section */}
      <div
        style={{
          background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
          padding: '3rem 2rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '2px solid #fbbf24',
        }}
      >
        <div style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>⚡</div>
          <h1 style={{ fontSize: '2.5rem', color: '#92400e', marginBottom: '1rem' }}>
            Бібліотека Легенд Ci
          </h1>
          <p style={{ fontSize: '1.1rem', color: '#78350f', lineHeight: '1.6' }}>
            Казкар зберігає легенди про Ci, її принципи та дуальність світобудови.
            Кожна легенда — це частина філософії Cimeika, що живе в пам'яті системи.
          </p>
        </div>
      </div>

      {/* Controls */}
      <div style={{ marginBottom: '2rem' }}>
        <div
          style={{
            display: 'flex',
            gap: '1rem',
            flexWrap: 'wrap',
            alignItems: 'center',
            marginBottom: '1rem',
          }}
        >
          {/* Search */}
          <div style={{ flex: '1 1 300px' }}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="🔍 Пошук легенд..."
              style={{
                width: '100%',
                padding: '0.75rem 1rem',
                border: '2px solid #e5e7eb',
                borderRadius: '8px',
                fontSize: '1rem',
              }}
            />
          </div>

          {/* Create Button */}
          <button
            onClick={() => setShowCreateForm(true)}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold',
              fontSize: '1rem',
              whiteSpace: 'nowrap',
              boxShadow: '0 4px 6px rgba(245, 158, 11, 0.3)',
            }}
          >
            ⚡ Створити легенду
          </button>
        </div>

        {/* Tag Filters */}
        {allTags.length > 0 && (
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
              Фільтр за тегами:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {allTags.map((tag) => {
                const isSelected = selectedTags.includes(tag);
                return (
                  <button
                    key={tag}
                    onClick={() => {
                      setSelectedTags(
                        isSelected
                          ? selectedTags.filter((t) => t !== tag)
                          : [...selectedTags, tag]
                      );
                    }}
                    style={{
                      padding: '0.5rem 1rem',
                      background: isSelected
                        ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                        : '#fff',
                      color: isSelected ? '#fff' : '#6b7280',
                      border: `2px solid ${isSelected ? '#f59e0b' : '#e5e7eb'}`,
                      borderRadius: '20px',
                      cursor: 'pointer',
                      fontSize: '0.875rem',
                      fontWeight: isSelected ? '600' : '400',
                      transition: 'all 0.2s ease',
                    }}
                  >
                    {tag}
                  </button>
                );
              })}
              {selectedTags.length > 0 && (
                <button
                  onClick={() => setSelectedTags([])}
                  style={{
                    padding: '0.5rem 1rem',
                    background: '#fee',
                    color: '#c00',
                    border: '2px solid #fcc',
                    borderRadius: '20px',
                    cursor: 'pointer',
                    fontSize: '0.875rem',
                  }}
                >
                  ✕ Очистити
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Stats */}
      <div
        style={{
          display: 'flex',
          gap: '1rem',
          marginBottom: '2rem',
          flexWrap: 'wrap',
        }}
      >
        <div
          style={{
            flex: '1 1 200px',
            background: '#fff',
            padding: '1.5rem',
            borderRadius: '8px',
            border: '2px solid #e5e7eb',
          }}
        >
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f59e0b' }}>
            {legends.length}
          </div>
          <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>Всього легенд</div>
        </div>
        {selectedTags.length > 0 && (
          <div
            style={{
              flex: '1 1 200px',
              background: '#fff',
              padding: '1.5rem',
              borderRadius: '8px',
              border: '2px solid #e5e7eb',
            }}
          >
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3b82f6' }}>
              {filteredLegends.length}
            </div>
            <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>Відфільтровано</div>
          </div>
        )}
      </div>

      {/* Error State */}
      {error && (
        <div
          style={{
            padding: '1rem',
            background: '#fee',
            color: '#c00',
            borderRadius: '8px',
            marginBottom: '2rem',
          }}
        >
          ❌ {error}
        </div>
      )}

      {/* Legends Gallery */}
      <LegendsGallery legends={filteredLegends} loading={loading} />
    </div>
  );
};

export default CiLegendsView;
