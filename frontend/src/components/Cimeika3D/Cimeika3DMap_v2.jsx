import React, { Suspense, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import StarField from './StarField';
import ModuleSphere from './ModuleSphere';
import ConnectionLine from './ConnectionLine';
import AudioLayer from './AudioLayer';

const Cimeika3DMap_v2 = ({ onModuleClick }) => {
  const [audioEnabled, setAudioEnabled] = useState(false);

  // Define 7 modules with their 3D positions (orbital arrangement around Ci)
  const modules = [
    {
      id: 'ci',
      name: 'Ci',
      position: [0, 0, 0], // Center
      description: 'Центральне ядро'
    },
    {
      id: 'kazkar',
      name: 'Казкар',
      position: [6, 2, 0],
      description: 'Оповідач'
    },
    {
      id: 'podija',
      name: 'ПоДія',
      position: [4, -3, 3],
      description: 'Події'
    },
    {
      id: 'nastrij',
      name: 'Настрій',
      position: [-5, 2, 2],
      description: 'Емоційна аналітика'
    },
    {
      id: 'malya',
      name: 'Маля',
      position: [-4, -2, -3],
      description: 'Творчість'
    },
    {
      id: 'gallery',
      name: 'Галерея',
      position: [2, 3, -4],
      description: 'Візуальна пам\'ять'
    },
    {
      id: 'calendar',
      name: 'Календар',
      position: [-2, -4, 1],
      description: 'Час'
    }
  ];

  // Generate connections from Ci to all other modules
  const connections = modules
    .filter(m => m.id !== 'ci')
    .map(m => ({
      start: modules[0].position,
      end: m.position
    }));

  const handleModuleClick = (module) => {
    console.log('Module clicked:', module);
    if (onModuleClick) {
      onModuleClick(module);
    }
  };

  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      {/* Audio control toggle */}
      <div style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        zIndex: 1000,
        background: 'rgba(0,0,0,0.5)',
        padding: '10px 15px',
        borderRadius: '8px',
        color: 'white',
        cursor: 'pointer',
        userSelect: 'none'
      }}
      onClick={() => setAudioEnabled(!audioEnabled)}
      >
        🔊 {audioEnabled ? 'ON' : 'OFF'}
      </div>

      {/* Module info overlay */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        zIndex: 1000,
        background: 'rgba(0,0,0,0.7)',
        padding: '15px 20px',
        borderRadius: '8px',
        color: 'white',
        maxWidth: '300px'
      }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: '18px' }}>Cimeika 3D Map</h3>
        <p style={{ margin: 0, fontSize: '14px', opacity: 0.8 }}>
          Обертайте мишею • Клікніть на модуль для переходу
        </p>
      </div>

      <Canvas
        shadows
        style={{ background: '#000' }}
      >
        <PerspectiveCamera makeDefault position={[15, 10, 15]} />
        <OrbitControls
          enablePan={false}
          minDistance={10}
          maxDistance={40}
          autoRotate
          autoRotateSpeed={0.5}
        />

        {/* Lighting */}
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={0.8} color="#ffffff" />
        <pointLight position={[-10, -10, -10]} intensity={0.4} color="#4a9eff" />
        
        <Suspense fallback={null}>
          {/* Background and stars */}
          <StarField />
          
          {/* Connection lines */}
          {connections.map((conn, i) => (
            <ConnectionLine
              key={`connection-${i}`}
              start={conn.start}
              end={conn.end}
              color="#4a9eff"
              opacity={0.2}
            />
          ))}
          
          {/* Module spheres */}
          {modules.map(module => (
            <ModuleSphere
              key={module.id}
              position={module.position}
              module={module}
              onClick={() => handleModuleClick(module)}
            />
          ))}
        </Suspense>
      </Canvas>

      {/* Audio layer */}
      <AudioLayer enabled={audioEnabled} volume={0.3} />
    </div>
  );
};

export default Cimeika3DMap_v2;
