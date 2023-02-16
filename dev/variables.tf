variable "prefix" {
  default = "app-p"
}

variable "computer_name" {
  type        = string
  description = "Name of the host computer."
}

variable "subscription_id" {
  type        = string
  description = "Subscription id of azure account."
}

variable "client_id" {
  type        = string
  description = "Application id of azure account."
}

variable "client_secret" {
  type        = string
  description = "Password of azure account."
}

variable "tenant_id" {
  type        = string
  description = "Tenant of azure account."
}

variable "admin_username" {
  type        = string
  description = "Username for the admin."
}

# variable "admin_password" {
#   type        = string
#   description = "Password for the admin."
# }