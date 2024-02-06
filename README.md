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

:warning: Disease maps are still work in progress and may change in subsequent iterations.

## Usage


```
import connect_toolbox as ct
import pandas as pd
import numpy as np

## EXAMPLE 1: evaluate PCS on a novel subject ##

# generate a random connectivity matrix as example
subject_connectivity = np.random.randn(82, 82)
subject_connectivity = (subject_connectivity + subject_connectivity.T) / 2
subject_connectivity[np.diag_indices(82)] = 0

# evaluate PCS score of schizophrenia
pcs = ct.models.PCS(dx="schizophrenia", modality="functional-connectivity", atlas="aparc+aseg")

subject_score = pcs.evaluate(subject_connectivity)
```

