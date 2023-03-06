#!/bin/bash
set -xeuo pipefail
cd "${0%/*}"

PROJECT_ID=self-service-analytics-tdah
IMAGE_NAME=http-to-gcs

gcloud container images delete gcr.io/${PROJECT_ID}/${IMAGE_NAME} --quiet
