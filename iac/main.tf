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

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_project_iam_member" "composer_worker" {
  project = var.project_id
  member  = "serviceAccount:ssa-tdah-composer@self-service-analytics-tdah.iam.gserviceaccount.com"
  role    = "roles/composer.worker"
}

resource "google_project_iam_member" "editor" {
  project = var.project_id
  member  = "serviceAccount:877794803636@cloudservices.gserviceaccount.com"
  role    = "roles/editor"
}


resource "google_composer_environment" "composer" {
  project = var.project_id
  name = "ssa-tdah-etl"
  region = var.region

  config {

    software_config {
      image_version = "composer-1.20.8-airflow-2.3.4"
    }

    node_config {
      service_account = "ssa-tdah-composer@self-service-analytics-tdah.iam.gserviceaccount.com"
    }

  }
}





output "service_account_key" {
  value     = google_service_account_key.key.private_key
  sensitive = true
}