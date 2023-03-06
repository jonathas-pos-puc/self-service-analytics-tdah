#!/bin/bash
set -xeuo pipefail

PROJECT_ID=self-service-analytics-tdah
BUCKET_NAME=${PROJECT_ID}-*

gsutil rb -f gs://${BUCKET_NAME}
