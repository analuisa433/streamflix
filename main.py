
from classes import (
    Filme,
    Serie,
    Usuario,
    conectar_banco,
    salvar_serie,
    carregar_series
)


# ==========================================
# CADASTRO INTERNO DO CATÁLOGO
# ==========================================

def criar_catalogo():

    catalogo = []

    # 10 FILMES

    filmes = [
        {"titulo": "Interestelar", "ano_lancamento": 2014, "classificacao_indicativa": "10+", "duracao": 169},
        {"titulo": "O Hobbit", "ano_lancamento": 2012, "classificacao_indicativa": "12+", "duracao": 169},
        {"titulo": "O Rei Leão", "ano_lancamento": 1994, "classificacao_indicativa": "Livre", "duracao": 88},
        {"titulo": "Deadpool", "ano_lancamento": 2016, "classificacao_indicativa": "18+", "duracao": 108},
        {"titulo": "Harry Potter e a Pedra Filosofal", "ano_lancamento": 2001, "classificacao_indicativa": "10+", "duracao": 152},
        {"titulo": "Vingadores: Ultimato", "ano_lancamento": 2019, "classificacao_indicativa": "12+", "duracao": 181},
        {"titulo": "Divertida Mente", "ano_lancamento": 2015, "classificacao_indicativa": "Livre", "duracao": 95},
        {"titulo": "Coringa", "ano_lancamento": 2019, "classificacao_indicativa": "16+", "duracao": 122},
        {"titulo": "Jurassic Park", "ano_lancamento": 1993, "classificacao_indicativa": "12+", "duracao": 127},
        {"titulo": "A Origem", "ano_lancamento": 2010, "classificacao_indicativa": "14+", "duracao": 148}
    ]

    for dados in filmes:
        filme = Filme.criar_do_catalogo(dados)
        catalogo.append(filme)

    # 10 SÉRIES

    series = [
        {
            "titulo": "Stranger Things",
            "ano_lancamento": 2016,
            "classificacao_indicativa": "16+",
            "episodios": [50, 55, 48, 60]
        },
        {
            "titulo": "The Office",
            "ano_lancamento": 2005,
            "classificacao_indicativa": "12+",
            "episodios": [22, 25, 23, 24]
        },
        {
            "titulo": "Friends",
            "ano_lancamento": 1994,
            "classificacao_indicativa": "12+",
            "episodios": [22, 23, 21, 24]
        },
        {
            "titulo": "Round 6",
            "ano_lancamento": 2021,
            "classificacao_indicativa": "18+",
            "episodios": [50, 60, 55, 58]
        },
        {
            "titulo": "The Mandalorian",
            "ano_lancamento": 2019,
            "classificacao_indicativa": "14+",
            "episodios": [40, 45, 42, 48]
        },
        {
            "titulo": "Wandinha",
            "ano_lancamento": 2022,
            "classificacao_indicativa": "12+",
            "episodios": [45, 50, 48, 52]
        },
        {
            "titulo": "Cobra Kai",
            "ano_lancamento": 2018,
            "classificacao_indicativa": "14+",
            "episodios": [30, 35, 32, 38]
        },
        {
            "titulo": "The Last of Us",
            "ano_lancamento": 2023,
            "classificacao_indicativa": "18+",
            "episodios": [55, 60, 50, 65]
        },
        {
            "titulo": "Anne with an E",
            "ano_lancamento": 2017,
            "classificacao_indicativa": "10+",
            "episodios": [45, 48, 46, 50]
        },
        {
            "titulo": "Avatar: A Lenda de Aang",
            "ano_lancamento": 2005,
            "classificacao_indicativa": "Livre",
            "episodios": [23, 24, 22, 25]
        }
    ]

    for dados in series:
        serie = Serie.criar_do_catalogo(dados)
        catalogo.append(serie)

    return catalogo


# ==========================================
# EXIBIR CATÁLOGO
# ==========================================

def listar_catalogo(catalogo):

    print("\n========== CATÁLOGO STREAMFLIX ==========")

    print("\n--------------- FILMES ------------------")

    for i, midia in enumerate(catalogo, start=1):
        if isinstance(midia, Filme):
            print(f"\nCódigo: {i}")
            midia.exibir_informacoes()

    print("\n--------------- SÉRIES ------------------")

    for i, midia in enumerate(catalogo, start=1):
        if isinstance(midia, Serie):
            print(f"\nCódigo: {i}")
            midia.exibir_informacoes()

    print("\n=========================================")


