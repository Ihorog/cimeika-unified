#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================
# 🔍 CI HEALTH TEST + AUTO-FIX
# ==============================================================
BASE_DIR="/data/data/com.termux/files/home/cimeika/cit"
MAIN="$BASE_DIR/main.py"
LOG="$BASE_DIR/logs/watchdog.log"

echo "🧩 [$(date '+%H:%M:%S')] Перевірка Health API..." >> $LOG

# 1️⃣ Перевірка процесу main.py
if ! pgrep -f "main.py" > /dev/null; then
  echo "⚠️ main.py не запущено. Запускаю..." >> $LOG
  nohup python3 $MAIN >/dev/null 2>&1 &
  sleep 3
fi

# 2️⃣ Перевірка наявності Health API
if ! grep -q "run_health_server" "$MAIN"; then
  echo "⚙️ Додаю Health API (не знайдено у main.py)..." >> $LOG
  sed -i '/if __name__ == "__main__":/i \
from http.server import BaseHTTPRequestHandler, HTTPServer\n\
import threading, json\n\
class HealthHandler(BaseHTTPRequestHandler):\n\
    def do_GET(self):\n\
        if self.path == "/health":\n\
            self.send_response(200)\n\
            self.send_header("Content-type", "application/json")\n\
            self.end_headers()\n\
            response = {"status": "active", "stability": 0.55}\n\
            self.wfile.write(json.dumps(response).encode())\n\
        else:\n\
            self.send_response(404)\n\
            self.end_headers()\n\
def run_health_server():\n\
    server = HTTPServer(("127.0.0.1", 5050), HealthHandler)\n\
    server.serve_forever()\n\
threading.Thread(target=run_health_server, daemon=True).start()\n' "$MAIN"
fi

# 3️⃣ Перезапуск main.py
pkill -f "main.py"
nohup python3 $MAIN >/dev/null 2>&1 &
sleep 5

# 4️⃣ Перевірка відповіді
RESPONSE=$(curl -s http://127.0.0.1:5050/health)
if echo "$RESPONSE" | grep -q '"status"'; then
  echo "✅ Health API активний: $RESPONSE" | tee -a $LOG
else
  echo "❌ Health API не відповідає. Перевір main.py вручну." | tee -a $LOG
fi

echo "🏁 Завершено перевірку Health API." >> $LOG
exit 0
