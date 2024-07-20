function PCS_scores = calculate_PCS(cnn, varargin)
% CALCULATE_PCS calculates the polyconnectomic scores from user connectivity matrices and cohen's d summary statistics
% Inputs:
%   cnn: A 2D or 3D matrix of connectivity data (regions x regions) or
%        (regions x regions x subjects)
%   disorder: The specific disorder (e.g., 'ADHD', 'schizophrenia', etc.) from the available summary statistics
%   gmean: Boolean indicating whether gmean corrected map is grabbed (leave blank if not wanted)
%   atlas: Specific atlas used in cnn creation (e.g., 'aparc', 'lausanne120', 'lausanne250')
%   p_threshold: p-value threshold for filtering (optional)
% Output:
%   PCS_scores: A vector of PCS scores
    
% Parse input arguments
p = inputParser;
addRequired(p, 'cnn');
addParameter(p, 'disorder', '');
addParameter(p, 'gmean', false); % Default is false
addParameter(p, 'atlas', '');
addParameter(p, 'p_threshold', 1, @isnumeric); % Default is 1

% Parse input arguments
parse(p, cnn, varargin{:});

% Extract parsed values
disorder = p.Results.disorder;
gmean = p.Results.gmean;
atlas = p.Results.atlas;
p_threshold = p.Results.p_threshold;

try
    % Load CSS 
    DiseaseMap_parent_path = 'diseasemaps';

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
    p_value_path = fullfile(CSS_folder, 'mega_analysis_pval.csv');

    % Load CSS matrix from path
    CSS_data = readtable(cohen_d_path, 'ReadVariableNames', true);
    CSS = table2array(CSS_data(:, 2:end));

    % Load p-value matrix if threshold is requested
    if ~isempty(p_threshold)
        p_value_data = readtable(p_value_path, 'ReadVariableNames', true);
        p_values = table2array(p_value_data(:, 2:end));
        p_values(isnan(p_values)) = 1; % Replace NaN with 1 (no effect)
    else
        p_values = [];
    end

    % Replace NaN with 0 in CSS
    CSS(isnan(CSS)) = 0;

    % Determine if cnn is 2D or 3D
    cnn_dims = ndims(cnn);
    if cnn_dims == 2
        cnn = reshape(cnn, size(cnn, 1), size(cnn, 2), 1);
    elseif cnn_dims > 3
        error('cnn has more than 3 dimensions, which is not supported');
    end

    % Input dimension/atlas check
    disp(['Size of cnn: ', mat2str(size(cnn(:,:,1)))]);
    disp(['Size of CSS: ', mat2str(size(CSS))]);
    if ~isequal(size(cnn(:,:,1)), size(CSS))
        warning('Dimensions of cnn and CSS do not match. cnn size: %s, CSS size: %s', ...
            mat2str(size(cnn(:,:,1))), mat2str(size(CSS)));
    end

    % Count subjects
    num_subjects = size(cnn, 3);
    PCS_scores = zeros(num_subjects, 1); % Preallocate
    disp(['Number of subjects: ', num2str(num_subjects)]);

    % Calculate PCS scores
    for i = 1:num_subjects
        PCS_scores(i) = compute_PCS(cnn(:,:,i), CSS, p_values, p_threshold);
    end

    % Handle NaN scores
    PCS_scores(PCS_scores == 0) = NaN;
    nan_count = sum(isnan(PCS_scores));
    disp([num2str(nan_count) '/' num2str(num_subjects) ' NaN PCS scores found']);

catch ME
    disp(['An error occurred when loading the data: ', ME.message]);
    PCS_scores = [];
end
end

function PCS = compute_PCS(cnn_matrix, CSS_matrix, p_value_matrix, p_threshold)
try
    if ~isempty(p_value_matrix) && ~isempty(p_threshold)
        % Apply p-value thresholding
        mask = p_value_matrix < p_threshold;
        filtered_CSS = CSS_matrix .* mask;
    else
        filtered_CSS = CSS_matrix;
    end
    
    PCS = cnn_matrix .* filtered_CSS;
    % Compute mean excluding zeros and NaNs
    PCS = mean(PCS(PCS ~= 0), 'omitnan'); 
catch ME
    error('Error occurred in the compute_PCS function: %s', ME.message);
end
end
