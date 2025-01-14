# Utiliser une image Python officielle comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier de dépendances dans le conteneur
COPY requirements.txt .

# Mettre à jour pip et installer les dépendances avec un délai d'attente augmenté
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copier tout le contenu de l'application dans le conteneur
COPY app.py .

# Exposer le port que Flask utilise (par défaut 5000)
EXPOSE 5000

# Définir la commande par défaut pour exécuter l'application
CMD ["python", "app.py"]
