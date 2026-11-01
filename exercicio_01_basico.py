"""
=============================================================
EXERCÍCIO 01 - NÍVEL BÁSICO
Banco de Grafos Neo4j com Python
Tema: Sistema de Biblioteca
=============================================================

Pré-requisitos:
    pip install neo4j

Configuração:
    - Neo4j rodando em localhost:7687
    - Usuário: neo4j
    - Senha: password

Para executar:
    python exercicio_01_basico.py
=============================================================
"""

from neo4j import GraphDatabase


URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)


# ==============================================================
# SETUP - Popula o banco com dados iniciais
# ==============================================================
def setup_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        session.run(
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

    print("✅ Banco populado com sucesso!\n")


# ==============================================================
# QUESTÃO 01
# Cria um novo livro chamado "O Cortiço"
# ==============================================================
def questao_01_criar_livro():
    with driver.session() as session:
        result = session.run(
            """
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
            """
        )

        livro = result.single()

    print("Q01 - Livro criado:", livro)


# ==============================================================
# QUESTÃO 02
# Cria o autor Aluísio Azevedo
# ==============================================================
def questao_02_criar_autor():
    with driver.session() as session:
        result = session.run(
            """
            CREATE (a:Autor {
                nome: 'Aluísio Azevedo',
                nacionalidade: 'Brasileiro'
            })
            RETURN a.nome AS nome,
                   a.nacionalidade AS nacionalidade
            """
        )

        autor = result.single()

    print("Q02 - Autor criado:", autor)


# ==============================================================
# QUESTÃO 03
# Cria o relacionamento ESCREVEU
# ==============================================================
def questao_03_criar_relacionamento():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Autor {nome: 'Aluísio Azevedo'})
            MATCH (l:Livro {titulo: 'O Cortiço'})
            CREATE (a)-[r:ESCREVEU]->(l)
            RETURN a.nome AS autor,
                   type(r) AS relacionamento,
                   l.titulo AS livro
            """
        )

        relacionamento = result.single()

    print("Q03 - Relacionamento criado:", relacionamento)


# ==============================================================
# QUESTÃO 04
# Lista todos os livros cadastrados
# ==============================================================
def questao_04_listar_livros():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (l:Livro)
            RETURN l.titulo AS titulo,
                   l.ano AS ano,
                   l.genero AS genero
            ORDER BY l.titulo
            """
        )

        livros = list(result)

    print("Q04 - Livros encontrados:")
    for livro in livros:
        print(f"  - {livro}")


# ==============================================================
# QUESTÃO 05
# Lista todos os autores cadastrados
# ==============================================================
def questao_05_listar_autores():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Autor)
            RETURN a.nome AS nome,
                   a.nacionalidade AS nacionalidade
            ORDER BY a.nome
            """
        )

        autores = list(result)

    print("Q05 - Autores encontrados:")
    for autor in autores:
        print(f"  - {autor}")


# ==============================================================
# QUESTÃO 06
# Busca um livro pelo título
# ==============================================================
def questao_06_buscar_livro_por_titulo():
    titulo = "Dom Casmurro"

    with driver.session() as session:
        result = session.run(
            """
            MATCH (l:Livro {titulo: $titulo})
            RETURN l
            """,
            titulo=titulo,
        )

        livro = result.single()

    print(f"Q06 - Livro encontrado: {livro}")


# ==============================================================
# QUESTÃO 07
# Atualiza o número de páginas do livro "1984"
# ==============================================================
def questao_07_atualizar_paginas():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (l:Livro {titulo: '1984'})
            SET l.paginas = 340
            RETURN l.titulo AS titulo,
                   l.paginas AS paginas
            """
        )

        livro = result.single()

    print("Q07 - Páginas atualizadas:", livro)


# ==============================================================
# QUESTÃO 08
# Lista os livros do gênero Romance
# ==============================================================
def questao_08_livros_por_genero():
    genero = "Romance"

    with driver.session() as session:
        result = session.run(
            """
            MATCH (l:Livro)
            WHERE l.genero = $genero
            RETURN l.titulo AS titulo,
                   l.ano AS ano
            ORDER BY l.ano
            """,
            genero=genero,
        )

        livros = list(result)

    print("Q08 - Livros do gênero Romance:")
    for livro in livros:
        print(f"  - {livro}")


