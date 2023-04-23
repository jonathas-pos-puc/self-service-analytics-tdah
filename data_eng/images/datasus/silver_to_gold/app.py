import argparse
import os
import sys

import pandas as pd
import pyarrow as pa
import requests
from google.cloud import storage


def convert_csv_to_parquet(csv_path, parquet_path):
    df = pd.read_csv(csv_path)
    table = pa.Table.from_pandas(df)
    pa.parquet.write_table(table, parquet_path)


def main(input_blob_name, output_blob_name):
    """_summary_

    Args:
        input_blob_name (str): _description_
        output_blob_name (str): _description_
    """

    input_bucket_name = "self-service-analytics-tdah-silver"
    output_bucket_name = "self-service-analytics-tdah-gold"

    storage_client = storage.Client.from_service_account_json("credentials.json")
    input_bucket = storage_client.get_bucket(input_bucket_name)
    output_bucket = storage_client.get_bucket(output_bucket_name)

    input_blob = input_bucket.get_blob(input_blob_name)
    if not input_blob:
        print(f"Input file not found: {input_bucket_name}/{input_blob_name}")
        sys.exit(1)

    csv_data = input_blob.download_as_text()
    with open("temp.csv", "w") as f:
        f.write(csv_data)

    convert_csv_to_parquet("temp.csv", "temp.parquet")

    with open("temp.parquet", "rb") as f:
        output_blob = output_bucket.blob(output_blob_name)
        output_blob.upload_from_file(f)

    print(f"File converted and uploaded to: {output_bucket_name}/{output_blob_name}")


if __name__ == "__main__":
    # Validando se o file_name foi passado
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_blob", dest="input_blob", help="input_blob")

    parser.add_argument("--output_blob", dest="output_blob", help="output_blob")

    known_args, args = parser.parse_known_args()
    main(known_args.input_blob, known_args.output_blob)
