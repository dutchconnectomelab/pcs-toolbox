import numpy as np

from connect_toolbox import utils


def test_vectorize():
    matrix = np.array(
        [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ]
    )
    np.testing.assert_equal(utils.vectorize(matrix), [1, 2, 3])

    # generate random matrix (symmetric, zero diagonal)
    matrix = np.random.randn(4, 4, 5)
    matrix = matrix + np.swapaxes(matrix, 0, 1)
    matrix[np.diag_indices(4)] = 0

    vector = utils.vectorize(matrix)
    assert vector.shape == (6, 5)
    np.testing.assert_equal(vector[:, 0], utils.vectorize(matrix[..., 0]))


def test_devectorize():
    matrix = np.array(
        [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ]
    )
    np.testing.assert_equal(utils.devectorize(np.array([1, 2, 3])), matrix)

    # generate random matrix (symmetric, zero diagonal)
    matrix = np.random.randn(4, 4, 5)
    matrix = matrix + np.swapaxes(matrix, 0, 1)
    matrix[np.diag_indices(4)] = 0

    vector = utils.vectorize(matrix)
    np.testing.assert_equal(utils.devectorize(vector), matrix)
