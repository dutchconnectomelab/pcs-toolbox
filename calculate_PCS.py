import os
from pathlib import Path

import numpy as np
import pandas as pd


def calculate_PCS(cnn, *, disorder, gmean, atlas):
    try:
        # Load appropriate CSS based file path
        DiseaseMap_parent_path = Path(__file__).parent / "diseasemaps"

        # Determine gmean key
        gmean_key = "_gmean" if gmean else ""

        # Construct folder and file paths
        disorder_path = f"fc_{disorder}_{atlas}{gmean_key}"
        CSS_folder = os.path.join(
            DiseaseMap_parent_path,
            "functional-connectivity",
            f"{atlas}{gmean_key}",
            disorder_path,
        )
        cohen_d_path = os.path.join(CSS_folder, "meta_analysis_cohen_d.csv")

        # Load CSS matrix from specified path
        CSS_data = pd.read_csv(cohen_d_path, header=0, comment="#")
        CSS = CSS_data.iloc[:, 1:].to_numpy()

        # Replace "nan" with np.nan
        CSS[CSS == "nan"] = np.nan
        CSS = CSS.astype(float)

        # Make matrix symmetric
        CSS[np.tril_indices_from(CSS)] = CSS.T[np.tril_indices_from(CSS)]

        # Determine if cnn is 2D or 3D
        cnn_dims = cnn.ndim
        if cnn_dims == 2:
            cnn = np.expand_dims(cnn, axis=2)
        elif cnn_dims > 3:
            raise ValueError("cnn has more than 3 dimensions, which is not supported")

        # Input dimension/atlas check
        if not np.all(cnn.shape[:2] == CSS.shape):
            print("ERROR: Matrix dimensions between CSS and CNN must match. Please ensure that the same atlas is being used with the same order of regions.")
            return None

        # Count subjects
        num_subjects = cnn.shape[2]
        PCS_scores = np.zeros(num_subjects)
        print(f"Number of subjects: {num_subjects}")

        # Calculate PCS scores
        for i in range(num_subjects):
            PCS_scores[i] = compute_PCS(cnn[:, :, i], CSS)

        # Handle NaN scores
        PCS_scores[PCS_scores == 0] = np.nan
        nan_count = np.isnan(PCS_scores).sum()
        print(f"{nan_count}/{num_subjects} NaN PCS scores found")

        return PCS_scores

    except Exception as e:
        print(f"An error occurred when loading the data: {str(e)}")
        return None


def compute_PCS(cnn_matrix, CSS_matrix):
    try:
        PCS = cnn_matrix * CSS_matrix
        PCS = np.nanmean(PCS[PCS != 0])
        return PCS
    except Exception as e:
        raise ValueError(f"Error occurred in the compute_PCS function: {str(e)}")
