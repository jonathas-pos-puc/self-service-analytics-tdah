#!/bin/bash
set -xeuo pipefail

PROJECT_ID=self-service-analytics-tdah
ZONE=us-central1-c
CLUSTER_NAME=http-to-gcs

gcloud container clusters create ${CLUSTER_NAME} \
--project="${PROJECT_ID}" \
--zone="${ZONE}" \
--machine-type="n1-standard-1" \
--disk-size="32" \
--enable-ip-alias \
--network="projects/${PROJECT_ID}/global/networks/default" \
--subnetwork="projects/${PROJECT_ID}/regions/us-central1/subnetworks/default" \
--enable-autoscaling \
--min-nodes="1" \
--max-nodes="3" \
--scopes=storage-rw,compute-ro
