#!/bin/bash

# Налаштування v2.4
PORT=8792
PROJECT_DIR="$HOME/cimeika/cit"
LOG_FILE="$PROJECT_DIR/logs/watchdog.log"
MAIN_SCRIPT="main.py"

cd "$PROJECT_DIR"

# Перевірка порту
if ! lsof -i:$PORT > /dev/null; then
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$TIMESTAMP] ⚠️ CIT v2.4 Down. Restarting main.py..." >> "$LOG_FILE"
    
    # Очищення перед запуском
    pkill -9 python
    
    # Запуск нового ядра
    nohup python3 "$MAIN_SCRIPT" > /dev/null 2>&1 &
    
    echo "[$TIMESTAMP] ✅ System Restored." >> "$LOG_FILE"
fi
