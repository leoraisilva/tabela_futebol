from src.controller.FutebolController import app
from src.services.PredictorPlay import PredictorPlay
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import glm


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    pred = PredictorPlay()
    df = pred.dataFrame()
    modelo_gols_pro = glm(
        formula='gols_pro ~ vitorias + empates + derrotas + gols_contra + vitorias_casa + empates_casa + derrotas_casa + vitorias_fora + empates_fora + derrotas_fora + ultimas_v + ultimas_e + ultimas_d',
        data=df,
        family=sm.families.Poisson()
    ).fit()

    print(modelo_gols_pro.summary())

    print()
    print()

    modelo_gols_contra = glm(
        formula='gols_contra ~ vitorias + empates + derrotas + gols_pro + vitorias_casa + empates_casa + derrotas_casa + vitorias_fora + empates_fora + derrotas_fora + ultimas_v + ultimas_e + ultimas_d',
        data=df,
        family=sm.families.Poisson()
    ).fit()

    print(modelo_gols_contra.summary())

    modelo_simplificado = glm(
        formula='gols_pro ~ saldo_gols + aproveitamento + aproveitamento_casa + aproveitamento_fora ',
        data=df,
        family=sm.families.Poisson()
    ).fit()

    print(modelo_simplificado.summary())

    print("Razão de dispersão:", modelo_gols_pro.deviance / modelo_gols_pro.df_resid)

    # Se > 1.25, considere Binomial Negativa:
    modelo_bn = glm(
        formula='gols_pro ~ vitorias + empates + derrotas + gols_contra',
        data=df,
        family=sm.families.NegativeBinomial()
    ).fit()

    