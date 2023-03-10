"""Metrics."""

from typing import Any, Dict, Union, List
from dataclasses import dataclass
import datetime

import pandas as pd
import numpy as np


@dataclass
class Metric:
    """Base class for Metric"""

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {}


@dataclass
class CountTotal(Metric):
    """Total number of rows in DataFrame"""

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {"total": len(df)}


@dataclass
class CountZeros(Metric):
    """Number of zeros in choosen column"""

    column: str

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = sum(df[self.column] == 0)
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountNull(Metric):
    """Number of empty values in choosen columns"""

    columns: List[str]
    aggregation: str = "any"  # either "all", or "any"

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        if self.aggregation == "any":
            k = sum(df[self.columns].isnull().any(axis=1))
        else:
            k = sum(df[self.columns].isnull().all(axis=1))
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountDuplicates(Metric):
    """Number of duplicates in choosen columns"""

    columns: List[str]

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = sum(df[self.columns].duplicated())
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountValue(Metric):
    """Number of values in choosen column"""

    column: str
    value: Union[str, int, float]

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = len(df[df[self.column] == self.value])
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountBelowValue(Metric):
    """Number of values below threshold"""

    column: str
    value: float
    strict: bool = False

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = sum(df[self.column] < self.value)
        if not self.strict:
            k += sum(df[self.column] == self.value)
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountBelowColumn(Metric):
    """Count how often column X below Y"""

    column_x: str
    column_y: str
    strict: bool = False

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = sum(df[self.column_x] < df[self.column_y])
        if not self.strict:
            k += sum(df[self.column_x] == df[self.column_y])
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountRatioBelow(Metric):
    """Count how often X / Y below Z"""

    column_x: str
    column_y: str
    column_z: str
    strict: bool = False

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        n = len(df)
        k = sum((df[self.column_x] / df[self.column_y]) < df[self.column_z])
        if not self.strict:
            k += sum((df[self.column_x] / df[self.column_y]) == df[self.column_z])
        return {"total": n, "count": k, "delta": k / n}


@dataclass
class CountCB(Metric):
    """Calculate lower/upper bounds for N%-confidence interval"""

    column: str
    conf: float = 0.95

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        lcb = np.percentile(df[self.column], [100 * (1 - self.conf) / 2, 100 * (1 - (1 - self.conf) / 2)])[0]
        ucb = np.percentile(df[self.column], [100 * (1 - self.conf) / 2, 100 * (1 - (1 - self.conf) / 2)])[1]
        # m = df[self.column].mean()
        # s = df[self.column].std()
        # dof = len(df[self.column]) - 1
        # t_crit = np.abs(t.ppf((1 - self.conf) / 2, dof))
        # lcb = m - s * t_crit / np.sqrt(len(df[self.column]))
        # ucb = m + s * t_crit / np.sqrt(len(df[self.column]))
        return {"lcb": lcb, "ucb": ucb}


@dataclass
class CountLag(Metric):
    """A lag between the latest date and today"""

    column: str
    fmt: str = "%Y-%m-%d"

    def __call__(self, df: pd.DataFrame) -> Dict[str, Any]:
        a = datetime.datetime.now().strftime(self.fmt)
        df[self.column] = pd.to_datetime(df[self.column])
        b = df[self.column].agg('max').strftime(self.fmt)
        lag = (datetime.datetime.strptime(a, self.fmt) - datetime.datetime.strptime(b, self.fmt)).days
        return {"today": a, "last_day": b, "lag": lag}
