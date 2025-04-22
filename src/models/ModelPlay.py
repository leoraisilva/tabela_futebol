
class ModelPlay:
    def __init__ (self, data_realizacao, mandante_escudo, mandante_escudo_nome_popular,
                  visitante_escudo, visitante_escudo_nome_popular, hora_realizacao, jogo_ja_comecou,
                  placar_oficial_mandante, placar_oficial_visitante, sede ):
        self.data_realizacao = data_realizacao
        self.mandante_escudo = mandante_escudo
        self.mandante_escudo_nome_popular = mandante_escudo_nome_popular
        self.visitante_escudo = visitante_escudo
        self.visitante_escudo_nome_popular = visitante_escudo_nome_popular
        self.hora_realizacao = hora_realizacao
        self.jogo_ja_comecou = jogo_ja_comecou
        self.placar_oficial_mandante = placar_oficial_mandante
        self.placar_oficial_visitante = placar_oficial_visitante
        self.sede = sede

    def to_dict(self):
        return {
            'mensagem': "Success operation",
            'data_realizacao': self.data_realizacao,
            'mandante_escudo': self.mandante_escudo,
            'mandante_escudo_nome_popular': self.mandante_escudo_nome_popular,
            'visitante_escudo': self.visitante_escudo,
            'visitante_escudo_nome_popular': self.visitante_escudo_nome_popular,
            'hora_realizacao': self.hora_realizacao,
            'jogo_ja_comecou': self.jogo_ja_comecou,
            'placar_oficial_mandante': self.placar_oficial_mandante,
            'placar_oficial_visitante': self.placar_oficial_visitante,
            'sede': self.sede
        }
