#!/data/data/com.termux/files/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "active",
                "stability": 0.55,
                "timestamp": time.strftime("%H:%M:%S")
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('127.0.0.1', 5050), HealthHandler)
print("✅ Health Daemon active on port 5050")
server.serve_forever()
