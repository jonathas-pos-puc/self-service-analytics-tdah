#!/bin/bash
set -xeuo pipefail

PROJECT_ID=self-service-analytics-tdah
ZONE=us-central1-c
CLUSTER_NAME=http-to-gcs

gcloud container clusters delete ${CLUSTER_NAME} \
--project="${PROJECT_ID}" \
--zone="${ZONE}" \
--quiet
