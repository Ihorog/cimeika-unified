import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './core/ThemeManager';
import CiOverlay from './components/CiOverlay';

// Import module views
import CiView from './modules/ci/CiView';
import PodijaView from './modules/podija/PodijaView';
import NastrijView from './modules/nastrij/NastrijView';
import MalyaView from './modules/malya/MalyaView';
import KazkarView from './modules/kazkar/KazkarView';
import CalendarView from './modules/calendar/CalendarView';
import GalleryView from './modules/gallery/GalleryView';

// Import styles
import './styles/themes.css';
import './styles/modules.css';
import './App.css';

function App() {
  return (
    <Router>
      <ThemeProvider>
        <div className="app">
          <Routes>
            <Route path="/" element={<Navigate to="/ci" replace />} />
            <Route path="/ci" element={<CiView />} />
            <Route path="/podija" element={<PodijaView />} />
            <Route path="/nastrij" element={<NastrijView />} />
            <Route path="/malya" element={<MalyaView />} />
            <Route path="/kazkar" element={<KazkarView />} />
            <Route path="/calendar" element={<CalendarView />} />
            <Route path="/gallery" element={<GalleryView />} />
          </Routes>
          
          {/* Global Ci Overlay */}
          <CiOverlay />
        </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;