# ==========================================
# SELECIONAR CONTEÚDO
# ==========================================

def selecionar_conteudo(catalogo):

    listar_catalogo(catalogo)

    try:
        codigo = int(input("\nDigite o código do conteúdo: "))

        if 1 <= codigo <= len(catalogo):
            return catalogo[codigo - 1]

        print("Código inválido!")

    except ValueError:
        print("Digite um número válido!")

    return None


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    catalogo = criar_catalogo()

    conn = conectar_banco()

    if conn:
        for midia in catalogo:
            if isinstance(midia, Serie):
                salvar_serie(conn, midia)

        # Carrega as séries cadastradas no banco.
        series_banco = carregar_series(conn)

        # Atualiza as séries do catálogo com os dados do banco.
        for serie_banco in series_banco:
            for i, midia in enumerate(catalogo):
                if isinstance(midia, Serie) and midia.titulo == serie_banco.titulo:
                    catalogo[i] = serie_banco
                    break

    usuario = None

    while True:

        print("\n")
        print("=========================================")
        print("             STREAMFLIX")
        print("=========================================")
        print("1. Cadastrar usuário")
        print("2. Listar catálogo de filmes e séries")
        print("3. Registrar visualização")
        print("4. Avaliar conteúdo")
        print("5. Consultar histórico")
        print("6. Consultar tempo total consumido")
        print("7. Receber recomendações")
        print("8. Sair")
        print("=========================================")

        opcao = input("Escolha uma opção: ")

        # 1. CADASTRAR USUÁRIO

        if opcao == "1":

            nome = input("\nDigite seu nome: ")

            try:
                idade = int(input("Digite sua idade: "))

                if idade < 0:
                    print("Idade inválida!")
                    continue

                usuario = Usuario(nome, idade)

                print(f"\nUsuário {nome} cadastrado com sucesso!")

            except ValueError:
                print("Digite uma idade válida!")

        # 2. LISTAR CATÁLOGO

        elif opcao == "2":

            listar_catalogo(catalogo)

        # 3. REGISTRAR VISUALIZAÇÃO

        elif opcao == "3":

            if usuario is None:
                print("\nCadastre um usuário primeiro!")
                continue

            midia = selecionar_conteudo(catalogo)

            if midia:
                usuario.registrar_visualizacao(midia)

        # 4. AVALIAR CONTEÚDO

        elif opcao == "4":

            if usuario is None:
                print("\nCadastre um usuário primeiro!")
                continue

            if not usuario.historico:
                print("\nVocê ainda não assistiu a nenhum conteúdo.")
                continue

            usuario.exibir_historico()

            titulo = input("\nDigite o título do conteúdo que deseja avaliar: ")

            if titulo not in usuario.historico:
                print("Conteúdo não encontrado no histórico.")
                continue

            try:
                nota = float(input("Digite sua nota (0 a 10): "))

                avaliacao = input("Escreva um comentário sobre o conteúdo: ")

                usuario.avaliar_conteudo(titulo, nota, avaliacao)

            except ValueError:
                print("Digite uma nota válida!")

        # 5. CONSULTAR HISTÓRICO

        elif opcao == "5":

            if usuario is None:
                print("\nCadastre um usuário primeiro!")
                continue

            usuario.exibir_historico()

        # 6. TEMPO TOTAL CONSUMIDO

        elif opcao == "6":

            if usuario is None:
                print("\nCadastre um usuário primeiro!")
                continue

            tempo = usuario.calcular_tempo_total_consumido()

            horas = tempo // 60
            minutos = tempo % 60

            print("\n========== TEMPO CONSUMIDO ==========")
            print(f"Usuário: {usuario.nome}")
            print(f"Total: {tempo} minutos")
            print(f"Equivalente a: {horas}h e {minutos}min")

        # 7. RECOMENDAÇÕES

        elif opcao == "7":

            if usuario is None:
                print("\nCadastre um usuário primeiro!")
                continue

            usuario.recomendar_conteudos(catalogo)

        # 8. SAIR

        elif opcao == "8":

            print("\nEncerrando a StreamFlix...")

            if conn:
                conn.close()
                print("Conexão com banco encerrada.")

            print("Obrigado por utilizar a StreamFlix!")
            break

        else:
            print("\nOpção inválida! Escolha uma opção de 1 a 8.")

if __name__ == "__main__":
    menu_principal()
