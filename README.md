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

**Vous pouvez tester notre application en ligne ici : [calculatrice-johanu-marel.randever.com](http://calculatrice-johanu-marel.randever.com/)**

---

## Architecture de l'application

Consultez le [README - Architecture](./application/README.md) pour plus de détails.

---

## Déploiement Kubernetes

Consultez le [README - Déploiement Kubernetes](./kubernetes/README.md) pour plus de détails.

---

## Fondation de l'Infrastructure

Consultez le [README - Fondation](./foundation/README.md) pour plus de détails.

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
<<<<<<< HEAD
=======
>>>>>>> 516159b94cc84d89567f5c1c5fe41461e17ed85d
>>>>>>> 0dbd0995a2d1e93e7ee4ab1301a1aaced4428f88
