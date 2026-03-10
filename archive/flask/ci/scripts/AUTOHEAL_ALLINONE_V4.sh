#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$HOME/cimeika/cit"
SRV="$ROOT/server"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/autoheal_v4.log"

echo "🤖 [CIT AUTOHEAL v4] $(date)" | tee -a "$LOG_FILE"

cd "$SRV" || exit 1
cp cit_server.py cit_server.py.bak.$(date +%Y%m%dT%H%M%S)
echo "📦 Резервна копія cit_server.py створена." | tee -a "$LOG_FILE"

# 1️⃣ Знайдемо усі процеси python, що слухають 87xx
echo "🧹 [CLEANUP] Пошук і завершення завислих процесів..." | tee -a "$LOG_FILE"
for pid in $(ps -A | grep python | awk '{print $1}'); do
  if cat /proc/$pid/cmdline 2>/dev/null | grep -q "cit_server.py"; then
    echo "🔻 Kill CIT process PID=$pid" | tee -a "$LOG_FILE"
    kill -9 "$pid" 2>/dev/null || true
  fi
done
sleep 2

# 2️⃣ Знайти вільний порт
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

echo "✅ [OK] Вільний порт: $PORT_FREE" | tee -a "$LOG_FILE"

# 3️⃣ Оновлення cit_server.py
sed -i "s/os.getenv(\"CIT_PORT\", *\"[0-9]*\")/os.getenv(\"CIT_PORT\", \"$PORT_FREE\")/" cit_server.py
echo "🧩 [PATCH] Оновлено порт до $PORT_FREE" | tee -a "$LOG_FILE"

# 4️⃣ Запуск сервера
echo "🚀 [START] Запуск CIT API..." | tee -a "$LOG_FILE"
nohup python cit_server.py > "$LOG_DIR/cit_${PORT_FREE}.log" 2>&1 &
sleep 5

# 5️⃣ Перевірка запуску
if ! grep -q "listening on" "$LOG_DIR/cit_${PORT_FREE}.log"; then
  echo "⚠️ [WARN] Сервер ще не вивів 'listening on' — перевіряю порти..." | tee -a "$LOG_FILE"
  ss -tulpen 2>/dev/null | grep ":$PORT_FREE" | tee -a "$LOG_FILE" || true
fi

# 6️⃣ Тестування API
echo "🧪 [TEST] /api/chat на порту $PORT_FREE..." | tee -a "$LOG_FILE"
REPLY=$(curl -s "http://127.0.0.1:$PORT_FREE/api/chat" -d '{"text":"ping"}' -H "Content-Type: application/json" || true)

if [ -n "$REPLY" ]; then
  echo "✅ [OK] API відповідає: $REPLY" | tee -a "$LOG_FILE"
else
  echo "⚠️ [WARN] Відповіді /api/chat немає — можливо, handler ще ініціалізується." | tee -a "$LOG_FILE"
fi

echo "♻️ [DONE] Автоматичне відновлення завершено $(date)" | tee -a "$LOG_FILE"
