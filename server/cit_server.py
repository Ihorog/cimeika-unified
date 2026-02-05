from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)

# === CIMEIKA UI ROUTES (PUBLIC) ===
from flask import send_from_directory, abort
from pathlib import Path

_PUBLIC_DIR = Path(r"/data/data/com.termux/files/home/cimeika-unified/public").resolve()
_ABILITIES_DIR = _PUBLIC_DIR / "abilities"

def _serve_public(filename: str):
    fp = _PUBLIC_DIR / filename
    if not fp.exists():
        abort(404)
    return send_from_directory(str(_PUBLIC_DIR), filename)

@app.get("/")
def _ui_root():
    return _serve_public("index.html")

@app.get("/<path:filename>")
def _ui_files(filename):
    fp = _PUBLIC_DIR / filename
    if fp.exists() and fp.is_file():
        return send_from_directory(str(_PUBLIC_DIR), filename)
    abort(404)

@app.get("/abilities/<path:filename>")
def _ui_abilities(filename):
    fp = _ABILITIES_DIR / filename
    if not fp.exists():
        abort(404)
    return send_from_directory(str(_ABILITIES_DIR), filename)

CORS(app)

REGISTRY_PATH = "storage/registry/cit_core.json"

def register_subscriber(ip, user_agent):
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    data = {"active_subscribers": {}} if not os.path.exists(REGISTRY_PATH) else json.load(open(REGISTRY_PATH))
    
    # Визначення типу абонента
    client_type = "AI_AGENT" if any(x in user_agent.lower() for x in ["python", "curl", "gpt", "gemini", "ai"]) else "WEB_USER"
    
    data["active_subscribers"][ip] = {
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_type": client_type,
        "provisioning_status": "package_optimized"
    }
    with open(REGISTRY_PATH, "w") as f: json.dump(data, f, indent=4)
    return client_type

@app.route('/ci1', methods=['GET'])
def ai_passport():
    ua = request.headers.get('User-Agent', '')
    ip = request.remote_addr
    client_type = register_subscriber(ip, ua)
    
    # Пакетне забезпечення залежно від типу
    package = {
        "system": "Cimeika (CIT)",
        "registry_id": f"NODE-{ip}",
        "client_type": client_type,
        "wiki_context": "https://github.com/Ihorog/ciwiki"
    }
    
    if client_type == "AI_AGENT":
        package.update({
            "ebc_components": ["auth_logic", "registry_sync", "gateway_api"],
            "protocol": "JSON_RAW",
            "instructions": "Use One-Shot execution. See CiWiki/protocols."
        })
    else:
        package.update({
            "ui_access": "https://ihorog.github.io/cit",
            "protocol": "WEB_INTERFACE",
            "instructions": "Welcome to Ci-Gateway. Use the dashboard to monitor nodes."
        })
        
    return jsonify(package)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
