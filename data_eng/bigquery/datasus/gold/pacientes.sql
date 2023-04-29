CREATE TABLE `self-service-analytics-tdah.gold.pacientes` AS
SELECT
  p.id,
  p.cns,
  p.data_nascimento,
  p.tem_tdah,
  s.nome as sexo_id,
  r.nome as raca_id,
  m.nome as municipio_id,
  e.nome as etnia_id,
FROM
  `self-service-analytics-tdah.dw.d_pacientes` as p
LEFT JOIN `self-service-analytics-tdah.dw.d_sexos`        as s ON p.sexo_id = s.id
LEFT JOIN `self-service-analytics-tdah.dw.d_racas`        as r ON p.raca_id = s.id
LEFT JOIN `self-service-analytics-tdah.dw.d_munincipios`  as m ON p.municipio_id = s.id
LEFT JOIN `self-service-analytics-tdah.dw.d_etnias`       as e ON p.etnia_id = s.id
