#!/bin/bash
set -xeuo pipefail
cd "${0%/*}"

PROJECT_ID=self-service-analytics-tdah
IMAGE_NAME=http-to-gcs
TAG_VERSION=latest

docker build -t ${IMAGE_NAME}:${TAG_VERSION} ../../infra/connectores/http_to_gcs/
docker tag ${IMAGE_NAME}:${TAG_VERSION} "gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG_VERSION}"
docker push "gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG_VERSION}"
