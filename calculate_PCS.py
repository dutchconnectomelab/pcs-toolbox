import os
from pathlib import Path

import numpy as np
import pandas as pd


def calculate_PCS(cnn, disorder, gmean, atlas, p_threshold=None):
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
        cohen_d_path = os.path.join(CSS_folder, "mega_analysis_cohen_d.csv")
        p_value_path = os.path.join(CSS_folder, "mega_analysis_pval.csv")

        # Load CSS matrix from specified path
        CSS_data = pd.read_csv(cohen_d_path, header=0, comment="#")
        CSS = CSS_data.iloc[:, 1:].to_numpy()

        # Load p-value matrix if thresholding is requested
        if p_threshold is not None:
            p_value_data = pd.read_csv(p_value_path, header=0, comment="#")
            p_values = p_value_data.iloc[:, 1:].to_numpy()
            p_values[p_values == "nan"] = np.nan
            p_values = p_values.astype(float)
            p_values[np.tril_indices_from(p_values)] = p_values.T[
                np.tril_indices_from(p_values)
            ]
        else:
            p_values = None

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
        print(f"Size of cnn: {cnn.shape[0]} x {cnn.shape[1]}")
        print(f"Size of CSS: {CSS.shape[0]} x {CSS.shape[1]}")
        if not np.all(cnn.shape[:2] == CSS.shape):
            print(
                f"Warning: Dimensions of cnn and CSS do not match. cnn size: {cnn.shape[:2]}, CSS size: {CSS.shape}"
            )

        # Count subjects
        num_subjects = cnn.shape[2]
        PCS_scores = np.zeros(num_subjects)
        print(f"Number of subjects: {num_subjects}")

        # Calculate PCS scores
        for i in range(num_subjects):
            PCS_scores[i] = compute_PCS(cnn[:, :, i], CSS, p_values, p_threshold)

        # Handle NaN scores
        PCS_scores[PCS_scores == 0] = np.nan
        nan_count = np.isnan(PCS_scores).sum()
        print(f"{nan_count}/{num_subjects} NaN PCS scores found")

        return PCS_scores

    except Exception as e:
        print(f"An error occurred when loading the data: {str(e)}")
        return None


def compute_PCS(cnn, CSS_matrix, p_value_matrix=None, p_threshold=None):
    try:
        if p_value_matrix is not None and p_threshold is not None:
            # Apply p-value thresholding
            mask = p_value_matrix < p_threshold
            filtered_CSS = np.where(mask, CSS_matrix, 0)
        else:
            filtered_CSS = CSS_matrix

        PCS = cnn * filtered_CSS
        PCS = np.nanmean(PCS[PCS != 0])
        return PCS
    except Exception as e:
        raise ValueError(f"Error occurred in the compute_PCS function: {str(e)}")
