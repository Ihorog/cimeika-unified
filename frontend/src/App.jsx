import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import HealthCheckPage from './pages/HealthCheckPage';
import SeoDemo from './pages/SeoDemo';
import CiView from './modules/Ci/views/CiView';
import KazkarView from './modules/Kazkar/views/KazkarView';
import PodijaView from './modules/Podija/views/PodijaView';
import NastrijView from './modules/Nastrij/views/NastrijView';
import MalyaView from './modules/Malya/views/MalyaView';
import CalendarView from './modules/Calendar/views/CalendarView';
import GalleryView from './modules/Gallery/views/GalleryView';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Health check route - standalone without layout */}
        <Route path="/health" element={<HealthCheckPage />} />
        
        {/* SEO Demo page - standalone */}
        <Route path="/seo-demo" element={<SeoDemo />} />
        
        {/* Main application routes */}
        <Route path="/" element={<MainLayout />}>
          <Route index element={<HomePage />} />
          <Route path="ci" element={<CiView />} />
          <Route path="kazkar" element={<KazkarView />} />
          <Route path="podija" element={<PodijaView />} />
          <Route path="nastrij" element={<NastrijView />} />
          <Route path="malya" element={<MalyaView />} />
          <Route path="calendar" element={<CalendarView />} />
          <Route path="gallery" element={<GalleryView />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
