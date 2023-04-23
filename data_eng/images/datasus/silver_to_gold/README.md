# SILVER TO GOLD
>

### Parametros

### Build e subir para o registry

```
PROJECT_ID=self-service-analytics-tdah
gcloud auth configure-docker
docker build -t silver-to-gold:latest .
docker tag silver-to-gold:latest "gcr.io/${PROJECT_ID}/silver-to-gold:latest"
docker push "gcr.io/${PROJECT_ID}/silver-to-gold:latest"
```

### Testar a imagem localmente
```
docker run --name test-img-latest silver-to-gold:latest
```

