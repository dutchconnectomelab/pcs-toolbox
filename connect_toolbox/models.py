import warnings
from typing import Iterable, Optional, Union

warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np

import connect_toolbox.data
from connect_toolbox import utils, validate


class PCS(object):
    """
    PolyConnectomic Score (PCS) model.
    """

    def __init__(
        self,
        *,
        dx: Optional[str] = None,
        modality: str = "functional-connectivity",
        metric: str = "gmean_scrubbed_0.01-0.1",
        atlas: str = "aparc+aseg",
        studies: Union[Iterable[str], str] = "all_studies",
    ) -> None:
        if dx:
            validate.dx(dx)
            validate.modality_and_metric(modality, metric)
            validate.atlas(atlas)
            self.dx = dx
            self.modality = modality
            self.metric = metric
            self.atlas = atlas
            self.studies = studies
            self.connectome_summary_statistics = connect_toolbox.data.compute_css(
                dx=dx, modality=modality, metric=metric, atlas=atlas, studies=studies
            )
        else:
            self.dx = None
            self.modality = None
            self.metric = None
            self.atlas = None
            self.studies = None
            self.connectome_summary_statistics = None

    def assert_fitted(self) -> None:
        """
        Assert that the PCS model has been fitted.
        """
        assert (
            self.connectome_summary_statistics is not None
        ), "PCS model not fitted yet."

    def evaluate(self, connectivity: np.ndarray) -> Union[np.ndarray, float]:
        """
        Evaluate the PCS model on a new subject.

        Parameters
        ----------
        connectivity : np.ndarray
            A 2D array with shape (n_regions, n_regions) containing the connectivity data,
            or a 3D array with shape (n_regions, n_regions, n_subjects) containing the connectivity
            data for multiple subjects.

        Returns
        -------
        np.ndarray | float
            The PCS score(s).
        """
        self.assert_fitted()

        assert connectivity.shape[0:2] == self.connectome_summary_statistics.shape, (
            f"Connectivity matrix shape ({connectivity.shape[0:2]}) does not match "
            f"connectome summary statistics ({self.connectome_summary_statistics.shape})."
        )
        css_vec = utils.vectorize(self.connectome_summary_statistics)
        return np.matmul(
            css_vec,
            utils.vectorize(connectivity),
        ) / len(css_vec)

    @property
    def css(self) -> np.ndarray:
        """
        Get the connectome summary statistics.
        """
        self.assert_fitted()
        return self.connectome_summary_statistics
