provider "google-beta" {
  project = var.project
  region  = var.region
  zone    = var.zone
}
#
#resource "google_composer_environment" "composer" {
#  provider = google-beta
#  name = "ssa-tdah-etl"
#  region = "us-east1"
#
#  config {
#
#    software_config {
#      image_version = "composer-1.20.8-airflow-2.3.4"
#    }
#
#    node_config {
#      service_account = "ssa-tdah-composer@self-service-analytics-tdah.iam.gserviceaccount.com"
#    }
#
#  }
#}
#

resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  project = "self-service-analytics-tdah"
  location = "us-central1"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  node_config {
    service_account = "ssa-tdah-composer@self-service-analytics-tdah.iam.gserviceaccount.com"
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  project = "self-service-analytics-tdah"
  name       = "my-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-medium"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = "ssa-tdah-composer@self-service-analytics-tdah.iam.gserviceaccount.com"
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
