import json
import sqlite3
import os
from pathlib import Path

def get_system_status():
    db_path = Path(__file__).parent.parent / "cit_system.db"
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Отримуємо дані
        events = conn.execute("SELECT title, event_date FROM calendar_events ORDER BY id DESC LIMIT 5").fetchall()
        files_count = conn.execute("SELECT COUNT(*) FROM file_index").fetchone()[0]
        conn.close()
        
        # Математична модель вектора (0.0 - 1.0)
        vector_state = round(min(1.0, (len(events) * 0.1) + (files_count * 0.02)), 2)
        
        return {
            "vector": vector_state,
            "events": [dict(e) for e in events],
            "files": files_count,
            "status": "active"
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}
