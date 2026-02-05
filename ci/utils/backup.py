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
