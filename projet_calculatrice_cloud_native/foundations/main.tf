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

# Namespace pour héberger des conteneurs (remplace l'ancien `scaleway_container_registry`)
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
resource "scaleway_rdb_instance" "calculator_db" {
  name          = "calculator-db-${var.environment}"
  node_type     = "DB-DEV-S" # Type d'instance
  engine        = "PostgreSQL-13"
  region        = var.region
  is_ha_cluster = var.is_ha_cluster
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
