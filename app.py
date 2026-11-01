import streamlit as st
from neo4j import GraphDatabase

st.set_page_config(
    page_title="Sistema de Biblioteca",
    page_icon="📚"
)


@st.cache_resource
def criar_driver():
    driver = GraphDatabase.driver(
        st.secrets["NEO4J_URI"],
        auth=(
            st.secrets["NEO4J_USER"],
            st.secrets["NEO4J_PASSWORD"]
        )
    )

    driver.verify_connectivity()
    return driver


try:
    driver = criar_driver()
    st.success("Conectado ao Neo4j Aura!")
except Exception as erro:
    st.error("Não foi possível conectar ao Neo4j Aura.")
    st.code(str(erro))
    st.stop()
