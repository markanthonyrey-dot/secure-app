import os
import logging
from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/items", methods=["GET"])
def get_items():
    items = [
        {"id": 1, "name": "Widget A"},
        {"id": 2, "name": "Widget B"},
    ]
    return jsonify({"items": items}), 200


@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "Missing required field: name"}), 400

    name = str(data["name"]).strip()
    if not name:
        return jsonify({"error": "Field 'name' must not be empty"}), 400

    new_item = {"id": 3, "name": name}
    logger.info("Created item: %s", new_item)
    return jsonify({"item": new_item}), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
