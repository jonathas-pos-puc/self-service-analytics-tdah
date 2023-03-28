provider "google" {
  project = "self-service-analytics-tdah"
  region = var.region
  zone   = var.zone
}

resource "google_storage_bucket" "default" {
  count         = length(var.lake_zones)
  name          = "${var.project}-bucket-${var.lake_zones[count.index]}"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true
}
