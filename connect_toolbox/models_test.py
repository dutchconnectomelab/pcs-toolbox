import numpy as np
import pandas as pd

from connect_toolbox import data, utils
from connect_toolbox.models import PCS


def test_pcs_evaluate():
    pcs = PCS(
        dx="schizophrenia",
        modality="functional-connectivity",
        atlas="aparc+aseg",
    )

    subject_connectivity = data.load_css(
        "schizophrenia",
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
        "aparc+aseg",
    )

    subject_score = pcs.evaluate(subject_connectivity)

    assert type(subject_score) == np.float64

    assert subject_score == np.inner(
        utils.vectorize(subject_connectivity), utils.vectorize(subject_connectivity)
    )

    connectivity = np.random.randn(82, 82, 10)
    connectivity = connectivity + np.swapaxes(connectivity, 0, 1)
    connectivity[np.diag_indices(82)] = 0

    pcs_scores = pcs.evaluate(connectivity)

    assert len(pcs_scores) == 10
    np.testing.assert_almost_equal(pcs_scores[5], pcs.evaluate(connectivity[..., 5]))


def test_pcs_fit():
    np.random.seed(42)  # for reproducibility

    # create random disease map of 100 x 100
    dm = np.random.randn(100, 100)
    dm = (dm + dm.T) / 2
    np.fill_diagonal(dm, 0)

    # create random demographics
    demographics = pd.DataFrame(
        {
            "dx": ["control"] * 64 + ["schizophrenia"] * 64,
            "age": np.random.uniform(18, 65, 128),
            "sex": np.random.choice(["male", "female"], 128),
        }
    )

    # create random subject data
    connectivity = np.random.randn(100, 100, 128)
    connectivity[:, :, 64:] += dm[..., np.newaxis]

    # add some confounding
    connectivity[:, :, demographics["sex"] == "male"] -= 0.1

    pcs = PCS()
    pcs.fit(
        demographics,
        connectivity,
        metric="cohen_d",
        variable_of_interest="dx",
        continuous_confounders=["age"],
        categorical_confounders=["sex"],
    )

    estimated_map = pcs.css

    assert estimated_map.shape == (100, 100)
    assert np.corrcoef(utils.vectorize(estimated_map), utils.vectorize(dm))[0, 1] > 0.8

    # create fresh subject data from the same distribution
    connectivity = np.random.randn(100, 100, 128)
    connectivity[:, :, 64:] += dm[..., np.newaxis]
    connectivity[:, :, demographics["sex"] == "male"] -= 0.1

    pcs_scores = pcs.evaluate(connectivity)
    assert np.mean(pcs_scores[:64]) < np.mean(pcs_scores[64:])
