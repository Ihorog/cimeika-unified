#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Додаємо шляхи
sys.path.insert(0, os.getcwd())
from core.indexer import index_file

vault_path = Path("storage/vault")
if not vault_path.exists():
    print("❌ Папка vault не знайдена.")
    sys.exit(1)

print("🔄 Починаю масову індексацію файлів у vault...")

for file_path in vault_path.glob("*"):
    if file_path.is_file():
        print(f"📄 Індексація: {file_path.name}")
        with open(file_path, "rb") as f:
            index_file(file_path.name, f.read())

print("✅ Всі файли проіндексовано. Тепер AI знає про ваші документи!")
