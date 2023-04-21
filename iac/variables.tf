variable "project" {
  description = "The ID of the project to create the bucket in."
  type        = string
  default     = "self-service-analytics-tdah"
}

variable "region" {
  type    = string
  default = "us-east1"
}

variable "zone" {
  type    = string
  default = "us-east1-b"
}

variable "lake_zones" {
  description = "Create Lake zones with these names"
  type        = list(string)
  default     = ["bronze", "silver", "gold"]
}
