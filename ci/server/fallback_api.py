from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    text = data.get("text", "")
    return jsonify({"ok": True, "reply": f"Echo: {text}"})

if __name__ == "__main__":
    port = int(os.getenv("CIT_PORT", "8800"))
    print(f"[FALLBACK] Flask listening on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
