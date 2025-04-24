import warnings
import pandas as pd
import statsmodels.api as sm
from statsmodels.genmod.families import NegativeBinomial, Poisson
from statsmodels.tools.tools import add_constant

class PredictorPlay:
    def __init__(self, alpha=None, auto_dispersion=True):
        self.alpha = alpha
        self.auto_dispersion = auto_dispersion
        self.model = None
        self.is_negative_binomial = False

    def check_dispersion(self, y, X):
        model_poisson = sm.GLM(y, X, family=Poisson()).fit(disp=0)
        chi2 = sum(model_poisson.resid_pearson ** 2)
        dispersion = chi2 / model_poisson.df_resid
        return dispersion > 1.25

    def fit(self, X, y):
        X = add_constant(X.copy())
        self.feature_names = X.columns.tolist()

        if self.auto_dispersion and self.check_dispersion(y, X):
            family = NegativeBinomial(alpha=self.alpha) if self.alpha else NegativeBinomial()
            self.is_negative_binomial = True
        else:
            family = Poisson()
            self.is_negative_binomial = False

        self.model = sm.GLM(y, X, family=family).fit()
        return self

    def predict(self, X):
        if not self.model:
            raise ValueError("Modelo não treinado. Chame .fit() primeiro.")
        X = add_constant(X.copy(), has_constant='add')
        return self.model.predict(X)

    def summary(self):
        """Retorna o resumo do modelo."""
        return self.model.summary() if self.model else "Modelo não treinado."

    def get_params(self):
        """Retorna os coeficientes do modelo."""
        if self.model:
            return {
                'params': self.model.params.to_dict(),
                'dispersion': self.alpha if self.is_negative_binomial else None
            }
        return None