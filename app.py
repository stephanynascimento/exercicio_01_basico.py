import streamlit as st
from neo4j import GraphDatabase


# ==============================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================

st.set_page_config(
    page_title="Sistema de Biblioteca",
    page_icon="📚",
    layout="wide"
)


# ==============================================================
# CONEXÃO COM O NEO4J AURA
# ==============================================================

URI = st.secrets["NEO4J_URI"]
USUARIO = st.secrets["NEO4J_USER"]
SENHA = st.secrets["NEO4J_PASSWORD"]


@st.cache_resource
def criar_driver():
    return GraphDatabase.driver(
        URI,
        auth=(USUARIO, SENHA)
    )


driver = criar_driver()


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


# ==============================================================
# CRIAÇÃO DO BANCO
# ==============================================================

def inicializar_banco():
    executar_consulta(
        """
        MATCH (n)
        DETACH DELETE n
        """
    )

    executar_consulta(
        """
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

          (u1)-[:AVALIOU {
              nota: 5
          }]->(l1),

          (u2)-[:AVALIOU {
              nota: 4
          }]->(l2),

          (u3)-[:AVALIOU {
              nota: 5
          }]->(l4),

          (u4)-[:AVALIOU {
              nota: 3
          }]->(l3)
        """
    )


# ==============================================================
# CONSULTAS DAS 15 QUESTÕES
# ==============================================================

questoes = {
    "Questão 01 - Criar livro": {
        "consulta": """
            CREATE (l:Livro {
                titulo: 'O Cortiço',
                ano: 1890,
                genero: 'Naturalismo',
                paginas: 320
            })
            RETURN l.titulo AS titulo,
                   l.ano AS ano,
                   l.genero AS genero,
                   l.paginas AS paginas
        """,
        "parametros": {}
    },

    "Questão 02 - Criar autor": {
        "consulta": """
            CREATE (a:Autor {
                nome: 'Aluísio Azevedo',
                nacionalidade: 'Brasileiro'
            })
            RETURN a.nome AS nome,
                   a.nacionalidade AS nacionalidade
        """,
        "parametros": {}
    },

    "Questão 03 - Criar relacionamento": {
        "consulta": """
            MATCH (a:Autor {nome: 'Aluísio Azevedo'})
            MATCH (l:Livro {titulo: 'O Cortiço'})
            CREATE (a)-[r:ESCREVEU]->(l)
            RETURN a.nome AS autor,
                   type(r) AS relacionamento,
                   l.titulo AS livro
        """,
        "parametros": {}
    },

    "Questão 04 - Listar livros": {
        "consulta": """
            MATCH (l:Livro)
            RETURN l.titulo AS titulo,
                   l.ano AS ano,
                   l.genero AS genero
            ORDER BY l.titulo
        """,
        "parametros": {}
    },

    "Questão 05 - Listar autores": {
        "consulta": """
            MATCH (a:Autor)
            RETURN a.nome AS nome,
                   a.nacionalidade AS nacionalidade
            ORDER BY a.nome
        """,
        "parametros": {}
    },

    "Questão 06 - Buscar livro pelo título": {
        "consulta": """
            MATCH (l:Livro {titulo: $titulo})
            RETURN l.titulo AS titulo,
                   l.ano AS ano,
                   l.genero AS genero,
                   l.paginas AS paginas
        """,
        "parametros": {
            "titulo": "Dom Casmurro"
        }
    },

    "Questão 07 - Atualizar páginas do livro 1984": {
        "consulta": """
            MATCH (l:Livro {titulo: '1984'})
            SET l.paginas = 340
            RETURN l.titulo AS titulo,
                   l.paginas AS paginas
        """,
        "parametros": {}
    },

    "Questão 08 - Listar livros por gênero": {
        "consulta": """
            MATCH (l:Livro)
            WHERE l.genero = $genero
            RETURN l.titulo AS titulo,
                   l.ano AS ano
            ORDER BY l.ano
        """,
        "parametros": {
            "genero": "Romance"
        }
    },

    "Questão 09 - Listar livros por autor": {
        "consulta": """
            MATCH (a:Autor {nome: $autor})-[:ESCREVEU]->(l:Livro)
            RETURN l.titulo AS titulo
            ORDER BY l.titulo
        """,
        "parametros": {
            "autor": "Machado de Assis"
        }
    },

    "Questão 10 - Usuários com empréstimos": {
        "consulta": """
            MATCH (u:Usuario)-[:EMPRESTOU]->(l:Livro)
            RETURN u.nome AS usuario,
                   l.titulo AS livro
            ORDER BY u.nome, l.titulo
        """,
        "parametros": {}
    },

    "Questão 11 - Empréstimos pendentes": {
        "consulta": """
            MATCH (u:Usuario)-[e:EMPRESTOU]->(l:Livro)
            WHERE e.devolvido = false
            RETURN u.nome AS usuario,
                   l.titulo AS livro,
                   e.data AS data_emprestimo
            ORDER BY e.data
        """,
        "parametros": {}
    },

    "Questão 12 - Excluir o livro O Cortiço": {
        "consulta": """
            MATCH (l:Livro {titulo: 'O Cortiço'})
            WITH l, count(l) AS quantidade
            DETACH DELETE l
            RETURN quantidade AS livros_excluidos
        """,
        "parametros": {}
    },

    "Questão 13 - Contar livros por autor": {
        "consulta": """
            MATCH (a:Autor)-[:ESCREVEU]->(l:Livro)
            RETURN a.nome AS autor,
                   count(l) AS total_livros
            ORDER BY total_livros DESC
        """,
        "parametros": {}
    },

    "Questão 14 - Livros publicados após 1950": {
        "consulta": """
            MATCH (l:Livro)
            WHERE l.ano > 1950
            RETURN l.titulo AS titulo,
                   l.ano AS ano
            ORDER BY l.ano
        """,
        "parametros": {}
    },

    "Questão 15 - Marcar livros disponíveis": {
        "consulta": """
            MATCH (:Usuario)-[e:EMPRESTOU]->(l:Livro)
            WHERE e.devolvido = true
            SET l.disponivel = true
            RETURN DISTINCT l.titulo AS livro,
                            l.disponivel AS disponivel
            ORDER BY l.titulo
        """,
        "parametros": {}
    }
}


# ==============================================================
# INTERFACE DO STREAMLIT
# ==============================================================

st.title("📚 Sistema de Biblioteca")

st.write(
    "Aplicação desenvolvida com Python, Neo4j e Streamlit."
)

st.divider()


if st.button("Inicializar banco de dados"):
    try:
        inicializar_banco()
        st.success("Banco de dados inicializado com sucesso!")
    except Exception as erro:
        st.error(f"Erro ao inicializar o banco de dados: {erro}")


st.divider()


st.subheader("Consultas da atividade")

questao_escolhida = st.selectbox(
    "Escolha uma questão:",
    list(questoes.keys())
)


if st.button("Executar questão", type="primary"):
    try:
        dados_questao = questoes[questao_escolhida]

        resultado = executar_consulta(
            dados_questao["consulta"],
            dados_questao["parametros"]
        )

        st.success("Questão executada com sucesso!")

        if resultado:
            st.dataframe(
                resultado,
                use_container_width=True
            )
        else:
            st.warning(
                "A consulta foi executada, mas não retornou resultados."
            )

    except Exception as erro:
        st.error(f"Erro ao executar a questão: {erro}")
