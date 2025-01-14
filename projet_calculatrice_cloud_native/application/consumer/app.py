import pika
import json
import redis

# Simuler un stockage pour les résultats (à remplacer par Redis en prod)
redis_client = redis.Redis(host='localhost', port=6378)

# Contexte sécurisé pour évaluer les expressions
ALLOWED_GLOBALS = {
    "__builtins__": None,  # Désactiver les fonctions intégrées pour la sécurité
    "math": __import__("math"),  # Autoriser le module math
    "abs": abs,
    "round": round
}

# Configuration RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='calculations')

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
