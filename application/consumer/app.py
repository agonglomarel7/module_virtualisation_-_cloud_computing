import pika
import json
import redis
import time
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.StreamHandler()
])
logger = logging.getLogger(__name__)

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

# Connexion à RabbitMQ
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

# Contexte sécurisé pour évaluer les expressions
ALLOWED_GLOBALS = {
    "__builtins__": None,
    "math": __import__("math"),
    "abs": abs,
    "round": round
}

def safe_eval(expression):
    """Évalue une expression mathématique en toute sécurité."""
    try:
        # Vérifier que l'expression ne contient que des caractères autorisés
        allowed_chars = "0123456789+-*/(). sqrtcbrtabsroundmath"
        if any(c not in allowed_chars for c in expression.replace(" ", "")):
            raise ValueError("Caractère non autorisé dans l'expression")

        return eval(expression, ALLOWED_GLOBALS)
    except Exception as e:
        raise ValueError(f"Erreur d'évaluation : {str(e)}")

def on_message(channel, method, properties, body):
    try:
        task = json.loads(body)
        operation_id = task.get("id")
        expression = task.get("expression")

        if not operation_id or not expression:
            logger.error("Tâche invalide reçue: %s", task)
            return

        # Évaluer l'expression mathématique
        result = safe_eval(expression)
        redis_client.set(operation_id, result)
        logger.info(f"Calcul terminé: {expression} = {result}")
    
    except Exception as e:
        error_message = f"Erreur : {str(e)}"
        redis_client.set(operation_id, error_message)
        logger.error("Erreur lors du traitement de la tâche: %s", error_message)

channel.basic_consume(queue='calculations', on_message_callback=on_message, auto_ack=True)

logger.info("Consommateur en attente de tâches...")
channel.start_consuming()
