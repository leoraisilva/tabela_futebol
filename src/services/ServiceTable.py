from sklearn.model_selection import train_test_split
from src.models.ModelPlay import ModelPlay
from src.models.ModelTable import ModelTable
from src.models.ModelHistoric import ModelHistoric

from src.repositories.DataRepository import DataRepository
from src.repositories.RequestTable import RequestTable

from src.services.DataFrameTable import DataFrameTable
from src.services.MatchPredictor import MatchPredictor
from src.services.PredictorPlay import PredictorPlay


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

    def const_historic(self):
        database = DataRepository()
        time = []

        table = self.const_table()
        competicao = ['brasileirao23', 'brasileirao24']

        for item in table:
            if item.nome_popular == "Atlético-MG":
                nome_popular = "atletico_mineiro"
            elif item.nome_popular == "São Paulo":
                nome_popular = "sao_paulo"
            elif item.nome_popular == "Bragantino":
                nome_popular = "redbull_bragantino"
            else:
                nome_popular = item.nome_popular
            for comp in competicao:
                jogos = database.total_jogos(nome_popular, comp)
                if jogos != 0:
                    vitorias = database.vitoria(nome_popular, comp)
                    derrotas = database.derrota(nome_popular, comp)
                    empates = database.empate(nome_popular, comp)
                    gols_favor = database.gol_favor(nome_popular, comp)
                    gols_contra = database.gol_contra(nome_popular, comp)
                    vitorias_casa = database.vitoria_casa(nome_popular, comp)
                    derrotas_casa = database.derrota_casa(nome_popular, comp)
                    empates_casa = database.empate_casa(nome_popular, comp)
                    vitorias_fora = vitorias - vitorias_casa
                    derrotas_fora = derrotas - derrotas_casa
                    empates_fora = empates - empates_casa
                    ultimos_jogos = ''
                    for i in item.ultimos_jogos:
                        ultimos_jogos += i
                    aux = ModelHistoric(
                        jogos, derrotas, vitorias, empates, gols_contra, gols_favor, nome_popular,
                        vitorias_casa, empates_casa, derrotas_casa, vitorias_fora, empates_fora,
                        derrotas_fora, ultimos_jogos
                    )
                    time.append(aux)
        return time

    def probability(self, mandante, visitante):
        dtf = DataFrameTable()
        dados_hist = self.const_historic()
        df = dtf.dataFrame(dados_hist)

        X = df[['vitorias', 'empates', 'derrotas', 'gols_contra']]
        y = df['gols_pro']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        predictor = PredictorPlay(auto_dispersion=True, verbose=True)
        predictor.fit(X_train, y_train)

        match_predictor = MatchPredictor(predictor)

        dados_time = self.const_table()
        for item in dados_time:
            if mandante == item.nome_popular:
                time_casa = {
                    'vitorias': item.vitorias,
                    'empates': item.empates,
                    'derrotas': item.derrotas,
                    'gols_contra': item.gols_contra
                }
            elif visitante == item.nome_popular:
                time_fora = {
                    'vitorias': item.vitorias,
                    'empates': item.empates,
                    'derrotas': item.derrotas,
                    'gols_contra': item.gols_contra
                }
        prediction = match_predictor.predict_match(time_casa, time_fora)

        probabilidade = {
                'vitoria': f"{(prediction['probabilities']['win'] * 100):.2f}",
                'empate': f"{(prediction['probabilities']['draw'] * 100):.2f}",
                'derrota': f"{(prediction['probabilities']['lose'] * 100):.2f}"
            }

        return probabilidade

