#!/bin/bash
set -xeuo pipefail

PROJECT_ID=self-service-analytics-tdah
LOCATION=us-east1
ENV_NAME=ssa-tdah-etl

gcloud composer environments delete ${ENV_NAME} \
--project ${PROJECT_ID} \
--location ${LOCATION} \
--quiet
