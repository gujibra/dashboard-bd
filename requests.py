def query_exportadores(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT dp.nome AS pais, SUM(dt.valor) AS total_exportado
    FROM ft_lancamento fl
    JOIN dm_pais dp ON fl.id_pais_origem = dp.id_pais
    JOIN dm_transacao dt ON fl.id_transacao = dt.id_transacao
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    {filtro_ano}
    GROUP BY dp.nome
    ORDER BY total_exportado DESC
    LIMIT 25
    """

def query_produtos(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT dt.produto, SUM(dt.quantidade) AS total_quantidade
    FROM ft_lancamento fl
    JOIN dm_transacao dt ON fl.id_transacao = dt.id_transacao
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    {filtro_ano}
    GROUP BY dt.produto
    ORDER BY total_quantidade DESC
    LIMIT 25
    """

def query_blocos(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT dmt.ano, dp.bloco_economico, SUM(dtr.valor) AS total_comercio
    FROM ft_lancamento fl
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    JOIN dm_pais dp ON fl.id_pais_origem = dp.id_pais
    JOIN dm_transacao dtr ON fl.id_transacao = dtr.id_transacao
    {filtro_ano}
    GROUP BY dmt.ano, dp.bloco_economico
    ORDER BY dmt.ano, dp.bloco_economico
    """

def query_parceiros(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT dp1.nome AS pais_origem, dp2.nome AS pais_destino, SUM(dt.valor) AS total_comercio
    FROM ft_lancamento fl
    JOIN dm_pais dp1 ON fl.id_pais_origem = dp1.id_pais
    JOIN dm_pais dp2 ON fl.id_pais_destino = dp2.id_pais
    JOIN dm_transacao dt ON fl.id_transacao = dt.id_transacao
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    {filtro_ano}
    GROUP BY dp1.nome, dp2.nome
    ORDER BY total_comercio DESC
    LIMIT 25
    """


def query_transporte(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT dt.transporte, COUNT(*) AS total_transacoes
    FROM ft_lancamento fl
    JOIN dm_transacao dt ON fl.id_transacao = dt.id_transacao
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    {filtro_ano}
    GROUP BY dt.transporte
    ORDER BY total_transacoes DESC
    """

def query_cambio(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT 
        dc.data,
        dc.moeda_origem,
        dc.moeda_destino,
        dc.taxa_cambio,
        SUM(dt.valor) AS valor_comercio
    FROM ft_lancamento fl
    JOIN dm_cambio dc ON fl.id_cambio = dc.id_cambio
    JOIN dm_transacao dt ON fl.id_transacao = dt.id_transacao
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    {filtro_ano}
    GROUP BY dc.data, dc.moeda_origem, dc.moeda_destino, dc.taxa_cambio
    ORDER BY dc.data
    """

def query_valor_anual(ano):
    filtro_ano = f"WHERE dmt.ano = {ano}" if ano != -1 else ""
    return f"""
    SELECT 
        dmt.ano,
        SUM(CASE WHEN dtr.tipo_transacao = 'EXPORT' THEN dtr.valor ELSE 0 END) AS total_exportado,
        SUM(CASE WHEN dtr.tipo_transacao = 'IMPORT' THEN dtr.valor ELSE 0 END) AS total_importado
    FROM ft_lancamento fl
    JOIN dm_tempo dmt ON fl.id_tempo = dmt.id_tempo
    JOIN dm_transacao dtr ON fl.id_transacao = dtr.id_transacao
    {filtro_ano}
    GROUP BY dmt.ano
    ORDER BY dmt.ano
    """