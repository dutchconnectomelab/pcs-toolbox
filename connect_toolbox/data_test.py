import numpy as np

from connect_toolbox import data, utils


def test_load_css():
    css = data.load_css(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc+aseg",
    )

    assert css.shape == (82, 82)

    # check that the matrix is symmetric
    np.testing.assert_allclose(css, css.T, atol=1e-8)

    # check diagonal is 0
    assert np.all(np.diag(css) == 0)

    # check that the mean is negative
    vals = utils.vectorize(css)
    assert np.mean(vals) < 0

    css_aparc = data.load_css(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc",
    )

    assert css_aparc.shape == (68, 68)

    np.testing.assert_allclose(css[14:, 14:], css_aparc, atol=1e-8)
