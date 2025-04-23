from statistics import linear_regression

from flask import Flask, request
from flask_cors import CORS

from src.models.ModelPlay import ModelPlay
from src.models.ModelTable import ModelTable
from src.models.ModelHistoric import ModelHistoric
from src.repositories.DataRepository import DataRepository
from src.repositories.RequestTable import RequestTable

app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

def const_table():
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

def const_play():
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

def mensagem_erro():
    return {
        "mensagem": "Erro no dado",
        "statusCode" : 400,
        "descricao" : "Bad Request"
    }

def const_historic():
    database = DataRepository()
    table = const_table()
    time = []
    for item in  table:
        nome_popular = item.nome_popular
        jogos = database.total_jogos(nome_popular)
        vitoria = database.vitoria(nome_popular)
        derrota = database.derrota(nome_popular)
        empate = database.empate(nome_popular)
        gol_favor = database.gol_favor(nome_popular)
        gol_contra = database.gol_contra(nome_popular)
        vitoria_casa = database.vitoria_casa(nome_popular)
        derrota_casa = database.derrota_casa(nome_popular)
        empate_casa = database.empate_casa(nome_popular)
        vitoria_fora = vitoria - vitoria_casa
        derrota_fora = derrota - derrota_casa
        empate_fora = empate - empate_casa
        aux = ModelHistoric(
            jogos, derrota, vitorias, empate, gol_contra, gol_favor, nome_popular,
            vitoria_casa, empate_casa, derrota_casa, vitoria_fora, empate_fora, derrota_fora
        )
        time.append(aux)
    return time

@app.route('/api/v1/tabela')
def table():
    model = const_historic()
    return_value = []
    for item in model:
        return_value = item.to_dict()
    return return_value

@app.route('/api/v1/jogos')
def play():
    model = const_play()
    return_value = []
    for item in model:
        return_value = item.to_dict()
    return return_value

@app.route('/api/v1/tabela/<posicao>')
def table_position(posicao):
    if int(posicao) < 0 or int(posicao) > 19:
        return mensagem_erro()
    model = const_table()
    return model[int(posicao)].to_dict()

@app.route('/api/v1/jogos/<partida>')
def play_partida(partida):
    if int(partida) < 0 or int(partida) > 9:
        return mensagem_erro()
    model = const_play()
    return model[int(partida)].to_dict()

