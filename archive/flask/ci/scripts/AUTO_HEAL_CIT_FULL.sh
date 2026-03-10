ROOT="$HOME/cimeika/cit"
#!/data/data/com.termux/files/usr/bin/bash
# === AUTO_HEAL_CIT_FULL.sh ===
# Повна автоматизація перевірки, оновлення і запуску CIT системи

set -euo pipefail
ROOT="/data/data/com.termux/files/home/cimeika/cit"
LOG_DIR="$ROOT/logs"
LOG_FILE="$LOG_DIR/autoheal.log"
PORT_API=8790
PORT_CHAT=8794

mkdir -p "$LOG_DIR"
cd "$ROOT" || exit 1

echo "🩺 [CIT AUTOHEAL] Старт $(date)" | tee -a "$LOG_FILE"

# 1️⃣ Синхронізація Git
echo "📡 [SYNC] Оновлення репозиторію..." | tee -a "$LOG_FILE"
git fetch origin main || true
git rebase origin/main || git reset --hard origin/main
git pull --rebase origin main || true

# 2️⃣ Локальний autosync
if [ -x "$ROOT/ci_sync.sh" ]; then
  echo "🔁 [SYNC] Виконую ci_sync.sh" | tee -a "$LOG_FILE"
  "$ROOT/ci_sync.sh" >>"$LOG_FILE" 2>&1 || true
fi

# 3️⃣ Перевірка активності порту 8790 / 8794
echo "🔍 [CHECK] Стан серверів..." | tee -a "$LOG_FILE"
  if [ -x "$ROOT/START_UIV2_AND_API.sh" ]; then
    echo "♻️ [RESTART] Виконую START_UIV2_AND_API.sh..." | tee -a "$LOG_FILE"
    "$ROOT/START_UIV2_AND_API.sh" >>"$LOG_FILE" 2>&1 || true
  elif [ -x "$ROOT/RESTART_API_AND_VERIFY_V1.sh" ]; then
    echo "♻️ [FALLBACK] Виконую RESTART_API_AND_VERIFY_V1.sh..." | tee -a "$LOG_FILE"
    "$ROOT/RESTART_API_AND_VERIFY_V1.sh" >>"$LOG_FILE" 2>&1 || true
  else
    echo "❌ [ERROR] Не знайдено запускових скриптів (UI/API)." | tee -a "$LOG_FILE"
  fi

if lsof -i :$PORT_CHAT >/dev/null 2>&1; then
  echo "✅ [RUNNING] Chat порт $PORT_CHAT активний" | tee -a "$LOG_FILE"
else
  echo "⚠️ [DOWN] Chat порт $PORT_CHAT неактивний, виконую перезапуск..." | tee -a "$LOG_FILE"

  # 4️⃣ Очищення портів
  if [ -x "$ROOT/RESTART_CLEAN_PORTS_V2.sh" ]; then
    "$ROOT/RESTART_CLEAN_PORTS_V2.sh" >>"$LOG_FILE" 2>&1 || true
  fi

  # 5️⃣ Рестарт API + UI
  if [ -x "$ROOT/START_UIV2_AND_API.sh" ]; then
    echo "♻️ [RESTART] Запуск CIT API та UI..." | tee -a "$LOG_FILE"
    "$ROOT/START_UIV2_AND_API.sh" >>"$LOG_FILE" 2>&1 || true
  else
    echo "❌ [ERROR] Не знайдено START_UIV2_AND_API.sh" | tee -a "$LOG_FILE"
  fi
fi

# 6️⃣ Тест-запит після рестарту
sleep 5
echo "🧪 [TEST] Перевірка /api/chat ..." | tee -a "$LOG_FILE"
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:$PORT_CHAT/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"ping"}' >>"$LOG_FILE" 2>&1 || echo "ERR" >>"$LOG_FILE"

# 7️⃣ Завершення
echo "✅ [DONE] Автоматична перевірка завершена $(date)" | tee -a "$LOG_FILE"
echo "📄 Лог: $LOG_FILE"
