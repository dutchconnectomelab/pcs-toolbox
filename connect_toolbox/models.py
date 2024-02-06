import warnings
from typing import Iterable, Optional, Union

warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np
import pandas as pd

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

        return np.matmul(
            utils.vectorize(self.connectome_summary_statistics),
            utils.vectorize(connectivity),
        )

    @property
    def css(self) -> np.ndarray:
        """
        Get the connectome summary statistics.
        """
        self.assert_fitted()
        return self.connectome_summary_statistics

    def fit(
        self,
        demographics: pd.DataFrame,
        connectivity: np.ndarray,
        variable_of_interest: str,
        baseline_condition: str = "control",
        continuous_confounders: Optional[Iterable[str]] = None,
        categorical_confounders: Optional[Iterable[str]] = None,
    ) -> "PCS":
        """
        Fit the PCS model to the data.

        The PCS model is a simple linear model that regresses the connectivity data on the variable of interest and
        confounders. The model is fitted using ordinary least squares. A fixed intercept is included in the model.

        Parameters
        ----------
        demographics : pd.DataFrame
            A dataframe with demographic information. Each row corresponds to a subject and each column to a demographic
            variable. The dataframe should contain at least the variable of interest and the confounders.
        connectivity : np.ndarray
            A 3D array with shape (n_regions, n_regions, n_subjects) containing the connectivity data.
        variable_of_interest : str
            The variable of interest in the demographics dataframe. Must be binary.
        baseline_condition : str, optional
            The baseline condition for the variable of interest. Default is "control".
        continuous_confounders : list of str, optional
            A list of continuous confounders in the demographics dataframe. Default is None.
        categorical_confounders : list of str, optional
            A list of categorical confounders in the demographics dataframe. Default is None.

        Returns
        -------
        PCS
            The fitted PCS model.
        """

        assert (
            variable_of_interest in demographics.columns
        ), "Variable of interest not found in demographics."

        assert demographics[variable_of_interest].nunique() == 2, (
            "Variable of interest must be binary. "
            f"Found {demographics[variable_of_interest].nunique()} unique values."
        )

        assert baseline_condition in demographics[variable_of_interest].unique(), (
            f"Baseline condition {baseline_condition} not found in demographics[{variable_of_interest}] "
            f"(unique values: {demographics[variable_of_interest].unique()})."
            "You can use the `baseline_condition` parameter to specify the baseline condition."
        )

        for confounder in continuous_confounders or []:
            assert (
                confounder in demographics.columns
            ), f"Continuous confounder {confounder} not found in demographics."

        for confounder in categorical_confounders or []:
            assert (
                confounder in demographics.columns
            ), f"Categorical confounder {confounder} not found in demographics."

        assert connectivity.shape[-1] == len(
            demographics
        ), "Number of subjects in demographics and connectivity do not match."

        def var_of_interest_to_binary(x: str) -> int:
            return 0 if x == baseline_condition else 1

        demographics = (
            demographics.copy()
        )  # avoid modifying the original dataframe (inefficient...)
        demographics[variable_of_interest] = demographics[variable_of_interest].apply(
            var_of_interest_to_binary
        )

        continuous_confounders = continuous_confounders or []
        categorical_confounders = categorical_confounders or []

        dep_var = utils.vectorize(connectivity)
        indep_var = pd.merge(
            demographics[[variable_of_interest] + continuous_confounders],
            pd.get_dummies(
                demographics[categorical_confounders],
                drop_first=True,
            ),
            left_index=True,
            right_index=True,
        ).to_numpy(dtype=float)

        # add intercept
        indep_var = np.hstack([indep_var, np.ones((indep_var.shape[0], 1))])

        betas = np.linalg.lstsq(indep_var, dep_var.T, rcond=None)[0]
        betas = betas[0, :]  # select betas for the variable of interest
        self.connectome_summary_statistics = utils.devectorize(betas)

        return self
