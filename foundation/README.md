# Terraform - Fondation de l'Infrastructure

## Les ressources de fondation suivantes sont définies via Terraform :

+ Namespace de registre de conteneurs : Création d'un espace de noms pour stocker les images Docker dans un registre Scaleway.
+ DNS : Enregistrement des domaines nécessaires pour l'application.
+ Cluster Kubernetes : Déploiement du cluster Kubernetes sur Scaleway.
+ Load Balancer : Mise en place de Load Balancers pour la gestion du trafic.
+ Base de données : Base de données PostgreSQL pour le stockage des données persistantes de l'application.

## Résultat de la commande terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  ### scaleway_container_namespace.calculator_registry will be created
  + resource "scaleway_container_namespace" "calculator_registry" {
      + destroy_registry      = false
      + id                    = (known after apply)
      + name                  = "calculator-registry-dev"
      + organization_id       = (known after apply)
      + project_id            = (known after apply)
      + region                = "fr-par"
      + registry_endpoint     = (known after apply)
      + registry_namespace_id = (known after apply)
    }

  ### scaleway_domain_record.calculator_dns will be created
  + resource "scaleway_domain_record" "calculator_dns" {
      + data            = (known after apply)
      + dns_zone        = "kiowy.net"
      + fqdn            = (known after apply)
      + id              = (known after apply)
      + keep_empty_zone = false
      + name            = "calculatrice-dev-marel-johanu-polytech-dijon"
      + priority        = (known after apply)
      + project_id      = (known after apply)
      + root_zone       = (known after apply)
      + ttl             = 3600
      + type            = "A"
    }

  ### scaleway_k8s_cluster.calculator_cluster will be created
  + resource "scaleway_k8s_cluster" "calculator_cluster" {
      + apiserver_url               = (known after apply)
      + cni                         = "cilium"
      + created_at                  = (known after apply)
      + delete_additional_resources = true
      + id                          = (known after apply)
      + kubeconfig                  = (sensitive value)
      + name                        = "calculator-cluster-dev"
      + organization_id             = (known after apply)
      + project_id                  = (known after apply)
      + region                      = "fr-par"
      + status                      = (known after apply)
      + type                        = (known after apply)
      + updated_at                  = (known after apply)
      + upgrade_available           = (known after apply)
      + version                     = "1.25.4"
      + wildcard_dns                = (known after apply)

      + auto_upgrade (known after apply)

      + autoscaler_config (known after apply)

      + open_id_connect_config (known after apply)
    }

  ### scaleway_lb.calculator_lb will be created
  + resource "scaleway_lb" "calculator_lb" {
      + id                      = (known after apply)
      + ip_address              = (known after apply)
      + ip_id                   = (known after apply)
      + ip_ids                  = (known after apply)
      + ipv6_address            = (known after apply)
      + name                    = "calculator-lb-dev"
      + organization_id         = (known after apply)
      + project_id              = (known after apply)
      + region                  = (known after apply)
      + ssl_compatibility_level = "ssl_compatibility_level_intermediate"
      + type                    = "lb-s"
      + zone                    = (known after apply)
    }

  ### scaleway_rdb_instance.calculator_db will be created
  + resource "scaleway_rdb_instance" "calculator_db" {
      + backup_same_region        = (known after apply)
      + backup_schedule_frequency = (known after apply)
      + backup_schedule_retention = (known after apply)
      + certificate               = (known after apply)
      + disable_backup            = false
      + endpoint_ip               = (known after apply)
      + endpoint_port             = (known after apply)
      + engine                    = "PostgreSQL-13"
      + id                        = (known after apply)
      + is_ha_cluster             = false
      + name                      = "calculator-db-dev"
      + node_type                 = "DB-DEV-S"
      + organization_id           = (known after apply)
      + project_id                = (known after apply)
      + read_replicas             = (known after apply)
      + region                    = "fr-par"
      + settings                  = (known after apply)
      + user_name                 = (known after apply)
      + volume_size_in_gb         = (known after apply)
      + volume_type               = "lssd"

      + load_balancer (known after apply)

      + logs_policy (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.V