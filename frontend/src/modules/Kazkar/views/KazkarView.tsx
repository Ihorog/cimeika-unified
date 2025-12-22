/**
 * Kazkar module main view
 * UI orchestration without business logic
 */
import React, { useEffect, useState } from 'react';
import { kazkarApi } from '../api';
import type { KazkarEntry, KazkarStats } from '../types';
import { KazkarEntryCard } from '../ui';
import { LegendForm } from '../components/LegendForm';
import '../../../styles/moduleView.css';

const KazkarView: React.FC = () => {
  const [stories, setStories] = useState<KazkarEntry[]>([]);
  const [stats, setStats] = useState<KazkarStats | null>(null);
  const [filterType, setFilterType] = useState<string>('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    loadData();
  }, [filterType]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [storiesData, statsData] = await Promise.all([
        filterType === 'all' ? kazkarApi.getStories() : 
        filterType === 'legend' ? kazkarApi.getLegends() :
        kazkarApi.getStories(filterType),
        kazkarApi.getStats()
      ]);
      setStories(storiesData);
      setStats(statsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSuccess = () => {
    setShowCreateForm(false);
    loadData(); // Reload data after creation
  };

  if (showCreateForm) {
    return (
      <div className="module-view kazkar-view">
        <div className="module-view-header">
          <h1>Казкар — Пам'ять</h1>
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
    <div className="module-view kazkar-view">
      <div className="module-view-header">
        <h1>Казкар — Пам'ять</h1>
        <p className="subtitle">Історії, спогади та легенди</p>
        <span className="module-view-status">🟢 Активний</span>
      </div>

      <div className="module-view-content">
        {stats && (
          <div style={{ marginBottom: '2rem', padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
            <h2>Статистика</h2>
            <p>Всього записів: <strong>{stats.total_stories}</strong></p>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
              {Object.entries(stats.by_type).map(([type, count]) => (
                <div key={type} style={{ padding: '0.5rem 1rem', background: '#fff', borderRadius: '4px' }}>
                  {type}: <strong>{count}</strong>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>Фільтр</h2>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
              {['all', 'legend', 'story', 'memory', 'fact'].map(type => (
                <button
                  key={type}
                  onClick={() => setFilterType(type)}
                  style={{
                    padding: '0.5rem 1rem',
                    background: filterType === type ? '#3b82f6' : '#e5e7eb',
                    color: filterType === type ? '#fff' : '#000',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  }}
                >
                  {type === 'all' ? 'Всі' : 
                   type === 'legend' ? '⚡ Легенди' :
                   type === 'story' ? '📖 Історії' :
                   type === 'memory' ? '💭 Спогади' :
                   '📌 Факти'}
                </button>
              ))}
            </div>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            style={{
              padding: '0.75rem 1.5rem',
              background: '#f59e0b',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold',
              whiteSpace: 'nowrap',
            }}
          >
            ⚡ Створити легенду
          </button>
        </div>

        {loading && <p>Завантаження...</p>}
        {error && <p style={{ color: 'red' }}>Помилка: {error}</p>}
        
        {!loading && !error && (
          <div>
            <h2>
              {filterType === 'legend' ? '⚡ Легенди' :
               filterType === 'story' ? '📖 Історії' :
               filterType === 'memory' ? '💭 Спогади' :
               filterType === 'fact' ? '📌 Факти' :
               'Всі записи'}
              {' '}({stories.length})
            </h2>
            {stories.length === 0 ? (
              <p style={{ color: '#666', fontStyle: 'italic' }}>
                {filterType === 'legend' 
                  ? 'Ще немає легенд. Створіть першу легенду!'
                  : 'Ще немає записів цього типу.'}
              </p>
            ) : (
              <div style={{ marginTop: '1rem' }}>
                {stories.map(story => (
                  <KazkarEntryCard key={story.id} entry={story} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default KazkarView;
