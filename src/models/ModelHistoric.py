class ModelHistoric:
    def __init__(self,jogos, derrotas, vitorias, empates, gols_contra, gols_pro, nome_popular,
                 vitorias_casa, empates_casa, derrotas_casa, vitorias_fora, empates_fora, derrotas_fora,
                 ultimos_jogos):
        self.jogos = jogos
        self.derrotas = derrotas
        self.vitorias = vitorias
        self.empates = empates
        self.gols_contra = gols_contra
        self.gols_pro = gols_pro
        self.nome_popular = nome_popular
        self.vitorias_casa = vitorias_casa
        self.empates_casa = empates_casa
        self.derrotas_casa = derrotas_casa
        self.vitorias_fora = vitorias_fora
        self.empates_fora = empates_fora
        self.derrotas_fora = derrotas_fora,
        self.ultimos_jogos = ultimos_jogos


    def to_dict(self):
        return {
            'mensagem': "Success operation",
            'jogos' : self.jogos,
            'derrotas' : self.derrotas,
            'vitorias' : self.vitorias,
            'empates' : self.empates,
            'gols_contra' : self.gols_contra,
            'gols_pro' : self.gols_pro,
            'nome_popular' : self.nome_popular,
            'vitorias_casa' : self.vitorias_casa,
            'empates_casa' : self.empates_casa,
            'derrotas_casa' : self.derrotas_casa,
            'vitorias_fora' : self.vitorias_fora,
            'empates_fora' : self.empates_fora,
            'derrotas_fora' : self.derrotas_fora,
            'ultimos_jogos' : self.ultimos_jogos
        }

    def win_rate(self):
        return self.vitorias/self.jogos

    def win_rate_casa(self):
        return self.vitorias_casa/(self.vitorias_casa + self.empates_casa + self.derrotas_casa)

    def win_rate_fora(self):
        return self.vitorias_fora/(self.vitorias_fora + self.empates_fora + self.derrotas_fora)

    def lost_rate(self):
        return self.derrotas / self.jogos

    def lost_rate_casa(self):
        return self.derrotas_casa / (self.vitorias_casa + self.empates_casa + self.derrotas_casa)

    def lost_rate_fora(self):
        return self.derrotas_fora / (self.vitorias_fora + self.empates_fora + self.derrotas_fora)

    def rate_win_for_win_casa (self):
        return self.vitorias_casa/self.vitorias

    def rate_win_for_win_fora (self):
        return self.vitorias_fora/self.vitorias

    def media_gol_favor(self):
        return self.gols_pro/self.jogos

    def media_gol_contra(self):
        return self.gols_contra/self.jogos

    def saldo_gol(self):
        return  self.gols_pro - self.gols_contra