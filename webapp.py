"""Simple Flask web application."""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello() -> dict:
    """Return a hello message."""
    return jsonify({"message": "hello from factory"})


if __name__ == "__main__":
    app.run(debug=True)