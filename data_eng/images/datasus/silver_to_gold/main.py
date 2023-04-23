import argparse
import os
import sys
from io import BytesIO, StringIO

import pandas as pd
import pyarrow
import pyarrow as pa
import requests
from google.cloud import bigquery, storage


def main():
    storage_client = storage.Client.from_service_account_json("credentials.json")
    bigquery_client = bigquery.Client.from_service_account_json("credentials.json")

    bucket_name = "self-service-analytics-tdah-silver"
    source_blob_name = "DATASUS/ADMG2301.parquet"
    dataset_id = "datasus"
    table_id = "siasus"

    # Buscar o arquivo Parquet do GCS
    bucket = storage_client.get_bucket(bucket_name)
    blob = storage.Blob(source_blob_name, bucket)
    content = blob.download_as_bytes()

    # Ler o arquivo Parquet usando o Pandas
    df = pd.read_parquet(BytesIO(content), engine="pyarrow")

    print(df.head())  # Exibe as primeiras linhas do DataFrame

    # Carregar o DataFrame do Pandas no BigQuery
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.PARQUET
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

    load_job = bigquery_client.load_table_from_dataframe(
        df, table_ref, job_config=job_config
    )
    load_job.result()  # Aguardar a conclusão do job

    print(f"Carregado {load_job.output_rows} linhas na tabela {dataset_id}.{table_id}.")


if __name__ == "__main__":
    # Validando se o file_name foi passado
    parser = argparse.ArgumentParser()
    main()
