# TAO Orbital MRI Radiomics Phenotyping

Research Harness topic workspace for a proposed public-data study of
thyroid-associated ophthalmopathy (TAO/TED) imaging phenotypes using
multi-tissue orbital MRI radiomics and CAS-linked clinical variables.

## Current status

`next gate complete / exploratory phenotype only`

The study is intended for the Thyroid Endocrinology section of *Frontiers in
Endocrinology*. The target question is whether multi-tissue orbital MRI
features identify reproducible TED phenotypes and whether those phenotypes are
associated with CAS-defined activity and available clinical characteristics.

The claimed 87-patient Figshare dataset and DOI
`10.6084/m9.figshare.21764519` are not verified. The accessible resource is
TOM500, DOI `10.6084/m9.figshare.27133389`, and its companion GitHub repository
contains `clinical_characteristics.csv` with 500 rows and CAS. No TSH, FT4,
TRAb, or proptosis fields are present.

## Documents

- `docs/RESEARCH_BRIEF.md`: delivery scope, endpoint, venue, and success criteria
- `docs/PROBLEM_ANCHOR.md`: scientific problem, closest baselines, and fatal risks
- `docs/FRONTIER_ATTENTION_EVIDENCE.md`: current field and journal-positioning signals
- `docs/DATA_VERIFICATION.md`: dataset identity and label-verification checklist
- `docs/PILOT_AUDIT.md`: first full-cohort pilot audit and go/no-go decision
- `docs/NEXT_GATE_AUDIT.md`: sensitivity, confounding, and adjusted-association gate
- `docs/EVALUATION_GATE_PROFILE.md`: promotion boundary and fatal-flaw status
- `AGENTS.md`: working constraints and promotion gates

## Directory layout

- `code/`: organized feature extraction, audit, statistical analysis, and visualization scripts
- `analysis/`: aggregate audit files, statistical results, and server evidence
- `manuscript/`: LaTeX source, compiled PDF, BibTeX, figures, tables, and build logs
- `docs/`: research brief, literature/context notes, evidence gates, and writing audits

The recommended GitHub repository name is `tom500-orbital-mri-phenotyping`.
Raw MRI files, masks, credentials, cookies, and local environments are not
part of the repository. See `code/README.md` for the reproducibility workflow.

Build the manuscript from the Frontiers manuscript directory with the local TeX Live installation:

```bash
cd manuscript/frontiers
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The manuscript source and frozen PDF are in `manuscript/frontiers/`. The four
publication figures are JPG files in the same directory. Generated LaTeX
intermediate files are intentionally excluded from version control.

The public release is intended for the repository
`https://github.com/Hajimi-Sudo/tom500-orbital-mri-phenotyping`.

The repository contains code and aggregate analysis evidence only. The
patient-level clinical table, derived feature tables, raw images, and masks
remain outside version control. See `analysis/README.md` for the public input
schema and artifact boundary.

## Immediate next actions

1. Freeze the volume-led phenotype definition and prepare exploratory figures.
2. Add a transparent covariate imbalance and null adjusted-validation table.
3. Seek an independent cohort or biochemical variables before claiming an
   independently validated activity biomarker.
