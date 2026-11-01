import streamlit as st
from neo4j import GraphDatabase


st.set_page_config(
    page_title="Sistema de Biblioteca",
    page_icon="📚"
)


URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "password"


@st.cache_resource
def conectar_banco():
    return GraphDatabase.driver(
        URI,
        auth=(USUARIO, SENHA)
    )


def executar_consulta(consulta, parametros=None):
    driver = conectar_banco()

    with driver.session() as session:
        resultado = session.run(
            consulta,
            parametros or {}
        )

        return [registro.data() for registro in resultado]


st.title("📚 Sistema de Biblioteca")

st.write("Consultas do banco de dados Neo4j")


if st.button("Inicializar banco de dados"):
    try:
        executar_consulta("MATCH (n) DETACH DELETE n")

        executar_consulta(
            """
            CREATE
              (a:Autor {nome: 'Machado de Assis', nacionalidade: 'Brasileiro'}),
              (a2:Autor {nome: 'Clarice Lispector', nacionalidade: 'Brasileira'}),
              (a3:Autor {nome: 'George Orwell', nacionalidade: 'Britânico'}),

              (l1:Livro {
                  titulo: 'Dom Casmurro',
                  ano: 1899,
                  genero: 'Romance',
                  paginas: 256
              }),

              (l2:Livro {
                  titulo: 'A Hora da Estrela',
                  ano: 1977,
                  genero: 'Romance',
                  paginas: 88
              }),

              (l3:Livro {
                  titulo: '1984',
                  ano: 1949,
                  genero: 'Distopia',
                  paginas: 328
              }),

              (l4:Livro {
                  titulo: 'Memórias Póstumas de Brás Cubas',
                  ano: 1881,
                  genero: 'Romance',
                  paginas: 280
              }),

              (a)-[:ESCREVEU]->(l1),
              (a2)-[:ESCREVEU]->(l2),
              (a3)-[:ESCREVEU]->(l3),
              (a)-[:ESCREVEU]->(l4)
            """
        )

        st.success("Banco inicializado com sucesso!")

    except Exception as erro:
        st.error(f"Erro ao conectar ao Neo4j: {erro}")


st.divider()


if st.button("Listar livros"):
    try:
        livros = executar_consulta(
            """
            MATCH (l:Livro)
            RETURN l.titulo AS titulo,
                   l.ano AS ano,
                   l.genero AS genero,
                   l.paginas AS paginas
            ORDER BY l.titulo
            """
        )

        if livros:
            st.dataframe(
                livros,
                use_container_width=True
            )
        else:
            st.warning("Nenhum livro foi encontrado.")

    except Exception as erro:
        st.error(f"Erro ao buscar livros: {erro}")
