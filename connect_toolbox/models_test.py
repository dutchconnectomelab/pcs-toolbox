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
    ) / len(utils.vectorize(subject_connectivity))

    connectivity = np.random.randn(82, 82, 10)
    connectivity = connectivity + np.swapaxes(connectivity, 0, 1)
    connectivity[np.diag_indices(82)] = 0

    pcs_scores = pcs.evaluate(connectivity)

    assert len(pcs_scores) == 10
    np.testing.assert_almost_equal(pcs_scores[5], pcs.evaluate(connectivity[..., 5]))
