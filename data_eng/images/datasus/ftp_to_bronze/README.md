# FTP TO BRONZE
> Pega os dados do datasus no formato padrão DBC, que é compactado e salva no bucket da zona BRONZE do projeto.
*Sempre vai sobreescrever os arquivos na zona bronze*

### Parametros
* FONTE
    - Descrição: Origem dos dados do datasus
    - Valor default: SIASUS
    - Valores possiveis:
        - SIASUS, SIHSUS, ....

* EPOCA
    - Descrição: Epocas das versões das origems
    - Valor default: 200801_
    - Valores possiveis(para o SIASUS):
        - Anteriores_a_1994, 199407_200712, 200801_

* SISTEMA
    - Descrição: Tipo de arquivo a ser baixado, o layout muda de acordo com o tipo de arquivo
    - Valor default: PA
    - Valores possiveis(para o SIASUS):
        - AD, AM, AN, AQ, AR, AR, AB, ACP, ATD, SAD, PS, BI

* UF
    - Descrição: Estados das unidades de saude
    - Valor default: MG
    - Valores possiveis:
        - Todos os estados + DF

* DATA_COMECO
    - Descrição: Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2301), Janeiro de 2023
    - Valor default: Se não for passado, pega o mês atual
    - Valores possiveis(para o SIASUS):
        - Entre 0801 ate o mês atual

* DATA_TERMINO
    - Descrição: Data dos arquivos a serem baixados no formato YYMM(ano, e mes: 2302), Fev de 2023
    - Valor default: Se não for passado, pega o mês atual
    - Valores possiveis(para o SIASUS):
        - Entre 0801 ate o mês atual

### Build e subir para o registry

```
PROJECT_ID=self-service-analytics-tdah
gcloud auth configure-docker
docker build -t ftp-to-bronze:latest .
docker tag ftp-to-bronze:latest "gcr.io/${PROJECT_ID}/ftp-to-bronze:latest"
docker push "gcr.io/${PROJECT_ID}/ftp-to-bronze:latest"
```

### Testar a imagem localmente
```
docker run --name test-img-latest ftp-to-bronze:latest --DATA_COMECO=2301 --DATA_COMECO=2302
```

