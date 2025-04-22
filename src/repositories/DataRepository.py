from fontTools.ttLib.ttVisitor import visit

from src.Database.Database import Database


class DataRepository:
    def vitoria_casa_confronto(self, mandante, visitante):
        table = "torneio"
        database = Database()
        query = (f'SELECT COUNT(*) FROM {table}'
                 f' WHERE time_mandante=\'{mandante}\' '
                 f'AND time_visitante=\'{visitante}\' '
                 f'AND gol_mandante > gol_visitante;')
        return database.execute(query)

    def vitoria_fora_confronto(self, visitante, mandante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_visitante=\'{visitante}\' '
             f'AND time_mandante=\'{mandante}\' '
             f'AND gol_mandante < gol_visitante;'
        )
        return database.execute(query)

    def quantidade_confronto(self, mandante, visitante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_mandante=\'{mandante}\' '
             f'AND time_visitante=\'{visitante}\' '
             f'OR time_mandante=\'{visitante}\' '
             f'AND time_visitante=\'{mandante}\' '
        )
        return database.execute(query)

    def vitoria_casa(self, mandante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_mandante=\'{mandante}\' '
             f'AND gol_mandante > gol_visitante;'
        )
        return database.execute(query)

    def derrota_casa(self, mandante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT COUNT(*) FROM {table}'
             f' WHERE time_mandante=\'{mandante}\' '
             f'AND gol_mandante < gol_visitante;'
        )
        return database.execute(query)

    def jogos_casa(self, mandante):
        table = "torneio"
        database = Database()
        query = (
             f'SELECT competicao, time_mandante, gol_mandante, gol_visitante, time_visitante FROM {table}'
             f' WHERE time_mandante=\'{mandante}\' '
        )
        return database.query(query)

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
        return database.execute(query)

