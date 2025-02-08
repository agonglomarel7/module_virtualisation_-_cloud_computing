import pika
import json
import redis
import time
import os

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
channel.queue_declare(queue='calculations')


# Contexte sécurisé pour évaluer les expressions
ALLOWED_GLOBALS = {
    "__builtins__": None,  # Désactiver les fonctions intégrées pour la sécurité
    "math": __import__("math"),  # Autoriser le module math
    "abs": abs,
    "round": round
}

def safe_eval(expression):
    """Évaluer une expression mathématique en toute sécurité."""
    return eval(expression, ALLOWED_GLOBALS)

def on_message(channel, method, properties, body):
    task = json.loads(body)
    operation_id = task.get("id")
    expression = task.get("expression")

    if not operation_id or not expression:
        print("Tâche invalide reçue :", task)
        return

    try:
        # Évaluer l'expression mathématique
        result = safe_eval(expression)
        redis_client.set(operation_id, result)

        print(f"Calcul terminé : {expression} = {result}")

    except Exception as e:
        redis_client[operation_id] = f"Erreur : {str(e)}"

channel.basic_consume(queue='calculations', on_message_callback=on_message, auto_ack=True)

print("Consommateur en attente de tâches...")
channel.start_consuming()
