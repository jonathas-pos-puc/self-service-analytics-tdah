CREATE TABLE `self-service-analytics-tdah.gold.pacientes` AS
with pacientes AS (
SELECT
  p.id,
  p.cns,
  p.data_nascimento,
  p.data_processamento,
  p.cid,
  p.tem_tdah,
  s.codigo as sexo,
  r.nome as raca,
  m.nome as municipio,
  e.nome as etnia,
  ROW_NUMBER() OVER (PARTITION BY p.id ORDER BY p.data_processamento DESC) AS rn
FROM
  `self-service-analytics-tdah.dw.d_pacientes` as p
LEFT JOIN `self-service-analytics-tdah.dw.d_sexos`        as s ON p.sexo_id = s.id
LEFT JOIN `self-service-analytics-tdah.dw.d_racas`        as r ON p.raca_id = s.id
LEFT JOIN `self-service-analytics-tdah.dw.d_munincipios`  as m ON p.municipio_id = s.id
LEFT JOIN `self-service-analytics-tdah.dw.d_etnias`       as e ON p.etnia_id = s.id
)
select * except(rn) from pacientes WHERE rn = 1;