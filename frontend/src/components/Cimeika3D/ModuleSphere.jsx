import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

const ModuleSphere = ({ 
  position, 
  module,
  onClick 
}) => {
  const sphereRef = useRef();
  const haloRef = useRef();
  const particlesRef = useRef();
  const glowRef = useRef();

  // Module-specific colors
  const moduleColors = {
    ci: { primary: '#667eea', glow: '#764ba2' },
    kazkar: { primary: '#f093fb', glow: '#f5576c' },
    podija: { primary: '#4facfe', glow: '#00f2fe' },
    nastrij: { primary: '#43e97b', glow: '#38f9d7' },
    malya: { primary: '#fa709a', glow: '#fee140' },
    gallery: { primary: '#30cfd0', glow: '#330867' },
    calendar: { primary: '#a8edea', glow: '#fed6e3' }
  };

  const colors = moduleColors[module.id] || moduleColors.ci;

  // Create orbital particles
  const particles = useMemo(() => {
    const count = 20;
    const positions = new Float32Array(count * 3);
    const velocities = [];
    
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const radius = 2 + Math.random() * 0.5;
      
      positions[i * 3] = Math.cos(angle) * radius;
      positions[i * 3 + 1] = Math.sin(angle) * radius;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 0.5;
      
      velocities.push({
        angle: angle,
        radius: radius,
        speed: 0.2 + Math.random() * 0.3,
        verticalSpeed: (Math.random() - 0.5) * 0.1
      });
    }
    
    return { positions, velocities };
  }, []);

  // Animation
  useFrame((state) => {
    const time = state.clock.elapsedTime;
    
    // Breathing effect for main sphere
    if (sphereRef.current) {
      const breathe = 1 + Math.sin(time * 0.5) * 0.05;
      sphereRef.current.scale.set(breathe, breathe, breathe);
    }
    
    // Halo pulsing
    if (haloRef.current) {
      const pulse = 1 + Math.sin(time * 0.7) * 0.1;
      haloRef.current.scale.set(pulse, pulse, pulse);
      haloRef.current.material.opacity = 0.2 + Math.sin(time * 0.5) * 0.1;
    }
    
    // Glow effect
    if (glowRef.current) {
      const glow = 1 + Math.sin(time * 0.8) * 0.15;
      glowRef.current.scale.set(glow, glow, glow);
    }
    
    // Animate particles
    if (particlesRef.current) {
      const positions = particlesRef.current.geometry.attributes.position.array;
      
      particles.velocities.forEach((vel, i) => {
        vel.angle += vel.speed * 0.01;
        vel.radius += Math.sin(time + i) * 0.001;
        
        positions[i * 3] = Math.cos(vel.angle) * vel.radius;
        positions[i * 3 + 1] = Math.sin(vel.angle) * vel.radius;
        positions[i * 3 + 2] += vel.verticalSpeed * 0.01;
        
        // Keep particles within bounds
        if (Math.abs(positions[i * 3 + 2]) > 1) {
          positions[i * 3 + 2] *= -0.5;
        }
      });
      
      particlesRef.current.geometry.attributes.position.needsUpdate = true;
      particlesRef.current.rotation.z += 0.001;
    }
  });

  return (
    <group position={position}>
      {/* Outer glow */}
      <mesh ref={glowRef} scale={1.5}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshBasicMaterial
          color={colors.glow}
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Halo ring */}
      <mesh ref={haloRef} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[1.5, 0.05, 16, 100]} />
        <meshBasicMaterial
          color={colors.primary}
          transparent
          opacity={0.3}
        />
      </mesh>
      
      {/* Main sphere */}
      <mesh 
        ref={sphereRef} 
        onClick={onClick}
        onPointerOver={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'pointer';
        }}
        onPointerOut={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'auto';
        }}
      >
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          color={colors.primary}
          emissive={colors.primary}
          emissiveIntensity={0.3}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>
      
      {/* Orbital particles */}
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particles.positions.length / 3}
            array={particles.positions}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.1}
          color={colors.primary}
          transparent
          opacity={0.8}
          sizeAttenuation
        />
      </points>
      
      {/* Module label */}
      <sprite position={[0, -2, 0]} scale={[2, 0.5, 1]}>
        <spriteMaterial
          color="#ffffff"
          transparent
          opacity={0.8}
        />
      </sprite>
    </group>
  );
};

export default ModuleSphere;
