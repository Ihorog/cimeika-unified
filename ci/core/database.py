import sqlite3, os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cit_system.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_all_tables():
    conn = get_db_connection()
    # Об'єднана ініціалізація для уникнення ImportError
    conn.execute("CREATE TABLE IF NOT EXISTS file_index (id INTEGER PRIMARY KEY, filename TEXT UNIQUE, content_summary TEXT, indexed_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS calendar_events (id INTEGER PRIMARY KEY, title TEXT, description TEXT, event_date TEXT, event_time TEXT, created_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT, status TEXT, created_at TEXT)")
    conn.commit()
    conn.close()
    print("✅ Database tables initialized.")

# Псевдоніми для зворотної сумісності
init_db = init_all_tables
init_index_table = init_all_tables
init_calendar_table = init_all_tables
