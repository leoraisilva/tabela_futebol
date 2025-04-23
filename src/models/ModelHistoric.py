class ModelHistoric:
    def __init__(self,jogos, derrotas, vitorias, empates, gols_contra, gols_pro, nome_popular,
                 vitorias_casa, empates_casa, derrotas_casa, vitorias_fora, empates_fora, derrotas_fora):
        self.jogos = jogos
        self.derrotas = derrotas
        self.vitorias = vitorias
        self.empates = empates
        self.gols_contra = gols_contra
        self.gols_pro = gols_pro
        self.saldo_gols = self.gols_pro - self.gols_contra
        self.nome_popular = nome_popular
        self.vitorias_casa = vitorias_casa
        self.empates_casa = empates_casa
        self.derrotas_casa = derrotas_casa
        self.vitorias_fora = vitorias_fora
        self.empates_fora = empates_fora
        self.derrotas_fora = derrotas_fora

    def to_dict(self):
        return {
            'mensagem': "Success operation",
            "jogos" : self.jogos,
            "derrotas" : self.derrotas,
            "vitorias" : self.vitorias,
            "empates" : self.empates,
            "gols_contra" : self.gols_contra,
            "gols_pro" : self.gols_pro,
            "saldo_gols" : self.saldo_gols,
            "nome_popular" : self.nome_popular,
            "vitorias_casa" : self.vitorias_casa,
            "empates_casa" : self.empates_casa,
            "derrotas_casa" : self.derrotas_casa,
            "vitorias_fora" : self.vitorias_fora,
            "empates_fora" : self.empates_fora,
            "derrotas_fora" : self.derrotas_fora
        }