from inspect import getcallargs

import numpy as np

from connect_toolbox import validate


def vectorize(matrix):
    validate.symmetric(matrix)
    if matrix.ndim == 3:
        return np.array([vectorize(matrix[..., i]) for i in range(matrix.shape[-1])]).T
    validate.zero_diagonal(matrix)
    return matrix[np.triu_indices(matrix.shape[0], k=1)]


def devectorize(vector: np.ndarray) -> np.ndarray:
    assert (
        type(vector) == np.ndarray
    ), f"Input must be a numpy array, instead got {type(vector)}."
    if vector.ndim == 2:
        res = np.array([devectorize(vector[:, i]) for i in range(vector.shape[1])])

        return np.moveaxis(res, 0, -1)
    n = int(0.5 * (1 + np.sqrt(1 + 8 * len(vector))))
    assert n * (n - 1) == 2 * len(
        vector
    ), f"Vector length ({len(vector)}) is not compatible with a square matrix."
    matrix = np.zeros((n, n))
    matrix[np.triu_indices(n, k=1)] = vector
    matrix += matrix.T
    return matrix
