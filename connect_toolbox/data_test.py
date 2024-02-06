from pathlib import Path

import numpy as np

from connect_toolbox import data, utils


def test_list_studies():
    sz_studies = data.list_studies(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc+aseg",
    )
    assert "COBRE" in sz_studies

    ad_studies = data.list_studies(
        "alzheimer", "functional-connectivity", "gmean_scrubbed_0.01-0.1", "aparc+aseg"
    )
    assert "COBRE" not in ad_studies


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


def test_compute_css():
    css = data.compute_css(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc+aseg",
        "all_studies",
    )

    assert css.shape == (82, 82)

    np.testing.assert_allclose(css, css.T, atol=1e-8)
    assert np.all(np.diag(css) == 0)

    vals = utils.vectorize(css)
    assert np.mean(vals) < 0

    css_precomputed = data.load_css(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc+aseg",
    )

    assert (
        np.corrcoef(utils.vectorize(css), utils.vectorize(css_precomputed))[0, 1] > 0.95
    )

    css = data.compute_css(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc+aseg",
        ["COBRE"],
    )

    dm_cobre = (
        Path(__file__).parent.parent
        / "diseasemaps"
        / "schizophrenia"
        / "functional-connectivity"
        / "aparc+aseg"
        / "gmean_scrubbed_0.01-0.1"
        / "studies"
        / "COBRE"
        / "cohen_d.csv"
    )

    css_precomputed = np.genfromtxt(dm_cobre, delimiter=",")
    css_precomputed = np.triu(css_precomputed, 1)
    css_precomputed += css_precomputed.T
    np.testing.assert_almost_equal(
        utils.vectorize(css), utils.vectorize(css_precomputed), decimal=5
    )
