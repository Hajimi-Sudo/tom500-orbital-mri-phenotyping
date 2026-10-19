# Option B Design

## Recommended title

**Multi-tissue orbital MRI radiomic subtyping of thyroid-associated
ophthalmopathy: an exploratory consensus-clustering study**

## Dataset correction

The TOM500 companion repository at
`https://github.com/guest0417/TOM500` provides
`clinical_characteristics.csv`. It has 500 patient rows and the fields:
`Id`, `StudyDate`, `BirthDate`, `Age`, `Sex`, `SmokingIndex`, `StartTime`,
`DiseaseDuration`, and `CAS`. The 500 numeric image IDs map one-to-one to the
training/validation split IDs. It does not provide TSH, FT4, TRAb, or proptosis.

The CAS distribution is 0:171, 1:128, 2:80, 3:67, 4:33, 5:17, 6:4. A
prespecified exploratory activity threshold of CAS >= 3 would yield 121/500
patients; this should be described as an association endpoint, not as proof
that a cluster is an activity state.

## What the data support

The defensible primary claim is:

> Multi-tissue orbital MRI features identify reproducible imaging phenotypes in
> a public TED cohort, and these phenotypes show measurable associations with
> CAS-defined clinical activity.

The data do not support:

> The clusters prove distinct Graves autoimmune injury mechanisms.

## Analysis plan

1. Audit image/clinical joins, mask label values, voxel spacing, orientation,
   crop coverage, and missing structures.
2. Extract patient-level features separately for the nine annotated tissues:
   volume, robust intensity summaries, and a restrained texture panel.
3. Aggregate bilateral structures within patient using mean/sum and absolute
   asymmetry; eyes are not independent observations.
4. Normalize features within the discovery set only; remove near-zero variance,
   highly redundant, and unstable features. Preserve volume-only and
   texture-only families as sensitivity analyses.
5. Estimate candidate cluster counts with consensus clustering or an equivalent
   reproducible method. Report silhouette, gap/PAC-type stability measures,
   bootstrap co-clustering stability, and cluster-size balance.
6. Discover clusters in the provided 400-case train split. Assign the 100-case
   validation split using nearest-centroid or a prespecified classifier; do not
   re-cluster validation data and call it external validation.
7. Compare the multi-tissue solution with volume-only, intensity-only, and
   single-tissue solutions. The added value is cross-tissue organization, not
   merely a larger feature count.
8. Test CAS as a continuous outcome and CAS >= 3 as an exploratory binary
   outcome, with effect sizes, confidence intervals, and multiplicity control.
   Age, sex, smoking index, and disease duration are covariates; thyroid
   laboratory and antibody claims are explicitly out of scope.

## Journal positioning

The endocrine fit is credible if TED and its clinical activity assessment remain
central and MRI is presented as a quantitative characterization of orbital
tissue involvement. A pure unsupervised segmentation/radiomics paper is more
naturally an imaging submission. For a Brief Research Report, use one compact
message, transparent stability analysis, and no mechanistic overclaim.

## Go/no-go gate

**Go now:** data linkage audit, mask audit, and a bounded clustering pilot.

**Go to manuscript:** clusters are stable, the held-out split shows reasonable
assignment consistency, and the CAS association survives sensitivity analyses.

**No-go:** unstable clusters, unresolved mask semantics, failed image/clinical
joins, or discussion claims about autoimmune mechanisms without biochemical
measurements.
