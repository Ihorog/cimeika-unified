/**
 * RadialMap Component
 * Interactive radial navigation map for Legend ci nodes
 */
import React, { useEffect, useRef, useState } from 'react';
import './RadialMap.css';

const RadialMap = ({ nodes, currentNode, onNodeClick, connections = [] }) => {
  const canvasRef = useRef(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [nodePositions, setNodePositions] = useState([]);

  useEffect(() => {
    if (!nodes || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(canvas.width, canvas.height) * 0.35;

    // Calculate positions for all nodes in a circle
    const positions = nodes.map((node, index) => {
      const angle = (index / nodes.length) * 2 * Math.PI - Math.PI / 2;
      return {
        id: node.id,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        angle
      };
    });

    setNodePositions(positions);

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw connections
    connections.forEach(conn => {
      const fromPos = positions.find(p => p.id === conn.from);
      const toPos = positions.find(p => p.id === conn.to);
      if (fromPos && toPos) {
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(251, 191, 36, 0.2)';
        ctx.lineWidth = 1;
        ctx.moveTo(fromPos.x, fromPos.y);
        ctx.lineTo(toPos.x, toPos.y);
        ctx.stroke();
      }
    });

    // Draw center (Ci)
    ctx.beginPath();
    ctx.fillStyle = '#f59e0b';
    ctx.arc(centerX, centerY, 30, 0, 2 * Math.PI);
    ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 20px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Ci', centerX, centerY);

    // Draw nodes
    positions.forEach((pos, index) => {
      const node = nodes[index];
      const isActive = currentNode && currentNode.id === node.id;
      const isHovered = hoveredNode === node.id;

      // Node circle
      ctx.beginPath();
      ctx.fillStyle = isActive ? '#f59e0b' : (isHovered ? '#fbbf24' : '#fef3c7');
      ctx.strokeStyle = isActive ? '#d97706' : '#f59e0b';
      ctx.lineWidth = isActive ? 3 : 2;
      ctx.arc(pos.x, pos.y, 25, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();

      // Node icon
      ctx.fillStyle = isActive ? '#fff' : '#92400e';
      ctx.font = '20px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(node.icon, pos.x, pos.y);
    });
  }, [nodes, currentNode, hoveredNode, connections]);

  const handleCanvasClick = (event) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Check if click is on any node
    nodePositions.forEach((pos, index) => {
      const distance = Math.sqrt((x - pos.x) ** 2 + (y - pos.y) ** 2);
      if (distance <= 25) {
        onNodeClick(nodes[index]);
      }
    });
  };

  const handleCanvasMouseMove = (event) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    let foundHover = null;
    nodePositions.forEach((pos, index) => {
      const distance = Math.sqrt((x - pos.x) ** 2 + (y - pos.y) ** 2);
      if (distance <= 25) {
        foundHover = nodes[index].id;
      }
    });

    setHoveredNode(foundHover);
  };

  return (
    <div className="radial-map-container">
      <canvas
        ref={canvasRef}
        width={800}
        height={800}
        className="radial-map-canvas"
        onClick={handleCanvasClick}
        onMouseMove={handleCanvasMouseMove}
        style={{ cursor: hoveredNode ? 'pointer' : 'default' }}
      />
      {hoveredNode && (
        <div className="radial-map-tooltip">
          {nodes.find(n => n.id === hoveredNode)?.title}
        </div>
      )}
    </div>
  );
};

export default RadialMap;
