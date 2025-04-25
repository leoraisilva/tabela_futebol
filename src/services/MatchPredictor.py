from typing import Dict, Tuple

import numpy as np
import pandas as pd
from scipy.stats import poisson

from src.services.PredictorPlay import PredictorPlay


class MatchPredictor:

    def __init__(self, model: PredictorPlay, max_goals: int = 8):

        self.model = model
        self.max_goals = max_goals
        self._goal_matrix = None

    def predict_match(self, home_stats: Dict, away_stats: Dict) -> Dict:
        try:
            # Previsão de gols
            home_mean = self._predict_goals(home_stats)
            away_mean = self._predict_goals(away_stats)

            # Cálculo de probabilidades
            probs = self._calculate_probabilities(home_mean, away_mean)

            # Placar mais provável
            likely_score = self._most_likely_score(home_mean, away_mean)

            return {
                'home_goals_mean': home_mean,
                'away_goals_mean': away_mean,
                'probabilities': probs,
                'most_likely_score': likely_score,
                'score_matrix': self._goal_matrix,
                'over_under': self._calculate_over_under(home_mean, away_mean)
            }

        except Exception as e:
            raise ValueError(f"Falha na previsão do jogo: {str(e)}")

    def _predict_goals(self, stats: Dict) -> float:
        """Preve a média de gols para um conjunto de estatísticas."""
        stats_df = pd.DataFrame([stats])
        return max(0.1, float(self.model.predict(stats_df)[0]))  # Evita valores negativos

    def _calculate_probabilities(self, home_mean: float, away_mean: float) -> Dict:
        """Calcula probabilidades de resultados usando distribuição Poisson."""
        self._goal_matrix = np.zeros((self.max_goals + 1, self.max_goals + 1))

        # Preenche a matriz de probabilidades
        for i in range(self.max_goals + 1):
            for j in range(self.max_goals + 1):
                self._goal_matrix[i, j] = poisson.pmf(i, home_mean) * poisson.pmf(j, away_mean)

        # Normaliza a matriz
        self._goal_matrix /= self._goal_matrix.sum()

        # Calcula probabilidades totais
        win_prob = np.sum(np.triu(self._goal_matrix, 1))  # Triângulo superior
        draw_prob = np.sum(np.diag(self._goal_matrix))  # Diagonal
        lose_prob = np.sum(np.tril(self._goal_matrix, -1))  # Triângulo inferior

        return {
            'win': win_prob,
            'draw': draw_prob,
            'lose': lose_prob,
            'both_to_score': 1 - (poisson.pmf(0, home_mean) + poisson.pmf(0, away_mean) -
                                  (poisson.pmf(0, home_mean) * poisson.pmf(0, away_mean))
                                  )
        }

    def _most_likely_score(self, home_mean: float, away_mean: float) -> Tuple[int, int]:
        """Determina o placar mais provável."""
        if self._goal_matrix is None:
            self._calculate_probabilities(home_mean, away_mean)
        idx = np.unravel_index(self._goal_matrix.argmax(), self._goal_matrix.shape)
        return (idx[0], idx[1])

    def _calculate_over_under(self, home_mean: float, away_mean: float,
                              thresholds: list = [0.5, 1.5, 2.5, 3.5]) -> Dict:
        """Calcula probabilidades over/under para vários thresholds."""
        total_mean = home_mean + away_mean
        return {
            f"over_{thresh}": 1 - poisson.cdf(thresh, total_mean)
            for thresh in thresholds
        }

    def get_odds(self, probabilities: Dict) -> Dict:
        """Converte probabilidades em odds decimais."""
        return {
            'win': 1 / probabilities['win'],
            'draw': 1 / probabilities['draw'],
            'lose': 1 / probabilities['lose']
        }