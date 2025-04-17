import json


class ModelTable:
    def __init__(self, aproveitamento, derrotas, empates, equipe_id, escudo, faixa_classificacao, faixa_classificacao_cor,
gols_contra, gols_pro, jogos, nome_popular, ordem, pontos, saldo_gols, sigla, ultimos_jogos, variacao, vitorias):
        self.aproveitamento = aproveitamento
        self.derrotas = derrotas
        self.empates = empates
        self.equipe_id = equipe_id
        self.escudo = escudo
        self.faixa_classificacao = faixa_classificacao
        self.faixa_classificacao_cor = faixa_classificacao_cor
        self.gols_contra = gols_contra
        self.gols_pro = gols_pro
        self.jogos = jogos
        self.nome_popular = nome_popular
        self.ordem = ordem
        self.pontos = pontos
        self.saldo_gols = saldo_gols
        self.sigla = sigla
        self.ultimos_jogos = ultimos_jogos
        self.variacao = variacao
        self.vitorias = vitorias

    def to_dict(self):
        return {
            'aproveitamento': self.aproveitamento,
            'derrotas': self.derrotas,
            'empates': self.empates,
            'equipe_id': self.equipe_id,
            'escudo': self.escudo,
            'faixa_classificacao': self.faixa_classificacao,
            'faixa_classificacao_cor': self.faixa_classificacao_cor,
            'gols_contra': self.gols_contra,
            'gols_pro': self.gols_pro,
            'jogos': self.jogos,
            'nome_popular': self.nome_popular,
            'ordem': self.ordem,
            'pontos': self.pontos,
            'saldo_gols': self.saldo_gols,
            'sigla': self.sigla,
            'ultimos_jogos': self.ultimos_jogos,
            'variacao': self.variacao,
            'vitorias': self.vitorias
        }
