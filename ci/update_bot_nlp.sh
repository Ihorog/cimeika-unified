#!/bin/bash
PROJECT_DIR="$HOME/cimeika/cit"
BOT_FILE="$PROJECT_DIR/core/telegram_bot.py"

# Оновлення файлу з посиленим NLP-промптом
cat > "$BOT_FILE" << 'INNER_EOF'
import telebot
import os
import requests
import json
import re
from pathlib import Path
from core.indexer import index_file
from core.database import get_db_connection
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

def save_event_to_db(event_data):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO calendar_events (title, event_date, event_time, description, created_at) VALUES (?, ?, ?, ?, ?)",
        (event_data['title'], event_data['date'], event_data['time'], event_data.get('desc', ''), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: str(message.chat.id) == ALLOWED_ID)
def handle_smart_message(message):
    text = message.text.lower()
    
    if any(word in text for word in ["запиши", "план", "вистава", "о ", "в ", "репетиція"]):
        now = datetime.now()
        prompt = f"""
        Аналізуй текст: "{message.text}"
        Сьогоднішня дата: {now.strftime('%Y-%m-%d, %A')}
        Витягни дані для календаря. Поверни ТІЛЬКИ чистий JSON без тексту навколо:
        {{"title": "назва", "date": "YYYY-MM-DD", "time": "HH:MM", "desc": "деталі"}}
        Важливо: Якщо дата 'завтра' - це {now.year}-{now.month}-{now.day+1}. Не повертай шаблони YYYY-MM-DD.
        """
        try:
            api_url = "http://localhost:8792/api/chat"
            ai_resp = requests.post(api_url, json={"message": prompt}).json()
            match = re.search(r'\{.*\}', ai_resp['reply'], re.DOTALL)
            if match:
                event_data = json.loads(match.group())
                save_event_to_db(event_data)
                bot.reply_to(message, f"📅 **Ci_Calendar оновлено!**\n📌 {event_data['title']}\n⏰ {event_data['date']} о {event_data['time']}")
                return
        except Exception as e:
            print(f"Calendar error: {e}")

    # Звичайний чат
    try:
        api_url = "http://localhost:8792/api/chat"
        resp = requests.post(api_url, json={"message": message.text})
        bot.reply_to(message, resp.json().get("reply", "Помилка"))
    except Exception as e:
        bot.reply_to(message, f"❌ {e}")

@bot.message_handler(content_types=['document', 'photo'])
def handle_docs(message):
    if str(message.chat.id) != ALLOWED_ID: return
    try:
        file_info = bot.get_file(message.document.file_id if message.document else message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = message.document.file_name if message.document else f"img_{file_info.file_id}.jpg"
        path = Path("storage/vault") / filename
        with open(path, 'wb') as f: f.write(downloaded_file)
        index_file(filename, downloaded_file)
        bot.reply_to(message, f"✅ Файл '{filename}' проіндексовано!")
    except Exception as e:
        bot.reply_to(message, f"❌ {e}")

def run_bot():
    if TOKEN and ALLOWED_ID:
        print("🤖 Telegram Bot v2.5.1 (NLP Fixed) запрацював...")
        bot.infinity_polling()
INNER_EOF

# Перезапуск системи
pkill -9 python
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)
nohup python3 "$PROJECT_DIR/main.py" > /dev/null 2>&1 &
echo "✅ Оновлення завершено. Система перезапущена."
