import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Initialize Cimeika modules
import { setupModules } from './app/modules'

// Setup modules on app startup
setupModules().then(results => {
  console.log('Cimeika modules initialized:', results);
}).catch(error => {
  console.error('Failed to initialize Cimeika modules:', error);
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
