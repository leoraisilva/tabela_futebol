import warnings
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.genmod.families import NegativeBinomial, Poisson
from statsmodels.tools.tools import add_constant
from sklearn.metrics import mean_poisson_deviance
from scipy.stats import poisson
from typing import Dict, Union, Tuple


class PredictorPlay:
    def __init__(self, alpha: float = None, auto_dispersion: bool = True, verbose: bool = False):
        """
        Inicializa o modelo de regressão para dados de contagem.

        Args:
            alpha: Parâmetro de dispersão para Binomial Negativa
            auto_dispersion: Se True, escolhe automaticamente entre Poisson e Binomial Negativa
            verbose: Se True, mostra mensagens detalhadas de diagnóstico
        """
        self.alpha = alpha
        self.auto_dispersion = auto_dispersion
        self.verbose = verbose
        self.model = None
        self.is_negative_binomial = False
        self.feature_names = None
        self._last_dispersion = None
        self._training_stats = None

    def _clean_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepara e limpa os dados de entrada."""
        X = pd.DataFrame(X).copy()
        y = pd.Series(y).copy()

        # Tratamento de valores especiais
        X = X.replace([np.inf, -np.inf], np.nan)
        valid_rows = ~X.isnull().any(axis=1) & ~y.isnull()

        X_clean = X[valid_rows].apply(pd.to_numeric, errors='coerce')
        y_clean = pd.to_numeric(y[valid_rows], errors='coerce')

        valid_rows = ~X_clean.isnull().any(axis=1) & ~y_clean.isnull()

        if self.verbose and (len(X) != len(X_clean[valid_rows])):
            removed = len(X) - len(X_clean[valid_rows])
            print(f"[INFO] Removidas {removed} linhas com dados inválidos")

        return X_clean[valid_rows], y_clean[valid_rows]

    def _check_dispersion(self, y: pd.Series, X: pd.DataFrame) -> bool:
        """Verifica a presença de superdispersão nos dados."""
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = sm.GLM(y, X, family=Poisson()).fit(disp=0)
                chi2 = np.sum(model.resid_pearson ** 2)
                dispersion = chi2 / model.df_resid
                self._last_dispersion = dispersion

                if self.verbose:
                    print(f"[DIAGNÓSTICO] Razão de dispersão: {dispersion:.3f}")
                    print(f"[DIAGNÓSTICO] {'Superdispersão detectada' if dispersion > 1.25 else 'Dispersão adequada'}")

                return dispersion > 1.25
        except Exception as e:
            if self.verbose:
                print(f"[ERRO] Verificação de dispersão falhou: {str(e)}")
            return False

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'PredictorPlay':
        """Treina o modelo com os dados fornecidos."""
        try:
            X_clean, y_clean = self._clean_data(X, y)

            if len(X_clean) < 10:
                raise ValueError(f"Dados insuficientes. Apenas {len(X_clean)} observações válidas.")

            X_clean = add_constant(X_clean)
            self.feature_names = X_clean.columns.tolist()

            # Seleção automática do modelo
            if self.auto_dispersion and self._check_dispersion(y_clean, X_clean):
                family = NegativeBinomial(alpha=self.alpha) if self.alpha else NegativeBinomial()
                self.is_negative_binomial = True
                if self.verbose:
                    print("[MODELO] Usando distribuição Binomial Negativa")
            else:
                family = Poisson()
                self.is_negative_binomial = False
                if self.verbose:
                    print("[MODELO] Usando distribuição Poisson")

            # Treinamento do modelo
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.model = sm.GLM(y_clean, X_clean, family=family).fit()
                self._training_stats = {
                    'n_obs': len(y_clean),
                    'deviance': self.model.deviance,
                    'aic': self.model.aic,
                    'bic': self.model.bic_llf
                }

            return self

        except Exception as e:
            raise ValueError(f"Falha no ajuste do modelo: {str(e)}")

    def predict(self, X: pd.DataFrame, return_ci: bool = False,
                alpha: float = 0.05) -> Union[pd.Series, Tuple[pd.Series, pd.Series, pd.Series]]:
        """Faz previsões para novos dados."""
        if not self.model:
            raise ValueError("Modelo não treinado. Execute o método fit() primeiro.")

        try:
            X = add_constant(pd.DataFrame(X).copy(), has_constant='add')

            if return_ci:
                pred = self.model.get_prediction(X)
                ci = pred.conf_int(alpha=alpha)
                return pred.predicted_mean, ci[:, 0], ci[:, 1]
            return self.model.predict(X)

        except Exception as e:
            raise ValueError(f"Falha na previsão: {str(e)}")

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Avalia o modelo em dados de teste."""
        try:
            y_pred = self.predict(X)
            return {
                'deviance': mean_poisson_deviance(y, y_pred),
                'mae': np.mean(np.abs(y - y_pred)),
                'mse': np.mean((y - y_pred) ** 2)
            }
        except Exception as e:
            raise ValueError(f"Falha na avaliação: {str(e)}")

    def summary(self) -> str:
        """Retorna um resumo estatístico do modelo."""
        if not self.model:
            return "Modelo não treinado. Execute o método fit() primeiro."

        summary = str(self.model.summary())

        if self.verbose and self._last_dispersion:
            print(f"\n[DIAGNÓSTICO] Razão de dispersão: {self._last_dispersion:.3f}")
            if self._last_dispersion > 1.25 and not self.is_negative_binomial:
                print("[AVISO] Superdispersão detectada - considere usar Binomial Negativa")

        return summary

    def get_params(self, as_frame: bool = False) -> Union[Dict, pd.DataFrame]:
        """Retorna os parâmetros do modelo."""
        if not self.model:
            return None

        params = {
            'params': self.model.params.to_dict(),
            'dispersion': self.alpha if self.is_negative_binomial else None,
            'family': 'NegativeBinomial' if self.is_negative_binomial else 'Poisson',
            'stats': self._training_stats
        }

        return pd.DataFrame.from_dict(params['params'], orient='index', columns=['coef']) if as_frame else params