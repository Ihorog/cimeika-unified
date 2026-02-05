#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# 🧠 CI DISABLE EMBEDDED HEALTH SERVER (v1.2)
# Автоматично видаляє дубльований Health API з main.py
# і відновлює стабільну роботу вузла CIT_Node_011
# ============================================================

BASE="/data/data/com.termux/files/home/cimeika/cit"
MAIN="$BASE/main.py"
LOG="$BASE/logs/watchdog.log"
BACKUP="$BASE/main_backup_$(date +%H%M%S).py"

echo "🧩 [$(date '+%H:%M:%S')] Початок процедури очищення main.py" | tee -a $LOG

# 1️⃣ Перевіряємо, чи main.py існує
if [ ! -f "$MAIN" ]; then
    echo "❌ Файл main.py не знайдено!" | tee -a $LOG
    exit 1
fi

# 2️⃣ Резервна копія
cp "$MAIN" "$BACKUP"
echo "📦 Резервна копія створена: $BACKUP" | tee -a $LOG

# 3️⃣ Видаляємо блок із HealthHandler і run_health_server
sed -i '/class HealthHandler/,/threading.Thread(target=run_health_server/d' "$MAIN"

# 4️⃣ Перевіряємо, чи не залишились зайві імпорти
sed -i '/import threading/d' "$MAIN"

echo "🧹 Вбудований Health API видалено з main.py" | tee -a $LOG

# 5️⃣ Перезапускаємо основний сервер
pkill -f main.py >/dev/null 2>&1
sleep 2
nohup python3 "$MAIN" >/dev/null 2>&1 &
sleep 3

# 6️⃣ Перевірка активності процесів
MAIN_STATUS=$(ps aux | grep main.py | grep -v grep >/dev/null && echo "active" || echo "inactive")
HEALTH_STATUS=$(curl -s http://127.0.0.1:5050/health | grep -q '"status": "active"' && echo "active" || echo "inactive")

# 7️⃣ Підсумок
if [ "$MAIN_STATUS" = "active" ] && [ "$HEALTH_STATUS" = "active" ]; then
    echo "✅ CIT_Node_011 стабільно активний." | tee -a $LOG
    echo "🔗 main.py: OK, health_api.py: OK (порт 5050)" | tee -a $LOG
else
    echo "⚠️ main.py або Health API неактивні, перевір лог." | tee -a $LOG
fi

# 8️⃣ Формуємо новий HealthReport
bash "$BASE/ci_generate_healthreport.sh" >/dev/null 2>&1

echo "🏁 [$(date '+%H:%M:%S')] Процедура завершена успішно." | tee -a $LOG
exit 0
