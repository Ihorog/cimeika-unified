/**
 * SEO Demo Page
 * Demonstrates the SEO metadata functionality
 */
import { useState, useEffect } from 'react';
import { seoService } from '../services';
import type { SeoData, SeoConfig } from '../services/seo';
import './SeoDemo.css';

const SeoDemo = () => {
  const [states, setStates] = useState<string[]>([]);
  const [selectedState, setSelectedState] = useState<string>('');
  const [intents, setIntents] = useState<string[]>([]);
  const [selectedIntent, setSelectedIntent] = useState<string>('');
  const [seoData, setSeoData] = useState<SeoData | null>(null);
  const [config, setConfig] = useState<SeoConfig | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [appliedState, setAppliedState] = useState<string>('');
  const [appliedIntent, setAppliedIntent] = useState<string>('');

  useEffect(() => {
    const loadInitialData = async () => {
      setLoading(true);
      const [fetchedStates, fetchedConfig] = await Promise.all([
        seoService.getStates(),
        seoService.getConfig(),
      ]);
      
      setStates(fetchedStates);
      setConfig(fetchedConfig);
      
      if (fetchedStates.length > 0) {
        setSelectedState(fetchedStates[0]);
      }
      
      setLoading(false);
    };

    loadInitialData();
  }, []);

  useEffect(() => {
    if (selectedState) {
      const loadIntents = async () => {
        const fetchedIntents = await seoService.getIntents(selectedState);
        setIntents(fetchedIntents);
        
        if (fetchedIntents.length > 0) {
          setSelectedIntent(fetchedIntents[0]);
        }
      };

      loadIntents();
    }
  }, [selectedState]);

  useEffect(() => {
    if (selectedState && selectedIntent) {
      const loadSeoData = async () => {
        const data = await seoService.getSeoData(selectedState, selectedIntent);
        setSeoData(data);
      };

      loadSeoData();
    }
  }, [selectedState, selectedIntent]);

  const handleApplySeo = () => {
    if (seoData) {
      seoService.updateDocumentMeta(seoData, selectedState, selectedIntent);
      setAppliedState(selectedState);
      setAppliedIntent(selectedIntent);
    }
  };

  const handleClearSeo = () => {
    seoService.clearDocumentMeta();
    setAppliedState('');
    setAppliedIntent('');
  };

  if (loading) {
    return (
      <div className="seo-demo">
        <div className="loading">Loading SEO configuration...</div>
      </div>
    );
  }

  return (
    <div className="seo-demo">
      <div className="seo-demo-header">
        <h1>SEO Matrix Demo</h1>
        <p>Explore and test SEO metadata for different emotional states and intents</p>
      </div>

      <div className="seo-demo-content">
        {/* Configuration Section */}
        <section className="seo-section">
          <h2>SEO Configuration</h2>
          {config && (
            <div className="config-display">
              <div className="config-item">
                <strong>Canonical Language:</strong> {config.canonical_lang}
              </div>
              <div className="config-item">
                <strong>Title Max Length:</strong> {config.rules.title_max} chars
              </div>
              <div className="config-item">
                <strong>Description Max Length:</strong> {config.rules.description_max} chars
              </div>
              <div className="config-item">
                <strong>Hreflang Patterns:</strong>
                <ul>
                  {Object.entries(config.hreflang_patterns).map(([lang, pattern]) => (
                    <li key={lang}>
                      <code>{lang}: {pattern}</code>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </section>

        {/* Selection Section */}
        <section className="seo-section">
          <h2>Select State & Intent</h2>
          <div className="selection-controls">
            <div className="control-group">
              <label htmlFor="state-select">Emotional State:</label>
              <select
                id="state-select"
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
              >
                {states.map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>
            </div>

            <div className="control-group">
              <label htmlFor="intent-select">Intent:</label>
              <select
                id="intent-select"
                value={selectedIntent}
                onChange={(e) => setSelectedIntent(e.target.value)}
              >
                {intents.map((intent) => (
                  <option key={intent} value={intent}>
                    {intent}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="action-buttons">
            <button onClick={handleApplySeo} className="btn-primary" disabled={!seoData}>
              Apply SEO Meta
            </button>
            <button onClick={handleClearSeo} className="btn-secondary">
              Clear SEO Meta
            </button>
          </div>

          {appliedState && appliedIntent && (
            <div className="applied-notice">
              ✓ SEO applied for: <strong>{appliedState} / {appliedIntent}</strong>
            </div>
          )}
        </section>

        {/* SEO Data Display */}
        {seoData && (
          <section className="seo-section">
            <h2>SEO Metadata Preview</h2>
            
            <div className="meta-preview">
              <h3>Meta Tags</h3>
              <div className="meta-item">
                <strong>Title:</strong>
                <div className="meta-value">{seoData.meta.title}</div>
                <div className={`validation ${seoData.validation.title.valid ? 'valid' : 'invalid'}`}>
                  Length: {seoData.validation.title.length} / {seoData.validation.title.max}
                  {!seoData.validation.title.valid && ' ⚠️ Too long!'}
                </div>
              </div>

              <div className="meta-item">
                <strong>Description:</strong>
                <div className="meta-value">{seoData.meta.description}</div>
                <div className={`validation ${seoData.validation.description.valid ? 'valid' : 'invalid'}`}>
                  Length: {seoData.validation.description.length} / {seoData.validation.description.max}
                  {!seoData.validation.description.valid && ' ⚠️ Too long!'}
                </div>
              </div>
            </div>

            <div className="url-preview">
              <h3>URLs</h3>
              <div className="url-item">
                <strong>Canonical URL:</strong>
                <code>{seoData.canonical_url}</code>
              </div>
            </div>

            <div className="hreflang-preview">
              <h3>Hreflang Tags</h3>
              <ul className="hreflang-list">
                {Object.entries(seoData.hreflang).map(([lang, url]) => (
                  <li key={lang}>
                    <code>
                      &lt;link rel="alternate" hreflang="{lang}" href="{url}" /&gt;
                    </code>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        )}

        {/* States Matrix */}
        <section className="seo-section">
          <h2>Available States & Intents</h2>
          <div className="matrix-display">
            {states.map((state) => (
              <div key={state} className="state-card">
                <h4>{state}</h4>
                <div className="intent-pills">
                  {intents.map((intent) => (
                    <span
                      key={intent}
                      className={`intent-pill ${selectedState === state && selectedIntent === intent ? 'active' : ''}`}
                      onClick={() => {
                        setSelectedState(state);
                        setSelectedIntent(intent);
                      }}
                    >
                      {intent}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default SeoDemo;
