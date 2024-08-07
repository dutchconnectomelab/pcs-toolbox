## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Input Data Format](#input-data-format)
5. [Usage in Python, MATLAB, and R](#usage-in-python-matlab-and-r)
6. [Function Parameters](#function-parameters)
7. [Supported Disorders](#supported-disorders)
8. [Global Mean Correction (gmean)](#global-mean-correction-gmean)
9. [Supported Atlas Parcellation Schemes](#supported-atlas-parcellation-schemes)
10. [Output PCS Scores](#output-pcs-scores)
11. [Citing the PCS-Toolbox](#citing-the-pcs-toolbox)
12. [License](#license)

## Introduction
The PCS-Toolbox calculates Polyconnectomic Scores (PCS) to quantify the presence of disease-related brain connectivity signatures in individual connectomes. PCS integrates existing knowledge of disorder-related brain circuitry, aggregating these connectivity signatures or connectome summary statistics (CSS) across the entire brain into a single, interpretable metric.

This repository includes toolbox scripts and CSS of connectivity signatures for various neuropsychiatric disorders. These CSS represent the strength and direction of associations between brain connections and specific disorders across connectomes. The CSS were generated through the following process:
- Effect size estimation per dataset: Cohen's d was computed for each brain connection, creating a connectivity matrix for each dataset within a disorder. This matrix indicates connections with decreased functional connectivity (FC) in patients (negative d) or increased FC in patients compared to controls (positive d).
- Meta-Analysis: A meta-analysis was conducted to aggregate these connectivity-wise effects across datasets for each disorder.

We provide the meta-analytic CSS for more than 10 disorders, encompassing approximately 5,000 patients and 5,000 controls across 20+ datasets, allowing researchers to compute PCS on their own data.

## Prerequisites
- Python 3.7+, MATLAB, or R
#### Required packages:
- Python: NumPy, Pandas, SciPy
- R: R.matlab
- MATLAB: No additional toolboxes required

## Setup
Clone this repository:

```git clone https://github.com/dutchconnectomelab/connect-toolbox.git```


### For R Users

1. **Download Required Files**: Similarly, download the R script `calculate_PCS.R` from this repository.

2. **Source Script**: Use the following command within R to source the `calculate_PCS.R` script for use:
   ```r
   source("/path/to/calculate_PCS.R")

### For MATLAB Users

1. **Download Required Files**: Instead of cloning the repository, download the MATLAB script `calculate_PCS.m` directly.

2. **Add Path**: Add the directory containing `calculate_PCS.m` to MATLAB's path using `addpath('/path/to/folder/containing/calculate_PCS')`.


### Installation Dependencies


In R, ensure you have the `R.matlab` package installed; you can install it using the following command within R:

```r
install.packages("R.matlab")
```

In Python, ensure you have the following packages installed:

- NumPy
- Pandas
- SciPy

You can install these packages in python using pip:

```bash
pip install numpy pandas scipy
```

### Input Data Format:

The `cnn` parameter is a connectivity matrix representing functional brain connections, typically a correlation matrix. The function `calculate_PCS` automatically detects the dimensions of the input `cnn` matrix to determine the number of regions of interest (ROI) and subjects:

- **2D Matrix (N_regions × N_regions):**
  If `cnn` is a 2D matrix, PCS is calculated assuming it represents the connectivity between ROIs for a single subject.

- **3D Matrix (N_regions × N_regions × N_subjects):**
  If `cnn` is a 3D matrix, PCS is calculated for each subject represented in the third dimension; computed individually for each subject's connectivity data.

This allows for flexibility in handling both single-subject and multi-subject connectivity data. It is crucial to ensure that the atlas used to generate the input connectivity matrix matches the atlas specified in the function parameters for accurate PCS calculation.


### Usage in R, MATLAB, and Python

#### R

```r
# Install the R.matlab package (if not already installed):
install.packages("R.matlab")
# Source the calculate_PCS.R script from your cloned repository:
source("path/to/your-repository/calculate_PCS.R")
# Load R.matlab package
library(R.matlab)
# Load RDS file with connectivity data
cnn <- readRDS("path/to/your-connectivity-matrix.rds")
# Calculate the PCS for schizophrenia using Desikian-Killiany atlas and global mean corrected
PCS_subject <- calculate_PCS(cnn, disorder='schizophrenia', gmean=TRUE, atlas='aparc')
```

#### MATLAB

```matlab
% Add the directory containing calculate_PCS.m to MATLAB's path:
addpath('path/to/your-repository')
% Load .mat or .csv connectivity data 
cnn = load('path/to/your-repository/connectivity_data.mat');
# cnn = readmatrix('or/path/to/connectivity_data/in/csv/format.csv');
# Calculate the PCS for schizophrenia using Desikian-Killiany atlas and global mean corrected
PCS_subject = calculate_PCS(cnn, 'disorder', 'schizophrenia', 'gmean', true, 'atlas', 'aparc');
```

#### Python

```python
# Install the required Python packages:
pip install numpy pandas

# Ensure the calculate_PCS.py script is available in your working directory or in your Python path:
sys.path.append('path/to/your-repository')

import numpy as np
from calculate_PCS import *
# Load .npy connectivity data
cnn = np.load('path/to/your-repository/connectivity_data.npy')
# Calculate the PCS for schizophrenia using Desikian-Killiany atlas and global mean corrected
PCS_subject = calculate_PCS(cnn, disorder='schizophrenia', gmean=True, atlas='aparc')
```

### Function Parameters

- `cnn`: User connectivity data (2D or 3D array)
- `disorder`: Name of the disorder (string)
- `gmean`: Boolean, whether to use functional global mean normalization
- `atlas`: Name of the brain atlas used in both `cnn` and CSS creation

### The PCS-Toolbox supports the following neuropsychiatric and neurodegenerative disorders:

- Alzheimer's Disease: `"alzheimer"`
- Anxiety Disorders: `"anxiety"`
- Attention Deficit Hyperactivity Disorder: `"adhd"`
- Autism Spectrum Disorder: `"autism"`
- Bipolar Disorder: `"bipolar"`
- Frontotemporal Dementia: `"ftd"`
- Major Depressive Disorder: `"depression"`
- Obsessive-compulsive disorder: `"ocd"`
- Parkinson's Disease: `"parkinson"`
- Schizoaffective Disorder: `"schizoaffective"`
- Schizophrenia: `"schizophrenia"`

When using the `calculate_PCS` function, specify the disorder parameter using its key (e.g., `'adhd'`, `'ftd'`, `'schizophrenia'`, etc.).

### Global Mean Correction (gmean)

Global mean signal correction is a technique used to reduce the impact of non-neural physiological noise in fMRI data, although its use is debated in the neuroimaging community as it can also remove some neural signals of interest. The PCS-Toolbox provides options for both corrected and uncorrected CSS, allowing researchers to choose based on their specific research questions and methodological preferences.

- When `gmean=True` (Python) or `gmean` is included (MATLAB/R), the toolbox uses functional CSS that have been corrected for global mean signal. This correction involved regressing out the framewise mean signal intensity of all brain voxels.

- When `gmean=False` (Python) or the parameter is omitted (MATLAB/R), the toolbox uses functional CSS without global mean signal correction.

We advise using CSS with `gmean` if the provided `cnn` also uses this preprocessing method.

### The PCS-Toolbox supports the following atlas parcellation schemes:
- <a href="#" title="CITATION NEEDED">`BB50human`</a> (78 regions)
- <a href="#" title="Brodmann, K. (1909). Vergleichende Lokalisationslehre der Grosshirnrinde in ihren Prinzipien dargestellt auf Grund des Zellenbaues. Barth.">`Brodmann`</a> (80 regions)
- <a href="#" title="Buckner, R. L., Krienen, F. M., Castellanos, A., Diaz, J. C., & Yeo, B. T. T. (2011). The organization of the human cerebellum estimated by intrinsic functional connectivity. Journal of Neurophysiology, 106(5), 2322–2345.">`BucknerCer17`</a> (34 regions)
- <a href="#" title="Buckner, R. L., Krienen, F. M., Castellanos, A., Diaz, J. C., & Yeo, B. T. T. (2011). The organization of the human cerebellum estimated by intrinsic functional connectivity. Journal of Neurophysiology, 106(5), 2322–2345.">`BucknerCer7`</a> (14 regions)
- <a href="#" title="Campbell, A. W. (1905). Histological studies on the localisation of cerebral function. University Press.">`Campbell`</a> (32 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`EconomoCT`</a> (32 regions)
- <a href="#" title="Flechsig, P. E. (1920). Anatomie des menschlichen Gehirns und Rückenmarks auf myelogenetischer Grundlage (Vol. 1). G. Thieme.">`Flechsig`</a> (94 regions)
- <a href="#" title="Fischl B, Salat DH, Busa E, Albert M, Dieterich M, Haselgrove C, van der Kouwe A, Killiany R, Kennedy D, Klaveness S, Montillo A, Makris N, Rosen B, Dale AM. Whole brain segmentation: automated labeling of neuroanatomical structures in the human brain. Neuron. 2002 Jan 31;33(3):341-55. doi: 10.1016/s0896-6273(02)00569-x">`fsSubCortical`</a> (130 regions)
- <a href="#" title="Kleist, K. (1934). Gehirnpathologie, vornehmlich aufgrund der Kriegserfahrungen. Leipzig, Barth.">`Kleist`</a> (100 regions)
- <a href="#" title="Diedrichsen, J. (2006). A spatially unbiased atlas template of the human cerebellum. NeuroImage, 33(1), 127–138.">`SUITCer`</a> (34 regions)
- <a href="#" title="Smith, G. E. (1907). A new topographical survey of the human cerebral cortex, being an account of the distribution of the anatomically distinct cortical areas and their relationship to the cerebral sulci. Journal of Anatomy and Physiology, 41(Pt 4), 237.">`Smith`</a> (88 regions)
- <a href="#" title="Tzourio-Mazoyer, N., Landeau, B., Papathanassiou, D., Crivello, F., Etard, O., Delcroix, N., et al. (2002). Automated anatomical labeling of activations in SPM using a macroscopic anatomical parcellation of the MNI MRI single-subject brain., 15(1), 273–289. http://doi.org/10.1006/nimg.2001.0978">`aal`</a> (82 regions)
- <a href="#" title="Fischl, B., van der Kouwe, A., Destrieux, C., Halgren, E., Ségonne, F., Salat, D. H., Busa, E., Seidman, L. J., Goldstein, J., Kennedy, D., Caviness, V., Makris, N., Rosen, B., Dale, A. M. (2004). Automatically parcellating the human cerebral cortex. Cereb Cortex, 14(1), 11-22. doi: 10.1093/cercor/bhg087">`aparc (Desikan-Killiany)`</a> (68 regions)
- <a href="#" title="Arslan, S., Ktena, S. I., Makropoulos, A., Robinson, E. C., Rueckert, D., Parisot, S. (2018). Human brain mapping: A systematic comparison of parcellation methods for the human cerebral cortex. NeuroImage, 170, 5-30. doi: 10.1016/j.neuroimage.2017.04.014">`arslan`</a> (50 regions)
- <a href="#" title="Fischl, B., Salat, D. H., Busa, E., Albert, M., Dieterich, M., Haselgrove, C., van der Kouwe, A., Killiany, R., Kennedy, D., Klaveness, S., Montillo, A., Makris, N., Rosen, B., Dale, A. M. (2002). Whole brain segmentation: automated labeling of neuroanatomical structures in the human brain. Neuron, 33(3), 341-55. doi: 10.1016/s0896-6273(02)00569-x">`aseg`</a> (14 regions)
- <a href="#" title="Baldassano, C., Beck, D. M., Fei-Fei, L. (2015). Parcellating connectivity in spatial maps. PeerJ, 3:e784. doi: 10.7717/peerj.784. PMID: 25737822; PMCID: PMC4338796.">`baldassano`</a> (170 regions)
- <a href="#" title="Fan, L., Li, H., Zhuo, J., Zhang, Y., Wang, J., Chen, L., Yang, Z., Chu, C., Xie, S., Laird, A. R., Fox, P. T., Eickhoff, S. B., Yu, C., Jiang, T. (2016). The Human Brainnetome Atlas: A New Brain Atlas Based on Connectional Architecture. Cereb Cortex, 26(8), 3508-26. doi: 10.1093/cercor/bhw157. Epub 2016 May 26. PMID: 27230218; PMCID: PMC4961028.">`brainnetome`</a> (212 regions)
- <a href="#" title="Fan, L., Li, H., Zhuo, J., Zhang, Y., Wang, J., Chen, L., Yang, Z., Chu, C., Xie, S., Laird, A. R., Fox, P. T., Eickhoff, S. B., Yu, C., Jiang, T. (2016). The Human Brainnetome Atlas: A New Brain Atlas Based on Connectional Architecture. Cereb Cortex, 26(8), 3508-26. doi: 10.1093/cercor/bhw157. Epub 2016 May 26. PMID: 27230218; PMCID: PMC4961028.">`brainnetome_subcortical`</a> (36 regions)
- <a href="#" title="Scholtens, L. H., de Reus, M. A., de Lange, S. C., Schmidt, R., van den Heuvel, M. P. (2018). An MRI Von Economo - Koskinas atlas. Neuroimage, 170, 249-256. doi: 10.1016/j.neuroimage.2016.12.069. Epub 2016 Dec 28. PMID: 28040542.">`economo`</a> (87 regions)
- <a href="#" title="Fan, L., Li, H., Zhuo, J., Zhang, Y., Wang, J., Chen, L., Yang, Z., Chu, C., Xie, S., Laird, A. R., Fox, P. T., Eickhoff, S. B., Yu, C., Jiang, T. (2016). The Human Brainnetome Atlas: A New Brain Atlas Based on Connectional Architecture. Cerebral Cortex (New York, N.Y. : 1991), 26(8), 3508–3526. http://doi.org/10.1093/cercor/bhw157">`fan`</a> (209 regions)
- <a href="#" title="Gordon, E. M., Laumann, T. O., Adeyemo, B., Huckins, J. F., Kelley, W. M., & Petersen, S. E. (2016). Generation and Evaluation of a Cortical Area Parcellation from Resting-State Correlations. Cerebral Cortex, 26(1), 288–303. http://doi.org/10.1093/cercor/bhu239">`gordon333dil`</a> (333 regions)
- <a href="#" title="Desikan, R. S., Ségonne, F., Fischl, B., Quinn, B. T., Dickerson, B. C., Blacker, D., Buckner, R. L., Dale, A. M., Maguire, R. P., Hyman, B. T., Albert, M. S., Killiany, R. J. (2006). An automated labeling system for subdividing the human cerebral cortex on MRI scans into gyral based regions of interest. Neuroimage, 31(3), 968-80.">`harvardoxford`</a> (96 regions)
- <a href="#" title="Glasser, M. F., Coalson, T. S., Robinson, E. C., Hacker, C. D., Harwell, J., Yacoub, E., et al. (2016). A multi-modal parcellation of human cerebral cortex. Nature. http://doi.org/10.1038/nature18933">`hcp-mmp-b (GLASSER)`</a> (362 regions)
- <a href="#" title="Beckmann, C. F., & Smith, S. M. (2004). Probabilistic independent component analysis for functional magnetic resonance imaging. IEEE Transactions on Medical Imaging, 23(2), 137-152. doi: 10.1109/TMI.2003.822821">`ica`</a> (20 regions)

### Output PCS Scores:
The calculate_PCS function returns an array of PCS scores, one for each subject in the input data. Higher PCS indicate a stronger presence of connectivity patterns associated with the specified disorder. Importantly, scores are relative measures and should be interpreted in comparison to a control group or normative data.

### Citing the PCS-Toolbox:
If you use the PCS-Toolbox in your research, please cite: 
- ___"APA CITATION OF ILAN'S PCS PAPER"___ 

Datasets used in the creation of CSS can be accessed via their respective websites:

Openly Accessible Datasets
- Autism Brain Imaging Data Exchange (ABIDE-I & ABIDE-II):  [fcon_1000.projects.nitrc.org/indi/abide](https://fcon_1000.projects.nitrc.org/indi/abide/)
- ADHD-200 Sample:  [nitrc.org/frs/?group_id=383](https://www.nitrc.org/frs/?group_id=383)
- Alzheimer's Disease Neuroimaging Initiative (ADNI-2/GO & ADNI-3):  [ida.loni.usc.edu](https://ida.loni.usc.edu)
- Bipolar & Schizophrenia Consortium for Parsing Intermediate Phenotypes (BSNIP-1): ([NDA](https://nda.nih.gov); NDAR ID: 2274)
- Centre for Biomedical Research Excellence (COBRE): [schizconnect.org](http://schizconnect.org)
- Consortium for Neuropsychiatric Phenomics (CNP): OpenNeuro [openneuro.org](http://openneuro.org)
- Healthy Brain Network (HBN): [fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network](http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network)
- Enhanced Nathan Kline Institute (NKI-Enhanced): [fcon_1000.projects.nitrc.org/indi/enhanced/](http://fcon_1000.projects.nitrc.org/indi/enhanced/)
- Open Access Series of Imaging Studies (OASIS-3): [oasis-brains.org](http://www.oasis-brains.org)
- Japanese Strategic Research Program for the Promotion of Brain Science (SRPBS): [bicr-resource.atr.jp/srpbs1600](https://bicr-resource.atr.jp/srpbs1600)
- UK Biobank (UKB): [ukbiobank.ac.uk](https://www.ukbiobank.ac.uk)

Restricted Access Datasets
- Marburg-Münster Affective Disorders Cohort Study (FOR2107): [for2107.de](http://for2107.de)

### License