# ==============================================================
# QUESTÃO 09
# Lista os livros escritos por Machado de Assis
# ==============================================================
def questao_09_livros_por_autor():
    autor = "Machado de Assis"

    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Autor {nome: $autor})-[:ESCREVEU]->(l:Livro)
            RETURN l.titulo AS titulo
            ORDER BY l.titulo
            """,
            autor=autor,
        )

        livros = list(result)

    print(f"Q09 - Livros de {autor}:")
    for livro in livros:
        print(f"  - {livro}")


# ==============================================================
# QUESTÃO 10
# Lista todos os usuários e seus empréstimos
# ==============================================================
def questao_10_usuarios_com_emprestimos():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:Usuario)-[:EMPRESTOU]->(l:Livro)
            RETURN u.nome AS usuario,
                   l.titulo AS livro
            ORDER BY u.nome, l.titulo
            """
        )

        emprestimos = list(result)

    print("Q10 - Empréstimos:")
    for emprestimo in emprestimos:
        print(f"  - {emprestimo}")


# ==============================================================
# QUESTÃO 11
# Lista os empréstimos pendentes
# ==============================================================
def questao_11_emprestimos_pendentes():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:Usuario)-[e:EMPRESTOU]->(l:Livro)
            WHERE e.devolvido = false
            RETURN u.nome AS usuario,
                   l.titulo AS livro,
                   e.data AS data_emprestimo
            ORDER BY e.data
            """
        )

        pendentes = list(result)

    print("Q11 - Empréstimos pendentes:")
    for pendente in pendentes:
        print(f"  - {pendente}")


# ==============================================================
# QUESTÃO 12
# Deleta o livro "O Cortiço"
# ==============================================================
def questao_12_deletar_livro():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (l:Livro {titulo: 'O Cortiço'})
            WITH l, count(l) AS quantidade
            DETACH DELETE l
            RETURN quantidade AS livros_deletados
            """
        )

        resultado = result.single()

    print("Q12 - Livro deletado:", resultado)


# ==============================================================
# QUESTÃO 13
# Conta quantos livros cada autor escreveu
# ==============================================================
def questao_13_contar_livros_por_autor():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Autor)-[:ESCREVEU]->(l:Livro)
            RETURN a.nome AS autor,
                   count(l) AS total_livros
            ORDER BY total_livros DESC, autor
            """
        )

        contagem = list(result)

    print("Q13 - Livros por autor:")
    for registro in contagem:
        print(f"  - {registro}")


# ==============================================================
# QUESTÃO 14
# Lista os livros publicados após 1950
# ==============================================================
def questao_14_livros_apos_1950():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (l:Livro)
            WHERE l.ano > 1950
            RETURN l.titulo AS titulo,
                   l.ano AS ano
            ORDER BY l.ano ASC
            """
        )

        livros = list(result)

    print("Q14 - Livros após 1950:")
    for livro in livros:
        print(f"  - {livro}")


# ==============================================================
# QUESTÃO 15
# Marca como disponíveis os livros devolvidos
# ==============================================================
def questao_15_marcar_livros_disponiveis():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:Usuario)-[e:EMPRESTOU]->(l:Livro)
            WHERE e.devolvido = true
            SET l.disponivel = true
            RETURN DISTINCT l.titulo AS livro,
                            l.disponivel AS disponivel
            ORDER BY l.titulo
            """
        )

        livros = list(result)

    print("Q15 - Livros marcados como disponíveis:")
    for livro in livros:
        print(f"  - {livro}")


# ==============================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================
if __name__ == "__main__":
    try:
        print("=" * 60)
        print("EXERCÍCIO 01 - NÍVEL BÁSICO - Sistema de Biblioteca")
        print("=" * 60)

        setup_database()

        questao_01_criar_livro()
        questao_02_criar_autor()
        questao_03_criar_relacionamento()
        questao_04_listar_livros()
        questao_05_listar_autores()
        questao_06_buscar_livro_por_titulo()
        questao_07_atualizar_paginas()
        questao_08_livros_por_genero()
        questao_09_livros_por_autor()
        questao_10_usuarios_com_emprestimos()
        questao_11_emprestimos_pendentes()
        questao_12_deletar_livro()
        questao_13_contar_livros_por_autor()
        questao_14_livros_apos_1950()
        questao_15_marcar_livros_disponiveis()

        print("\n✅ Exercício executado com sucesso!")

    except Exception as erro:
        print(f"\n❌ Erro durante a execução: {erro}")

    finally:
        driver.close()
