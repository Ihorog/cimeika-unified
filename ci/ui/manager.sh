#!/bin/bash
# Cimeika CIT Process Manager
# Usage: ./manager.sh [start|stop|restart|logs|status]

CIT_DIR="/data/data/com.termux/files/home/cimeika/cit"
API_PORT=8000
UI_PORT=8010

function check_status() {
    echo "--- STATUS ---"
    if pgrep -f "python main.py" > /dev/null; then
        echo "✅ API: ONLINE (PID $(pgrep -f "python main.py"))"
    else
        echo "🔴 API: OFFLINE"
    fi
    if pgrep -f "vite" > /dev/null; then
        echo "✅ UI:  ONLINE (PID $(pgrep -f "vite"))"
    else
        echo "🔴 UI:  OFFLINE"
    fi
}

function stop_services() {
    echo ">>> Зупинка сервісів..."
    pkill -f "python main.py"
    pkill -f "vite"
    pkill -f "uvicorn"
    echo "✅ Всі процеси зупинено."
}

function show_logs() {
    echo ">>> Останні 10 рядків логів:"
    echo "--- API LOG ---"
    tail -n 10 "$CIT_DIR/api.log" 2>/dev/null
    echo "--- UI LOG ---"
    tail -n 10 "$CIT_DIR/ui/ui.log" 2>/dev/null
}

function start_services() {
    stop_services
    echo ">>> Запуск Cimeika CIT..."
    cd "$CIT_DIR" || exit
    source venv/bin/activate
    
    nohup python main.py > api.log 2>&1 &
    echo "✅ API запущено (Port $API_PORT)"
    
    cd ui || exit
    nohup npm run preview -- --port $UI_PORT --host > ui.log 2>&1 &
    echo "✅ UI запущено (Port $UI_PORT)"
    
    echo "⏳ Очікування ініціалізації..."
    sleep 3
    check_status
}

case "$1" in
    start)   start_services ;;
    stop)    stop_services ;;
    restart) start_services ;;
    status)  check_status ;;
    logs)    show_logs ;;
    *)       echo "Usage: ./manager.sh {start|stop|restart|status|logs}" ;;
esac
