from src.ModelPlay import ModelPlay
from src.RequestTable import RequestTable
from src.ServiceTable import app

def test():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
