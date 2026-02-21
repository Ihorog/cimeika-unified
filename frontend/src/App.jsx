import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './core/ThemeManager';
import MainLayout from './layouts/MainLayout';

// Import module views
import CiView from './modules/ci/CiView';
import PodijaView from './modules/podija/PodijaView';
import NastrijView from './modules/nastrij/NastrijView';
import MalyaView from './modules/malya/MalyaView';
import KazkarView from './modules/kazkar/KazkarView';
import CalendarView from './modules/calendar/CalendarView';
import GalleryView from './modules/gallery/GalleryView';

// Import Legend ci
import { LegendCiView } from './modules/LegendCi';

// Import pages
import Chat from './pages/Chat';
import WelcomePage from './pages/WelcomePage';

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
            {/* Welcome page as root */}
            <Route path="/" element={<WelcomePage />} />
            
            {/* Main app with layout */}
            <Route path="/app" element={<MainLayout />}>
              <Route index element={<Navigate to="/app/ci" replace />} />
              <Route path="ci" element={<CiView />} />
              <Route path="legends" element={<LegendCiView />} />
              <Route path="chat" element={<Chat />} />
              <Route path="podija" element={<PodijaView />} />
              <Route path="nastrij" element={<NastrijView />} />
              <Route path="malya" element={<MalyaView />} />
              <Route path="kazkar" element={<KazkarView />} />
              <Route path="calendar" element={<CalendarView />} />
              <Route path="gallery" element={<GalleryView />} />
            </Route>

            {/* /podiya top-level route */}
            <Route path="/podiya" element={<MainLayout />}>
              <Route index element={<PodijaView />} />
            </Route>
            
            {/* Redirects for old legend URLs */}
            <Route path="/ci/legend" element={<Navigate to="/app/legends" replace />} />
            <Route path="/kazkar/legends" element={<Navigate to="/app/legends" replace />} />
          </Routes>
        </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;
