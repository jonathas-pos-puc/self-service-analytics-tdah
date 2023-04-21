variable "project_id" {
  description = "The ID of the project to create the bucket in."
  type        = string
  default     = "self-service-analytics-tdah"
}

variable "region" {
  type        = string
  description = "The region to deploy resources in."
  default = "us-central1"
}

variable "zone" {
  type        = string
  description = "The zone to deploy resources in."
  default = "us-central1-a"
}

variable "credentials_file" {
  type        = string
  description = "Path to the Google Cloud credentials file."
}

variable "lake_zones" {
  description = "Create Lake zones with these names"
  type        = list(string)
  default     = ["bronze", "silver", "gold"]
}
