
Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  [32m+[0m create[0m

Terraform will perform the following actions:

[1m  # scaleway_container_namespace.calculator_registry[0m will be created
[0m  [32m+[0m[0m resource "scaleway_container_namespace" "calculator_registry" {
      [32m+[0m[0m destroy_registry      = false
      [32m+[0m[0m id                    = (known after apply)
      [32m+[0m[0m name                  = "calculator-registry-dev"
      [32m+[0m[0m organization_id       = (known after apply)
      [32m+[0m[0m project_id            = (known after apply)
      [32m+[0m[0m region                = "fr-par"
      [32m+[0m[0m registry_endpoint     = (known after apply)
      [32m+[0m[0m registry_namespace_id = (known after apply)
    }

[1m  # scaleway_domain_record.calculator_dns[0m will be created
[0m  [32m+[0m[0m resource "scaleway_domain_record" "calculator_dns" {
      [32m+[0m[0m data            = (known after apply)
      [32m+[0m[0m dns_zone        = "kiowy.net"
      [32m+[0m[0m fqdn            = (known after apply)
      [32m+[0m[0m id              = (known after apply)
      [32m+[0m[0m keep_empty_zone = false
      [32m+[0m[0m name            = "calculatrice-dev-marel-johanu-polytech-dijon"
      [32m+[0m[0m priority        = (known after apply)
      [32m+[0m[0m project_id      = (known after apply)
      [32m+[0m[0m root_zone       = (known after apply)
      [32m+[0m[0m ttl             = 3600
      [32m+[0m[0m type            = "A"
    }

[1m  # scaleway_k8s_cluster.calculator_cluster[0m will be created
[0m  [32m+[0m[0m resource "scaleway_k8s_cluster" "calculator_cluster" {
      [32m+[0m[0m apiserver_url               = (known after apply)
      [32m+[0m[0m cni                         = "cilium"
      [32m+[0m[0m created_at                  = (known after apply)
      [32m+[0m[0m delete_additional_resources = true
      [32m+[0m[0m id                          = (known after apply)
      [32m+[0m[0m kubeconfig                  = (sensitive value)
      [32m+[0m[0m name                        = "calculator-cluster-dev"
      [32m+[0m[0m organization_id             = (known after apply)
      [32m+[0m[0m project_id                  = (known after apply)
      [32m+[0m[0m region                      = "fr-par"
      [32m+[0m[0m status                      = (known after apply)
      [32m+[0m[0m type                        = (known after apply)
      [32m+[0m[0m updated_at                  = (known after apply)
      [32m+[0m[0m upgrade_available           = (known after apply)
      [32m+[0m[0m version                     = "1.25.4"
      [32m+[0m[0m wildcard_dns                = (known after apply)

      [32m+[0m[0m auto_upgrade (known after apply)

      [32m+[0m[0m autoscaler_config (known after apply)

      [32m+[0m[0m open_id_connect_config (known after apply)
    }

[1m  # scaleway_lb.calculator_lb[0m will be created
[0m  [32m+[0m[0m resource "scaleway_lb" "calculator_lb" {
      [32m+[0m[0m id                      = (known after apply)
      [32m+[0m[0m ip_address              = (known after apply)
      [32m+[0m[0m ip_id                   = (known after apply)
      [32m+[0m[0m ip_ids                  = (known after apply)
      [32m+[0m[0m ipv6_address            = (known after apply)
      [32m+[0m[0m name                    = "calculator-lb-dev"
      [32m+[0m[0m organization_id         = (known after apply)
      [32m+[0m[0m project_id              = (known after apply)
      [32m+[0m[0m region                  = (known after apply)
      [32m+[0m[0m ssl_compatibility_level = "ssl_compatibility_level_intermediate"
      [32m+[0m[0m type                    = "lb-s"
      [32m+[0m[0m zone                    = (known after apply)
    }

[1m  # scaleway_rdb_instance.calculator_db[0m will be created
[0m  [32m+[0m[0m resource "scaleway_rdb_instance" "calculator_db" {
      [32m+[0m[0m backup_same_region        = (known after apply)
      [32m+[0m[0m backup_schedule_frequency = (known after apply)
      [32m+[0m[0m backup_schedule_retention = (known after apply)
      [32m+[0m[0m certificate               = (known after apply)
      [32m+[0m[0m disable_backup            = false
      [32m+[0m[0m endpoint_ip               = (known after apply)
      [32m+[0m[0m endpoint_port             = (known after apply)
      [32m+[0m[0m engine                    = "PostgreSQL-13"
      [32m+[0m[0m id                        = (known after apply)
      [32m+[0m[0m is_ha_cluster             = false
      [32m+[0m[0m name                      = "calculator-db-dev"
      [32m+[0m[0m node_type                 = "DB-DEV-S"
      [32m+[0m[0m organization_id           = (known after apply)
      [32m+[0m[0m project_id                = (known after apply)
      [32m+[0m[0m read_replicas             = (known after apply)
      [32m+[0m[0m region                    = "fr-par"
      [32m+[0m[0m settings                  = (known after apply)
      [32m+[0m[0m user_name                 = (known after apply)
      [32m+[0m[0m volume_size_in_gb         = (known after apply)
      [32m+[0m[0m volume_type               = "lssd"

      [32m+[0m[0m load_balancer (known after apply)

      [32m+[0m[0m logs_policy (known after apply)
    }

[1mPlan:[0m 5 to add, 0 to change, 0 to destroy.
[0m[90m
─────────────────────────────────────────────────────────────────────────────[0m

Note: You didn't use the -out option to save this plan, so Terraform can't
guarantee to take exactly these actions if you run "terraform apply" now.
