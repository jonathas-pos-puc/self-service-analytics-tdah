from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.kubernetes_engine import (
    GKECreateClusterOperator,
    GKEDeleteClusterOperator,
    GKEStartPodOperator,
)

GCP_PROJECT_ID = "self-service-analytics-tdah"
GKE_LOCATION = "us-central1"
GKE_CLUSTER_NAME = "us-central1-ssa-tdah-85388d06-gke"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "gke_spark_dbf_to_parquet",
    default_args=default_args,
    description="Convert DBF files to Parquet using Spark on GKE",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 4, 24),
    catchup=False,
) as dag:
    start = DummyOperator(
        task_id="start",
    )

    end = DummyOperator(
        task_id="end",
    )

    ftp_to_bronze = GKEStartPodOperator(
        task_id="ftp_to_bronze",
        project_id=GCP_PROJECT_ID,
        location=GKE_LOCATION,
        cluster_name=GKE_CLUSTER_NAME,
        namespace="default",
        image=f"gcr.io/{GCP_PROJECT_ID}/pyspark-dbf-converter",
        name="dbf-to-parquet-conversion",
        arguments=["main.py"],
    )

    bronze_to_silver = GKEStartPodOperator(
        task_id="bronze_to_silver",
        project_id=GCP_PROJECT_ID,
        location=GKE_LOCATION,
        cluster_name=GKE_CLUSTER_NAME,
        namespace="default",
        image=f"gcr.io/{GCP_PROJECT_ID}/pyspark-dbf-converter",
        name="dbf-to-parquet-conversion",
        arguments=["main.py"],
    )

    silver_to_bq = GKEStartPodOperator(
        task_id="silver_to_bq",
        project_id=GCP_PROJECT_ID,
        location=GKE_LOCATION,
        cluster_name=GKE_CLUSTER_NAME,
        namespace="default",
        image=f"gcr.io/{GCP_PROJECT_ID}/pyspark-dbf-converter",
        name="dbf-to-parquet-conversion",
        arguments=["main.py"],
    )

    (
        start
        >> ftp_to_bronze
        >> bronze_to_silver
        >> silver_to_bq
        >> end
    )
