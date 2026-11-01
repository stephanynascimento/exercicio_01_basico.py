import streamlit as st


st.set_page_config(
    page_title="Sistema de Biblioteca",
    page_icon="📚"
)


st.title("📚 Sistema de Biblioteca")

st.write(
    "Aplicação desenvolvida com Python, Neo4j e Streamlit."
)

st.success("O Streamlit está funcionando corretamente!")

st.header("Atividade")

st.write("Este projeto contém 15 questões sobre um sistema de biblioteca.")

questoes = [
    "Questão 01 - Criar livro",
    "Questão 02 - Criar autor",
    "Questão 03 - Criar relacionamento",
    "Questão 04 - Listar livros",
    "Questão 05 - Listar autores",
    "Questão 06 - Buscar livro por título",
    "Questão 07 - Atualizar páginas",
    "Questão 08 - Livros por gênero",
    "Questão 09 - Livros por autor",
    "Questão 10 - Usuários com empréstimos",
    "Questão 11 - Empréstimos pendentes",
    "Questão 12 - Deletar livro",
    "Questão 13 - Contar livros por autor",
    "Questão 14 - Livros após 1950",
    "Questão 15 - Livros disponíveis"
]

questao = st.selectbox(
    "Escolha uma questão:",
    questoes
)

st.write("Questão escolhida:")
st.info(questao)

if st.button("Executar questão"):
    st.success(f"{questao} selecionada com sucesso!")
