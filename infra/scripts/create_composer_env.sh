#!/bin/bash
set -xeuo pipefail

PROJECT_ID=self-service-analytics-tdah
LOCATION=us-east1
ZONE=us-east1-b
ENV_NAME=ssa-tdah-etl
IMAGE_VERSION="composer-1.17.8-airflow-2.1.4"
PYTHON_VERSION=3
NODE_COUNT=3
DISK_SIZE="100GB"
MACHINE_TYPE="n1-standard-1"
NETWORK="projects/${PROJECT_ID}/global/networks/default"

gcloud composer environments create ${ENV_NAME} \
    --location=${LOCATION} \
    --zone ${ZONE} \
    --machine-type ${MACHINE_TYPE} \
    --image-version ${IMAGE_VERSION} \
    --network ${NETWORK} \
    --python-version ${PYTHON_VERSION} \
    --node-count ${NODE_COUNT} \
    --disk-size ${DISK_SIZE}
