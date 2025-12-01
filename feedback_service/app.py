from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

from config import AppConfigSingleton
from repository import FeedbackRepository

app = Flask(__name__)
# Allow cross-origin requests from localhost:5002 and 5001
CORS(app, resources={r"/*": {"origins": ["http://localhost:5002", "http://127.0.0.1:5002", "http://localhost:5001", "http://127.0.0.1:5001"]}})

# Singleton config
config = AppConfigSingleton.get_instance()
repo = FeedbackRepository(config.storage_file_path)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    text = (payload.get("text") or "").strip()

    if not name or not email or not text:
        return jsonify({"error": "name, email and text are required"}), 400

    record = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "text": text,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    saved = repo.add_feedback(record)
    return jsonify(saved), 201

@app.route("/feedback", methods=["GET"])
def list_feedback():
    return jsonify(repo.list_feedback()), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

