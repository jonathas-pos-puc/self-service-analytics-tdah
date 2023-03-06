#!/bin/bash
set -xeuo pipefail
cd "${0%/*}"

PROJECT_ID=self-service-analytics-tdah

gcloud iam service-accounts create ssa-tdah-composer
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:ssa-tdah-composer@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/composer.admin"
gcloud iam service-accounts keys create ../airflow/keyfile.json --iam-account ssa-tdah-composer@${PROJECT_ID}.iam.gserviceaccount.com
gcloud auth activate-service-account ssa-tdah-composer@${PROJECT_ID}.iam.gserviceaccount.com --key-file=../airflow/keyfile.json
