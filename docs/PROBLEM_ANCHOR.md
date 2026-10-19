# Problem Anchor

## Concrete problem

TED has marked variation in the relative involvement of extraocular muscles,
orbital fat, lacrimal gland, and other orbital tissues. TOM500 makes it
possible to ask whether these patterns form reproducible patient-level imaging
phenotypes and whether they track the available CAS-based clinical activity
measure rather than treating all TED as one homogeneous morphology.

## Beneficiary

Endocrinologists and multidisciplinary thyroid-eye-disease teams that need a
more quantitative description of orbital tissue involvement and its clinical
activity correlate.

## Closest baselines

- Tissue-volume and asymmetry summaries.
- Single-tissue MRI radiomics.
- Existing TED MRI studies focused on activity or treatment response rather
  than reproducible multi-tissue phenotype stability.

## Baseline mode

`public-dataset-analysis / replication-access-check`

## Paper and data access status

- Target journal scope: identified; Thyroid Endocrinology is the intended
  section.
- Relevant prior literature: accessible at the metadata/full-text level.
- Claimed seed dataset: unresolved; TOM500 is now the active dataset.
- Supplied DOI `10.6084/m9.figshare.21764519`: not verified at initialization.
- Closely matching verified public dataset: TOM500,
  `10.6084/m9.figshare.27133389`; available metadata indicates T2WI, masks, and
  basic clinical variables, but does not establish CAS/TSH/FT4/TRAb availability.

## Fatal flaws

- The claimed 87-case endocrine package cannot be independently verified.
- The TOM500 image/clinical linkage fails or CAS is not auditable.
- The cluster solution is unstable or cannot be replicated in held-out data.
- MRI acquisition heterogeneity or missing acquisition metadata prevents
  meaningful radiomics harmonization.
- The analysis overfits a high-dimensional feature set despite 500 patients.

## Pilot boundary

Before full modeling, run only a data audit and a small phenotype pilot:

- enumerate patients, sequences, masks, and clinical fields;
- quantify missingness, CAS balance, and mask coverage;
- verify bilateral-eye aggregation at patient level;
- test reproducibility of a limited set of intensity, volume, and texture
  features;
- estimate cluster stability under bootstrap resampling and feature-family
  sensitivity.

No autoimmune-mechanism claim, clinical claim, feature ranking, or final
cluster solution should be promoted from this pilot alone.
