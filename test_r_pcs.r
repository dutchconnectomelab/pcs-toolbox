# TEST usage of R script calculate_PCS function

#options(repos = c(CRAN = "https://cloud.r-project.org"))
#install.packages("R.matlab")

# Load R.matlab package
library(R.matlab)

# Load our .mat file format cnn
mat_data <- readMat("/Users/admin/Documents/v2023-08-23/venv73/DATA/COBRE/connectivity_gmean_scrubbed_0.01-0.1_aparc.mat")

# Extract cnn data from loaded .mat file
cnn <- mat_data$connectivity  # Adjust this line based on the structure of your subject data (we have .mat file)

# Set parameters
disorder <- 'schizophrenia'
gmean <- TRUE
atlas <- 'aparc'

# Call calculate_PCS function
source("/Users/admin/Documents/v2023-08-23/venv73/PCS_Toolbox/calculate_PCS.r")
PCS_scores <- calculate_PCS(cnn, disorder, gmean, atlas, p_threshold=0.01)

# Print first few scores
print(head(PCS_scores))

# Save scores to CSV
write.csv(PCS_scores, file = "PCS_scores.csv", row.names = FALSE)

# Save scores as R data file
save(PCS_scores, file = "PCS_scores.RData")

# Print completion message
cat("PCS scores have been saved to 'PCS_scores.csv' and 'PCS_scores.RData'\n")
