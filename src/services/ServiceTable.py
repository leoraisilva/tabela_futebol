from statistics import linear_regression

from src.models.ModelPlay import ModelPlay
from src.models.ModelTable import ModelTable
from src.models.ModelHistoric import ModelHistoric
from src.repositories.DataRepository import DataRepository
from src.repositories.RequestTable import RequestTable

class ServiceTable:

    def const_table(self):
        table = RequestTable()
        content = table.tabela("https://ge.globo.com/futebol/brasileirao-serie-a/")
        model = []
        for item in content:
            aux = ModelTable(
                item["aproveitamento"],
                item["derrotas"],
                item["empates"],
                item["equipe_id"],
                item["escudo"],
                item["faixa_classificacao"],
                item["faixa_classificacao_cor"],
                item["gols_contra"],
                item["gols_pro"],
                item["jogos"],
                item["nome_popular"],
                item["ordem"],
                item["pontos"],
                item["saldo_gols"],
                item["sigla"],
                item["ultimos_jogos"],
                item["variacao"],
                item["vitorias"]
            )
            model.append(aux)
        return model

    def const_play(self):
        play = RequestTable()
        content = play.jogos("https://ge.globo.com/futebol/brasileirao-serie-a/")
        model = []
        for item in content:
            aux = ModelPlay(
                item["data_realizacao"],
                item["equipes"]["mandante"]["escudo"],
                item["equipes"]["mandante"]["nome_popular"],
                item["equipes"]["visitante"]["escudo"],
                item["equipes"]["visitante"]["nome_popular"],
                item["hora_realizacao"],
                item["jogo_ja_comecou"],
                item["placar_oficial_mandante"],
                item["placar_oficial_visitante"],
                item["sede"]["nome_popular"]
            )
            model.append(aux)
        return model

    def mensagem_erro(self):
        return {
            "mensagem": "Erro no dado",
            "statusCode" : 400,
            "descricao" : "Bad Request"
        }

    def const_historic(self, mandante, visitante):
        database = DataRepository()
        time = []
        dict = {mandante : 0, visitante: 0}

        table = self.const_table()
        for i in range(0, len(table) - 1):
            if table[i].nome_popular == mandante:
                dict[mandante] = i
            elif table[i].nome_popular == visitante:
                dict[visitante] = i

        for a in dict:

            if a == "Atlético-MG":
                nome_popular = "atletico_mineiro"
            elif a == "São Paulo":
                nome_popular = "sao_paulo"
            elif a == "Bragantino":
                nome_popular = "redbull_bragantino"
            else:
                nome_popular = table[dict[a]].nome_popular
            jogos = database.total_jogos(nome_popular)
            vitorias = database.vitoria(nome_popular)
            derrotas = database.derrota(nome_popular)
            empates = database.empate(nome_popular)
            gols_favor = database.gol_favor(nome_popular)
            gols_contra = database.gol_contra(nome_popular)
            vitorias_casa = database.vitoria_casa(nome_popular)
            derrotas_casa = database.derrota_casa(nome_popular)
            empates_casa = database.empate_casa(nome_popular)
            vitorias_fora = vitorias - vitorias_casa
            derrotas_fora = derrotas - derrotas_casa
            empates_fora = empates - empates_casa
            ultimos_jogos = ''
            for i in table[dict[a]].ultimos_jogos:
                ultimos_jogos += i
            confronto_vitorias = database.vitoria_confronto(mandante, visitante)
            confronto_derrotas = database.derrota_confronto(mandante, visitante)
            confronto_empates = database.empate_confronto(mandante, visitante)
            aux = ModelHistoric(
                jogos, derrotas, vitorias, empates, gols_contra, gols_favor, nome_popular,
                vitorias_casa, empates_casa, derrotas_casa, vitorias_fora, empates_fora,
                derrotas_fora, ultimos_jogos, confronto_vitorias, confronto_derrotas, confronto_empates
            )
            time.append(aux)
        return time



