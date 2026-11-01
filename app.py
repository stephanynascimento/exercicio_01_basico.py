import streamlit as st
import exercicio_01_basico as biblioteca


st.set_page_config(
    page_title="Sistema de Biblioteca",
    page_icon="📚"
)

st.title("📚 Sistema de Biblioteca")
st.write("Atividade com Python, Neo4j e Streamlit.")


if st.button("Inicializar banco de dados", use_container_width=True):
    try:
        biblioteca.setup_database()
        st.success("Banco de dados inicializado com sucesso.")
    except Exception as erro:
        st.error(f"Erro ao inicializar o banco: {erro}")


st.divider()


if st.button("Executar todas as questões", use_container_width=True):
    try:
        biblioteca.questao_01_criar_livro()
        biblioteca.questao_02_criar_autor()
        biblioteca.questao_03_criar_relacionamento()
        biblioteca.questao_04_listar_livros()
        biblioteca.questao_05_listar_autores()
        biblioteca.questao_06_buscar_livro_por_titulo()
        biblioteca.questao_07_atualizar_paginas()
        biblioteca.questao_08_livros_por_genero()
        biblioteca.questao_09_livros_por_autor()
        biblioteca.questao_10_usuarios_com_emprestimos()
        biblioteca.questao_11_emprestimos_pendentes()
        biblioteca.questao_12_deletar_livro()
        biblioteca.questao_13_contar_livros_por_autor()
        biblioteca.questao_14_livros_apos_1950()
        biblioteca.questao_15_marcar_livros_disponiveis()

        st.success("Todas as questões foram executadas com sucesso.")

    except Exception as erro:
        st.error(f"Erro durante a execução: {erro}")


st.info(
    "O Neo4j precisa estar em execução em bolt://localhost:7687 "
    "com a senha configurada no arquivo exercicio_01_basico.py."
)
