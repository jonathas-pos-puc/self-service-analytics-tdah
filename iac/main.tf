provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
  credentials = file(var.credentials_file)
}

resource "google_service_account" "sa_ssa_tdah" {
  account_id   = "sa-ssa-tdah"
  display_name = "service account de ssa"
}

resource "google_project_iam_binding" "binding" {
  project = google_service_account.sa_ssa_tdah.project
  role    = "roles/editor"

  members = [
    "serviceAccount:${google_service_account.sa_ssa_tdah.email}",
  ]
}

resource "google_service_account_key" "key" {
  service_account_id = google_service_account.sa_ssa_tdah.name
}

# Crie os buckets usando a função count e o sufixo de cada um
resource "google_storage_bucket" "buckets" {
  count    = length(var.lake_zones)
  name     = "${var.project_id}-${var.lake_zones[count.index]}"
  location = var.region
}

output "service_account_key" {
  value     = google_service_account_key.key.private_key
  sensitive = true
}