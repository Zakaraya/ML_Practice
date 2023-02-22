import numpy as np
from typing import Tuple
from scipy import stats


def cpc_sample(
        n_samples: int, conversion_rate: float, reward_avg: float, reward_std: float
) -> np.ndarray:
    """Sample data."""
    # конверсия совершения действия (action) пользователем, conversion rate
    cvr = np.random.binomial(n=1, p=conversion_rate, size=n_samples)
    # плата за действие, cost-per-action
    cpa = np.random.normal(loc=reward_avg, scale=reward_std, size=n_samples)
    # плата за клик, cost-per-click
    cpc = cpa * cvr
    return cpc


def t_test(cpc_a: np.ndarray, cpc_b: np.ndarray, alpha=0.05
) -> Tuple[bool, float]:
    """Perform t-test.

    Parameters
    ----------
    cpc_a: np.ndarray :
        first samples
    cpc_b: np.ndarray :
        second samples
    alpha :
         (Default value = 0.05)

    Returns
    -------
    Tuple[bool, float] :
        True if difference is significant, False otherwise
        p-value
    """
    p_value = stats.ttest_ind(cpc_a, cpc_b)[1]
    return (True, p_value) if p_value < alpha else (False, p_value)
