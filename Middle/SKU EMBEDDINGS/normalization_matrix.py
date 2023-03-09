import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


class Normalization:
    @staticmethod
    def by_column(matrix: csr_matrix) -> csr_matrix:
        """Normalization by column

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        # Normalize the matrix by column
        norm_matrix = matrix.multiply(1 / matrix.sum(axis=0))
        return norm_matrix.tocsr()

    @staticmethod
    def by_row(matrix: csr_matrix) -> csr_matrix:
        """Normalization by row

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        # Normalize the matrix by row
        norm_matrix = matrix.multiply(1 / matrix.sum(axis=1))
        return norm_matrix.tocsr()

    @staticmethod
    def tf_idf(matrix: csr_matrix) -> csr_matrix:
        """Normalization using tf-idf

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        # Calculate the term frequency (TF)
        tf = Normalization.by_row(matrix)

        # Calculate the inverse document frequency (IDF)
        n_users = matrix.shape[0]
        idf = np.log(n_users / matrix.astype(bool).sum(axis=0))

        # Normalization using tf-idf
        norm_matrix = tf.multiply(idf)
        return norm_matrix.tocsr()

    @staticmethod
    def bm_25(
            matrix: csr_matrix, k1: float = 2.0, b: float = 0.75
    ) -> csr_matrix:
        """Normalization based on BM-25

        Args:
            matrix (csr_matrix): User-Item matrix of size (N, M)

        Returns:
            csr_matrix: Normalized matrix of size (N, M)
        """
        # Calculate the term frequency (TF)
        tf = Normalization.by_row(matrix)

        # Calculate the inverse document frequency (IDF)
        n_users = matrix.shape[0]
        idf = np.log(n_users / matrix.astype(bool).sum(axis=0))

        k = (k1 * ((1 - b) + b * (matrix.sum(axis=1) / matrix.mean())))
        norm_matrix = tf.multiply((k1 + b) / (tf + k)) * idf
        return norm_matrix.tocsr()
