#!/bin/bash
set -xeuo pipefail
cd "${0%/*}"

PROJECT_ID=self-service-analytics-tdah

gcloud iam service-accounts create ssa-tdah-registry
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:ssa-tdah-registry@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/storage.admin"
gcloud iam service-accounts keys create ../images/http_to_gcs/keyfile.json --iam-account ssa-tdah-registry@${PROJECT_ID}.iam.gserviceaccount.com
gcloud auth activate-service-account ssa-tdah-registry@${PROJECT_ID}.iam.gserviceaccount.com --key-file=../images/http_to_gcs/keyfile.json
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://gcr.io
gcloud auth configure-docker
