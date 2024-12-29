from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines par défaut

@app.route("/")
def home():
    return "Bienvenue sur l'API de calculatrice !"

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()
        expression = data.get("expression", "")

        allowed_chars = "0123456789+-*/(). "
        if not all(char in allowed_chars for char in expression):
            return jsonify({"error": "Expression invalide"}), 400

        result = eval(expression)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
