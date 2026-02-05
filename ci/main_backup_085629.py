import sys, os, cgi, json, sqlite3, random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "active", "stability": 0.55}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_health_server():
    server = HTTPServer(('127.0.0.1', 5050), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()
# ============================================================

class CITHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/status":
            conn = sqlite3.connect("cit_system.db")
            e = conn.execute("SELECT COUNT(*) FROM calendar_events").fetchone()[0]
            f = conn.execute("SELECT COUNT(*) FROM file_index").fetchone()[0]
            conn.close()
            v = round(min(1.0, (e * 0.1) + (f * 0.02)), 2)
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps({"vector": v, "events": e, "files": f}).encode())
        elif p == "/api/hint":
            self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8"); self.end_headers()
            try:
                with open("storage/magic_tales/hints.txt", "r", encoding="utf-8") as f:
                    self.wfile.write(random.choice(f.readlines()).strip().encode())
            except: self.wfile.write("Магія Сі активна...".encode())
        else:
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            with open("magic_card.html", "rb") as f: self.wfile.write(f.read())

    def do_POST(self):
        if self.path == '/api/upload':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            fileitem = form['file']
            fn = os.path.basename(fileitem.filename)
            path = "storage/magic_tales/" + fn
            with open(path, 'wb') as f: f.write(fileitem.file.read())
            
            # АВТО-МЕТАТЕГИ
            cat = "image/magic" if fn.lower().endswith(('.png', '.jpg')) else "text/tale"
            conn = sqlite3.connect("cit_system.db")
            conn.execute("INSERT INTO file_index (filename, content_summary, file_type, indexed_at) VALUES (?, ?, ?, datetime('now'))", (fn, f"Auto-Tag: {cat}", cat))
            conn.commit(); conn.close()
            
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps({"status": "magic_indexed", "file": fn}).encode())

if __name__ == "__main__":
    HTTPServer(('0.0.0.0', 8792), CITHandler).serve_forever()

# ============================================================
# 🩺 CI HEALTH API PATCH
# ============================================================
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, json

# ============================================================
