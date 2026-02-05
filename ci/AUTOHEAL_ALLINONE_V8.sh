#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$HOME/cimeika/cit"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/autoheal_v8.log"
FALLBACK="$ROOT/server/fallback_api.py"

echo "🤖 [CIT AUTOHEAL v8] $(date)" | tee -a "$LOG_FILE"

# 🔧 Перевірка Flask
if ! python -c "import flask" 2>/dev/null; then
  echo "🧩 Flask не знайдено — встановлюю..." | tee -a "$LOG_FILE"
  pip install -q flask flask_cors
fi

# 🔁 Головний безкінечний цикл моніторингу
while true; do
  NOW=$(date)
  echo "🩺 [CHECK] $NOW" | tee -a "$LOG_FILE"

  # Перевірка активності порту
  PORT_ACTIVE=$(lsof -i -P -n | grep "python" | grep -oE ':[0-9]+' | sed 's/://g' | head -n1 || true)

  if [ -z "$PORT_ACTIVE" ]; then
    echo "⚠️ [WARN] Немає активного сервера — шукаю вільний порт..." | tee -a "$LOG_FILE"
    for p in $(seq 8790 8810); do
      if ! lsof -i :$p >/dev/null 2>&1; then
        PORT=$p
        break
      fi
    done
    PORT=${PORT:-8800}
    echo "✅ [OK] Вільний порт знайдено: $PORT" | tee -a "$LOG_FILE"

    # Запуск Flask fallback
    cat > "$FALLBACK" <<'PY'
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

    echo "🚀 [START] Запуск Flask fallback на порту $PORT ..." | tee -a "$LOG_FILE"
    CIT_PORT=$PORT nohup python "$FALLBACK" > "$LOG_DIR/fallback_${PORT}.log" 2>&1 &
    sleep 5
    PORT_ACTIVE=$PORT
  fi

  # 🔍 Перевірка відповіді API
  REPLY=$(curl -s "http://127.0.0.1:$PORT_ACTIVE/api/chat" \
    -d '{"text":"ping"}' -H "Content-Type: application/json" || true)

  if echo "$REPLY" | grep -q "Echo"; then
    echo "✅ [OK] API відповідає на порту $PORT_ACTIVE." | tee -a "$LOG_FILE"
  else
    echo "❌ [FAIL] API не відповідає — перезапуск..." | tee -a "$LOG_FILE"
    pkill -f fallback_api.py 2>/dev/null || true
    sleep 2
  fi

  echo "⏳ [WAIT] Наступна перевірка через 60 секунд..." | tee -a "$LOG_FILE"
  sleep 60
done

