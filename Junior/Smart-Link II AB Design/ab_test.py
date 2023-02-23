import numpy as np
from typing import Tuple
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


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


def ab_test(
        n_simulations: int,
        n_samples: int,
        conversion_rate: float,
        mde: float,
        reward_avg: float,
        reward_std: float,
        alpha: float = 0.05,
) -> float:
    """Do the A/B test (simulation)."""

    type_2_errors = np.zeros(n_simulations)
    for i in range(n_simulations):
        # Generate one cpc sample with the given conversion_rate, reward_avg, and reward_std
        # Generate another cpc sample with the given conversion_rate * mde, reward_avg, and reward_std
        # Check t-test and save type 2 error
        cpc_a = cpc_sample(n_samples, conversion_rate, reward_avg, reward_std)
        cpc_b = cpc_sample(n_samples, conversion_rate * (1 + mde), reward_avg, reward_std)
        t_statistic = t_test(cpc_a, cpc_b, alpha)[0]
        type_2_errors[i] = not t_statistic
    # Calculate the type 2 errors rate
    type_2_errors_rate = sum(type_2_errors) / len(type_2_errors)

    return type_2_errors_rate
