/**
 * Main Layout Component
 * Provides navigation and structure for all pages
 */
import { Link, Outlet, useLocation } from 'react-router-dom';
import './MainLayout.css';

const MainLayout = () => {
  const location = useLocation();

  const modules = [
    { path: '/', name: 'Головна', id: 'home' },
    { path: '/ci', name: 'Ci', id: 'ci', description: 'Центральне ядро' },
    { path: '/podija', name: 'ПоДія', id: 'podija', description: 'Події' },
    { path: '/nastrij', name: 'Настрій', id: 'nastrij', description: 'Емоції' },
    { path: '/malya', name: 'Маля', id: 'malya', description: 'Ідеї' },
    { path: '/kazkar', name: 'Казкар', id: 'kazkar', description: 'Пам\'ять' },
    { path: '/calendar', name: 'Календар', id: 'calendar', description: 'Час' },
    { path: '/gallery', name: 'Галерея', id: 'gallery', description: 'Медіа' },
  ];

  return (
    <div className="main-layout">
      <header className="main-header">
        <div className="header-content">
          <Link to="/" className="logo">
            <h1>CIMEIKA</h1>
            <span className="subtitle">Сімейка</span>
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
    </div>
  );
};

export default MainLayout;
