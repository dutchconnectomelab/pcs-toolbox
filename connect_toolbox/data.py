from pathlib import Path

import numpy as np

from connect_toolbox import utils, validate

DISEASEMAP_DIR = Path(__file__).parent.parent / "diseasemaps"


def _load_map(mapfile: Path) -> (np.ndarray, list):
    def _val(el):
        try:
            return float(el)
        except:
            assert "nan" in el.lower()
            return np.nan

    def _row(line):
        els = line.split(",")[1:]
        els = [_val(el) for el in els]
        return els

    txt = mapfile.read_text().strip()
    lines = txt.split("\n")
    lines = [l for l in lines if not l.startswith("#")]
    areas = lines[0].split(",")[1:]
    lines = lines[1:]
    rows = [_row(l) for l in lines]
    dm = np.stack(rows)
    dm = np.triu(dm, 1)
    dm += dm.T

    assert (
        len(areas) == dm.shape[0]
    ), f"Error when parsing {mapfile}: areas and dimension dm do not match."

    return dm, areas


def load_css(
    dx: str,
    modality: str,
    metric: str,
    atlas: str,
) -> np.ndarray:
    validate.dx(dx)
    validate.modality_and_metric(modality, metric)
    validate.atlas(atlas)

    if atlas == "aparc":
        res = load_css(dx, modality, metric, "aparc+aseg")
        return res[14:, 14:]

    dm_path = DISEASEMAP_DIR / dx / modality / atlas / metric / "mega_analysis"

    if not dm_path.exists():
        raise ValueError(f"Data not found at {dm_path}.")

    return _load_map(dm_path / "cohen_d.csv")[0]


def compute_css(
    dx: str,
    modality: str,
    metric: str,
    atlas: str,
    study: str,
) -> np.ndarray:
    validate.dx(dx)
    validate.modality_and_metric(modality, metric)
    validate.atlas(atlas)
    raise NotImplementedError("compute_css not implemented yet.")
