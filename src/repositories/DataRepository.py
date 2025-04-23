from fontTools.ttLib.ttVisitor import visit

from src.Database.Database import Database


class DataRepository:

    def total_jogos(self, time):
        table = "torneio"
        database = Database()
        query = (
            f'SELECT COUNT(*) FROM {table}'
            f' WHERE time_mandante=\'{time}\' OR time_visitante=\'{time}\'; '
        )
        return database.execute(query)

    def vitoria(self, time):
        table = "torneio"
        database = Database()
        query = (
            f'SELECT COUNT(*) FROM {table}'
            f' WHERE time_mandante=\'{time}\' AND gol_mandante > gol_visitante  '
            f' OR time_visitante=\'{time}\' AND gol_mandante < gol_visitante '
        )
        return database.execute(query)

    def derrota(self, time):
        table = "torneio"
        database = Database()
        query = (
            f'SELECT COUNT(*) FROM {table}'
            f' WHERE time_mandante=\'{time}\' AND gol_mandante < gol_visitante '
            f' OR time_visitante=\'{time}\' AND gol_mandante > gol_visitante '
        )
        return database.execute(query)

    def empate(self, time):
        table = "torneio"
        database = Database()
        query = (
            f'SELECT COUNT(*) FROM {table}'
            f' WHERE time_mandante=\'{time}\' AND gol_mandante = gol_visitante '
            f' OR time_visitante=\'{time}\' AND gol_mandante = gol_visitante '
        )
        return database.execute(query)

    def gol_favor(self, time):
        table = "torneio"
        database = Database()
        query = (
            f'SELECT ('
            f'SELECT sum(gol_mandante) FROM {table} '
            f'WHERE time_mandante=\'{time}\' ) +'
            f'(SELECT sum(gol_visitante) FROM {table} '
            f'WHERE time_visitante=\'{time}\') AS gol_favor;'
        )
        return database.execute(query)

    def gol_contra(self, time):
        table = "torneio"
        database = Database()
        query = (
            f'SELECT ('
            f'SELECT sum(gol_visitante) FROM {table} '
            f'WHERE time_mandante=\'{time}\' ) +'
            f'(SELECT sum(gol_mandante) FROM {table} '
            f'WHERE time_visitante=\'{time}\') AS gol_favor;'
        )
        return database.execute(query)

    def vitoria_casa(self, time):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_mandante=\'{time}\' '
             f'AND gol_mandante > gol_visitante;'
        )
        return database.execute(query)

    def derrota_casa(self, time):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_mandante=\'{time}\' '
             f'AND gol_mandante < gol_visitante;'
        )
        return database.execute(query)

    def empate_casa(self, time):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_mandante=\'{time}\' '
             f'AND gol_mandante = gol_visitante;'
        )
        return database.execute(query)

    def vitoria_confronto(self, mandante, visitante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f'WHERE time_mandante=\'{mandante}\' '
             f'AND time_visitante=\'{visitante}\''
             f'AND gol_mandante > gol_visitante;'
        )
        return database.execute(query)

    def derrota_confronto(self, mandante, visitante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f'WHERE time_mandante=\'{mandante}\' '
             f'AND time_visitante=\'{visitante}\''
             f'AND gol_mandante < gol_visitante;'
        )
        return database.execute(query)

    def empate_fora_confronto(self, mandante, visitante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f'WHERE time_mandante=\'{mandante}\' '
             f'AND time_visitante=\'{visitante}\''
             f'AND gol_mandante = gol_visitante;'
        )
        return database.execute(query)


    def jogos_confronto(self, mandante, visitante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT competicao, time_mandante, gol_mandante, gol_visitante, time_visitante FROM {table}'
             f' WHERE time_mandante=\'{mandante}\' '
             f'AND time_visitante=\'{visitante}\' '
             f'OR time_mandante=\'{visitante}\' '
             f'AND time_visitante=\'{mandante}\' '
        )
        return database.query(query)


