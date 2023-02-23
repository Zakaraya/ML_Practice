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


def ab_test_p_values(
        n_simulations: int,
        n_samples: int,
        conversion_rate: float,
        mde: float,
        reward_avg: float,
        reward_std: float,
        alpha: float = 0.05,
) -> float:
    """Do the A/B test (simulation) and collect p-values."""
    p_values = []
    for i in range(n_simulations):
        # Generate two cpc samples with the same cvr, reward_avg, and reward_std
        # Check t-test and save p-value
        cpc_a = cpc_sample(n_samples, conversion_rate, reward_avg, reward_std)
        cpc_b = cpc_sample(n_samples, conversion_rate * (1 + mde), reward_avg, reward_std)
        p_value = t_test(cpc_a, cpc_b, alpha)[1]
        p_values.append(p_value)

    # Plot the histogram of p-values
    plt.hist(p_values, bins=50)
    plt.xlabel('p-value')
    plt.ylabel('Frequency')
    plt.title('Distribution of p-values')
    plt.show()
    sns.kdeplot(p_values, shade=True)
    plt.show()

    # Calculate the type 1 errors rate
    type_1_errors_rate = sum([p < alpha for p in p_values]) / len(p_values)

    return type_1_errors_rate


ab_test_p_values(n_simulations=1000, n_samples=100, conversion_rate=0.5, mde=0.1, reward_avg=1, reward_std=0.6,
                 alpha=0.05)
