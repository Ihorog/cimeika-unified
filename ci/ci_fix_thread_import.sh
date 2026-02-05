#!/data/data/com.termux/files/usr/bin/bash
# ===========================================================
# 🧠 CI FIX THREAD IMPORT
# Додає відсутній import threading і json, якщо їх немає
# ===========================================================
BASE="/data/data/com.termux/files/home/cimeika/cit"
MAIN="$BASE/main.py"
LOG="$BASE/logs/watchdog.log"

echo "🧩 [$(date '+%H:%M:%S')] Початок перевірки імпортів..." >> $LOG

# Перевірка чи існує рядок import threading
if ! grep -q "import threading" "$MAIN"; then
    echo "⚙️ Додаю 'import threading, json' у верхню частину main.py" >> $LOG
    sed -i '1aimport threading, json' "$MAIN"
else
    echo "ℹ️ Імпорт threading вже присутній." >> $LOG
fi

# Перезапуск
pkill -f main.py
sleep 2
nohup python3 "$MAIN" >/dev/null 2>&1 &
sleep 4

RESPONSE=$(curl -s http://127.0.0.1:5050/health)
if echo "$RESPONSE" | grep -q '"status"'; then
    echo "✅ Health API активний: $RESPONSE" >> $LOG
else
    echo "❌ Health API досі не відповідає." >> $LOG
fi

echo "🏁 Завершено перевірку імпортів." >> $LOG
exit 0
