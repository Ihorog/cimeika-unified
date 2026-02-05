#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# 🩺 CI HEALTH DAEMON
# Окремий процес для Health API (порт 5050)
# ============================================================
BASE="/data/data/com.termux/files/home/cimeika/cit"
DAEMON="$BASE/health_api.py"
LOG="$BASE/logs/watchdog.log"

echo "🧩 [$(date '+%H:%M:%S')] Перевірка Health Daemon..." >> $LOG

# --- створення або оновлення health_api.py ---
cat > "$DAEMON" <<'EOF'
#!/data/data/com.termux/files/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "active",
                "stability": 0.55,
                "timestamp": time.strftime("%H:%M:%S")
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('127.0.0.1', 5050), HealthHandler)
print("✅ Health Daemon active on port 5050")
server.serve_forever()
EOF

chmod +x "$DAEMON"

# --- зупиняємо старі екземпляри ---
pkill -f health_api.py
sleep 1

# --- запускаємо новий ---
nohup python3 "$DAEMON" >/dev/null 2>&1 &
sleep 3

# --- перевіряємо відповідь ---
RESPONSE=$(curl -s http://127.0.0.1:5050/health)
if echo "$RESPONSE" | grep -q '"status"'; then
    echo "✅ Health Daemon активний: $RESPONSE" >> $LOG
else
    echo "❌ Health Daemon не відповідає!" >> $LOG
fi

echo "🏁 [$(date '+%H:%M:%S')] Завершено запуск Health Daemon." >> $LOG
exit 0
