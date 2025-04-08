from requests import *
import pandas as pd
import plotly.express as px

def plot(st, engine, ano):
    df_exportadores = pd.read_sql(query_exportadores(ano), engine)
    fig_exportadores_bar = px.bar(df_exportadores, x="pais", y="total_exportado", title="Países Exportadores", color_discrete_sequence=["#4774f5"])

    df_produtos = pd.read_sql(query_produtos(ano), engine)
    fig_produtos_treemap = px.treemap(df_produtos, path=["produto"], values="total_quantidade", title="Produtos por Volume", color_discrete_sequence=["#4774f5"])

    df_parceiros = pd.read_sql(query_parceiros(ano), engine)
    fig_parceiros_sunburst = px.sunburst(df_parceiros, path=["pais_origem", "pais_destino"], values="total_comercio", title="Principais Parceiros Comerciais", color_discrete_sequence=["#4774f5"])

    df_transporte = pd.read_sql(query_transporte(ano), engine)
    fig_transporte_pie = px.pie(df_transporte, names="transporte", values="total_transacoes", title="Distribuição por Transporte", color_discrete_sequence=["#4774f5"])


    df_valor_anual = pd.read_sql(query_valor_anual(ano), engine)
    fig_valor_anual = px.bar(df_valor_anual, x="ano", y=["total_exportado", "total_importado"], barmode="group", title="Importação vs Exportação por Ano", color_discrete_sequence=["#4774f5"])

    
    df_blocos = pd.read_sql(query_blocos(ano), engine)
    fig_blocos_line = px.line(df_blocos, x="ano", y="total_comercio", color="bloco_economico", title="Evolução do Comércio por Bloco Econômico", color_discrete_sequence=px.colors.qualitative.Set2)


    df_cambio = pd.read_sql(query_cambio(ano), engine)
    
    if not df_cambio.empty:
        fig_cambio_line = px.line(df_cambio, x="data", y="taxa_cambio", 
                                title="Variação das Taxas de Câmbio",
                                color_discrete_sequence=["#4774f5"])
        
        fig_cambio_comercio = px.scatter(df_cambio, x="taxa_cambio", y="valor_comercio",
                               title="Relação entre Câmbio e Comércio",
                               color_discrete_sequence=["#4774f5"])
        
        
        correlacao = df_cambio["taxa_cambio"].corr(df_cambio["valor_comercio"])
       

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_exportadores_bar, use_container_width=True)    
        st.plotly_chart(fig_valor_anual, use_container_width=True)      
        if(ano == -1):  
            st.plotly_chart(fig_cambio_line, use_container_width=True)
        st.plotly_chart(fig_transporte_pie, use_container_width=True)
        
   
    with col2:
        st.plotly_chart(fig_parceiros_sunburst, use_container_width=True)
        st.plotly_chart(fig_produtos_treemap, use_container_width=True)
        if(ano == -1):
            st.plotly_chart(fig_cambio_comercio, use_container_width=True) 
            st.plotly_chart(fig_blocos_line, use_container_width=True)
               
        
    
    if(ano == -1):
        st.metric(label="Correlação Câmbio-Comércio", 
                     value=f"{correlacao:.2f}",
                     help="Valores próximos de 1 indicam relação positiva, próximos de -1 relação negativa")
            
 
