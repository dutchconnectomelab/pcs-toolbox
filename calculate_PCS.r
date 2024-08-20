calculate_PCS <- function(cnn, disorder, gmean, atlas) {
  tryCatch({
    # Load appropriate CSS based on input arguments
    # DiseaseMap_parent_path <- 'PATH/TO/CSS/FOLDER'
    DiseaseMap_parent_path <- 'diseasemaps'
    
    # Determine gmean key
    gmean_key <- if (gmean) '_gmean' else ''
    
    # Construct folder and file paths
    disorder_path <- sprintf('fc_%s_%s%s', disorder, atlas, gmean_key)
    CSS_folder <- file.path(DiseaseMap_parent_path, 'functional-connectivity', sprintf('%s%s', atlas, gmean_key), disorder_path)
    cohen_d_path <- file.path(CSS_folder, 'meta_analysis_cohen_d.csv')
    
    # Load CSS matrix from specified path
    CSS_data <- read.csv(cohen_d_path, header = TRUE, check.names = FALSE, comment.char = "#")
    CSS <- as.matrix(CSS_data[, -1])
    
    # Replace "nan" with NA
    CSS[CSS == "nan"] <- NA
    CSS <- apply(CSS, 2, as.numeric)
    
    # Make matrix symmetric
    CSS[lower.tri(CSS)] <- t(CSS)[lower.tri(CSS)]
    
    # Determine if cnn is 2D or 3D
    cnn_dims <- length(dim(cnn))
    if (cnn_dims == 2) {
      cnn <- array(cnn, dim = c(dim(cnn), 1))
    } else if (cnn_dims > 3) {
      stop('cnn has more than 3 dimensions, which is not supported')
    }
    
    # Input dimension/atlas check
    cat('Size of cnn:', paste(dim(cnn)[1:2], collapse = ' x '), '\n')
    cat('Size of CSS:', paste(dim(CSS), collapse = ' x '), '\n')
    
    if (!all(dim(cnn)[1:2] == dim(CSS))) {
      warning(sprintf('Dimensions of cnn and CSS do not match. cnn size: %s, CSS size: %s',
                      paste(dim(cnn)[1:2], collapse = ' x '), paste(dim(CSS), collapse = ' x ')))
    }
    
    # Count subjects
    num_subjects <- dim(cnn)[3]
    PCS_scores <- numeric(num_subjects)
    cat('Number of subjects:', num_subjects, '\n')
    
    # Calculate PCS scores
    for (i in 1:num_subjects) {
      PCS_scores[i] <- compute_PCS(cnn[,,i], CSS)
    }
    
    # Handle NaN scores
    PCS_scores[PCS_scores == 0] <- NA
    nan_count <- sum(is.na(PCS_scores))
    cat(sprintf('%d/%d NaN PCS scores found\n', nan_count, num_subjects))
    
    # Return PCS scores
    return(PCS_scores)
    
  }, error = function(e) {
    cat('An error occurred when loading the data:', e$message, '\n')
    return(NULL)
  })
}

compute_PCS <- function(cnn_matrix, CSS_matrix) {
  tryCatch({
    PCS <- cnn_matrix * CSS_matrix
    # Compute mean excluding NAs and zero values
    PCS <- mean(PCS[PCS != 0], na.rm = TRUE)
    return(PCS)
  }, error = function(e) {
    stop(sprintf('Error occurred in the compute_PCS function: %s', e$message))
  })
}
