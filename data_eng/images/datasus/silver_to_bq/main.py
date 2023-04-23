import argparse
import json
from datetime import datetime

from google.cloud import bigquery, storage


# Função para carregar arquivo parquet no BigQuery
def load_parquet_to_bigquery(bigquery_client, file_path, dataset_id):
    # Extrai o nome da tabela do nome do arquivo
    table_name = file_path.split("/")[-1].replace(".parquet", "")

    # Configura o job para carregar o arquivo parquet
    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.PARQUET)
    table_ref = bigquery_client.dataset(dataset_id).table(table_name)

    # Carrega o arquivo parquet na tabela
    with open(file_path, "rb") as source_file:
        job = bigquery_client.load_table_from_file(
            source_file, table_ref, job_config=job_config
        )

    job.result()
    print(
        f"Arquivo {file_path} carregado com sucesso no BigQuery na tabela {table_name}"
    )


def main(dataset_id):
    # Autenticação
    # Supondo que você tenha a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS configurada
    storage_client = storage.Client.from_service_account_json("credentials.json")
    bigquery_client = bigquery.Client.from_service_account_json("credentials.json")

    # Configurações
    bucket_name = "self-service-analytics-tdah-silver"
    control_file_name = "control_file.json"

    # Lendo arquivo de controle
    bucket = storage_client.get_bucket(bucket_name)
    control_blob = bucket.get_blob(control_file_name)

    if control_blob:
        control_data = json.loads(control_blob.download_as_text())
        last_loaded_timestamp = datetime.fromisoformat(
            control_data["last_loaded_timestamp"]
        )
    else:
        last_loaded_timestamp = datetime.min

    # Iterando pelos arquivos do bucket
    newest_timestamp = last_loaded_timestamp
    for blob in bucket.list_blobs():
        if blob.name.endswith(".parquet") and blob.updated > last_loaded_timestamp:
            file_path = f"/tmp/{blob.name}"
            blob.download_to_filename(file_path)
            load_parquet_to_bigquery(bigquery_client, file_path, dataset_id)

            if blob.updated > newest_timestamp:
                newest_timestamp = blob.updated

    # Atualizando arquivo de controle
    if newest_timestamp > last_loaded_timestamp:
        control_data = {"last_loaded_timestamp": newest_timestamp.isoformat()}
        if control_blob:
            control_blob.upload_from_string(json.dumps(control_data))
        else:
            control_blob = bucket.blob(control_file_name)
            control_blob.upload_from_string(json.dumps(control_data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carrega arquivos Parquet no BigQuery")
    parser.add_argument(
        "--dataset_id", dest="dataset_id", help="ID do dataset do BigQuery"
    )

    args = parser.parse_args()
    main(args.dataset_id)
