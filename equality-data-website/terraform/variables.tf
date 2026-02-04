
variable "service_name" {
  type = string
  description = "The short name of the service."
  default = "edp_web"
}

variable "service_name_hyphens" {
  type = string
  description = "The short name of the service (using hyphen-style)."
  default = "edp-web"
}

variable "environment" {
  type = string
  description = "The environment name."
}

variable "environment_hyphens" {
  type = string
  description = "The environment name (using hyphen-style)."
}

variable "prevent_email_spoofing" {
  type = bool
  description = "Should terraform create DNS records to prevent email spoofing (only required for the prod environment)"
  default = false
}

variable "aws_region" {
  type = string
  description = "The AWS region used for the provider and resources."
  default = "eu-west-2"
}
