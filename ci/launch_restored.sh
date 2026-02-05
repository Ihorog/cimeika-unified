#!/bin/bash
# Вбиваємо старі процеси
pkill -f "uvicorn"
pkill -f "vite"

echo ">>> Starting Cimeika API (main.py)..."
source venv/bin/activate
# Запускаємо main.py як фон
nohup python main.py > api.log 2>&1 &
API_PID=$!

echo ">>> Starting Cimeika UI..."
cd ui
# Запускаємо Vite у режимі preview (легше для планшета) на порту 8010
nohup npm run preview -- --port 8010 --host > ui.log 2>&1 &
UI_PID=$!

echo "=================================================="
echo "✅ SYSTEM ONLINE"
echo "📡 API: http://localhost:8000 (PID: $API_PID)"
echo "🖥️ UI:  http://localhost:8010 (PID: $UI_PID)"
echo "=================================================="
echo "Логи пишуться в api.log та ui/ui.log"
