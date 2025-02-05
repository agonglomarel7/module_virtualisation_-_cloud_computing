from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
import uuid
import json
import redis
import time
import os

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines par défaut

# Connexion à Redis
def connect_to_redis():
    # Récupération du port via la variable d'environnement, avec une valeur par défaut
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    while True:
        try:
            redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
            # Test de connexion
            redis_client.ping()
            print("Connected to Redis")
            return redis_client
        except redis.ConnectionError:
            print("Waiting for Redis...")
            time.sleep(5)

# Utilisation de la fonction de connexion
redis_client = connect_to_redis()


# Configuration RabbitMQ
def connect_to_rabbitmq():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, heartbeat=0))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(5)

connection = connect_to_rabbitmq()
channel = connection.channel()

# Déclarer la file d'attente RabbitMQ (assurez-vous que cette queue est bien créée)
channel.queue_declare(queue='calculations')


@app.route("/api", methods=['GET'], strict_slashes=False)
def home():
    return "Bienvenue sur l'API de calculatrice !"

@app.route("/api/calculate", methods=["POST"])
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

@app.route("/api/result/<operation_id>", methods=["GET"])
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
    app.run(host='0.0.0.0', port=5000, debug=True)
