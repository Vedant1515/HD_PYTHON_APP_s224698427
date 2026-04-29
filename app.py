from flask import Flask, jsonify
from calculator import add, subtract, multiply, divide

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "SIT707 CI/CD App Running"})

@app.route("/add/<int:a>/<int:b>")
def add_route(a, b):
    return jsonify({"result": add(a, b)})

@app.route("/divide/<int:a>/<int:b>")
def divide_route(a, b):
    try:
        return jsonify({"result": divide(a, b)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
