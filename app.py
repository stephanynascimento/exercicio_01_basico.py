import streamlit as st
from neo4j import GraphDatabase

st.set_page_config(
    page_title="Biblioteca Neo4j",
    page_icon="📚"
)


@st.cache_resource
def criar_driver():
    uri = st.secrets["NEO4J_URI"]
    usuario = st.secrets["NEO4J_USER"]
    senha = st.secrets["NEO4J_PASSWORD"]

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
    st.code(str(erro))
    st.stop()


# A partir daqui entram:
# setup_database()
# questao_01()
# questao_02()
# ...
# interface do Streamlit
