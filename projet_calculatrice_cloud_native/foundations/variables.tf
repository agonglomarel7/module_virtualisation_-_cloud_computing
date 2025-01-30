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
  description = "Activer la haute disponibilité pour la base de données"
  type        = bool
  default     = false
}

variable "subdomain" {
  description = "Nom de sous-domaine basé sur l'environnement"
  type        = string
  default     = "calculatrice-dev-marel-johanu-polytech-dijon"
}
