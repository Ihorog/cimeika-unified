import { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState('Checking...')
  const [logs, setLogs] = useState(['System initialized...'])

  // Функція перевірки здоров'я бекенду
  const checkHealth = async () => {
    try {
      // Стукаємо на порт 8000 (наш Python API)
      const res = await fetch('http://localhost:8000/v1/health')
      const data = await res.json()
      setStatus('ONLINE')
      addLog(`Health check: ${JSON.stringify(data)}`)
    } catch (e) {
      setStatus('OFFLINE (Check API)')
      addLog('Error connecting to API on port 8000')
    }
  }

  const addLog = (msg) => {
    setLogs(prev => [ `> ${msg}`, ...prev ])
  }

  useEffect(() => {
    checkHealth()
  }, [])

  return (
    <div className="min-h-screen p-4 md:p-8 max-w-4xl mx-auto">
      {/* Header */}
      <header className="flex justify-between items-center mb-8 border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-3xl font-bold text-emerald-400 tracking-tighter">CIMEIKA <span className="text-xs text-slate-500">v2.0 Local</span></h1>
          <p className="text-xs text-slate-400">System Dashboard // Termux Node</p>
        </div>
        <div className={`px-3 py-1 rounded text-xs font-bold ${status.includes('ONLINE') ? 'bg-emerald-900 text-emerald-300' : 'bg-red-900 text-red-300'}`}>
          CORE: {status}
        </div>
      </header>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Module 1: Quick Actions */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 shadow-lg">
          <h2 className="text-xl font-bold text-purple-400 mb-4">⚡ Quick Actions</h2>
          <div className="space-y-3">
            <button onClick={() => addLog('Ping signal sent...')} className="w-full bg-slate-700 hover:bg-slate-600 text-left px-4 py-2 rounded transition border border-slate-600">
              📡 Ping Network
            </button>
            <button onClick={checkHealth} className="w-full bg-slate-700 hover:bg-slate-600 text-left px-4 py-2 rounded transition border border-slate-600">
              🔄 Reconnect Core
            </button>
            <button className="w-full bg-slate-700 hover:bg-slate-600 text-left px-4 py-2 rounded transition border border-slate-600 opacity-50 cursor-not-allowed">
              🧙‍♂️ Summon Avatar (Coming Soon)
            </button>
          </div>
        </div>

        {/* Module 2: System Logs */}
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700 font-mono text-xs h-64 overflow-y-auto shadow-inner">
          <h2 className="text-slate-500 mb-2 sticky top-0 bg-slate-900">SYSTEM LOGS</h2>
          {logs.map((log, i) => (
            <div key={i} className="mb-1 text-emerald-500/80">{log}</div>
          ))}
        </div>

      </div>

      {/* Footer */}
      <footer className="mt-12 text-center text-slate-600 text-xs">
        <p>Cimeika Project // Identity-Driven Architecture</p>
      </footer>
    </div>
  )
}

export default App
