#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$HOME/cimeika/cit"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/autoheal_watchdog.log"

echo "🧠 [CIT AUTOHEAL v6] $(date)" | tee -a "$LOG_FILE"

function start_fallback() {
  PORT=${1:-8800}
  echo "🧩 [FALLBACK] Запуск Flask API на порту $PORT ..." | tee -a "$LOG_FILE"
  cat > "$ROOT/server/fallback_api.py" <<'PY'
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    text = data.get("text", "")
    return jsonify({"ok": True, "reply": f"Echo: {text}"})

if __name__ == "__main__":
    port = int(os.getenv("CIT_PORT", "8800"))
    print(f"[FALLBACK] Flask listening on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
PY
  nohup python "$ROOT/server/fallback_api.py" > "$LOG_DIR/fallback_${PORT}.log" 2>&1 &
  sleep 3
}

while true; do
  echo "🩺 [CHECK] $(date)" | tee -a "$LOG_FILE"

  # Знайдемо активний порт або виберемо вільний
  PORT_FREE=""
  for p in $(seq 8790 8810); do
    if ! ss -tulpen 2>/dev/null | grep -q ":$p"; then
      PORT_FREE=$p
      break
    fi
  done
  PORT=${PORT_FREE:-8790}

  # Перевірка CIT
  if ps -A | grep -q cit_server.py; then
    echo "✅ [OK] CIT процес активний." | tee -a "$LOG_FILE"
  else
    echo "⚠️ [WARN] CIT не запущено, пробую перезапустити..." | tee -a "$LOG_FILE"
    pkill -f flask 2>/dev/null || true
    nohup python "$ROOT/server/cit_server.py" > "$LOG_DIR/cit_${PORT}.log" 2>&1 &
    sleep 5
    if ! grep -q "listening on" "$LOG_DIR/cit_${PORT}.log"; then
      echo "❌ CIT не піднявся — запускаю Flask fallback..." | tee -a "$LOG_FILE"
      start_fallback "$PORT"
    fi
  fi

  # Перевірка API
  REPLY=$(curl -s "http://127.0.0.1:$PORT/api/chat" -d '{"text":"ping"}' -H "Content-Type: application/json" || true)
  if echo "$REPLY" | grep -q "Echo"; then
    echo "✅ [OK] API відповідає: $REPLY" | tee -a "$LOG_FILE"
  else
    echo "⚠️ [WARN] API не відповідає — перевіряю повторно..." | tee -a "$LOG_FILE"
    sleep 5
    REPLY=$(curl -s "http://127.0.0.1:$PORT/api/chat" -d '{"text":"ping"}' -H "Content-Type: application/json" || true)
    if [ -z "$REPLY" ]; then
      echo "❌ [FAIL] API неактивне. Перезапуск..." | tee -a "$LOG_FILE"
      pkill -f cit_server.py 2>/dev/null || true
      pkill -f flask 2>/dev/null || true
      start_fallback "$PORT"
    fi
  fi

  echo "⏳ [WAIT] Наступна перевірка через 60 секунд..." | tee -a "$LOG_FILE"
  sleep 60
done
