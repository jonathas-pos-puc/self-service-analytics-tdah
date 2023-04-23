# BRONZE TO SILVER
> Pega os dados da zona bronze, converte e salva na zona silver
*Sempre vai sobreescrever os arquivos na zona silver*

### Parametros
### Build e subir para o registry

```
PROJECT_ID=self-service-analytics-tdah
gcloud auth configure-docker
docker build -t bronze-to-silver:latest .
docker tag bronze-to-silver:latest "gcr.io/${PROJECT_ID}/bronze-to-silver:latest"
docker push "gcr.io/${PROJECT_ID}/bronze-to-silver:latest"
```

### Testar a imagem localmente
```
docker run --name test-img-latest bronze-to-silver:latest
```

