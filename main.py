import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from plot import plot 


engine = create_engine('mysql+pymysql://root:1337@localhost:3306/trabalho')

st.set_page_config(page_title="Dashboard", page_icon="resources/icon.png", layout="wide")

anos_query = "SELECT DISTINCT ano FROM dm_tempo ORDER BY ano"
anos = pd.read_sql(anos_query, engine)["ano"].tolist()
anos.insert(0, "Geral")
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos)


if ano_selecionado == "Geral":
    plot(st, engine, -1)
else:
    plot(st, engine, ano_selecionado)
    
    



   
