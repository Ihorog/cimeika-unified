from flask import Flask, jsonify, request
from flask_cors import CORS
import event_engine
import json
import os

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "node": os.getenv("NODE_NAME", "Android-Ihorog")})


@app.route('/get-calendar', methods=['GET'])
def get_cal():
    if not os.path.exists('calendar.json'):
        return jsonify([])
    with open('calendar.json', 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/ask-gemini', methods=['POST'])
def ask():
    text = (request.json or {}).get('text', '')
    res = f"Ci (GitHub Node): {text}"
    if any(word in text.lower() for word in ["завтра", "о ", "план"]):
        fake = '{"title": "' + text + \
            '", "date": "2026-02-01", "time": "12:00"}'
        res += f"\n\n[ПоДія]: {event_engine.process_raw_text(fake)}"
    return jsonify({"status": "success", "response": res})


if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5000)), host=os.getenv("HOST", "0.0.0.0"))
