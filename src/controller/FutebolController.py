
from flask import Flask, request
from flask_cors import CORS

from src.services.ServiceTable import ServiceTable

app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

def const():
    return ServiceTable()

@app.route('/api/v1/probabilidade/<mandante>/<visitante>')
def probabilidade(mandante, visitante):
    model = const().probability(mandante, visitante)
    return model


@app.route('/api/v1/tabela')
def table():
    model = const().const_table()
    return_value = []
    for item in model:
        return_value.append(item.to_dict())
    return return_value

@app.route('/api/v1/jogos')
def play():
    model = const().const_play()
    return_value = []
    for item in model:
        return_value.append(item.to_dict())
    return return_value

@app.route('/api/v1/tabela/<posicao>')
def table_position(posicao):
    if int(posicao) < 0 or int(posicao) > 19:
        return const().mensagem_erro()
    model = const().const_table()
    return model[int(posicao)].to_dict()

@app.route('/api/v1/jogos/<partida>')
def play_partida(partida):
    if int(partida) < 0 or int(partida) > 9:
        return const().mensagem_erro()
    model = const().const_play()
    return model[int(partida)].to_dict()