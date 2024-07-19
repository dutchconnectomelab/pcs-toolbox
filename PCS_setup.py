import numpy as np
import scipy.io
from calculate_PCS import calculate_PCS

# Load .mat file
mat_data = scipy.io.loadmat('/Users/admin/Documents/v2023-08-23/venv73/DATA/COBRE/connectivity_gmean_scrubbed_0.01-0.1_aparc.mat')

# Extract cnn data from loaded .mat file
cnn = mat_data['connectivity']

# Set parameters
disorder = 'schizophrenia'
gmean = True
atlas = 'aparc'

# Call calculate_PCS function
PCS_scores = calculate_PCS(cnn, disorder, gmean, atlas, p_threshold=1)

# Print first few scores
print("First few PCS scores:")
print(PCS_scores[:5])

# Save scores to CSV
np.savetxt("PCS_scores.csv", PCS_scores, delimiter=",")

# Save scores as .npy file
np.save("PCS_scores.npy", PCS_scores)
print("PCS scores have been saved to 'PCS_scores.csv' and 'PCS_scores.npy'")