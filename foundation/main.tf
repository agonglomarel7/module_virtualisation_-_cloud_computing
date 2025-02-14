terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = "~> 2.0"
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  region = var.region
}

# Namespace pour héberger des conteneurs
resource "scaleway_container_namespace" "calculator_registry" {
  name   = "calculator-registry-${var.environment}"
  region = var.region
}

# Cluster Kubernetes avec argument obligatoire
resource "scaleway_k8s_cluster" "calculator_cluster" {
  name                        = "calculator-cluster-${var.environment}"
  cni                         = "cilium"
  version                     = "1.25.4"
  region                      = var.region
  delete_additional_resources = true # Argument obligatoire
}

# Base de données avec `node_type`
resource "scaleway_redis_cluster" "calculator_db" {
  name         = "calculator-db-${var.environment}"
  node_type    = "REDIS-S"        # Type d'instance Scaleway pour Redis
  version      = "6.2"            # Version de Redis
  cluster_size = var.cluster_size # Nombre de nœuds Redis

  # Identifiants obligatoires
  user_name = var.redis_user
  password  = var.redis_password
}



# LoadBalancer avec type requis
resource "scaleway_lb" "calculator_lb" {
  name = "calculator-lb-${var.environment}"
  #region = var.region
  type = "lb-s" # Type requis
}

# Enregistrement DNS avec `dns_zone` et `data`
resource "scaleway_domain_record" "calculator_dns" {
  dns_zone = "kiowy.net"
  name     = var.subdomain
  type     = "A"
  data     = scaleway_lb.calculator_lb.id
}
