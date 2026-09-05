/**
 * Main Layout Component
 * Provides navigation and structure for all pages
 */
import { Link, Outlet, useLocation } from 'react-router-dom';
import CiFAB from '../components/CiFAB/CiFAB';
import CimeikaLogo from '../assets/ci-logo.png';
import './MainLayout.css';

const MainLayout = () => {
  const location = useLocation();

  const modules = [
    { path: '/', name: 'Головна', id: 'home' },
    { path: '/app/ci', name: 'Ci', id: 'ci', description: 'Центральне ядро' },
    { path: '/app/podija', name: 'ПоДія', id: 'podija', description: 'Події' },
    { path: '/app/nastrij', name: 'Настрій', id: 'nastrij', description: 'Емоції' },
    { path: '/app/malya', name: 'Маля', id: 'malya', description: 'Ідеї' },
    { path: '/app/kazkar', name: 'Казкар', id: 'kazkar', description: 'Пам\'ять' },
    { path: '/app/calendar', name: 'Календар', id: 'calendar', description: 'Час' },
    { path: '/app/gallery', name: 'Галерея', id: 'gallery', description: 'Медіа' },
  ];

  return (
    <div className="main-layout">
      <header className="main-header">
        <div className="header-content">
          <Link to="/" className="logo">
            <img src={CimeikaLogo} alt="CIMEIKA" className="logo-image" />
          </Link>
          <nav className="main-nav">
            {modules.slice(1).map(module => (
              <Link
                key={module.id}
                to={module.path}
                className={`nav-link ${location.pathname === module.path ? 'active' : ''}`}
                title={module.description}
              >
                {module.name}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="main-footer">
        <p>Створено з ❤️ для організації життя</p>
      </footer>

      {/* Global Ci FAB - always accessible */}
      <CiFAB />
    </div>
  );
};

export default MainLayout;
