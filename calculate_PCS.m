function PCS_scores = calculate_PCS(cnn, varargin)
    % CALCULATE_PCS calculates the polyconnectomic scores from user connectivity matrices and cohen's d summary statistics
    % Inputs:
    %   cnn: A 2D or 3D matrix of connectivity data (regions x regions) or
    %        (regions x regions x subjects)
    %   disorder: The specific disorder (e.g., 'ADHD', 'schizophrenia', etc.) from the available summary statistics
    %   gmean: Boolean indicating whether gmean corrected map is grabbed (leave blank if not wanted)
    %   atlas: Specific atlas used in cnn creation (e.g., 'aparc', 'lausanne120', 'lausanne250')
    % Output:
    %   PCS_scores: A vector of PCS scores
    
    % Parse input arguments
    p = inputParser;
    addRequired(p, 'cnn');
    addParameter(p, 'disorder', '', @ischar);
    addParameter(p, 'gmean', false, @islogical);
    addParameter(p, 'atlas', '', @ischar);
    
    % Parse input arguments
    parse(p, cnn, varargin{:});
    
    % Extract parsed values
    disorder = p.Results.disorder;
    gmean = p.Results.gmean;
    atlas = p.Results.atlas;
    
    try
        % Load CSS 
        DiseaseMap_parent_path = '/diseasemaps';
        % Determine gmean key
        if gmean
            gmean_key = '_gmean';
        else
            gmean_key = '';
        end
    
        % Construct folder and file paths
        disorder_path = sprintf('fc_%s_%s%s', disorder, atlas, gmean_key);
        CSS_folder = fullfile(DiseaseMap_parent_path, 'functional-connectivity', sprintf('%s%s', atlas, gmean_key), disorder_path);
        cohen_d_path = fullfile(CSS_folder, 'mega_analysis_cohen_d.csv');
    
        % Load CSS matrix from path
        CSS_data = readtable(cohen_d_path, 'ReadVariableNames', true);
        CSS = table2array(CSS_data(:, 2:end));
    
        % Replace NaN with 0 in CSS
        CSS(isnan(CSS)) = 0;
    
        % Determine if cnn is 2D or 3D
        cnn_dims = ndims(cnn);
        if cnn_dims == 2
            cnn = reshape(cnn, size(cnn, 1), size(cnn, 2), 1);
        elseif cnn_dims > 3
            error('Invalid cnn Dimensions: The cnn matrix should have 2 or 3 dimensions only. Please check your input.');
        end
    
        % Input dimension/atlas check
        disp(['Size of cnn: ', mat2str(size(cnn(:,:,1)))]);
        disp(['Size of CSS: ', mat2str(size(CSS))]);
        if ~isequal(size(cnn(:,:,1)), size(CSS))
            warning('Dimension Mismatch: The dimensions of the cnn matrix (%s) do not match the dimensions of the CSS matrix (%s). Please ensure that both matrices have compatible sizes.', ...
                mat2str(size(cnn(:,:,1))), mat2str(size(CSS)));
        end
    
        % Count subjects
        num_subjects = size(cnn, 3);
        PCS_scores = zeros(num_subjects, 1); % Preallocate
        disp(['Number of subjects: ', num2str(num_subjects)]);
    
        % Calculate PCS scores
        for i = 1:num_subjects
            PCS_scores(i) = compute_PCS(cnn(:,:,i), CSS);
        end
    
        % Handle NaN scores
        PCS_scores(PCS_scores == 0) = NaN;
        nan_count = sum(isnan(PCS_scores));
        disp([num2str(nan_count) '/' num2str(num_subjects) ' NaN PCS scores found']);
    
    catch ME
        disp(['An error occurred while processing the data: ', ME.message, ' Please check your input files and paths.']);
        PCS_scores = [];
    end
    end
    
    function PCS = compute_PCS(cnn_matrix, CSS_matrix)
    try
        PCS = cnn_matrix .* CSS_matrix;
        % Compute mean excluding zeros and NaNs
        PCS = mean(PCS(PCS ~= 0), 'omitnan'); 
    catch ME
        error('An error occurred while computing PCS scores: %s. Please check the dimensions and values of your input matrices.', ME.message);
    end
    end
