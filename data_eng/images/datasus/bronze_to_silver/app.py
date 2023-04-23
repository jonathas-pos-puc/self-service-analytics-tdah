import argparse
from io import BytesIO, StringIO

import pandas as pd
from dbfread import DBF
from google.cloud import storage


def list_files(bucket_name, client):
    """_summary_

    Args:
        bucket_name (_type_): _description_
        client (_type_): _description_

    Returns:
        _type_: _description_
    """
    bucket = client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs())
    return [blob.name for blob in blobs]


def convert_and_upload_parquet(bucket_name, blob_name, silver_bucket_name, client):
    """_summary_

    Args:
        bucket_name (_type_): _description_
        blob_name (_type_): _description_
        silver_bucket_name (_type_): _description_
        client (_type_): _description_
    """
    bronze_bucket = client.get_bucket(bucket_name)
    silver_bucket = client.get_bucket(silver_bucket_name)
    blob = bronze_bucket.blob(blob_name)

    dbf_data = blob.download_as_text()

    table = DBF(StringIO(dbf_data), load=True)
    df = pd.DataFrame(iter(table))

    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer)

    parquet_blob_name = blob_name.replace(".dbc", ".parquet")
    parquet_blob = silver_bucket.blob(parquet_blob_name)
    parquet_blob.upload_from_file(parquet_buffer, rewind=True)


def main():
    INPUT_BUCKET_NAME = "self-service-analytics-tdah-bronze"
    OUTPUT_BUCKET_NAME = "self-service-analytics-tdah-silver"

    storage_client = storage.Client.from_service_account_json("credentials.json")

    bronze_files = list_files(INPUT_BUCKET_NAME, storage_client)
    print("bronze_files")
    print(bronze_files)

    silver_files = list_files(OUTPUT_BUCKET_NAME, storage_client)
    print("silver_files")
    print(silver_files)

    new_files = [
        file
        for file in bronze_files
        if file.replace(".dbc", ".parquet") not in silver_files
    ]

    for file in new_files:
        print(f"Convertendo e salvando o arquivo: {file}")
        convert_and_upload_parquet(
            INPUT_BUCKET_NAME, file, OUTPUT_BUCKET_NAME, storage_client
        )
        print(
            f"Arquivo {file} salvo como {file.replace('.dbc', '.parquet')} no bucket {OUTPUT_BUCKET_NAME}"
        )


if __name__ == "__main__":
    main()
