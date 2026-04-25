
from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/")
def home():
    return jsonify({"message": "Secure App API running"}), 200

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400
    return jsonify({"echo": data["text"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
