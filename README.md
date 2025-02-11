<<<<<<< HEAD
# module_virtualisation_-_cloud_computing

sudo docker-compose up  --build -d
=======
# Rapport du Projet - Calculatrice Cloud Native

## Membres du Groupe
- **GANDONOU Johanu**
- **AGONGLO Marel**

---

## Introduction

Ce projet consiste à déployer une **Calculatrice Cloud Native** en utilisant des technologies modernes de virtualisation et de cloud computing. L'application est architecturée autour de microservices, avec une infrastructure définie en code (IaC) via Terraform, et déployée sur un cluster Kubernetes. L'application permet d'effectuer des opérations mathématiques de base (addition, soustraction, multiplication, division) et stocke les résultats dans une base de données Redis. Les calculs sont gérés via une file d'attente RabbitMQ, et l'interface utilisateur est accessible via un frontend.

---

## Architecture du Projet

L'application est composée de plusieurs microservices :

1. **Frontend** : Interface utilisateur permettant de saisir des calculs et de récupérer les résultats.
2. **Backend (API)** : Service qui reçoit les demandes de calcul, les place dans une file d'attente RabbitMQ, et récupère les résultats depuis Redis.
3. **Consumer** : Service qui consomme les messages de la file d'attente RabbitMQ, effectue les calculs, et stocke les résultats dans Redis.
4. **Redis** : Base de données clé-valeur pour stocker les résultats des calculs.
5. **RabbitMQ** : Système de file d'attente pour gérer les calculs à effectuer.

---

## Déploiement Kubernetes

### Fichiers de Configuration

1. **Namespace** : `01-namespace.yaml`
   - Crée un namespace dédié pour le projet : `johanu-marel`.

2. **ReplicaSets** : `02-replicasets.yaml`
   - Définit les ReplicaSets pour chaque microservice :
     - `redis-rs` : Gère le pod Redis.
     - `rabbitmq-rs` : Gère le pod RabbitMQ.
     - `backend-rs` : Gère le pod Backend (API).
     - `frontend-rs` : Gère le pod Frontend.
     - `consumer-rs` : Gère le pod Consumer.

3. **Services** : `03-services.yaml`
   - Définit les services pour exposer les pods :
     - `redis` : Expose le service Redis sur le port 6379.
     - `rabbitmq` : Expose le service RabbitMQ sur les ports 5672 (AMQP) et 15672 (Management).
     - `backend` : Expose le service Backend sur le port 5000.
     - `frontend` : Expose le service Frontend sur le port 80.

### 4. **Ingress** : `04-ingress.yaml`

Le fichier `04-ingress.yaml` définit les règles Ingress pour exposer les services Frontend et Backend via deux domaines distincts. Ces règles permettent de rediriger le trafic entrant vers les services appropriés en fonction du chemin et du domaine demandé.

#### Règles Ingress Définies

1. **Première Règle Ingress** :  
   Cette règle est conforme aux exigences du projet et utilise le domaine suivant :
   - **Domaine** : `calculatrice-johanu-marel-polytech-dijon.kiowy.net`
   - **Chemins** :
     - `/` : Redirige le trafic vers le service **Frontend** sur le port 80.
     - `/api` : Redirige le trafic vers le service **Backend** sur le port 5000.

   **Accès Local** :  
   Pour accéder à l'application via ce domaine, il est nécessaire de configurer le fichier `hosts` de votre machine pour mapper ce domaine à l'adresse IP du LoadBalancer Kubernetes. Voici comment procéder :

   - **Linux & MacOS** :
     ```bash
     sudo echo "34.77.144.136 calculatrice-johanu-marel-polytech-dijon.kiowy.net" >> /etc/hosts
     ```
   - **Windows** :
     - Ouvrez le fichier `C:\Windows\System32\drivers\etc\hosts` avec un éditeur de texte (en mode administrateur).
     - Ajoutez la ligne suivante à la fin du fichier :
       ```
       34.77.144.136 calculatrice-johanu-marel-polytech-dijon.kiowy.net
       ```

   Après cette configuration, vous pouvez accéder à l'application via un navigateur en utilisant l'URL :  
   `http://calculatrice-johanu-marel-polytech-dijon.kiowy.net`.

2. **Deuxième Règle Ingress** :  
   Cette règle a été ajoutée pour rendre l'application accessible sur Internet via notre propre serveur. Elle utilise un domaine personnalisé :
   - **Domaine** : `calculatrice-johanu-marel.randever.com`
   - **Chemins** :
     - `/` : Redirige le trafic vers le service **Frontend** sur le port 80.
     - `/api` : Redirige le trafic vers le service **Backend** sur le port 5000.

   **Accès Public** :  
   Ce domaine est configuré pour pointer vers l'adresse IP publique de notre serveur, ce qui permet d'accéder à l'application depuis n'importe où sur Internet. Aucune modification du fichier `hosts` n'est nécessaire pour ce domaine.

   Vous pouvez accéder à l'application via un navigateur en utilisant l'URL :  
   `http://calculatrice-johanu-marel.randever.com`.

---

### Pourquoi Deux Règles Ingress ?

- **Première Règle** :  
  Cette règle est conforme aux exigences du projet et permet de tester l'application localement en simulant un accès via un domaine personnalisé. Elle est utile pour les tests et les démonstrations en environnement de développement.

- **Deuxième Règle** :  
  Cette règle a été ajoutée pour rendre l'application accessible publiquement sur Internet. Elle permet de partager l'application avec d'autres utilisateurs sans qu'ils aient besoin de modifier leur fichier `hosts`.

---

## Fonctionnement de l'Application

### Demande de Calcul

1. L'utilisateur saisit une opération mathématique via l'interface Frontend.
2. Le Frontend envoie une requête HTTP POST à l'API Backend.
3. L'API Backend place le calcul dans la file d'attente RabbitMQ et retourne un ID de calcul.
4. Le Consumer récupère le calcul de la file d'attente, effectue l'opération, et stocke le résultat dans Redis.

### Récupération du Résultat

1. Une fois le Frontend a reçu l'ID du calcul, il envoie une requête HTTP GET à l'API Backend.
2. L'API Backend récupère le résultat depuis Redis et le retourne au Frontend.
3. Le Frontend affiche le résultat à l'utilisateur.

---

## Conclusion

Ce projet nous a permis de mettre en pratique les concepts de virtualisation et de cloud computing, en déployant une application cloud-native sur un cluster Kubernetes. L'utilisation de Terraform pour l'infrastructure, Kubernetes pour le déploiement, et des technologies comme Redis et RabbitMQ pour la gestion des données et des files d'attente, a permis de créer une application robuste et scalable.
>>>>>>> 516159b94cc84d89567f5c1c5fe41461e17ed85d
