import json
from core.database import get_db_connection
from datetime import datetime

def register_calendar_routes(router):
    @router.route("/api/calendar/add")
    def add_event(h):
        # Логіка додавання події через API
        pass

    @router.route("/api/calendar/list")
    def list_events(h):
        conn = get_db_connection()
        events = conn.execute("SELECT * FROM calendar_events ORDER BY event_date ASC").fetchall()
        conn.close()
        
        h.send_response(200)
        h.send_header("Content-Type", "application/json")
        h.end_headers()
        h.wfile.write(json.dumps([dict(ix) for ix in events]).encode())
