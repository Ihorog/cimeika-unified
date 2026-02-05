#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$HOME/cimeika/cit"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/autoheal_v7.log"

echo "🤖 [CIT AUTOHEAL v7] $(date)" | tee -a "$LOG_FILE"

# 1️⃣ Перевірка наявності Flask
if ! python -c "import flask" 2>/dev/null; then
  echo "🧩 Flask не знайдено — встановлюю..." | tee -a "$LOG_FILE"
  pip install -q flask flask_cors || echo "⚠️ pip install flask не вдалося"
fi

# 2️⃣ Завершити старі процеси
pkill -f cit_server.py 2>/dev/null || true
pkill -f fallback_api.py 2>/dev/null || true
sleep 2

# 3️⃣ Знайти вільний порт без ss/netstat
PORT_FREE=""
for p in $(seq 8790 8810); do
  if ! lsof -i :$p >/dev/null 2>&1; then
    PORT_FREE=$p
    break
  fi
done

PORT=${PORT_FREE:-8800}
echo "✅ [OK] Вільний порт: $PORT" | tee -a "$LOG_FILE"

# 4️⃣ Спроба запустити CIT
cd "$ROOT/server" || exit 1
nohup python cit_server.py > "$LOG_DIR/cit_${PORT}.log" 2>&1 &
sleep 5

if grep -q "listening on" "$LOG_DIR/cit_${PORT}.log"; then
  echo "✅ [OK] CIT API запущено на порту $PORT" | tee -a "$LOG_FILE"
else
  echo "⚠️ [WARN] CIT не піднявся — створюю Flask fallback..." | tee -a "$LOG_FILE"

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
  sleep 4
fi

# 5️⃣ Тестуємо відповіді
REPLY=$(curl -s "http://127.0.0.1:$PORT/api/chat" -d '{"text":"ping"}' -H "Content-Type: application/json" || true)

if echo "$REPLY" | grep -q "Echo"; then
  echo "✅ [OK] API відповідає: $REPLY" | tee -a "$LOG_FILE"
else
  echo "❌ [FAIL] API не відповідає навіть через Flask. Перевір лог: $LOG_DIR/fallback_${PORT}.log" | tee -a "$LOG_FILE"
  tail -n 20 "$LOG_DIR/fallback_${PORT}.log" | tee -a "$LOG_FILE"
fi

echo "♻️ [DONE] $(date)" | tee -a "$LOG_FILE"
