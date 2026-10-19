# TOM500 orbital MRI phenotyping code

This directory contains the analysis scripts used for the volume-led,
multi-tissue orbital MRI phenotype study. The scripts operate at the patient
level and do not treat bilateral eyes as independent observations.

## Feature definition

The primary representation contains 18 variables: nine physical tissue
volumes and nine compositional fractions. For tissue (i), the fraction is

`V_i / sum(V_j)`

over the nine annotated tissues. The sensitivity representation adds 27
within-mask intensity summaries, consisting of the mean, standard deviation,
and 90th percentile for each tissue. The combined sensitivity representation
therefore contains 45 variables.

## Script map

- `01_feature_extraction/pilot_multitissue.py`: audit image-mask pairs,
  extract patient-level features, and evaluate candidate K-means solutions.
- `02_audit/recompute_compositional_fractions.py`: recompute fractions using
  the audited nine-tissue denominator.
- `03_analysis/next_gate_analysis.py`: run scaling, feature-family, tissue,
  and clinical sensitivity analyses.
- `03_analysis/adjusted_association.py`: fit covariate-adjusted continuous
  and binary CAS association models.
- `03_analysis/ordinal_cas_sensitivity.py`: fit the ordinal CAS sensitivity
  model and inspect threshold-specific fits.
- `04_visualization/make_figures_tables.py`: regenerate JPG manuscript figures
  and CSV tables from frozen analysis outputs.

## Input layout

Raw data are not included in this repository. When extracting from NIfTI
files, provide a data root with the following layout:

```text
data_root/
  train/image/*.nii.gz
  train/label/*.nii.gz
  val/image/*.nii.gz
  val/label/*.nii.gz
```

The clinical table must contain an `Id` column and the fields used by the
analysis, including `Age`, `Sex`, `SmokingIndex`, `DiseaseDuration`, and
`CAS`. A previously audited feature table can be supplied instead of raw
NIfTI files with `--features-in` and `--audit-in`.

## Reproduction commands

Run commands from the project root. The commands below write to the existing
`analysis/` evidence directory and are intended for a server with the raw
dataset mounted locally.

```bash
python code/01_feature_extraction/pilot_multitissue.py \
  --data-root /path/to/TOM500 \
  --clinical analysis/clinical_characteristics.csv \
  --out-dir analysis \
  --bootstrap 1000 \
  --seed 20261019

python code/02_audit/recompute_compositional_fractions.py

python code/03_analysis/next_gate_analysis.py \
  --features analysis/pilot_features.csv \
  --clinical analysis/clinical_characteristics.csv \
  --audit analysis/feature_audit.json \
  --out-dir analysis \
  --bootstrap 1000 \
  --seed 20261019

python code/03_analysis/adjusted_association.py \
  --features analysis/pilot_features.csv \
  --clinical analysis/clinical_characteristics.csv \
  --audit analysis/feature_audit.json \
  --out analysis/adjusted_association.json \
  --seed 20261019

python code/03_analysis/ordinal_cas_sensitivity.py \
  --features analysis/pilot_features.csv \
  --clinical analysis/clinical_characteristics.csv \
  --out analysis/ordinal_cas_sensitivity.json \
  --seed 20261019

python code/04_visualization/make_figures_tables.py
```

The visualization command writes the four JPG figures to
`manuscript/frontiers/` and the CSV tables to `manuscript/tables/`.

The commands are designed for the remote analysis server that has the raw
TOM500 NIfTI files mounted. They are not intended to be run on the manuscript
workstation. A full rerun should record the Python version, package versions,
input data version, fixed split, seed, and output hashes.

The archived JSON files under `analysis/` are frozen evidence from the
server-run analyses used for the manuscript. Patient-level clinical tables and
feature tables are excluded from the public repository because they are not
needed to inspect the code and may contain row-level clinical information.
Re-running the scripts can produce different intermediate random streams if
software versions differ. The fixed split, seed, feature definition,
preprocessing order, and bootstrap count should therefore be reported with any
new run.

## Data and privacy

Do not commit raw MRI files, masks, patient-level derived tables, Baidu Netdisk
cookies, SSH credentials, private server paths, or other access tokens. Obtain
TOM500 directly from its public repository and follow its access and citation
conditions. The intended public repository is
`https://github.com/Hajimi-Sudo/tom500-orbital-mri-phenotyping`.
