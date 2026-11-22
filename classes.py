

import sqlite3
from sqlite3 import Error


# ==========================================
# CLASSE BASE
# ==========================================

class Midia:
    def __init__(self, titulo, ano_lancamento, classificacao_indicativa):
        self.titulo = titulo
        self.metadados = (ano_lancamento, classificacao_indicativa)

    @classmethod
    def criar_do_catalogo(cls, dados):
        return cls(
            dados["titulo"],
            dados["ano_lancamento"],
            dados["classificacao_indicativa"]
        )

    def obter_duracao_total_minutos(self):
        return 0

    def exibir_informacoes(self):
        ano, classificacao = self.metadados

        print(f"Título: {self.titulo}")
        print(f"Ano: {ano}")
        print(f"Classificação indicativa: {classificacao}")


# ==========================================
# CLASSE FILME
# ==========================================

class Filme(Midia):
    def __init__(self, titulo, ano_lancamento, classificacao_indicativa, duracao):
        super().__init__(titulo, ano_lancamento, classificacao_indicativa)
        self.duracao = duracao

    @classmethod
    def criar_do_catalogo(cls, dados):
        return cls(
            dados["titulo"],
            dados["ano_lancamento"],
            dados["classificacao_indicativa"],
            dados["duracao"]
        )

    def obter_duracao_total_minutos(self):
        return self.duracao

    def exibir_informacoes(self):
        super().exibir_informacoes()
        print(f"Tipo: Filme")
        print(f"Duração: {self.duracao} minutos")


# ==========================================
# CLASSE SERIE
# ==========================================

class Serie(Midia):
    def __init__(self, titulo, ano_lancamento, classificacao_indicativa):
        super().__init__(titulo, ano_lancamento, classificacao_indicativa)
        self.episodios = []

    @classmethod
    def criar_do_catalogo(cls, dados):
        serie = cls(
            dados["titulo"],
            dados["ano_lancamento"],
            dados["classificacao_indicativa"]
        )

        for duracao in dados.get("episodios", []):
            serie.adicionar_episodio(duracao)

        return serie

    def adicionar_episodio(self, duracao):
        if duracao > 0:
            self.episodios.append(duracao)
        else:
            print("Duração inválida!")

    def obter_duracao_total_minutos(self):
        return sum(self.episodios)

    def exibir_informacoes(self):
        super().exibir_informacoes()
        print("Tipo: Série")
        print(f"Quantidade de episódios: {len(self.episodios)}")
        print(f"Duração por episódios: {self.episodios}")


# ==========================================
# CLASSE USUARIO
# ==========================================

class Usuario:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        self.historico = {}
        self.conteudos_assistidos = set()

    def registrar_visualizacao(self, midia):
        if midia.titulo in self.conteudos_assistidos:
            print("Este conteúdo já foi registrado como assistido.")
            return False

        self.historico[midia.titulo] = {
            "midia": midia,
            "nota": None,
            "avaliacao": "Sem avaliação",
            "duracao_consumida": midia.obter_duracao_total_minutos()
        }

        self.conteudos_assistidos.add(midia.titulo)

        print(f"\n{midia.titulo} registrado como assistido!")
        return True

    def avaliar_conteudo(self, titulo, nota, avaliacao):
        if titulo not in self.historico:
            print("Este conteúdo não está no seu histórico.")
            return

        if not 0 <= nota <= 10:
            print("A nota deve estar entre 0 e 10.")
            return

        self.historico[titulo]["nota"] = nota
        self.historico[titulo]["avaliacao"] = avaliacao

        print("Avaliação registrada com sucesso!")

    def calcular_tempo_total_consumido(self):
        return sum(
            item["duracao_consumida"]
            for item in self.historico.values()
        )

    def exibir_historico(self):
        print(f"\n========== HISTÓRICO DE {self.nome.upper()} ==========")

        if not self.historico:
            print("Nenhum conteúdo assistido.")
            return

        for titulo, dados in self.historico.items():
            print(f"\nConteúdo: {titulo}")
            print(f"Nota: {dados['nota'] if dados['nota'] is not None else 'Não avaliado'}")
            print(f"Avaliação: {dados['avaliacao']}")
            print(f"Duração consumida: {dados['duracao_consumida']} minutos")

    def recomendar_conteudos(self, catalogo):
        print(f"\n========== RECOMENDAÇÕES PARA {self.nome.upper()} ==========")

        recomendacoes = []

        for midia in catalogo:
            if midia.titulo in self.conteudos_assistidos:
                continue

            classificacao = midia.metadados[1]

            if classificacao == "Livre":
                idade_minima = 0
            else:
                try:
                    idade_minima = int(classificacao.replace("+", ""))
                except ValueError:
                    continue

            if self.idade >= idade_minima:
                recomendacoes.append(midia)

        if not recomendacoes:
            print("Nenhum conteúdo disponível para recomendação.")
            return

        for midia in recomendacoes:
            print(f"\n{midia.titulo}")
            print(f"Classificação: {midia.metadados[1]}")
            print(f"Duração: {midia.obter_duracao_total_minutos()} minutos")


# ==========================================
# BANCO DE DADOS
# ==========================================

def conectar_banco(nome_banco="streamflix.db"):
    try:
        conn = sqlite3.connect(nome_banco)

        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS series (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT,
                    ano_lancamento INTEGER,
                    classificacao_indicativa TEXT,
                    episodios TEXT
                )
            """)

        return conn

    except Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


def salvar_serie(conn, serie):
    ano, classificacao = serie.metadados
    episodios_texto = ",".join(str(d) for d in serie.episodios)

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO series (
                titulo,
                ano_lancamento,
                classificacao_indicativa,
                episodios
            )
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM series WHERE titulo = ?
            )
        """, (
            serie.titulo,
            ano,
            classificacao,
            episodios_texto,
            serie.titulo
        ))

        conn.commit()

    except Error as e:
        print(f"Erro ao salvar série: {e}")


def carregar_series(conn):
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT titulo, ano_lancamento,
                   classificacao_indicativa, episodios
            FROM series
        """)

        linhas = cursor.fetchall()
        series = []

        for titulo, ano, classificacao, episodios_texto in linhas:
            serie = Serie(titulo, ano, classificacao)

            if episodios_texto:
                for item in episodios_texto.split(","):
                    serie.adicionar_episodio(int(item))

            series.append(serie)

        return series

    except Error as e:
        print(f"Erro ao carregar séries: {e}")
        return []
