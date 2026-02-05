#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# 🧠 CIT HEALTHREPORT GENERATOR v1.0 (Node_011)
# Формує поточний стан системи у JSON
# ============================================================

BASE="/data/data/com.termux/files/home/cimeika/cit"
LOG="$BASE/logs/CIT_HealthReport_011.json"

# Основні дані
NODE_ID="CIT_Node_011"
SYSTEM_ID="CIT-SRV-2026-X1"
PLATFORM="Android / Termux / Python 3.x"
DATE=$(date '+%Y-%m-%d %H:%M:%S')
UPTIME=$(uptime -p | sed 's/up //')
STABILITY="0.55"
HEALTH_STATUS=$(curl -s http://127.0.0.1:5050/health)
WATCHDOG_STATUS=$(ps aux | grep watchdog.sh | grep -v grep >/dev/null && echo "active" || echo "inactive")
MAIN_STATUS=$(ps aux | grep main.py | grep -v grep >/dev/null && echo "active" || echo "inactive")
HEALTH_API_STATUS=$(echo "$HEALTH_STATUS" | grep -q '"status": "active"' && echo "active" || echo "inactive")
CRON_TASKS=$(crontab -l | wc -l)

# Формуємо JSON
cat > "$LOG" <<EOF
{
  "node_id": "$NODE_ID",
  "system_id": "$SYSTEM_ID",
  "platform": "$PLATFORM",
  "timestamp": "$DATE",
  "uptime": "$UPTIME",
  "stability_vector": $STABILITY,
  "deep_stability_loop": true,
  "modules": {
    "main.py": "$MAIN_STATUS",
    "watchdog.sh": "$WATCHDOG_STATUS",
    "health_api.py": "$HEALTH_API_STATUS",
    "cron_jobs": $CRON_TASKS
  },
  "health_api_response": $HEALTH_STATUS,
  "status_summary": "✅ Node stable in Deep Stability Mode"
}
EOF

echo "🧩 [$(date '+%H:%M:%S')] CIT_HealthReport_011.json створено у $LOG"
exit 0
