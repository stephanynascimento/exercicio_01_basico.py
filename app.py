import streamlit as st
from neo4j import GraphDatabase

st.set_page_config(
    page_title="Teste Neo4j",
    page_icon="🔌"
)

st.title("Teste de conexão com o Neo4j Aura")

try:
    uri = st.secrets["NEO4J_URI"]
    usuario = st.secrets["NEO4J_USER"]
    senha = st.secrets["NEO4J_PASSWORD"]

    st.write("Endereço utilizado:", uri)
    st.write("Usuário utilizado:", usuario)
    st.write("Senha carregada:", "Sim")

    driver = GraphDatabase.driver(
        uri,
        auth=(usuario, senha)
    )

    driver.verify_connectivity()

    st.success("Conexão realizada com sucesso!")

except Exception as erro:
    st.error("Falha na conexão.")
    st.code(str(erro))
