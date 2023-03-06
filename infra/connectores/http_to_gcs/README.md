# HTTP_TO_GCS
> Imagem que baixa um arquivo e salva no bucket do projeto

### Parametros
* filename
* bucket

kubectl create secret generic service-account-credentials --from-file=key.json=/secrets/credentials.json

### Build e subir para o registry

```
PROJECT_ID=self-service-analytics-tdah
gcloud auth configure-docker
docker build -t http-to-gcs:latest .
docker tag http-to-gcs:latest "gcr.io/${PROJECT_ID}/http-to-gcs:latest"
docker push "gcr.io/${PROJECT_ID}/http-to-gcs:latest"
```

### Testar a imagem localmente
```
docker run --name test-img-latest http-to-gcs:latest --file_name=file.csv --bucket_name=self-service-analytics-tdah-lake-bronze
```

