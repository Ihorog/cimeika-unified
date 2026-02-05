#!/data/data/com.termux/files/usr/bin/bash
# =============================================================
# 🛡️ CI STABILITY PATCH 011→012a
# Мета: виправлення помилкових рестартів main.py у CIT_Node_011
# =============================================================

LOG_DIR="/data/data/com.termux/files/home/cimeika/cit/logs"
WD_FILE="/data/data/com.termux/files/home/cimeika/cit/watchdog.sh"
TMP_FAILCOUNT="/data/data/com.termux/files/home/cimeika/cit/tmp_watchdog_failcount"

echo "🧩 [$(date '+%H:%M:%S')] Запуск ci_stability_patch.sh..." >> $LOG_DIR/watchdog.log

# --- Резервна копія поточного watchdog ---
if [ -f "$WD_FILE" ]; then
  cp "$WD_FILE" "${WD_FILE}.bak"
  echo "📦 Резервна копія watchdog.sh створена." >> $LOG_DIR/watchdog.log
fi

# --- Новий захищений watchdog ---
cat > $WD_FILE <<'EOF'
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
EOF

chmod +x $WD_FILE

# --- Перезапуск Watchdog ---
pkill -f watchdog.sh
nohup bash $WD_FILE >/dev/null 2>&1 &
echo "♻️ Watchdog оновлено та перезапущено." >> $LOG_DIR/watchdog.log

# --- Контрольний запуск ---
sleep 2
if pgrep -f watchdog.sh > /dev/null; then
  echo "✅ [$(date '+%H:%M:%S')] ci_stability_patch застосовано успішно." >> $LOG_DIR/watchdog.log
else
  echo "❌ [$(date '+%H:%M:%S')] Watchdog не запущено!" >> $LOG_DIR/watchdog.log
fi
exit 0
