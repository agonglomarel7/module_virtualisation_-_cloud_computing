from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
import uuid
import json
import redis

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines par défaut

@app.route("/")
def home():
    return "Bienvenue sur l'API de calculatrice !"

# Configuration Redis
redis_client = redis.StrictRedis(host='localhost', port=6378, db=0)  # Port corrigé à 6379

# Configuration RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Déclarer la file d'attente RabbitMQ (assurez-vous que cette queue est bien créée)
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
        redis_client.set(operation_id, "pending")

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
        if not redis_client.exists(operation_id):
            return jsonify({"error": "ID non trouvé"}), 404

        result = redis_client.get(operation_id)
        if result == "pending":
            return jsonify({"message": "Résultat non encore disponible"}), 202

        # Si le résultat est disponible, le retourner sous forme de string
        return jsonify({"result": result.decode('utf-8')})  # Décoder les octets en string

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
