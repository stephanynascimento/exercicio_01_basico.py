import streamlit as st
from neo4j import GraphDatabase


# ==============================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================

st.set_page_config(
    page_title="Biblioteca Neo4j",
    page_icon="📚",
    layout="wide"
)


# ==============================================================
# CONEXÃO COM O NEO4J AURA
# ==============================================================

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


# ==============================================================
# FUNÇÕES AUXILIARES
# ==============================================================

def executar_consulta(consulta, parametros=None):
    with driver.session() as session:
        resultado = session.run(
            consulta,
            parametros or {}
        )
        return [registro.data() for registro in resultado]


def executar_comando(consulta, parametros=None):
    with driver.session() as session:
        resultado = session.run(
            consulta,
            parametros or {}
        )
        resumo = resultado.consume()
        return resumo


# ==============================================================
# SETUP - POPULA O BANCO
# ==============================================================

def setup_database():
    consulta = """
    MATCH (n)
    DETACH DELETE n
    """

    executar_comando(consulta)

    consulta_criacao = """
    CREATE
      (a:Autor {
          nome: 'Machado de Assis',
          nacionalidade: 'Brasileiro'
      }),

      (a2:Autor {
          nome: 'Clarice Lispector',
          nacionalidade: 'Brasileira'
      }),

      (a3:Autor {
          nome: 'George Orwell',
          nacionalidade: 'Britânico'
      }),

      (a4:Autor {
          nome: 'Gabriel García Márquez',
          nacionalidade: 'Colombiano'
      }),

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

      (l5:Livro {
          titulo: 'Cem Anos de Solidão',
          ano: 1967,
          genero: 'Realismo Mágico',
          paginas: 448
      }),

      (l6:Livro {
          titulo: 'A Paixão Segundo G.H.',
          ano: 1964,
          genero: 'Romance',
          paginas: 180
      }),

      (l7:Livro {
          titulo: 'A Revolução dos Bichos',
          ano: 1945,
          genero: 'Fábula',
          paginas: 112
      }),

      (u1:Usuario {
          nome: 'Ana Silva',
          email: 'ana@email.com',
          idade: 28
      }),

      (u2:Usuario {
          nome: 'Bruno Costa',
          email: 'bruno@email.com',
          idade: 35
      }),

      (u3:Usuario {
          nome: 'Carla Mendes',
          email: 'carla@email.com',
          idade: 22
      }),

      (u4:Usuario {
          nome: 'Diego Rocha',
          email: 'diego@email.com',
          idade: 41
      }),

      (a)-[:ESCREVEU]->(l1),
      (a)-[:ESCREVEU]->(l4),
      (a2)-[:ESCREVEU]->(l2),
      (a2)-[:ESCREVEU]->(l6),
      (a3)-[:ESCREVEU]->(l3),
      (a3)-[:ESCREVEU]->(l7),
      (a4)-[:ESCREVEU]->(l5),

      (u1)-[:EMPRESTOU {
          data: '2024-01-10',
          devolvido: true
      }]->(l1),

      (u1)-[:EMPRESTOU {
          data: '2024-03-15',
          devolvido: false
      }]->(l3),

      (u2)-[:EMPRESTOU {
          data: '2024-02-20',
          devolvido: true
      }]->(l2),

      (u2)-[:EMPRESTOU {
          data: '2024-04-01',
          devolvido: false
      }]->(l5),

      (u3)-[:EMPRESTOU {
          data: '2024-01-25',
          devolvido: true
      }]->(l4),

      (u4)-[:EMPRESTOU {
          data: '2024-03-30',
          devolvido: false
      }]->(l7),

      (u1)-[:AVALIOU {nota: 5}]->(l1),
      (u2)-[:AVALIOU {nota: 4}]->(l2),
      (u3)-[:AVALIOU {nota: 5}]->(l4),
      (u4)-[:AVALIOU {nota: 3}]->(l3)
    """

    executar_comando(consulta_criacao)


# ==============================================================
# QUESTÃO 01
# ==============================================================

def questao_01():
    consulta = """
    CREATE (livro:Livro {
        titulo: 'O Cortiço',
        ano: 1890,
        genero: 'Naturalismo',
        paginas: 320
    })
    RETURN livro
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 02
# ==============================================================

def questao_02():
    consulta = """
    CREATE (autor:Autor {
        nome: 'Aluísio Azevedo',
        nacionalidade: 'Brasileiro'
    })
    RETURN autor
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 03
# ==============================================================

def questao_03():
    consulta = """
    MATCH (autor:Autor {nome: 'Aluísio Azevedo'})
    MATCH (livro:Livro {titulo: 'O Cortiço'})
    CREATE (autor)-[rel:ESCREVEU]->(livro)
    RETURN autor.nome AS autor,
           livro.titulo AS livro,
           type(rel) AS relacionamento
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 04
# ==============================================================

def questao_04():
    consulta = """
    MATCH (livro:Livro)
    RETURN livro.titulo AS titulo,
           livro.ano AS ano,
           livro.genero AS genero
    ORDER BY livro.titulo
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 05
# ==============================================================

