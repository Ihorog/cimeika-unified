import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { BackgroundThemeProvider } from './components/BackgroundTheme';
import MainLayout from './layouts/MainLayout';
import CiEntryScreen from './components/CiEntryScreen';
import CiButton from './components/CiButton';
import WelcomePage from './pages/WelcomePage';
import HomePage from './pages/HomePage';
import HealthCheckPage from './pages/HealthCheckPage';
import SeoDemo from './pages/SeoDemo';
import Chat from './pages/Chat';
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
      <BackgroundThemeProvider>
        <Routes>
          {/* Welcome page as default - beautiful landing */}
          <Route index element={<WelcomePage />} />
          
          {/* CANON v1.0.0: Ci Entry Screen - quick capture */}
          <Route path="/capture" element={<CiEntryScreen />} />
          
          {/* Health check route - standalone without layout */}
          <Route path="/health" element={<HealthCheckPage />} />
          
          {/* SEO Demo page - standalone */}
          <Route path="/seo-demo" element={<SeoDemo />} />
          
          {/* Legacy home page - accessible via /home with layout */}
          <Route path="/home" element={<MainLayout />}>
            <Route index element={<HomePage />} />
          </Route>
          
          {/* Cimeika modules - unfold after Ci action */}
          <Route element={<MainLayout />}>
            <Route path="/ci" element={<CiView />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/kazkar" element={<KazkarView />} />
            <Route path="/podija" element={<PodijaView />} />
            <Route path="/nastrij" element={<NastrijView />} />
            <Route path="/malya" element={<MalyaView />} />
            <Route path="/calendar" element={<CalendarView />} />
            <Route path="/gallery" element={<GalleryView />} />
          </Route>
        </Routes>
        
        {/* Global Ci Button - visible on all pages except welcome */}
        <CiButton />
      </BackgroundThemeProvider>
    </Router>
  );
}

export default App;
