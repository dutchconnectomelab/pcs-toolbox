The CONNECT project investigates cross-disorder brain connectivity changes using MRI data. 
This repository provides tools and results developed in the context of the  CONNECT project.

## :hammer: Installation

In a terminal, run:

```
git clone https://github.com/dutchconnectomelab/connect-toolbox
python3 -m pip install -e connect-toolbox
```

To update to the latest version, simply run:

```
cd connect-toolbox
git pull
```

## Diseasemaps

Diseasemaps are provided in `diseasemaps/`.

## Usage

### Example 1: evaluate PCS on a novel subject.

```
import numpy as np

import connect_toolbox as ct

# generate a random connectivity matrix as example
subject_connectivity = np.random.randn(82, 82)
subject_connectivity = (subject_connectivity + subject_connectivity.T) / 2
subject_connectivity[np.diag_indices(82)] = 0

# evaluate PCS score of schizophrenia
pcs = ct.PCS(dx="schizophrenia", modality="functional-connectivity", atlas="aparc+aseg")

subject_score = pcs.evaluate(subject_connectivity)
```

### Example 2: use only a subset of datasets

```
pcs = ct.PCS(
    dx="schizophrenia",
    modality="functional-connectivity",
    atlas="aparc+aseg",
    studies=["COBRE"],
)
```

This is especially useful when you want to run PCS on a public dataset and ensure it is excluded from fitting the model:

```
all_studies = ct.data.list_studies(
    dx="alzheimer",
    modality="functional-connectivity",
    metric="gmean_scrubbed_0.01-0.1",
    atlas="aparc+aseg",
)

included_studies = [study for study in all_studies if "ADNI" not in study]

pcs = ct.PCS(
    dx="alzheimer",
    modality="functional-connectivity",
    metric="gmean_scrubbed_0.01-0.1",
    atlas="aparc+aseg",
    studies=included_studies,
)
```

