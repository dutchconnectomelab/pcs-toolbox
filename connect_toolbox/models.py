from typing import Iterable, Optional, Union

import numpy as np

import connect_toolbox.data
from connect_toolbox import utils, validate


class PCS(object):

    def __init__(
        self,
        *,
        dx: Optional[str] = None,
        modality: str = "fmri",
        metric: str = "gmean_scrubbed_0.01-0.1",
        atlas: str = "aparc+aseg",
        study: Union[Iterable[str], str] = "mega_analysis",
    ) -> None:
        validate.dx(dx)
        validate.modality_and_metric(modality, metric)
        validate.atlas(atlas)
        if dx:
            self.dx = dx
            self.modality = modality
            self.metric = metric
            self.atlas = atlas
            self.study = study
            if study == "mega_analysis":
                self.connectome_summary_statistics = connect_toolbox.data.load_css(
                    dx=dx, modality=modality, metric=metric, atlas=atlas
                )
            else:
                self.connectome_summary_statistics = connect_toolbox.data.compute_css(
                    dx=dx, modality=modality, metric=metric, atlas=atlas, study=study
                )
        else:
            self.dx = None
            self.modality = None
            self.metric = None
            self.atlas = None
            self.study = None
            self.connectome_summary_statistics = None

    def assert_fitted(self) -> None:
        assert self.dx is not None, "PCS model not fitted yet."
        assert (
            self.connectome_summary_statistics is not None
        ), "PCS model not fitted yet."

    def evaluate(self, connectivity: np.ndarray) -> np.ndarray | float:
        self.assert_fitted()

        return np.matmul(
            utils.vectorize(self.connectome_summary_statistics),
            utils.vectorize(connectivity),
        )

    @property
    def css(self) -> np.ndarray:
        return self.connectome_summary_statistics

    def fit(
        self,
        demographics,
        connectivity,
        metric,
        variable_of_interest,
        continuous_confounders,
        categorical_confounders,
    ):
        pass
        pass
