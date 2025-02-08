import pika

def test_rabbitmq():
    # Connexion à RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=0))
    channel = connection.channel()

    # Déclarer une file d'attente
    channel.queue_declare(queue='test_queue')

    # Envoyer un message
    channel.basic_publish(exchange='', routing_key='test_queue', body='Hello, RabbitMQ!')
    print("Message envoyé à la file d'attente 'test_queue'.")

    # Fonction de rappel pour consommer les messages
    def callback(ch, method, properties, body):
        print(f"Message reçu: {body.decode('utf-8')}")
        connection.close()  # Fermer la connexion après avoir reçu le message

    # Consommer le message
    channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)
    print('En attente de messages...')
    channel.start_consuming()

if __name__ == "__main__":
    test_rabbitmq()
