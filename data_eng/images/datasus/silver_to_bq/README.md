# SILVER TO BQ
>

### Parametros

### Build e subir para o registry

```
PROJECT_ID=self-service-analytics-tdah
gcloud auth configure-docker
docker build -t silver-to-bq:latest .
docker tag silver-to-bq:latest "gcr.io/${PROJECT_ID}/silver-to-bq:latest"
docker push "gcr.io/${PROJECT_ID}/silver-to-bq:latest"
```

### Testar a imagem localmente
```
docker run --name test-img-latest silver-to-bq:latest
```

