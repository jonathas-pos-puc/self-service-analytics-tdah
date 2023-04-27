from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.kubernetes_engine import (
    GKECreateClusterOperator,
    GKEDeleteClusterOperator,
    GKEStartPodOperator,
)

GCP_PROJECT_ID = Variable.get("gcp_project_id")
GKE_LOCATION = Variable.get("gke_location")
GKE_CLUSTER_NAME = Variable.get("gke_cluster_name")

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

    create_cluster = GKECreateClusterOperator(
        task_id="create_cluster",
        project_id=GCP_PROJECT_ID,
        location=GKE_LOCATION,
        cluster_name=GKE_CLUSTER_NAME,
        body={
            "cluster": {
                "name": GKE_CLUSTER_NAME,
                "initial_node_count": 1,
                "node_config": {
                    "machine_type": "n1-standard-1",
                    "oauth_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
                },
                "addons_config": {
                    "http_load_balancing": {},
                    "horizontal_pod_autoscaling": {},
                    "network_policy_config": {"disabled": True},
                },
            }
        },
        dag=dag,
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

    delete_cluster = GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id=GCP_PROJECT_ID,
        name=GKE_CLUSTER_NAME,
        location=GKE_LOCATION,
        trigger_rule="all_done",  # This ensures the cluster is deleted even if the conversion task fails
        dag=dag,
    )

    (
        start
        >> create_cluster
        >> ftp_to_bronze
        >> bronze_to_silver
        >> silver_to_bq
        >> delete_cluster
        >> end
    )
