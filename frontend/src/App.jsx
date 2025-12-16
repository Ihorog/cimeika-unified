import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [modules, setModules] = useState([])
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    // Fetch modules from backend
    fetch(import.meta.env.VITE_API_URL + '/api/v1/modules')
      .then(res => res.json())
      .then(data => {
        setModules(data.modules)
        setStatus('success')
      })
      .catch(err => {
        console.error('Failed to fetch modules:', err)
        setStatus('error')
      })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>CIMEIKA — Сімейка</h1>
        <p>Центральна екосистема проєкту Cimeika</p>
      </header>

      <main>
        <section className="modules-section">
          <h2>7 Модулів</h2>
          {status === 'loading' && <p>Завантаження...</p>}
          {status === 'error' && (
            <p className="error">Помилка завантаження. Перевірте backend.</p>
          )}
          {status === 'success' && (
            <div className="modules-grid">
              {modules.map(module => (
                <div key={module.id} className="module-card">
                  <h3>{module.name}</h3>
                  <p>{module.description}</p>
                  <span className="status">🟡 В розробці</span>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      <footer>
        <p>Створено з ❤️ для організації життя</p>
      </footer>
    </div>
  )
}

export default App
