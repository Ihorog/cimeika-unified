#!/data/data/com.termux/files/usr/bin/bash
# ===========================================================
# ⚙️ CI FIX HEALTH ORDER
# Переміщує Health API блок у початок main.py
# ===========================================================
BASE="/data/data/com.termux/files/home/cimeika/cit"
MAIN="$BASE/main.py"
BACK="$BASE/main_backup_fix_$(date +%H%M).py"
LOG="$BASE/logs/watchdog.log"

echo "🧩 Початок фіксу Health API порядку..." >> $LOG

cp "$MAIN" "$BACK"
echo "📦 Резервна копія: $(basename $BACK)" >> $LOG

# Витягуємо блок HealthHandler і вставляємо на початок після імпортів
awk '
BEGIN {block=0}
{
    if ($0 ~ /class HealthHandler/) {block=1}
    if (block==1) print > "tmp_health_block.py"
    if ($0 ~ /# ============================================================/ && block==1) {block=2}
    if (block!=1) print > "tmp_main_rest.py"
}
END {print "✅ Блок Health API виділено"}
' "$MAIN"

# Збираємо новий main.py
(head -n 3 tmp_main_rest.py && cat tmp_health_block.py && tail -n +4 tmp_main_rest.py) > "$MAIN"
rm tmp_health_block.py tmp_main_rest.py

# Перезапуск
pkill -f main.py
sleep 2
nohup python3 "$MAIN" >/dev/null 2>&1 &
echo "♻️ main.py перезапущено після фіксу порядку." >> $LOG
sleep 3

RESPONSE=$(curl -s http://127.0.0.1:5050/health)
if echo "$RESPONSE" | grep -q '"status"'; then
    echo "✅ Health API працює: $RESPONSE" >> $LOG
else
    echo "⚠️ Health API досі не відповідає." >> $LOG
fi
echo "🏁 Фікс завершено." >> $LOG
