from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import pika
import uuid
import json

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines par défaut

@app.route("/")
def home():
    return send_from_directory("/frontend", "index.html")

# Simuler un stockage pour les résultats (à remplacer par Redis en prod)
results_cache = {}

# Configuration RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='calculations')

@app.route("/calculate", methods=["POST"])
def request_calculation():
    try:
        data = request.get_json()
        expression = data.get("expression")

        if not expression or not isinstance(expression, str):
            return jsonify({"error": "Requête invalide. Une expression mathématique est attendue."}), 400

        # Générer un ID unique pour l'opération
        operation_id = str(uuid.uuid4())
        results_cache[operation_id] = None  # Réserver l'ID dans le cache

        # Envoyer la tâche à RabbitMQ
        channel.basic_publish(
            exchange='',
            routing_key='calculations',
            body=json.dumps({"id": operation_id, "expression": expression})
        )

        return jsonify({"id": operation_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/result/<operation_id>", methods=["GET"])
def get_result(operation_id):
    try:
        # Vérifier si l'opération existe dans le cache
        if operation_id not in results_cache:
            return jsonify({"error": "ID non trouvé"}), 404

        result = results_cache[operation_id]
        if result is None:
            return jsonify({"message": "Résultat non encore disponible"}), 202
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)