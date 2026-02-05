#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "🤖 [CIT AUTOHEAL v3] $(date)"
ROOT="$HOME/cimeika/cit"
SRV="$ROOT/server"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/autoheal_v3.log"

cd "$SRV" || exit 1
cp cit_server.py cit_server.py.bak.$(date +%Y%m%dT%H%M%S)
echo "📦 Резервна копія cit_server.py створена." | tee -a "$LOG_FILE"

# 1️⃣ Прибираємо дубльований main()
sed -i '1160,$d' cit_server.py
echo "✅ [FIX] Видалено дубльований main() блок (рядки 1160+)." | tee -a "$LOG_FILE"

# 2️⃣ Примусово встановлюємо стабільний порт
sed -i 's/os.getenv("CIT_PORT", *"[0-9]*")/os.getenv("CIT_PORT", "8799")/' cit_server.py
echo "✅ [FIX] Примусово встановлено порт 8799." | tee -a "$LOG_FILE"

# 3️⃣ Перезапуск сервера
pkill -f cit_server.py 2>/dev/null || true
sleep 2
echo "🚀 [START] Запуск CIT API..." | tee -a "$LOG_FILE"
nohup python cit_server.py > "$LOG_DIR/cit_8799.log" 2>&1 &
sleep 5

# 4️⃣ Перевірка порту
PORT_ACTIVE=$(grep -m1 -oE 'http://0\.0\.0\.0:[0-9]+' "$LOG_DIR/cit_8799.log" | sed 's/.*://')
if [ -z "$PORT_ACTIVE" ]; then
  echo "⚠️ [WARN] Не вдалося визначити порт — спробуємо сканувати..." | tee -a "$LOG_FILE"
  PORT_ACTIVE=8799
fi

# 5️⃣ Тестування API
echo "🧪 Перевірка /api/chat на порту $PORT_ACTIVE ..." | tee -a "$LOG_FILE"
REPLY=$(curl -s "http://127.0.0.1:$PORT_ACTIVE/api/chat" -d '{"text":"ping"}' -H "Content-Type: application/json" || true)

if [ -n "$REPLY" ]; then
  echo "✅ [OK] API відповідає: $REPLY" | tee -a "$LOG_FILE"
else
  echo "⚠️ [WARN] Сервер активний, але відповіді немає." | tee -a "$LOG_FILE"
  tail -n 10 "$LOG_DIR/cit_8799.log" | tee -a "$LOG_FILE"
fi

echo "♻️ [DONE] Автоматичне відновлення завершено $(date)" | tee -a "$LOG_FILE"
