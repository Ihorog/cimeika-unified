import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { gradientBackgroundShader } from '../../shaders/gradientBackground';

const StarField = () => {
  const meshRef = useRef();
  const particlesRef = useRef();

  // Shader material for background
  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        colorTop: { value: new THREE.Color(0x1a1a2e) }, // Dark blue-purple
        colorBottom: { value: new THREE.Color(0x0f0f1e) } // Very dark blue
      },
      vertexShader: gradientBackgroundShader.vertexShader,
      fragmentShader: gradientBackgroundShader.fragmentShader,
      side: THREE.BackSide
    });
  }, []);

  // Create star particles
  const particles = useMemo(() => {
    const count = 1000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    
    for (let i = 0; i < count; i++) {
      // Random position in sphere
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const radius = 50 + Math.random() * 50;
      
      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);
      
      // Warm/cold color variation
      const warmth = Math.random();
      colors[i * 3] = 0.8 + warmth * 0.2; // R
      colors[i * 3 + 1] = 0.8 + warmth * 0.15; // G
      colors[i * 3 + 2] = 0.9 + warmth * 0.1; // B
    }
    
    return { positions, colors };
  }, []);

  // Animate
  useFrame((state) => {
    if (meshRef.current) {
      shaderMaterial.uniforms.time.value = state.clock.elapsedTime;
    }
    
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.0001;
      particlesRef.current.rotation.x += 0.00005;
    }
  });

  return (
    <>
      {/* Background sphere with shader */}
      <mesh ref={meshRef} scale={[100, 100, 100]}>
        <sphereGeometry args={[1, 32, 32]} />
        <primitive object={shaderMaterial} attach="material" />
      </mesh>
      
      {/* Star particles */}
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particles.positions.length / 3}
            array={particles.positions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={particles.colors.length / 3}
            array={particles.colors}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.15}
          vertexColors
          transparent
          opacity={0.8}
          sizeAttenuation
        />
      </points>
    </>
  );
};

export default StarField;
