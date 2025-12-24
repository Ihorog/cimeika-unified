/**
 * LegendCiView - Main view for interactive Legend ci
 * Provides radial navigation and interactive node exploration
 */
import React, { useEffect, useState } from 'react';
import useLegendCiStore from '../store';
import { legendCiApi } from '../services/api';
import RadialMap from '../components/RadialMap';
import NodeView from '../components/NodeView';
import './LegendCiView.css';

const LegendCiView = () => {
  const {
    nodes,
    metadata,
    currentNode,
    userState,
    visitedNodes,
    loading,
    error,
    setNodes,
    setMetadata,
    setCurrentNode,
    visitNode,
    setUserState,
    setLoading,
    setError,
    getConnectedNodes,
    getProgress
  } = useLegendCiStore();

  const [showNodeView, setShowNodeView] = useState(false);

  useEffect(() => {
    loadLegendData();
  }, []);

  const loadLegendData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [nodesData, metadataData] = await Promise.all([
        legendCiApi.getNodes(),
        legendCiApi.getMetadata()
      ]);
      setNodes(nodesData.nodes);
      setMetadata(metadataData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = (node) => {
    setCurrentNode(node);
    visitNode(node.id);
    setShowNodeView(true);
    
    // Update user state based on interaction
    if (userState === 'overview') {
      setUserState('immersion');
    }
  };

  const handleCloseNodeView = () => {
    setShowNodeView(false);
  };

  const handleNavigateToNode = (node) => {
    setCurrentNode(node);
    visitNode(node.id);
  };

  // Get connections for visualization
  const connections = nodes.flatMap(node =>
    (node.connections || []).map(connId => ({
      from: node.id,
      to: connId
    }))
  );

  const connectedNodes = currentNode ? getConnectedNodes(currentNode.id) : [];
  const progress = getProgress();

  if (loading) {
    return (
      <div className="legend-ci-view loading">
        <div className="loading-spinner">⚡</div>
        <p>Завантаження Легенди ci...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="legend-ci-view error">
        <div className="error-message">
          <h2>Помилка завантаження</h2>
          <p>{error}</p>
          <button onClick={loadLegendData} className="retry-button">
            Спробувати знову
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="legend-ci-view">
      {/* Hero Section */}
      <div className="legend-ci-hero">
        <div className="legend-ci-hero-icon">✨</div>
        <h1 className="legend-ci-hero-title">Легенда ci</h1>
        <p className="legend-ci-hero-subtitle">
          {metadata?.subtitle || 'Жива модель еволюції знань і сенсів'}
        </p>
      </div>

      {/* State Selector */}
      <div className="legend-ci-state-selector">
        <button
          className={`state-btn ${userState === 'overview' ? 'active' : ''}`}
          onClick={() => setUserState('overview')}
        >
          <span className="state-icon">🗺️</span>
          <span>Огляд</span>
        </button>
        <button
          className={`state-btn ${userState === 'immersion' ? 'active' : ''}`}
          onClick={() => setUserState('immersion')}
        >
          <span className="state-icon">🔍</span>
          <span>Занурення</span>
        </button>
        <button
          className={`state-btn ${userState === 'integration' ? 'active' : ''}`}
          onClick={() => setUserState('integration')}
        >
          <span className="state-icon">✨</span>
          <span>Інтеграція</span>
        </button>
      </div>

      {/* Progress Bar */}
      <div className="legend-ci-progress">
        <div className="progress-bar-container">
          <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
        </div>
        <div className="progress-text">
          Досліджено: {visitedNodes.length} з {nodes.length} вузлів ({progress}%)
        </div>
      </div>

      {/* Radial Map */}
      <div className="legend-ci-map-section">
        <h2 className="section-title">Навігаційна Карта</h2>
        <p className="section-description">
          Клікніть на вузол для дослідження. Центр — Ci, ядро системи.
        </p>
        <RadialMap
          nodes={nodes}
          currentNode={currentNode}
          onNodeClick={handleNodeClick}
          connections={connections}
        />
      </div>

      {/* Structure Overview */}
      {metadata && metadata.structure && (
        <div className="legend-ci-structure">
          <h2 className="section-title">Структура Легенди</h2>
          <div className="structure-grid">
            {Object.entries(metadata.structure).map(([section, nodeIds]) => (
              <div key={section} className="structure-card">
                <h3 className="structure-card-title">{section}</h3>
                <div className="structure-card-nodes">
                  {nodeIds.map(id => {
                    const node = nodes.find(n => n.id === id);
                    return node ? (
                      <button
                        key={id}
                        className={`structure-node ${visitedNodes.includes(id) ? 'visited' : ''}`}
                        onClick={() => handleNodeClick(node)}
                      >
                        {node.icon} {node.title}
                      </button>
                    ) : null;
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Node View Modal */}
      {showNodeView && currentNode && (
        <NodeView
          node={currentNode}
          onClose={handleCloseNodeView}
          onNavigate={handleNavigateToNode}
          connectedNodes={connectedNodes}
        />
      )}
    </div>
  );
};

export default LegendCiView;
