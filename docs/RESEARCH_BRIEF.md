# Research Brief

## Topic

Multi-tissue orbital MRI radiomic subtyping of thyroid-associated ophthalmopathy
with CAS-linked clinical characterization

## Proposed question

Among patients with thyroid-associated ophthalmopathy, can quantitative features
from multiple orbital tissues identify reproducible patient-level imaging
phenotypes, and are those phenotypes associated with CAS-defined activity,
age, sex, smoking index, and disease duration?

## Intended contribution

The paper should be positioned as an endocrine-imaging phenotype study. The
central contribution is not automated eye imaging alone; it is a reproducible
description of coordinated extraocular-muscle and orbital-tissue involvement
in TED, followed by CAS-linked clinical characterization. The available table
does not support claims about thyroid laboratory or antibody activity.

## Target venue

- Journal: *Frontiers in Endocrinology*
- Section: Thyroid Endocrinology
- Intended article type: Original Research, subject to author-guideline check

## Proposed endpoint hierarchy

1. Primary: cluster stability and reproducibility of patient-level imaging
   phenotypes.
2. Secondary: association of cluster membership with continuous CAS and a
   prespecified active/inactive threshold, preferably CAS >= 3.
3. Exploratory: association with age, sex, smoking index, and disease duration.
4. Not available in the current table: TRAb, TSH, FT4, and proptosis.

## Candidate model comparison

- Volume-only phenotype: tissue volumes and bilateral asymmetry.
- Intensity phenotype: robust intensity summaries per tissue.
- Radiomic phenotype: a restrained, prespecified texture panel.
- Multi-tissue phenotype: combined features after patient-level scaling and
  stability filtering.

The multi-tissue solution should only be promoted if it is stable across
bootstrap resamples, insensitive to reasonable feature-family choices, and
reproduces in the provided validation split. Cluster separation alone is not
enough.

## Minimum success criteria

- Verified patient-level data dictionary and reproducible MRI/mask/clinical
  linkage.
- No patient-level overlap between resampling folds.
- Feature extraction and selection reproducible from raw images and masks.
- Bootstrap cluster stability, feature-family sensitivity, and held-out
  replication.
- CAS association with uncertainty and multiplicity control.
- Clear disclosure of single-center/public-dataset limitations and lack of
  external validation.

## Stop criteria

Stop or re-scope the clinical-association component if the GitHub table cannot
be linked to all image IDs. Do not claim thyroid laboratory, antibody, or
autoimmune-mechanism associations because those fields are absent.

## Assumptions recorded at initialization

- The user wants a new topic directory under `medicine`.
- The target journal is *Frontiers in Endocrinology*.
- The proposed cohort is public and retrospective.
- The data identity and claimed clinical labels are not yet established.
