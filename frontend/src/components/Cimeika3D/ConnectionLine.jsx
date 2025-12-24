import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

const ConnectionLine = ({ start, end, color = '#4a9eff', opacity = 0.3 }) => {
  const lineRef = useRef();
  const materialRef = useRef();

  // Create line geometry
  const points = useMemo(() => {
    const curve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(...start),
      new THREE.Vector3(
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2 + 2,
        (start[2] + end[2]) / 2
      ),
      new THREE.Vector3(...end)
    );
    
    return curve.getPoints(50);
  }, [start, end]);

  const geometry = useMemo(() => {
    const geom = new THREE.BufferGeometry().setFromPoints(points);
    return geom;
  }, [points]);

  // Animate opacity with breathing effect
  useFrame((state) => {
    if (materialRef.current) {
      const breathe = Math.sin(state.clock.elapsedTime * 0.5) * 0.2 + 0.8;
      materialRef.current.opacity = opacity * breathe;
    }
  });

  return (
    <line ref={lineRef} geometry={geometry}>
      <lineBasicMaterial
        ref={materialRef}
        color={color}
        transparent
        opacity={opacity}
        linewidth={2}
      />
    </line>
  );
};

export default ConnectionLine;
