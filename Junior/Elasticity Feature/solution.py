"""Модуль рассчета коэффициента детерминации как эластичности товара"""
import pandas as pd
import numpy as np
from scipy import stats


def elasticity_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    :param df:
    sku — уникальный идентификатор товара.
    dates — уникальный день.
    price — средняя цена для товара-дня.
    qty — суммарное кол-во покупок.
    :return:
    sku - уникальный идентификатор товара.
    elasticity -  коэффициент детерминации линейной регрессии R2 как оценка эластичности товара
    """
    df_copy = df.copy()
    df_copy['qty'] = df_copy['qty'].apply(lambda x: np.log(x + 1))
    groups = df_copy.groupby('sku')
    result = pd.DataFrame({'sku': [], 'elasticity': []})
    for i, group in groups:
        predictor = group['price']
        target = group['qty']
        result.loc[len(result.index)] = {'sku': i, 'elasticity': stats.linregress(predictor, target).rvalue ** 2}
    result['sku'] = result['sku'].astype('int64')
    return result
