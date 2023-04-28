CREATE TABLE `self-service-analytics-tdah.dw.f_boletim` (
  coduni INT64,
  gestao INT64,
  ufmun INT64,blcrea
  tpups INT64,
  tippre INT64,
  dt_pro INT64,
  cid INT64,
  tem_tdah BOOL,
);

CREATE TABLE `self-service-analytics-tdah.dw.f_boletim`
SELECT
  CODUNI as ,
  GESTAO as ,
  CASE
    WHEN cid LIKE 'F90%' THEN TRUE
    ELSE FALSE
  END AS tem_tdah
FROM
  `self-service-analytics-tdah.datasus.d`;
