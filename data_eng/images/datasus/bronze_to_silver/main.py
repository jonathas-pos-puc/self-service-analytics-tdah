import os
import tempfile
import argparse
from io import BytesIO

from google.cloud import storage
from pysus.utilities.readdbc import read_dbc


def dbc_to_dataframe(input_path):
    """Converte um arquivo DBC para Parquet."""
    data = read_dbc(input_path, encoding="iso-8859-1")
    return data


def list_files(bucket_name, client):
    bucket = client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs())
    return [blob.name for blob in blobs]


def convert_and_upload_parquet(bucket_name, blob_name, silver_bucket_name, client):
    bronze_bucket = client.get_bucket(bucket_name)
    silver_bucket = client.get_bucket(silver_bucket_name)
    blob = bronze_bucket.blob(blob_name)

    with tempfile.NamedTemporaryFile(suffix=".dbc", delete=False) as temp_dbc:
        blob.download_to_file(temp_dbc)
        temp_dbc.flush()

        df = dbc_to_dataframe(temp_dbc.name)

        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer)

        parquet_blob_name = blob_name.replace(".dbc", ".parquet")
        parquet_blob = silver_bucket.blob(parquet_blob_name)
        parquet_blob.upload_from_file(parquet_buffer, rewind=True)

        os.remove(temp_dbc.name)


def main(
    epoca,
    sistema,
    uf,
    data_comeco,
    data_termino,
):
    """Baixa arquivo ou arquivos do datasus e salva na zona bronze do projeto

    Args:
        epoca (str): Epocas das versões das origems, Valor default: 200801_
        sistema (str): Tipo de arquivo a ser baixado, o layout muda de acordo com o tipo de arquivo, Valor default: PA
        uf (str): Estados da unidade de saude
        data_comeco (str): Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023
        data_termino (str): Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023
    """

    INPUT_BUCKET_NAME = "self-service-analytics-tdah-bronze"
    OUTPUT_BUCKET_NAME = "self-service-analytics-tdah-silver"

    storage_client = storage.Client.from_service_account_json("credentials.json")

    bronze_files = list_files(INPUT_BUCKET_NAME, storage_client)
    silver_files = list_files(OUTPUT_BUCKET_NAME, storage_client)

    new_files = [
        file
        for file in bronze_files
        if file.replace(".dbc", ".parquet") not in silver_files
    ]

    print("new_files")
    print(new_files)

    for file in new_files:
        print(f"Convertendo e salvando o arquivo: {file}")
        convert_and_upload_parquet(
            INPUT_BUCKET_NAME, file, OUTPUT_BUCKET_NAME, storage_client
        )
        print(
            f"Arquivo {file} salvo como {file.replace('.dbc', '.parquet')} no bucket {OUTPUT_BUCKET_NAME}"
        )


if __name__ == "__main__":
    # Validando se o file_name foi passado
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--epoca",
        dest="epoca",
        help="Epocas das versões das origems, Valor default: 200801_",
    )

    parser.add_argument(
        "--sistema",
        dest="sistema",
        help="Tipo de arquivo a ser baixado, o layout muda de acordo com o tipo de arquivo, Valor default: PA",
    )

    parser.add_argument(
        "--uf", dest="uf",help="Estados da unidade de saude"
    )

    parser.add_argument(
        "--data_comeco",
        dest="data_comeco",
        help="Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023",
    )

    parser.add_argument(
        "--data_termino",
        dest="data_termino",
        help="Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023",
    )

    kargs, args = parser.parse_known_args()
    main(
        kargs.epoca,
        kargs.sistema,
        kargs.uf,
        kargs.data_comeco,
        kargs.data_termino,
    )

