import json
from core.openai_client import chat
from core.database import get_db_connection
from utils.json_helpers import read_json

def get_context_from_db(query):
    conn = get_db_connection()
    # Шукаємо збіги в описах файлів
    rows = conn.execute(
        "SELECT filename, content_summary FROM file_index WHERE content_summary LIKE ? OR filename LIKE ? LIMIT 3",
        (f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()
    
    if not rows: return ""
    
    context = "\nКонтекст із локальних файлів:\n"
    for r in rows:
        context += f"- Файл '{r['filename']}': {r['content_summary']}\n"
    return context

def register_api_routes(router):
    @router.route("/api/chat")
    def handle_chat(h):
        data = read_json(h)
        user_msg = data.get("message", "")
        
        # 1. Пошук контексту
        local_context = get_context_from_db(user_msg)
        
        # 2. Формування фінального промпту
        final_prompt = f"{local_context}\n\nПитання користувача: {user_msg}"
        
        result = chat(final_prompt)
        
        h.send_response(200)
        h.send_header("Content-Type", "application/json")
        h.end_headers()
        h.wfile.write(json.dumps(result).encode())
