import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import time


st.set_page_config(
    page_title="Dashboard de Temperaturas IoT",
    page_icon="🌡️",
    layout="wide"
)

DB_PASSWORD = '33131580' # <-- TROQUE AQUI PELA SUA SENHA
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/postgres"

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados: {e}")
    st.stop()

@st.cache_data(ttl=600) # Cache de 10 minutos
def load_data(view_name):
    """ Carrega dados de uma view específica do banco de dados. """
    try:
        query = f"SELECT * FROM {view_name};"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Não foi possível carregar os dados da view '{view_name}': {e}")
        return pd.DataFrame() 

st.title("🌡️ Dashboard de Monitoramento de Temperaturas IoT")


df_avg_temp = load_data('avg_temp_por_dispositivo')
df_leituras_hora = load_data('leituras_por_hora')
df_temp_max_min = load_data('temp_max_min_por_dia')

if not df_avg_temp.empty and not df_leituras_hora.empty and not df_temp_max_min.empty:

    st.header("Média de Temperatura por Dispositivo")
    fig1 = px.bar(
        df_avg_temp,
        x='device_id',
        y='avg_temp',
        title='Temperatura Média (°C) por Dispositivo',
        labels={'device_id': 'Identificação do Dispositivo', 'avg_temp': 'Temperatura Média (°C)'},
        color='avg_temp',
        color_continuous_scale=px.colors.sequential.YlOrRd
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.header("Leituras por Hora do Dia")
    fig2 = px.line(
        df_leituras_hora.sort_values(by='hora'),
        x='hora',
        y='contagem',
        title='Volume de Leituras de Temperatura por Hora',
        markers=True,
        labels={'hora': 'Hora do Dia (24h)', 'contagem': 'Número de Leituras'}
    )
    st.plotly_chart(fig2, use_container_width=True)


    st.header("Variação Diária de Temperatura")
    df_temp_melted = df_temp_max_min.melt(
        id_vars='data',
        value_vars=['temp_max', 'temp_min'],
        var_name='Tipo de Temperatura',
        value_name='Temperatura (°C)'
    )
    fig3 = px.line(
        df_temp_melted,
        x='data',
        y='Temperatura (°C)',
        color='Tipo de Temperatura',
        title='Temperaturas Máximas e Mínimas Registradas por Dia',
        markers=True,
        labels={'data': 'Data', 'value': 'Temperatura (°C)'}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Dashboard carregado com sucesso!")

else:
    st.warning("Um ou mais conjuntos de dados não puderam ser carregados. Verifique as views no banco de dados e a conexão.")