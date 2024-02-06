from pathlib import Path
from typing import Iterable, Union

import numpy as np

from connect_toolbox import validate

DISEASEMAP_DIR = Path(__file__).parent.parent / "diseasemaps"


def _atlas_nodes(atlas: str) -> int:
    if atlas == "aparc":
        return 68
    elif atlas == "aparc+aseg":
        return 82
    else:
        raise ValueError(f"Invalid atlas: {atlas}")


def load_css(
    dx: str,
    modality: str,
    metric: str,
    atlas: str,
) -> np.ndarray:
    """
    Load the connectome summary statistics (CSS) for a given disease, modality, metric and atlas.

    This is currently a wrapper around `compute_css` with `studies="all_studies"`.

    Parameters
    ----------
    dx : str
        Disease name.
    modality : str
        Modality name.
    metric : str
        Metric name.
    atlas : str
        Atlas name.

    Returns
    -------
    np.ndarray
        Connectome summary statistics (CSS) matrix.
    """
    validate.dx(dx)
    validate.modality_and_metric(modality, metric)
    validate.atlas(atlas)

    return compute_css(dx, modality, metric, atlas, "all_studies")


def list_studies(dx, modality, metric, atlas):
    """
    List the studies available for a given disease, modality, metric and atlas.

    Parameters
    ----------
    dx : str
        Disease name.
    modality : str
        Modality name.
    metric : str
        Metric name.
    atlas : str
        Atlas name.

    Returns
    -------
    List[str]
        List of study names.
    """
    validate.dx(dx)
    validate.modality_and_metric(modality, metric)
    validate.atlas(atlas)

    dm_path = DISEASEMAP_DIR / dx / modality / atlas / metric / "studies"

    if not dm_path.exists():
        raise ValueError(f"Data not found at {dm_path}.")

    return [
        f.name for f in dm_path.iterdir() if f.is_dir() and (f / "cohen_d.csv").exists()
    ]


def _fit_tau_iterative(eff, var_eff, tau2_start=0, atol=1e-5, maxiter=50):
    """Paule-Mandel iterative estimate of between random effect variance

    implementation follows DerSimonian and Kacker 2007 Appendix 8
    see also Kacker 2004

    This function is copied from statsmodels.stats.meta_analysis._fit_tau_iterative.

    Parameters
    ----------
    eff : ndarray
        effect sizes
    var_eff : ndarray
        variance of effect sizes
    tau2_start : float
        starting value for iteration
    atol : float, default: 1e-5
        convergence tolerance for absolute value of estimating equation
    maxiter : int
        maximum number of iterations

    Returns
    -------
    tau2 : float
        estimate of random effects variance tau squared
    converged : bool
        True if iteration has converged.

    """
    tau2 = tau2_start
    k = eff.shape[0]
    converged = False
    for i in range(maxiter):
        w = 1 / (var_eff + tau2)
        m = w.dot(eff) / w.sum(0)
        resid_sq = (eff - m) ** 2
        q_w = w.dot(resid_sq)
        # estimating equation
        ee = q_w - (k - 1)
        if ee < 0:
            tau2 = 0
            converged = 0
            break
        if np.allclose(ee, 0, atol=atol):
            converged = True
            break
        # update tau2
        delta = ee / (w**2).dot(resid_sq)
        tau2 += delta

    return tau2, converged


def _combine_effects(e, v):
    # This function is adapted from statsmodels.stats.meta_analysis.combine_effects
    tau2, _ = _fit_tau_iterative(e, v)
    w = 1 / (v + tau2)
    return w.dot(e) / w.sum()


def compute_css(
    dx: str,
    modality: str,
    metric: str,
    atlas: str,
    studies: Union[str, Iterable[str]],
) -> np.ndarray:
    """
    Compute the connectome summary statistics (CSS) for a given list of studies.

    Effect sizes are combined using a meta-analytic approach, and the combined effect
    size is returned as the CSS.

    Parameters
    ----------
    dx : str
        Disease name.
    modality : str
        Modality name.
    metric : str
        Metric name.
    atlas : str
        Atlas name.
    studies : Union[str, Iterable[str]]
        Study name(s); use "all_studies" to include all studies. Studies can
        be listed with `list_studies`.

    Returns
    -------
    np.ndarray
        Connectome summary statistics (CSS) matrix.
    """
    validate.dx(dx)
    validate.modality_and_metric(modality, metric)
    validate.atlas(atlas)

    if atlas == "aparc":
        css_aparc_aseg = compute_css(dx, modality, metric, "aparc+aseg", studies)
        return css_aparc_aseg[14:, 14:]

    if studies == "all_studies":
        studies = list_studies(dx, modality, metric, atlas)
    elif isinstance(studies, str):
        studies = [studies]
    else:
        studies = studies

    dm_path = DISEASEMAP_DIR / dx / modality / atlas / metric / "studies"

    if not dm_path.exists():
        raise ValueError(f"Data not found at {dm_path}.")

    nodes = _atlas_nodes(atlas)

    dms = np.zeros((nodes, nodes, len(studies)))
    varmaps = np.zeros((nodes, nodes, len(studies)))

    for i, study in enumerate(studies):
        cohen_d_file = dm_path / study / "cohen_d.csv"
        varmap_file = dm_path / study / "var_map.csv"
        assert cohen_d_file.exists(), f"File not found: {cohen_d_file}"
        assert varmap_file.exists(), f"File not found: {varmap_file}"
        dms[:, :, i] = np.genfromtxt(cohen_d_file, delimiter=",")
        varmaps[:, :, i] = np.genfromtxt(varmap_file, delimiter=",")

    combined_map = np.zeros((nodes, nodes))

    for i in range(nodes):
        for j in range(i + 1, nodes):
            e = dms[i, j, :]
            v = varmaps[i, j, :]

            included = ~np.isnan(e)
            assert included.any(), f"No data for {i}, {j} in any study."
            combined_map[i, j] = _combine_effects(e[included], v[included])
            combined_map[j, i] = combined_map[i, j]

    assert ~np.isnan(combined_map).any(), "NaN values in combined_map."

    return combined_map
