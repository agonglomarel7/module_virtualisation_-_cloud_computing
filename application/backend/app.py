import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
import uuid
import json
import redis
import time
import os

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines par défaut

# Connexion à Redis
def connect_to_redis():
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    while True:
        try:
            redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
            redis_client.ping()
            logger.info("Connected to Redis")
            return redis_client
        except redis.ConnectionError:
            logger.warning("Waiting for Redis...")
            time.sleep(5)

redis_client = connect_to_redis()

# Configuration RabbitMQ
def connect_to_rabbitmq():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, heartbeat=0))
            logger.info("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            logger.warning("Waiting for RabbitMQ...")
            time.sleep(5)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='calculations')

@app.route("/api", methods=['GET'], strict_slashes=False)
def home():
    logger.info("Accueil de l'API consulté")
    return "Bienvenue sur l'API de calculatrice !"

@app.route("/api/calculate", methods=["POST"], strict_slashes=False)
def request_calculation():
    try:
        data = request.get_json()
        expression = data.get("expression")

        if not expression or not isinstance(expression, str):
            logger.warning("Requête invalide reçue")
            return jsonify({"error": "Requête invalide. Une expression mathématique est attendue."}), 400

        operation_id = str(uuid.uuid4())
        redis_client.set(operation_id, "pending")
        channel.basic_publish(
            exchange='',
            routing_key='calculations',
            body=json.dumps({"id": operation_id, "expression": expression})
        )
        logger.info(f"Tâche envoyée : {expression} avec ID {operation_id}")
        return jsonify({"id": operation_id})
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de la tâche : {e}")
        return jsonify({"error": str(e)}), 400

@app.route("/api/result/<operation_id>", methods=["GET"], strict_slashes=False)
def get_result(operation_id):
    try:
        if not redis_client.exists(operation_id):
            logger.warning(f"ID non trouvé : {operation_id}")
            return jsonify({"error": "ID non trouvé"}), 404

        result = redis_client.get(operation_id)
        if result == b"pending":
            logger.info(f"Résultat non encore disponible pour {operation_id}")
            return jsonify({"message": "Résultat non encore disponible"}), 202

        logger.info(f"Résultat retourné pour {operation_id}: {result.decode('utf-8')}")
        return jsonify({"result": result.decode('utf-8')})
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du résultat : {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    logger.info("Démarrage du backend Flask")
    app.run(host='0.0.0.0', port=5000, debug=True)
