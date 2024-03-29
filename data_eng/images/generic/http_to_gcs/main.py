# Imagem para baixar o arquivo HTTP e subir no GCS

import argparse
import sys

import requests
from google.cloud import storage


def download_file(endpoint, file_name):
    """
    Baixa o aquivo e salva no POD

    Args:
        endpoint (str): Url completa para baixar o arquivo
        file_name (str): Nome que o arquivo no POD
    """
    try:
        r = requests.get(endpoint)
        with open(file_name, "wb") as f:
            f.write(r.content)
    except requests.RequestException as e:
        raise SystemExit(e)


def upload_to_gcs(bucket_name, file_name):
    """
    Faz o upload do arquivo baixado para o GCS
    OBS: O upload é feito mantendo o nome original do arquivo

    Args:
        bucket_name (str): Nome do bucket para onde o arquivo deve ir
        file_name (str): Nome do arquivo
    """
    storage_client = storage.Client.from_service_account_json("credentials.json")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)


def main(endpoint, file_name, bucket_name):
    """
    Função principal que recebe o nome do arquivo via parametro

    Args:
        endpoint (str): endpoint
        file_name (str): Nome do arquivo
        bucket_name (str): Nome do bucket para onde o arquivo vai
    """

    # Baixando o aquivo para o POD
    download_file(endpoint, file_name)

    # Subindo o arquivo para o bucket
    upload_to_gcs(bucket_name, file_name)


if __name__ == "__main__":
    # Validando se o file_name foi passado
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", help="URL do arquivo que será baixado")

    parser.add_argument(
        "--file_name",
        dest="file_name",
        help="Nome do arquivo que será enviado para o bucket",
    )

    parser.add_argument(
        "--bucket_name",
        dest="bucket_name",
        help="Nome do bucket para onde o arquivo vai",
    )

    known_args, args = parser.parse_known_args()
    main(known_args.url, known_args.file_name, known_args.bucket_name)
