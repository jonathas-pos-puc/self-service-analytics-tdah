import argparse
import io
import os
import re
from ftplib import FTP

import pandas as pd
from google.cloud import storage


def month_range(start, end):
    date_start = pd.to_datetime(start, format="%y%m")
    date_end = pd.to_datetime(end, format="%y%m")

    months = pd.date_range(date_start, date_end, freq="M")
    months = months.strftime("%y%m").tolist()

    return months


def get_ftp_files(ftp, path, sistema, uf, yymm_start, yymm_end):
    file_list = ftp.nlst(path)
    print(f"Primeiro arquivo FTP: {file_list[0]}")

    yymm_range = month_range(yymm_start, yymm_end)
    print(f"Primeiro month_range: {yymm_range}")

    print(f"Prefix: {sistema}{uf}")
    # Expressão regular para buscar os arquivos pelo padrão {SISTEMA}{UF}{YYMM}{letra}.dbc
    padrao = re.compile(rf"^{sistema}{uf}(\d{{2}}\d{{2}})\w?\.dbc$")

    # Filtra os arquivos pela expressão regular e pelos valores de YYMM desejados
    filtered_files = [
        arquivo
        for arquivo in file_list
        if padrao.match(os.path.basename(arquivo))
        and padrao.match(os.path.basename(arquivo)).group(1) in yymm_range
    ]
    return filtered_files


def get_ftp_file(ftp, ftp_path):
    # Criar um buffer de bytes em memória
    file_buffer = io.BytesIO()

    # Baixar o arquivo do FTP para o buffer
    ftp.retrbinary(f"RETR {ftp_path}", file_buffer.write)
    return file_buffer


def is_blob_exists(bucket, bucket_name, blob_name):
    blob = bucket.get_blob(blob_name)
    if blob:
        print(f"file found: {bucket_name}/{blob_name}")
        return True
    else:
        print(f"file not found: {bucket_name}/{blob_name}")
        return False


def upload_blob(file_buffer, bucket, bucket_name, blob_name):
    # Criar um novo blob e fazer upload do arquivo
    blob = bucket.blob(blob_name)
    file_buffer.seek(0)  # Resetar a posição do buffer
    blob.upload_from_file(file_buffer)
    file_buffer.close()
    print(f"ENVIADO PARA: {bucket_name}/{blob_name}")


def main(
    fonte="SIASUS",
    epoca="200801_",
    sistema="AD",
    uf="MG",
    data_comeco="2301",
    data_termino="2305",
):
    """Baixa arquivo ou arquivos do datasus e salva na zona bronze do projeto

    Args:
        fonte (str): Origem dos dados do datasus, Valor default: SIASUS
        epoca (str): Epocas das versões das origems, Valor default: 200801_
        sistema (str): Tipo de arquivo a ser baixado, o layout muda de acordo com o tipo de arquivo, Valor default: PA
        uf (str): Estados da unidade de saude
        data_comeco (str): Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023
        data_termino (str): Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023
    """

    OUTPUT_BUCKET_NAME = "self-service-analytics-tdah-bronze"
    FTP_HOST = "ftp.datasus.gov.br"
    ftp = FTP(FTP_HOST)
    ftp.login()

    storage_client = storage.Client.from_service_account_json("credentials.json")
    # storage_client = storage.Client()
    output_bucket = storage_client.get_bucket(OUTPUT_BUCKET_NAME)
    ftp_path = f"/dissemin/publicos/{fonte}/{epoca}/Dados/"
    print(f"ftp_path: {ftp_path}")

    ftp_files = get_ftp_files(ftp, ftp_path, sistema, uf, data_comeco, data_termino)
    print(f"Total de arquivos filtrados: {len(ftp_files)}")

    print("Inicio baixando arquivos")
    for filename in ftp_files:
        blob_name = os.path.basename(filename)
        gcs_blob_path = f"DATASUS/{blob_name}"
        print(f"filename: {filename}")
        print(f"gcs_blob_path: {gcs_blob_path}")
        if is_blob_exists(output_bucket, OUTPUT_BUCKET_NAME, gcs_blob_path):
            print(f"JA EXISTE: {gcs_blob_path}")
        else:
            ftp_file = get_ftp_file(ftp, filename)
            upload_blob(ftp_file, output_bucket, OUTPUT_BUCKET_NAME, gcs_blob_path)

    print("Fim baixando arquivos")


if __name__ == "__main__":
    # Validando se o file_name foi passado
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--FONTE",
        dest="fonte",
        default="SIASUS",
        help="Origem dos dados do datasus, Valor default: SIASUS",
    )

    parser.add_argument(
        "--EPOCA",
        dest="epoca",
        default="200801_",
        help="Epocas das versões das origems, Valor default: 200801_",
    )

    parser.add_argument(
        "--SISTEMA",
        dest="sistema",
        default="AD",
        help="Tipo de arquivo a ser baixado, o layout muda de acordo com o tipo de arquivo, Valor default: PA",
    )

    parser.add_argument(
        "--UF", dest="uf", default="MG", help="Estados da unidade de saude"
    )

    parser.add_argument(
        "--DATA_COMECO",
        dest="data_comeco",
        default="2301",
        help="Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023",
    )

    parser.add_argument(
        "--DATA_TERMINO",
        dest="data_termino",
        default="2305",
        help="Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023",
    )

    kargs, args = parser.parse_known_args()
    main(
        kargs.fonte,
        kargs.epoca,
        kargs.sistema,
        kargs.uf,
        kargs.data_comeco,
        kargs.data_termino,
    )
