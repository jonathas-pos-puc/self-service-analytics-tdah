CREATE TABLE `self-service-analytics-tdah.gold.boletim_individualizado` AS
SELECT
  b.id_cnes as unidade_atentimento,
  b.gestao,
  m.nome as municipio_estabelecimento,
  u.nome as tipo_estabelecimento,
  p.nome as tipo_prestador,
  b.data_processamento,
  b.data_atendimento,
  b.cod_procedimento,
  f.nome as tipo_financiamento,
  b.cns_profissional,
  o.codigo as cbo,
  o.nome as cbo_descricao,
  c.descricao as cid_descricao,
  c.codigo as cid,
  b.cns_paciente,
  b.idade_paciente,
  b.quantidade_produzida,
  b.quantidade_aprovada,
  b.valor_produzido,
  b.valor_aprovado,
FROM
  `self-service-analytics-tdah.dw.f_boletim` as b
LEFT JOIN `self-service-analytics-tdah.gold.pacientes`             as a ON b.cns_paciente = a.cns
LEFT JOIN `self-service-analytics-tdah.dw.d_munincipios`           as m ON b.municipio_estabelecimento_id = m.id
LEFT JOIN `self-service-analytics-tdah.dw.d_cids`                  as c ON b.cid_id = c.id
LEFT JOIN `self-service-analytics-tdah.dw.d_tipo_estabelecimentos` as u ON b.tipo_estabelecimento_id = u.id
LEFT JOIN `self-service-analytics-tdah.dw.d_tipo_prestadores`      as p ON b.tipo_prestadore_id = p.id
LEFT JOIN `self-service-analytics-tdah.dw.d_tipo_financiamentos`   as f ON b.tipo_financiamento_id = f.id
LEFT JOIN `self-service-analytics-tdah.dw.d_cbos`                  as o ON b.cbo_id = o.id