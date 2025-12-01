from flask import Flask, jsonify
from flask_cors import CORS
import requests
from collections import Counter
from datetime import datetime

from sentiment import RuleBasedSentimentAdapter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5002", "http://127.0.0.1:5002"]}})

adapter = RuleBasedSentimentAdapter()

FEEDBACK_SERVICE_URL = "http://127.0.0.1:5000"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/analyse", methods=["GET"])
def analyse():
    try:
        resp = requests.get(f"{FEEDBACK_SERVICE_URL}/feedback", timeout=5)
        resp.raise_for_status()
        feedback_list = resp.json()
    except Exception as e:
        return jsonify({"error": f"failed to fetch feedback: {e}"}), 502

    sentiment_counts = Counter()
    keyword_counter = Counter()
    trend_counter = Counter()

    for fb in feedback_list:
        text = fb.get("text", "")
        sentiment = adapter.analyse_text(text)
        sentiment_counts[sentiment] += 1

        for kw in adapter.extract_keywords(text):
            keyword_counter[kw] += 1

        ts = fb.get("timestamp")
        date_key = None
        if ts:
            try:
                # Expect ISO format
                date_key = datetime.fromisoformat(ts.replace("Z","")).date().isoformat()
            except Exception:
                date_key = None
        if date_key:
            trend_counter[date_key] += 1

    # Top 5 keywords
    top_keywords = [{"word": w, "count": c} for w, c in keyword_counter.most_common(5)]
    trends = [{"date": d, "count": c} for d, c in sorted(trend_counter.items())]

    result = {
        "sentiment_distribution": {
            "positive": sentiment_counts.get("positive", 0),
            "negative": sentiment_counts.get("negative", 0),
            "neutral": sentiment_counts.get("neutral", 0),
        },
        "keywords": top_keywords,
        "trends": trends,
        "total_feedback": len(feedback_list)
    }
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
	
