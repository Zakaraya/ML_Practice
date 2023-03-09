from typing import Dict

import pandas as pd
from scipy.sparse import csr_matrix


class UserItemMatrix:
    def __init__(self, sales_data: pd.DataFrame):
        """Class initialization. You can make necessary
        calculations here.

        Args:
            sales_data (pd.DataFrame): Sales dataset.

        Example:
            sales_data (pd.DataFrame):

                user_id  item_id  qty   price
            0        1      118    1   626.66
            1        1      285    1  1016.57
            2        2     1229    3   518.99
            3        4     1688    2   940.84
            4        5     2068    1   571.36
            ...

        """
        self.sales_data = sales_data
        self.user_id = sales_data['user_id'].unique()
        self.item_id = sales_data['item_id'].unique()
        self.user_id = sorted(self.user_id)
        self.item_id = sorted(self.item_id)

    @property
    def user_count(self) -> int:
        """
        Returns:
            int: the number of users in sales_data.
        """
        return len(self.user_id)

    @property
    def item_count(self) -> int:
        """
        Returns:
            int: the number of items in sales_data.
        """
        return len(self.item_id)

    @property
    def user_map(self) -> Dict[int, int]:
        """Creates a mapping from user_id to matrix rows indexes.

        Example:
            sales_data (pd.DataFrame):

                user_id  item_id  qty   price
            0        1      118    1   626.66
            1        1      285    1  1016.57
            2        2     1229    3   518.99
            3        4     1688    2   940.84
            4        5     2068    1   571.36

            user_map (Dict[int, int]):
                {1: 0, 2: 1, 4: 2, 5: 3}

        Returns:
            Dict[int, int]: User map
        """
        user_id_matrix = {}
        for i in range(len(self.user_id)):
            user_id_matrix[self.user_id[i]] = i
        return user_id_matrix

    @property
    def item_map(self) -> Dict[int, int]:
        """Creates a mapping from item_id to matrix rows indexes.

        Example:
            sales_data (pd.DataFrame):

                user_id  item_id  qty   price
            0        1      118    1   626.66
            1        1      285    1  1016.57
            2        2     1229    3   518.99
            3        4     1688    2   940.84
            4        5     2068    1   571.36

            item_map (Dict[int, int]):
                {118: 0, 285: 1, 1229: 2, 1688: 3, 2068: 4}

        Returns:
            Dict[int, int]: Item map
        """
        item_id_matrix = {}
        for i in range(len(self.item_id)):
            item_id_matrix[self.item_id[i]] = i
        return item_id_matrix

    @property
    def csr_matrix(self) -> csr_matrix:
        """User items matrix in form of CSR matrix.

        User row_ind, col_ind as
        rows and cols indecies (mapped from user/item map).

        Returns:
            csr_matrix: CSR matrix
        """
        data = self.sales_data['qty']
        row = list(map(lambda x: self.user_map[x], self.sales_data['user_id']))
        col = list(map(lambda x: self.item_map[x], self.sales_data['item_id']))
        return csr_matrix((data, (row, col)), shape=(self.user_count, self.item_count))
