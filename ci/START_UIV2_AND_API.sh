#!/data/data/com.termux/files/usr/bin/bash
# === START_UIV2_AND_API.sh (Interactive Auto-Heal Edition) ===
# Запуск CIT UI + API із запитом токена

set -euo pipefail
ROOT="/data/data/com.termux/files/home/cimeika/cit"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

echo "🚀 [CIT START] Ініціалізація CIT UI + API..."
cd "$ROOT" || exit 1

# === 1️⃣ Запит токена, якщо відсутній ===
if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "🔑 Введи свій OpenAI API Token (sk-...):"
  read -r OPENAI_API_KEY
  export OPENAI_API_KEY
  echo "OPENAI_API_KEY=$OPENAI_API_KEY" > "$ROOT/.env"
  echo "✅ Токен збережено у $ROOT/.env"
else
  echo "✅ Використовується існуючий токен із середовища."
fi

# === 2️⃣ Очищення портів ===
if [ -x "$ROOT/RESTART_CLEAN_PORTS_V2.sh" ]; then
  "$ROOT/RESTART_CLEAN_PORTS_V2.sh"
else
  echo "⚠️ [WARN] Не знайдено RESTART_CLEAN_PORTS_V2.sh"
fi

# === 3️⃣ Запуск API ===
if [ -f "$ROOT/server/cit_server.py" ]; then
  echo "▶️ Запуск API (8790)..."
  nohup env OPENAI_API_KEY="$OPENAI_API_KEY" python "$ROOT/server/cit_server.py" \
    >"$LOG_DIR/cit_8790.log" 2>&1 &
else
  echo "⚠️ [WARN] Не знайдено server/cit_server.py"
fi

# === 4️⃣ Запуск UI ===
if [ -d "$ROOT/ui" ]; then
  echo "▶️ Запуск UI (8010)..."
  cd "$ROOT/ui"
  nohup npm run start >"$LOG_DIR/ui_8010.log" 2>&1 &
else
  echo "⚠️ [WARN] Не знайдено директорію UI"
fi

echo "✅ [CIT READY] UI + API запущено."
