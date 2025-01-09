import redis

def test_redis():
    # Connexion à Redis
    client = redis.Redis(host='localhost', port=6378)

    # Définir une clé
    client.set('test_key', 'Hello, Redis!')

    # Récupérer la clé
    value = client.get('test_key')

    # Afficher la valeur
    print(f"Valeur de 'test_key': {value.decode('utf-8')}")

if __name__ == "__main__":
    test_redis()
