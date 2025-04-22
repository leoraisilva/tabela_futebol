
from flask import Flask, request
from flask_cors import CORS

from src.ModelPlay import ModelPlay
from src.ModelTable import ModelTable
from src.RequestTable import RequestTable

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
        model.append(aux.to_dict())

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
        model.append(aux.to_dict())
    return model

def mensagem_erro():
    return {
        "mensagem": "Erro no dado",
        "statusCode" : 400,
        "descricao" : "Bad Request"
    }

@app.route('/api/v1/tabela')
def table():
    model = const_table()
    return model

@app.route('/api/v1/jogos')
def play():
    model = const_play()
    return model

@app.route('/api/v1/tabela/<posicao>')
def table_position(posicao):
    if int(posicao) < 0 or int(posicao) > 19:
        return mensagem_erro()
    model = const_table()
    return model[int(posicao)]

@app.route('/api/v1/jogos/<partida>')
def play_partida(partida):
    if int(partida) < 0 or int(partida) > 9:
        return mensagem_erro()
    model = const_play()
    return model[int(partida)]