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
11. [Citing the PCS toolbox](#citing-the-pcs-toolbox)
12. [License](#license)

## Introduction
The PCS toolbox calculates polyconnectomic score (PCS) to quantify the presence of disease-related brain connectivity signatures in individual connectomes. PCS integrates existing knowledge of disorder-related brain circuitry, aggregating these connectivity signatures or connectome summary statistics (CSS) across the entire brain into a single, interpretable metric.

This repository includes toolbox scripts and CSS of resting-state functional connectivity (FC) signatures for various neuropsychiatric disorders. These CSS represent the strength and direction of associations between brain connections and specific disorders across connectomes. The CSS were generated through the following process:
- Effect size estimation per dataset: Cohen’s d was computed for each FC, corrected for age, sex, in-scanner motion, and site, generating a connectivity matrix for each dataset within a disorder. This matrix indicates connections with hypo-connectivity in patients (negative d) or hyper-connectivity in patients compared to controls (positive d).
- Meta-Analysis: these connectivity-wise effects were aggregated across datasets for each disorder using a meta-analytic approach with a random-effects model.

We provide the meta-analytic CSS for 11 neuropsychiatric and neurological disorders, encompassing 10,667 individuals (5,325 patients, 5,342 unique controls) across 22 datasets, allowing researchers to compute PCS on their own data.

## Prerequisites
- Python 3.7+, MATLAB, or R
#### Required packages:
- Python: NumPy >= v1.21.0
- R: No additional packages required
- MATLAB: No additional toolboxes required

## Setup
Clone this repository:

```git clone https://github.com/dutchconnectomelab/pcs-toolbox.git```


### For R Users

1. **Download Required Files**: Similarly, download the R script `calculate_PCS.R` from this repository.

2. **Source Script**: Use the following command within R to source the `calculate_PCS.R` script for use:
   ```r
   source("/path/to/calculate_PCS.R")

### For MATLAB Users

1. **Download Required Files**: Instead of cloning the repository, download the MATLAB script `calculate_PCS.m` directly.

2. **Add Path**: Add the directory containing `calculate_PCS.m` to MATLAB's path using `addpath('/path/to/folder/containing/calculate_PCS')`.


### Installation Dependencies

In Python, ensure you have the following packages installed:

- NumPy

You can install these packages in python using pip:

```bash
pip install numpy
```

### Input Data Format:

The `cnn` parameter is a connectivity matrix representing functional brain connections, typically a correlation matrix. The function `calculate_PCS` automatically detects the dimensions of the input `cnn` matrix to determine the number of regions of interest (ROI) and subjects:

- **2D Matrix (N_regions × N_regions):**
  If `cnn` is a 2D matrix, PCS is calculated assuming it represents the connectivity between ROIs for a single subject.

- **3D Matrix (N_regions × N_regions × N_subjects):**
  If `cnn` is a 3D matrix, PCS is calculated for each subject represented in the third dimension; computed individually for each subject's connectivity data.

This allows for flexibility in handling both single-subject and multi-subject connectivity data. It is crucial to ensure that the atlas used to generate the input connectivity matrix matches the atlas specified in the function parameters for accurate PCS calculation.

### Ensure consistency in dimensions and region order

To successfully calculate PCS, the connectivity matrix of a subject must match the dimensions of the CSS for the specified atlas. If the dimensions do not align, PCS calculations will not function correctly.
Additionally, it is crucial that the order of regions in the connectivity matrix corresponds exactly to the order in the CSS. You can verify the order of regions by checking the index and columns of the CSS files provided. Please make sure to verify these details before running your analysis.

### Usage in R, MATLAB, and Python

#### R

```r
# Source the calculate_PCS.R script from your cloned repository:
source("path/to/your-repository/calculate_PCS.R")
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
pip install numpy 

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

### The PCS toolbox supports the following neuropsychiatric and neurodegenerative disorders:

- Alzheimer's disease: `"alzheimer"`
- Anxiety-related disorders: `"anxiety"`
- Attention-deficit/hyperactivity disorder: `"adhd"`
- Autism spectrum disorder: `"autism"`
- Bipolar disorder: `"bipolar"`
- Frontotemporal dementia: `"ftd"`
- Major depressive disorder: `"depression"`
- Obsessive-compulsive disorder: `"ocd"`
- Parkinson's disease: `"parkinson"`
- Schizoaffective disorder: `"schizoaffective"`
- Schizophrenia: `"schizophrenia"`

When using the `calculate_PCS` function, specify the disorder parameter using its key (e.g., `'adhd'`, `'ftd'`, `'schizophrenia'`, etc.).

The demographics of the samples used to compute the CSS per disorder are as follows:

| Disorder                                 |   Patients, n |   Controls, n | Age (Mean ± SD)   | Male/Female, n   |   Datasets, n |
|------------------------------------------|---------------|---------------|-------------------|------------------|---------------|
| Alzheimer's disease                      |           270 |           866 | 72.0 ± 8.9        | 510/626          |             4 |
| Anxiety-related disorders                |           366 |           840 | 27.1 ± 21.3       | 505/701          |             3 |
| Attention-deficit/hyperactivity disorder |          1211 |          1417 | 19.1 ± 16.7       | 1518/1110        |             4 |
| Autism spectrum disorder                 |          1151 |          2086 | 21.6 ± 14.3       | 2530/707         |             4 |
| Bipolar disorder                         |           320 |          1790 | 36.3 ± 13.8       | 975/1135         |             5 |
| Frontotemporal dementia                  |           156 |           143 | 64.0 ± 8.5        | 144/155          |             2 |
| Major depressive disorder                |           884 |          1605 | 33.9 ± 15.8       | 1122/1367        |             4 |
| Obsessive-compulsive disorder            |            98 |           261 | 12.7 ± 4.5        | 170/189          |             3 |
| Parkinson’s disease                      |           102 |           125 | 66.4 ± 8.5        | 110/117          |             4 |
| Schizoaffective disorder                 |           235 |           812 | 37.2 ± 12.8       | 403/644          |             3 |
| Schizophrenia                            |           532 |          1882 | 36.5 ± 13.6       | 1254/1160        |             6 |

### Global Mean Correction (gmean)

Global mean signal correction is a technique used to reduce the impact of non-neural physiological noise in fMRI data, although its use is debated in the neuroimaging community as it can also remove some neural signals of interest. The PCS toolbox provides options for both corrected and uncorrected CSS, allowing researchers to choose based on their specific research questions and methodological preferences.

- When `gmean=True` (Python) or `gmean` is included (MATLAB/R), the toolbox uses functional CSS that have been corrected for global mean signal. This correction involved regressing out the framewise mean signal intensity of all brain voxels.

- When `gmean=False` (Python) or the parameter is omitted (MATLAB/R), the toolbox uses functional CSS without global mean signal correction.

We advise using CSS with `gmean` if the provided `cnn` also uses this preprocessing method.

### The PCS toolbox supports the following atlas parcellation schemes:
- <a href="#" title="Fischl, B., van der Kouwe, A., Destrieux, C., Halgren, E., Ségonne, F., Salat, D. H., Busa, E., Seidman, L. J., Goldstein, J., Kennedy, D., Caviness, V., Makris, N., Rosen, B., Dale, A. M. (2004). Automatically parcellating the human cerebral cortex. Cereb Cortex, 14(1), 11-22. doi: 10.1093/cercor/bhg087">`aparc (Desikan-Killiany)`</a> (68 regions)
- <a href="#" title="Ardesch, D. J., Scholtens, L. H., Li, L., Preuss, T. M., Rilling, J. K., & van den Heuvel, M. P. (2019). Evolutionary expansion of connectivity between multimodal association areas in the human brain compared with chimpanzees. Proceedings of the National Academy of Sciences, 116(14), 7101-7106. DOI: 10.1073/pnas.1818512116. PMID: 30886094. PMCID: PMC6452697.">`BB50human`</a> (76 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`Brodmann`</a> (78 regions)
- <a href="#" title="Fan, L., Li, H., Zhuo, J., Zhang, Y., Wang, J., Chen, L., Yang, Z., Chu, C., Xie, S., Laird, A. R., Fox, P. T., Eickhoff, S. B., Yu, C., Jiang, T. (2016). The Human Brainnetome Atlas: A New Brain Atlas Based on Connectional Architecture. Cereb Cortex, 26(8), 3508-26. doi: 10.1093/cercor/bhw157. Epub 2016 May 26. PMID: 27230218; PMCID: PMC4961028.">`brainnetome`</a> (210 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`Campbell`</a> (34 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`EconomoCT`</a> (30 regions)
- <a href="#" title="Scholtens, L. H., de Reus, M. A., de Lange, S. C., Schmidt, R., van den Heuvel, M. P. (2018). An MRI Von Economo - Koskinas atlas. Neuroimage, 170, 249-256. doi: 10.1016/j.neuroimage.2016.12.069. Epub 2016 Dec 28. PMID: 28040542.">`economo`</a> (86 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`Flechsig`</a> (92 regions)
- <a href="#" title="Glasser, M. F., Coalson, T. S., Robinson, E. C., Hacker, C. D., Harwell, J., Yacoub, E., et al. (2016). A multi-modal parcellation of human cerebral cortex. Nature. http://doi.org/10.1038/nature18933">`hcp-mmp-b (Glasser)`</a> (360 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`Kleist`</a> (98 regions)
- <a href="#" title="Cammoun L, Gigandet X, Meskaldji D, Thiran JP, Sporns O, Do KQ, et al. (2012). Mapping the human connectome at multiple scales with diffusion spectrum MRI. J Neurosci Methods, 203, 386–397. doi: 10.1016/j.jneumeth.2011.09.031">`lausanne120`</a> (114 regions)
- <a href="#" title="Cammoun L, Gigandet X, Meskaldji D, Thiran JP, Sporns O, Do KQ, et al. (2012). Mapping the human connectome at multiple scales with diffusion spectrum MRI. J Neurosci Methods, 203, 386–397. doi: 10.1016/j.jneumeth.2011.09.031">`lausanne250`</a> (219 regions)
- <a href="#" title="Cammoun L, Gigandet X, Meskaldji D, Thiran JP, Sporns O, Do KQ, et al. (2012). Mapping the human connectome at multiple scales with diffusion spectrum MRI. J Neurosci Methods, 203, 386–397. doi: 10.1016/j.jneumeth.2011.09.031">`lausanne500`</a> (448 regions)
- <a href="#" title="Whitaker KJ, Vértes PE, Romero-Garcia R, Váša F, Moutoussis M, Prabhu G, Weiskopf N, Callaghan MF, Wagstyl K, Rittman T, Tait R, Ooi C, Suckling J, Inkster B, Fonagy P, Dolan RJ, Jones PB, Goodyer IM; NSPN Consortium; Bullmore ET. (2016). Adolescence is associated with genomically patterned consolidation of the hubs of the human brain connectome. Proc Natl Acad Sci U S A, 113(32), 9105-10. doi: 10.1073/pnas.1601745113">`nspn500`</a> (308 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer100-yeo7`</a> (100 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer300-yeo7`</a> (300 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer400-yeo7`</a> (400 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer500-yeo7`</a> (500 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer600-yeo7`</a> (600 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer700-yeo7`</a> (700 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer800-yeo7`</a> (800 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer900-yeo7`</a> (900 regions)
- <a href="#" title="Schaefer A, Kong R, Gordon EM, Laumann TO, Zuo XN, Holmes AJ, Eickhoff SB, Yeo BTT. Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI. Cereb Cortex. 2018 Sep 1;28(9):3095-3114. doi: 10.1093/cercor/bhx179. PMID: 28981612; PMCID: PMC6095216.">`schaefer1000-yeo7`</a> (1000 regions)
- <a href="#" title="Pijnenburg, R., Scholtens, L. H., Ardesch, D. J., de Lange, S. C., Wei, Y., & van den Heuvel, M. P. (2021). Myelo- and cytoarchitectonic microstructural and functional human cortical atlases reconstructed in common MRI space. NeuroImage, 239, Article 118274. https://doi.org/10.1016/j.neuroimage.2021.118274">`Smith`</a> (88 regions)
- <a href="#" title="Yeo BT, Krienen FM, Sepulcre J, Sabuncu MR, Lashkari D, Hollinshead M, Roffman JL, Smoller JW, Zöllei L, Polimeni JR, Fischl B, Liu H, Buckner RL. (2011). The organization of the human cerebral cortex estimated by intrinsic functional connectivity. J Neurophysiol, 106(3), 1125-65. doi: 10.1152/jn.00338.2011">`yeo17dil`</a> (116 regions)

### Output PCS Scores:
The calculate_PCS function returns an array of PCS scores, one for each subject in the input data. Higher PCS indicate a stronger presence of connectivity patterns associated with the specified disorder. Importantly, scores are relative measures and should be interpreted in comparison to a control group or normative data.

### Datasets
Datasets used in the creation of CSS can be accessed via their respective websites:

Openly Accessible Datasets
- Autism Brain Imaging Data Exchange (ABIDE-I & ABIDE-II):  [fcon_1000.projects.nitrc.org/indi/abide](https://fcon_1000.projects.nitrc.org/indi/abide/)
- Advancing Research and Treatment for Frontotemporal Lobar Degeneration - Longitudinal Evaluation of Familial Frontotemporal Dementia Subjects (ARTFL-LEFFTDS): [memory.ucsf.edu/research/studies/nifd](memory.ucsf.edu/research/studies/nifd) 
- ADHD-200 Sample:  [nitrc.org/frs/?group_id=383](https://www.nitrc.org/frs/?group_id=383)
- Alzheimer's Disease Neuroimaging Initiative (ADNI-2/GO & ADNI-3):  [ida.loni.usc.edu](https://ida.loni.usc.edu)
- Boston Adolescent Neuroimaging of Depression and Anxiety (BANDA): ([NDA](https://nda.nih.gov); NDAR ID: 3037)
- Bipolar & Schizophrenia Consortium for Parsing Intermediate Phenotypes (B-SNIP1): ([NDA](https://nda.nih.gov); NDAR ID: 2274)
- Bipolar & Schizophrenia Consortium for Parsing Intermediate Phenotypes 2 (B-SNIP2): ([NDA](https://nda.nih.gov); NDAR ID: 2165)
- Latin American Brain Health Institute (BrainLat): [synapse.org](https://www.synapse.org/Synapse:syn51549340/wiki/624187)
- Centre for Biomedical Research Excellence (COBRE): [schizconnect.org](http://schizconnect.org)
- Consortium for Neuropsychiatric Phenomics (CNP): OpenNeuro [openneuro.org](http://openneuro.org)
- Healthy Brain Network (HBN): [fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network](http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network)
- Enhanced Nathan Kline Institute (NKI-Enhanced): [fcon_1000.projects.nitrc.org/indi/enhanced/](http://fcon_1000.projects.nitrc.org/indi/enhanced/)
- Open Access Series of Imaging Studies (OASIS-3): [oasis-brains.org](http://www.oasis-brains.org)
- Brain Function and Genetics in Pediatric Obsessive-Compulsive Behaviors (OCD-Pediatric): ([NDA](https://nda.nih.gov); NDAR ID: 2955)
- Task Control Circuit Targets for Obsessive Compulsive Behaviors in Children (OCD-Task): ([NDA](https://nda.nih.gov); NDAR ID: 3044)
- Parkinson’s Disease Yonemaya: [openfmri.org](https://openneuro.org/datasets/ds000245/versions/00001)
- Parkinson’s Disease Tao Wu and NEUROCON: [fcon_1000.projects.nitrc.org/indi/retro/parkinsons.html](fcon_1000.projects.nitrc.org/indi/retro/parkinsons.html)
- Japanese Strategic Research Program for the Promotion of Brain Science (SRPBS): [bicr-resource.atr.jp/srpbs1600](https://bicr-resource.atr.jp/srpbs1600)

Restricted Access Datasets
- Marburg-Münster Affective Disorders Cohort Study (FOR2107): [for2107.de](http://for2107.de)
  
### Citing the PCS toolbox
When using PCS toolbox, please cite the following paper:
Libedinsky, I., Helwegen, K., Boonstra, J., Guerrero Simón, L., Gruber, M., Repple, J., et al. (2024). Polyconnectomic scoring of functional connectivity patterns across eight neuropsychiatric and three neurodegenerative disorders. Biological Psychiatry. https://doi.org/10.1016/j.biopsych.2024.10.007

When computing PCS for a particular disorder using the precomputed CSS, please cite the corresponding papers listed in [Citations](/citations.md).
These sources were used for computing the CSS.

### License
pcs-toolbox © 2024 by dutchconnectomelab is licensed under CC BY-NC 4.0.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/
