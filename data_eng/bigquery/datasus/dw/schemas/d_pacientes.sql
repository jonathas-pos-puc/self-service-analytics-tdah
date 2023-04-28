CREATE TABLE `self-service-analytics-tdah.dw.d_pacientes` AS
SELECT
  distinct FARM_FINGERPRINT(d.CNS_PAC) as id,
  d.CNS_PAC as cns,
  s.id as sexo_id,
  r.id as raca_id,
  m.id as municipio_id,
  e.id as etnia_id,
  c.id as cid_id,
  SAFE.PARSE_DATE('%y%m%d', d.DTNASC) AS data_nascimento,
  CASE
    WHEN d.CIDPRI LIKE 'F90%' THEN TRUE
    ELSE FALSE
  END AS tem_tdah,
FROM
  `self-service-analytics-tdah.datasus.d` as d
LEFT JOIN `self-service-analytics-tdah.dw.d_sexos`       as s ON d.SEXOPAC = s.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_racas`       as r ON d.RACACOR = r.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_munincipios`  as m ON d.MUNPAC = CAST(m.codigo AS STRING)
LEFT JOIN `self-service-analytics-tdah.dw.d_etnias`      as e ON d.ETNIA = e.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_cids`        as c ON d.CIDPRI = c.codigo
