variable "environment" {
  description = "Environnement cible (dev ou prod)"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "Région Scaleway (doit être en France)"
  type        = string
  default     = "fr-par"
}

variable "database_size" {
  description = "Taille de la base de données (en Go)"
  type        = number
  default     = 10
}

variable "is_ha_cluster" {
  description = "Activer la haute disponibilité pour Redis"
  type        = bool
  default     = false
}

variable "redis_user" {
  description = "Nom d'utilisateur Redis"
  type        = string
  default     = "default_user"
}

variable "redis_password" {
  description = "Mot de passe Redis"
  type        = string
  sensitive   = true
}

variable "cluster_size" {
  description = "Nombre de nœuds dans le cluster Redis"
  type        = number
  default     = 1
}


variable "subdomain" {
  description = "Nom de sous-domaine basé sur l'environnement"
  type        = string
  default     = "calculatrice-dev-marel-johanu-polytech-dijon"
}
