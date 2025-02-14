## Architecture du Projet

L'application est composée de plusieurs microservices :

1. **Frontend** : Interface utilisateur permettant de saisir des calculs et de récupérer les résultats.
2. **Backend (API)** : Service qui reçoit les demandes de calcul, les place dans une file d'attente RabbitMQ, et récupère les résultats depuis Redis.
3. **Consumer** : Service qui consomme les messages de la file d'attente RabbitMQ, effectue les calculs, et stocke les résultats dans Redis.
4. **Redis** : Base de données clé-valeur pour stocker les résultats des calculs.
5. **RabbitMQ** : Système de file d'attente pour gérer les calculs à effectuer.
