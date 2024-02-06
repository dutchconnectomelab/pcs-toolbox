import numpy as np


def dx(dx_name: str) -> None:
    assert (
        type(dx_name) == str
    ), f"Diagnosis must be a string, instead got {type(dx_name)}."
    assert dx_name in [
        "addiction",
        "adhd",
        "alzheimer",
        "anxiety",
        "autism",
        "bipolar",
        "dementia_other",
        "depression",
        "ftd",
        "insomnia",
        "mci",
        "ocd",
        "pain",
        "parkinson",
        "schizophrenia",
    ], f"Unrecognized diagnosis {dx_name} - no disease map available for this diagnosis."


def modality_and_metric(modality: str, metric: str) -> None:
    assert type(modality) == str, "Modality must be a string."
    assert type(metric) == str, "Metric must be a string."
    availabe_metrics = {
        "functional-connectivity": ["gmean_scrubbed_0.01-0.1", "scrubbed_0.01-0.1"],
        "structural-connectivity": ["mean_fa"],
        "morphology": ["thickness", "volume", "surface_area"],
    }
    assert modality in availabe_metrics, f"Unrecognized modality {modality}."
    assert (
        metric in availabe_metrics[modality]
    ), f"Unrecognized metric {metric} (available metrics: {availabe_metrics[modality]})."


def atlas(atlas_name: str) -> None:
    assert type(atlas_name) == str, "Atlas name must be a string."
    assert atlas_name in ["aparc+aseg", "aparc"], f"Unrecognized atlas {atlas_name}."


def symmetric(matrix: np.ndarray) -> None:
    assert (
        type(matrix) == np.ndarray
    ), f"Input must be a numpy array, instead got {type(matrix)}."
    if matrix.ndim == 3:
        if matrix.shape[1] == matrix.shape[2]:
            if matrix.shape[0] != matrix.shape[1]:
                raise ValueError(
                    "Matrix must be square and subjects in the last dimension, "
                    "i.e. with dimensions (n, n, m), instead got (n, m, m)."
                )
    assert (
        matrix.shape[0] == matrix.shape[1]
    ), f"Matrix must be square, instead got {matrix.shape}."
    assert np.allclose(
        matrix, np.swapaxes(matrix, 0, 1), atol=1e-8
    ), "Matrix must be symmetric."


def zero_diagonal(matrix: np.ndarray) -> None:
    assert type(matrix) == np.ndarray, "Input must be a numpy array."
    assert np.all(np.diag(matrix) == 0), "Diagonal must be zero."
