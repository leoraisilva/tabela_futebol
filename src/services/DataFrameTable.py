import pandas as pd

class DataFrameTable:

    def dataFrame(self, dados):
        colunas = [
            'nome_popular',
            'jogos',
            'vitorias',
            'empates',
            'derrotas',
            'gols_pro',
            'gols_contra',
            'vitorias_casa',
            'empates_casa',
            'derrotas_casa',
            'vitorias_fora',
            'empates_fora',
            'derrotas_fora',
            'ultimas_partidas',
        ]
        df = pd.DataFrame(columns=colunas)
        dados_times = []
        for dado in dados:
            aux = {
                'nome_popular': dado.nome_popular,
                'jogos': dado.jogos,
                'vitorias': dado.vitorias,
                'empates': dado.empates,
                'derrotas': dado.derrotas,
                'gols_pro': dado.gols_pro,
                'gols_contra': dado.gols_contra,
                'vitorias_casa': dado.vitorias_casa,
                'empates_casa': dado.empates_casa,
                'derrotas_casa': dado.derrotas_casa,
                'vitorias_fora': dado.vitorias_fora,
                'empates_fora': dado.empates_fora,
                'derrotas_fora': dado.derrotas_fora,
                'ultimas_partidas': dado.ultimos_jogos
            }
            dados_times.append(aux)
        df = pd.DataFrame(dados_times)
        df['derrotas_fora'] = df['derrotas_fora'].apply(
            lambda x: x[0] if isinstance(x, tuple) else x
        )
        df['ultimas_partidas'] = df['ultimas_partidas'].apply(
            lambda x: x[0] if isinstance(x, tuple) else x
        )
        df['gols_pro'] = pd.to_numeric(df['gols_pro'], errors='coerce')
        df['gols_contra'] = pd.to_numeric(df['gols_contra'], errors='coerce')

        df['saldo_gols'] = df['gols_pro'] - df['gols_contra']
        df['aproveitamento'] = (df['vitorias'] * 3 + df['empates']) / (df['jogos'] * 3)
        df['aproveitamento_casa'] = (df['vitorias_casa'] * 3 + df['empates_casa']) / (
                (df['vitorias_casa'] + df['empates_casa'] + df['derrotas_casa']) * 3)
        df['aproveitamento_fora'] = (df['vitorias_fora'] * 3 + df['empates_fora']) / (
                (df['vitorias_fora'] + df['empates_fora'] + df['derrotas_fora']) * 3)

        # Processando a coluna 'ultimas_partidas' para extrair features
        def calcular_ultimos_resultados(sequencia):
            v = sequencia.count('v')
            e = sequencia.count('e')
            d = sequencia.count('d')
            return pd.Series([v, e, d], index=['ultimas_v', 'ultimas_e', 'ultimas_d'])

        df[['ultimas_v', 'ultimas_e', 'ultimas_d']] = df['ultimas_partidas'].apply(calcular_ultimos_resultados)

        return df