#!/data/data/com.termux/files/usr/bin/bash
LOG_DIR="/data/data/com.termux/files/home/cimeika/cit/logs"
TMP_FAILCOUNT="/data/data/com.termux/files/home/cimeika/cit/tmp_watchdog_failcount"

# 1️⃣ Перевірка health-endpoint
if curl -s --max-time 5 http://127.0.0.1:5050/health | grep -q '"status":"active"'; then
  echo "[OK] $(date '+%H:%M:%S') Health OK." >> $LOG_DIR/watchdog.log
  echo "0" > $TMP_FAILCOUNT
  exit 0
else
  FAILS=$(cat $TMP_FAILCOUNT 2>/dev/null || echo 0)
  FAILS=$((FAILS+1))
  echo $FAILS > $TMP_FAILCOUNT
  echo "⚠️ $(date '+%H:%M:%S') Health-check failed ($FAILS)." >> $LOG_DIR/watchdog.log
fi

# 2️⃣ Подвійна перевірка перед рестартом
if [ "$(cat $TMP_FAILCOUNT)" -ge 2 ]; then
  echo "⚠️ $(date '+%H:%M:%S') CIT v2.4 Down confirmed. Restarting main.py..." >> $LOG_DIR/watchdog.log
  pkill -f main.py
  nohup python3 /data/data/com.termux/files/home/cimeika/cit/main.py >/dev/null 2>&1 &
  echo "✅ $(date '+%H:%M:%S') System Restored." >> $LOG_DIR/watchdog.log
  echo "0" > $TMP_FAILCOUNT
fi
