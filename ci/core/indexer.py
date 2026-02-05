import json
from core.database import get_db_connection
from core.openai_client import chat
from datetime import datetime, timezone

def index_file(filename, content_bytes):
    # Беремо початок файлу для аналізу (текстовий зріз)
    sample = content_bytes[:3000].decode(errors='ignore')
    
    # Запит до AI для створення конспекту
    prompt = f"Ти — системний аналітик. Зроби дуже короткий (1-2 речення) опис змісту цього файлу '{filename}':\n\n{sample}"
    response = chat(prompt)
    summary = response.get("reply", "Опис відсутній")

    conn = get_db_connection()
    conn.execute(
        "INSERT OR REPLACE INTO file_index (filename, content_summary, file_type, indexed_at) VALUES (?, ?, ?, ?)",
        (filename, summary, filename.split('.')[-1], datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()
    return summary
