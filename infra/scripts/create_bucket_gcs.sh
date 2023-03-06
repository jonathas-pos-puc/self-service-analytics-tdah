#!/bin/bash
set -xeuo pipefail

# Cria um bucket para receber os aquivos do source, para depois subir para o BQ

# Por Default o PROJECT_ID já é puxado quando vc tem o sdk configurado
# Mas como o projeto que trabalho é com GCP, realmente estou colocando um controle a mais
PROJECT_ID=self-service-analytics-tdah

# O Default já é o Standard, que no caso do teste é o mais interessante
# mas após o carregamento podemos mudar para outra classe se quisermos economizar e ter um backup
STORAGE_CLASS=standard

# E é uma das location que participa dos servicos gratis
BUCKET_LOCATION=us-east1

# Por boas praticas é interessante manter o nome do projeto no bucket, já que o id é global
BUCKET_ZONES=( bronze silver gold )

# Não vou informar nenhuma politica de --retention
# Comando para criar o bucket
BUCKET_NAME=${PROJECT_ID}-bronze
for zone in "${zones[@]}"
do
    gsutil mb -p ${PROJECT_ID}-${zone} -c ${STORAGE_CLASS} -l ${BUCKET_LOCATION} gs://${BUCKET_NAME}/
done

