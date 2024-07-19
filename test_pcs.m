% Example usage of calculate_PCS function in MatLab
try
    % Load your own cnn (a matrix of connectiivty)
    data = load('/Users/admin/Documents/v2023-08-23/venv73/DATA/COBRE/connectivity_gmean_scrubbed_0.01-0.1_aparc.mat');
    
    if isfield(data, 'connectivity')
        cnn = data.connectivity;
    else
        error('Variable ''cnn'' not found in the loaded data.');
    end

    % Set analysis parameters
    disorder = 'schizophrenia'; 
    gmean = true;
    atlas = 'aparc';
    p_threshold = 1;

    % Call calculate_PCS function
    PCS_scores = calculate_PCS_pval(cnn, disorder, gmean, atlas, p_threshold);

    % Completion message
    disp('PCS Scores Calculated!');

catch ME
    disp(['An error occurred: ', ME.message]);
end
