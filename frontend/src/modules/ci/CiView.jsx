import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Cimeika3DMap_v2 } from '../../components/Cimeika3D';

const CiView = () => {
  const navigate = useNavigate();

  const handleModuleClick = (module) => {
    // Navigate to the clicked module
    if (module.id !== 'ci') {
      navigate(`/${module.id}`);
    }
  };

  return (
    <div className="module-view ci-view" style={{ padding: 0, margin: 0, height: '100vh', overflow: 'hidden' }}>
      <Cimeika3DMap_v2 onModuleClick={handleModuleClick} />
    </div>
  );
};

export default CiView;
