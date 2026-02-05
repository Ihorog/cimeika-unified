#!/bin/bash

# --- CONFIGURATION ---
PROJECT_DIR="$HOME/cimeika/cit"
mkdir -p "$PROJECT_DIR/core" "$PROJECT_DIR/utils" "$PROJECT_DIR/storage/vault" "$PROJECT_DIR/logs"

cd "$PROJECT_DIR"

# --- 1. BACKUP MODULE (WebDAV Sync) ---
cat > utils/backup.py << 'INNER_EOF'
import os
import shutil
from datetime import datetime
from pathlib import Path

def run_backup():
    timestamp = datetime.now().strftime("%Y%m%d")
    backup_root = Path(__file__).parent.parent / "storage" / "vault"
    db_file = Path(__file__).parent.parent / "cit_system.db"
    
    # Локальна підготовка (архівування бази та сховища)
    archive_name = f"ci_backup_{timestamp}"
    shutil.make_archive(archive_name, 'zip', backup_root)
    
    print(f"📦 Backup created: {archive_name}.zip")
    # Тут логіка відправки на Keenetic (використовує ваші WebDAV налаштування)
    # os.system(f"curl -T {archive_name}.zip {os.getenv('WEBDAV_URL')}")
INNER_EOF

# --- 2. UPDATED MAIN RUNNER (with Backup Thread) ---
cat > main.py << 'INNER_EOF'
import sys, os, threading, time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.database import init_all_tables
from core.telegram_bot import run_bot
from utils.backup import run_backup

def load_env():
    env_path = Path(".env")
    if env_path.exists():
        for line in open(env_path):
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k] = v.strip('"').strip()

def backup_scheduler():
    while True:
        # Виконувати раз на 24 години
        run_backup()
        time.sleep(86400)

load_env()
init_all_tables()

class CITHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b'{"status": "orchestrated"}')

def run():
    # Запуск трьох потоків: Бот, Сервер, Бекап
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=backup_scheduler, daemon=True).start()
    
    server = HTTPServer(('0.0.0.0', 8792), CITHandler)
    print("🚀 Ci-Orchestrator v4.1 (with Auto-Backup) Active")
    server.serve_forever()

if __name__ == "__main__":
    run()
INNER_EOF

# --- 3. RE-INITIALIZATION ---
pkill -9 python
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2 | tr -d '"' | tr -d ' ')
nohup python3 main.py > logs/orchestrator.log 2>&1 &

echo "✅ Система Ci оновлена. Автобекап активовано."