def questao_05():
    consulta = """
    MATCH (autor:Autor)
    RETURN autor.nome AS nome,
           autor.nacionalidade AS nacionalidade
    ORDER BY autor.nome
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 06
# ==============================================================

def questao_06():
    consulta = """
    MATCH (livro:Livro {titulo: $titulo})
    RETURN livro.titulo AS titulo,
           livro.ano AS ano,
           livro.genero AS genero,
           livro.paginas AS paginas
    """

    return executar_consulta(
        consulta,
        {"titulo": "Dom Casmurro"}
    )


# ==============================================================
# QUESTÃO 07
# ==============================================================

def questao_07():
    consulta = """
    MATCH (livro:Livro {titulo: '1984'})
    SET livro.paginas = 340
    RETURN livro.titulo AS titulo,
           livro.paginas AS paginas
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 08
# ==============================================================

def questao_08():
    consulta = """
    MATCH (livro:Livro)
    WHERE livro.genero = $genero
    RETURN livro.titulo AS titulo,
           livro.ano AS ano
    ORDER BY livro.ano
    """

    return executar_consulta(
        consulta,
        {"genero": "Romance"}
    )


# ==============================================================
# QUESTÃO 09
# ==============================================================

def questao_09():
    consulta = """
    MATCH (autor:Autor)-[:ESCREVEU]->(livro:Livro)
    WHERE autor.nome = $autor
    RETURN livro.titulo AS titulo
    ORDER BY livro.titulo
    """

    return executar_consulta(
        consulta,
        {"autor": "Machado de Assis"}
    )


# ==============================================================
# QUESTÃO 10
# ==============================================================

def questao_10():
    consulta = """
    MATCH (usuario:Usuario)-[:EMPRESTOU]->(livro:Livro)
    RETURN usuario.nome AS usuario,
           livro.titulo AS livro
    ORDER BY usuario.nome, livro.titulo
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 11
# ==============================================================

def questao_11():
    consulta = """
    MATCH (usuario:Usuario)-[emprestimo:EMPRESTOU]->(livro:Livro)
    WHERE emprestimo.devolvido = false
    RETURN usuario.nome AS usuario,
           livro.titulo AS livro,
           emprestimo.data AS data
    ORDER BY emprestimo.data
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 12
# ==============================================================

def questao_12():
    consulta = """
    MATCH (livro:Livro {titulo: 'O Cortiço'})
    DETACH DELETE livro
    """

    executar_comando(consulta)

    return [
        {
            "mensagem": "O livro O Cortiço foi excluído."
        }
    ]


# ==============================================================
# QUESTÃO 13
# ==============================================================

def questao_13():
    consulta = """
    MATCH (autor:Autor)-[:ESCREVEU]->(livro:Livro)
    RETURN autor.nome AS autor,
           count(livro) AS total_livros
    ORDER BY total_livros DESC, autor
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 14
# ==============================================================

def questao_14():
    consulta = """
    MATCH (livro:Livro)
    WHERE livro.ano > 1950
    RETURN livro.titulo AS titulo,
           livro.ano AS ano
    ORDER BY livro.ano
    """

    return executar_consulta(consulta)


# ==============================================================
# QUESTÃO 15
# ==============================================================

def questao_15():
    consulta = """
    MATCH (usuario:Usuario)-[emprestimo:EMPRESTOU]->(livro:Livro)
    WHERE emprestimo.devolvido = true
    SET livro.disponivel = true
    RETURN DISTINCT livro.titulo AS livro,
           livro.disponivel AS disponivel
    ORDER BY livro.titulo
    """

    return executar_consulta(consulta)


# ==============================================================
# INTERFACE DO STREAMLIT
# ==============================================================

st.title("📚 Sistema de Biblioteca")
st.subheader("Neo4j + Python + Streamlit")

st.success("Conexão com o Neo4j Aura estabelecida com sucesso.")


st.warning(
    "A inicialização apaga todos os dados atuais do banco e recria os dados da atividade."
)

if st.button("🗄️ Inicializar banco de dados"):
    try:
        setup_database()
        st.success("Banco populado com sucesso!")
    except Exception as erro:
        st.error("Erro ao inicializar o banco.")
        st.code(str(erro))


st.divider()


questoes = {
    "Questão 01 - Criar livro": questao_01,
    "Questão 02 - Criar autor": questao_02,
    "Questão 03 - Criar relacionamento": questao_03,
    "Questão 04 - Listar livros": questao_04,
    "Questão 05 - Listar autores": questao_05,
    "Questão 06 - Buscar Dom Casmurro": questao_06,
    "Questão 07 - Atualizar páginas de 1984": questao_07,
    "Questão 08 - Livros de Romance": questao_08,
    "Questão 09 - Livros de Machado de Assis": questao_09,
    "Questão 10 - Usuários com empréstimos": questao_10,
    "Questão 11 - Empréstimos pendentes": questao_11,
    "Questão 12 - Excluir O Cortiço": questao_12,
    "Questão 13 - Contar livros por autor": questao_13,
    "Questão 14 - Livros após 1950": questao_14,
    "Questão 15 - Marcar livros disponíveis": questao_15,
}


questao_escolhida = st.selectbox(
    "Escolha uma questão:",
    list(questoes.keys())
)


if st.button("▶️ Executar questão"):
    try:
        funcao = questoes[questao_escolhida]
        resultado = funcao()

        st.success(f"{questao_escolhida} executada com sucesso.")

        if resultado:
            st.dataframe(
                resultado,
                use_container_width=True
            )
        else:
            st.info("A consulta não retornou registros.")

    except Exception as erro:
        st.error("Erro ao executar a questão.")
        st.code(str(erro))


st.divider()
st.caption("Projeto de biblioteca usando Python, Streamlit e Neo4j Aura.")
