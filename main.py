from src.services.DataFrameTable import DataFrameTable
from src.services.ServiceTable import ServiceTable
from src.services.PredictorPlay import PredictorPlay
import pandas as pd

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    dtf = DataFrameTable()

    df = dtf.dataFrame('Internacional', 'Juventude')
    df = pd.concat([df, dtf.dataFrame('Botafogo', 'Fluminense')], ignore_index=True)
    df = pd.concat([df, dtf.dataFrame('Flamengo', 'Corinthians')], ignore_index=True)
    df = pd.concat([df, dtf.dataFrame('Vitória', 'Grêmio')], ignore_index=True)
    df = pd.concat([df, dtf.dataFrame('Palmeiras', 'Bahia')], ignore_index=True)
    df = pd.concat([df, dtf.dataFrame('Cruzeiro', 'Vasco')], ignore_index=True)
    df = pd.concat([df, dtf.dataFrame('Santos', 'Bragantino')], ignore_index=True)


    X = df[['vitorias', 'empates', 'derrotas', 'gols_contra']]
    y = df['gols_pro']

    model = PredictorPlay(auto_dispersion=True)
    model.fit(X, y)

    print(model.summary())
    print("\nParâmetros:", model.get_params())

    novo_time = pd.DataFrame({
        'vitorias': [8],
        'empates': [4],
        'derrotas': [3],
        'gols_contra': [12]
    })

    previsao = model.predict(novo_time)
    print(f"\nGols pró previstos: {previsao[0]:.2f}")
