# Source R script for calculate_PCS function
source("calculate_PCS.r")

test_calculate_PCS_lausanne120 <- function() {
  # Load single subject
  load("tests/single-subject_L120_test_cnn.RData")

  # Test calculate_PCS
  pcs_scores <- calculate_PCS(cnn, disorder = 'schizophrenia', gmean = TRUE, atlas = 'lausanne120')

  # Assertions
  stopifnot(!is.null(pcs_scores))  # Ensure result is not null
  stopifnot(length(pcs_scores) == 1)  # Ensure 1 PCS score for single subject
  # Print results
  print(pcs_scores)
  # Add assertion for approximate equality
  stopifnot(all.equal(pcs_scores, -0.0017041, tolerance = 1e-5))
  print("Testing_complete!")
}

# Run the test
test_calculate_PCS_lausanne120()
