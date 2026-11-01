import streamlit as st
from neo4j import GraphDatabase


st.set_page_config(
    page_title="Sistema de Biblioteca",
    page_icon="📚",
    layout="wide"
)


@st.cache_resource
def criar_driver():
    try:
        uri = st.secrets["NEO4J_URI"]
        usuario = st.secrets["NEO4J_USER"]
        senha = st.secrets["NEO4J_PASSWORD"]
    except KeyError as erro:
        raise Exception(
            f"Secret ausente no Streamlit: {erro}"
        )

    driver = GraphDatabase.driver(
        uri,
        auth=(usuario, senha)
    )

    driver.verify_connectivity()
    return driver


try:
    driver = criar_driver()
except Exception as erro:
    st.error("Não foi possível conectar ao Neo4j Aura.")
    st.error(f"Detalhes do erro: {erro}")
    st.stop()


st.title("📚 Sistema de Biblioteca")
st.success("Conexão com o Neo4j Aura estabelecida com sucesso!")
