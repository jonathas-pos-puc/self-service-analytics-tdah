#!/bin/bash
set -xeuo pipefail

PROJECT_ID=self-service-analytics-tdah
LOCATION=us-east1
ZONE=us-east1-b
gcloud compute disks create --size=100GB --zone ${ZONE} nfs-disk

kubectl create -f nfs-server-deployment.yml
kubectl create -f nfs-cluster-ip-service.yml
