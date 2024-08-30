import sys
import os
import numpy as np

# Add parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculate_PCS import calculate_PCS

def test_calculate_PCS():
    # Test calculate_PCS with single subject lausanne120 cnn
    print("Auto_Testing_PCS_calculator_on_single_subject...")
    # Load single subject
    cnn = np.load('tests/single-subject_L120_test_cnn.npy')
    # Calculate PCS
    pcs_scores = calculate_PCS(cnn, disorder='schizophrenia', gmean=True, atlas='lausanne120')
    # Warnings
    assert pcs_scores is not None, "PCS calculation failed for atlas 'lausanne120'"
    assert len(pcs_scores) == 1, "PCS calculation returned incorrect number of scores for atlas 'lausanne120'"
    np.testing.assert_almost_equal(pcs_scores, -0.0017041)
    # Results
    print(pcs_scores)
    print("Testing_complete!")

if __name__ == "__main__":
    test_calculate_PCS()
