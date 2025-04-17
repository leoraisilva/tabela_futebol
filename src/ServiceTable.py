
from flask import Flask, request
from flask_cors import CORS
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
        model.append(aux)

    return model

@app.route('/api/v1/tabela/<posicao>')
def table_position(posicao):
    model = const_table()
    return model[int(posicao)].to_dict()