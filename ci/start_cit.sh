#!/bin/bash
PROJECT_DIR="$HOME/cimeika/cit"
cd "$PROJECT_DIR"

# Вбиваємо старі процеси
pkill -9 python

# Явно завантажуємо ключ з .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "🔑 Ключ завантажено: ${OPENAI_API_KEY:0:7}..."
else
    echo "❌ Файл .env не знайдено!"
    exit 1
fi

# Запуск
nohup python3 main.py > logs/cit_run.log 2>&1 &

echo "🚀 CIT v2.5.2 запущено. Перевірте бота через 5 секунд."
