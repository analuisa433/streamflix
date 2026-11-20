import sqlite3
from sqlite3 import Error


class Midia:
    def __init__(self, titulo, ano_lancamento, classificacao_indicativa):
        self.titulo = titulo
        self.metadados = (ano_lancamento, classificacao_indicativa)

    def obter_duracao_total_minutos(self):
        return 0

    def exibir_informacoes(self):
        ano, classificacao = self.metadados
        print("Título:", self.titulo)
        print("Ano de lançamento:", ano)
        print("Classificação indicativa:", classificacao)


class Filme(Midia):
    def __init__(self, titulo, ano_lancamento, classificacao_indicativa, duracao):
        super().__init__(titulo, ano_lancamento, classificacao_indicativa)
        self.duracao = duracao

    def obter_duracao_total_minutos(self):
        return self.duracao


class Serie(Midia):
    def __init__(self, titulo, ano_lancamento, classificacao_indicativa):
        super().__init__(titulo, ano_lancamento, classificacao_indicativa)
        self.episodios = []

    def adicionar_episodio(self, duracao):
        if duracao > 0:
            self.episodios.append(duracao)
        else:
            print("Duração inválida!")

    def obter_duracao_total_minutos(self):
        return sum(self.episodios)


def conectar_banco(nome_banco="streamflix.db"):
    try:
        conn = sqlite3.connect(nome_banco)
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS series (
                    id INTEGER PRIMARY KEY,
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
    episodios_texto = ",".join(str(d) for d in serie.episodios)
    ano, classificacao = serie.metadados
    sql = """
        INSERT INTO series (titulo, ano_lancamento, classificacao_indicativa, episodios)
        VALUES (?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (serie.titulo, ano, classificacao, episodios_texto))
        conn.commit()
        print("Série salva com sucesso!")
    except Error as e:
        print(f"Erro ao salvar série: {e}")


def carregar_series(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, ano_lancamento, classificacao_indicativa, episodios FROM series")
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
        print(f"Erro ao consultar séries: {e}")
        return []