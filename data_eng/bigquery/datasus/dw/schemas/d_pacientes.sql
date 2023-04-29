CREATE TABLE `self-service-analytics-tdah.dw.d_pacientes` AS
with pacientes AS (
SELECT
  distinct FARM_FINGERPRINT(d.CNS_PAC) as id,
  d.CNS_PAC as cns,
  d.DT_PROCESS as data_processamento,
  s.id as sexo_id,
  r.id as raca_id,
  m.id as municipio_id,
  e.id as etnia_id,
  d.CIDPRI as cid,
  COALESCE(
    SAFE.PARSE_DATE('%y%m%d', d.DTNASC),
    SAFE.PARSE_DATE('%Y%m%d', d.DTNASC),
    SAFE.PARSE_DATE('%y%m%e', d.DTNASC),
    SAFE.PARSE_DATE('%Y%m%e', d.DTNASC)
  ) AS data_nascimento,
  CASE
    WHEN d.CIDPRI LIKE '0000' THEN "CID Inválido"
    WHEN d.CIDPRI LIKE 'F90%' THEN "SIM"
    ELSE "NÃO"
  END AS tem_tdah,
  ROW_NUMBER() OVER (PARTITION BY d.CNS_PAC ORDER BY d.DT_PROCESS DESC) AS rn
FROM
  `self-service-analytics-tdah.datasus.d` as d
LEFT JOIN `self-service-analytics-tdah.dw.d_sexos`       as s ON d.SEXOPAC = s.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_racas`       as r ON d.RACACOR = r.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_munincipios`  as m ON d.MUNPAC = CAST(m.codigo AS STRING)
LEFT JOIN `self-service-analytics-tdah.dw.d_etnias`      as e ON d.ETNIA = e.codigo
)
select * except(rn) from pacientes WHERE rn = 1;