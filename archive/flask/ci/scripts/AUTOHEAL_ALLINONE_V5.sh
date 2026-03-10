#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$HOME/cimeika/cit"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/autoheal_v5.log"

echo "🤖 [CIT AUTOHEAL v5] $(date)" | tee -a "$LOG_FILE"

# 1️⃣ Очистка старих процесів
echo "🧹 [CLEANUP] Завершення завислих процесів..." | tee -a "$LOG_FILE"
pkill -f cit_server.py 2>/dev/null || true
pkill -f flask 2>/dev/null || true
sleep 2

# 2️⃣ Знаходимо вільний порт
PORT_FREE=""
for p in $(seq 8790 8810); do
  if ! ss -tulpen 2>/dev/null | grep -q ":$p"; then
    PORT_FREE=$p
    break
  fi
done

if [ -z "${PORT_FREE:-}" ]; then
  echo "❌ [ERROR] Немає вільних портів (8790–8810)." | tee -a "$LOG_FILE"
  exit 1
fi

echo "✅ [OK] Вільний порт знайдено: $PORT_FREE" | tee -a "$LOG_FILE"

# 3️⃣ Запуск CIT, якщо можливо
cd "$ROOT/server" || exit 1
nohup python cit_server.py > "$LOG_DIR/cit_${PORT_FREE}.log" 2>&1 &
sleep 5

if grep -q "listening on" "$LOG_DIR/cit_${PORT_FREE}.log"; then
  echo "✅ [OK] CIT API працює на $PORT_FREE" | tee -a "$LOG_FILE"
else
  echo "⚠️ [WARN] CIT не запустився. Створюю fallback Flask сервер..." | tee -a "$LOG_FILE"

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

  nohup python "$ROOT/server/fallback_api.py" > "$LOG_DIR/fallback_${PORT_FREE}.log" 2>&1 &
  sleep 3
  echo "✅ [OK] Flask fallback сервер запущено на порту $PORT_FREE" | tee -a "$LOG_FILE"
fi

# 4️⃣ Тест запиту
REPLY=$(curl -s "http://127.0.0.1:$PORT_FREE/api/chat" -d '{"text":"ping"}' -H "Content-Type: application/json" || true)

if [ -n "$REPLY" ]; then
  echo "✅ [OK] API відповідає: $REPLY" | tee -a "$LOG_FILE"
else
  echo "⚠️ [WARN] Немає відповіді від API." | tee -a "$LOG_FILE"
fi

echo "♻️ [DONE] Автоматичне відновлення завершено $(date)" | tee -a "$LOG_FILE"
