#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# 🩺 CI HEALTH API PATCH — додає /health endpoint до main.py
# ============================================================

BASE_DIR="/data/data/com.termux/files/home/cimeika/cit"
MAIN_FILE="$BASE_DIR/main.py"
BACKUP_FILE="$BASE_DIR/main_backup_$(date +%H%M).py"
LOG_FILE="$BASE_DIR/logs/watchdog.log"

echo "🧩 [$(date '+%H:%M:%S')] Початок оновлення Health API..." >> $LOG_FILE

# --- 1️⃣ Резервна копія ---
if [ -f "$MAIN_FILE" ]; then
    cp "$MAIN_FILE" "$BACKUP_FILE"
    echo "📦 Резервна копія main.py збережена як $(basename $BACKUP_FILE)" >> $LOG_FILE
else
    echo "❌ Не знайдено main.py, патч перервано." >> $LOG_FILE
    exit 1
fi

# --- 2️⃣ Перевірка наявності блоку Health API ---
if grep -q "def run_health_server" "$MAIN_FILE"; then
    echo "ℹ️ Health API вже додано. Пропуск оновлення." >> $LOG_FILE
else
    echo "⚙️ Додаю Health API..." >> $LOG_FILE

    cat >> "$MAIN_FILE" <<'EOF'

# ============================================================
# 🩺 CI HEALTH API PATCH
# ============================================================
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "active", "stability": 0.55}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_health_server():
    server = HTTPServer(('127.0.0.1', 5050), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()
# ============================================================
EOF
fi

# --- 3️⃣ Перезапуск main.py ---
pkill -f main.py
sleep 2
nohup python3 "$MAIN_FILE" >/dev/null 2>&1 &
echo "♻️ Перезапущено main.py з новим Health API." >> $LOG_FILE

# --- 4️⃣ Перевірка відповіді Health API ---
sleep 5
RESPONSE=$(curl -s http://127.0.0.1:5050/health)
if echo "$RESPONSE" | grep -q '"status":'; then
    echo "✅ Health API активний: $RESPONSE" >> $LOG_FILE
else
    echo "⚠️ Health API не відповідає. Перевір main.py вручну." >> $LOG_FILE
fi

echo "🏁 [$(date '+%H:%M:%S')] Патч завершено." >> $LOG_FILE
exit 0
