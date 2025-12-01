from flask import Flask, render_template

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)

