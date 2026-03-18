"""Simple Flask web application."""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello() -> dict:
    """Return a hello message."""
    return jsonify({"message": "hello from factory"})


@app.route('/ping', methods=['GET'])
def ping() -> dict:
    return jsonify({"pong": True})


if __name__ == "__main__":
    app.run(debug=True)