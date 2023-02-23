import numpy as np
from scipy import stats


def calculate_sample_size(
        reward_avg: float, reward_std: float, mde: float, alpha: float, beta: float
) -> int:
    """Calculate sample size.

    Parameters
    ----------
    reward_avg: float :
        average reward
    reward_std: float :
        standard deviation of reward
    mde: float :
        minimum detectable effect
    alpha: float :
        significance level
    beta: float :
        type 2 error probability

    Returns
    -------
    int :
        sample size

    """
    assert mde > 0, "mde should be greater than 0"

    # Implement your solution here

    sample_size = int(np.floor(
        (2 * np.power((stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(1 - beta)) * reward_std, 2)) / (
                    np.power(mde, 2) * 100)
    ))

    return sample_size


def calculate_mde(
        reward_std: float, sample_size: int, alpha: float, beta: float
) -> float:
    """Calculate minimal detectable effect.

    Parameters
    ----------
    reward_std: float :
        standard deviation of reward
    sample_size: int :
        sample size
    alpha: float :
        significance level
    beta: float :
        type 2 error probability

    Returns
    -------
    float :
        minimal detectable effect

    """

    # Implement your solution here
    mde = np.sqrt(2) * (stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(1 - beta)) * reward_std / np.sqrt(
        sample_size)

    return mde
