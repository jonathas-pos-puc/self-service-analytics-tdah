CREATE TABLE `self-service-analytics-tdah.dw.f_boletim` AS
SELECT
  d.CODUNI as id_cnes,
  d.GESTAO as gestao,
  m.id as municipio_estabelecimento_id,
  u.id as tipo_estabelecimento_id,
  p.id as tipo_prestadore_id,
  d.DT_PROCESS as data_processamento,
  d.DT_ATEND as data_atendimento,
  d.PROC_ID as cod_procedimento,
  f.id as tipo_financiamento_id,
  d.CNSPROF as cns_profissional,
  o.id as cbo_id,
  c.id as cid_id,
  d.CNS_PAC as cns_paciente,
  d.IDADEPAC as idade_paciente,
  d.QT_APRES as quantidade_produzida,
  d.QT_APROV as quantidade_aprovada,
  d.VL_APRES as valor_produzido,
  d.VL_APROV as valor_aprovado,
FROM
  `self-service-analytics-tdah.datasus.d` as d
LEFT JOIN `self-service-analytics-tdah.dw.d_munincipios`           as m ON d.UFMUN = CAST(m.codigo AS STRING)
LEFT JOIN `self-service-analytics-tdah.dw.d_cids`                  as c ON d.CIDPRI = c.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_tipo_estabelecimentos` as u ON d.TPUPS = u.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_tipo_prestadores`      as p ON d.TIPPRE = p.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_tipo_financiamentos`   as f ON d.TPFIN = f.codigo
LEFT JOIN `self-service-analytics-tdah.dw.d_cbos`                  as o ON d.CBOPROF = o.codigo




