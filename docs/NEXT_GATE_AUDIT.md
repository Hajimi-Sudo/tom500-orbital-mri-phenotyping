# Next-Gate Audit

## Data and image contract

- 500 cases were analyzed with a fixed 400/100 train-validation split and no
  split overlap.
- All 500 image/mask pairs loaded successfully with shape `(512, 512, 20)`.
- Mask values 0-9 occurred in every case, including all nine annotated tissue
  labels.
- The dominant voxel spacing was `(0.3125, 0.3125, 3.85)` mm in 467/500
  cases. The remaining cases had small but nonzero spacing variation; physical
  volumes were computed from each image header and must remain the primary
  volume representation.
- The final tissue fractions were audited as (f_i=V_i/sum_{j=1}^{9}V_j).
  The legacy nonzero-MRI-denominator fractions summed to 0.0313--0.0632 per
  case and were retained only as an audit reference; all final clustering and
  association results use the corrected fractions.
- The 18-feature primary family comprised 9 physical volumes and 9 fractions.
  Each tissue contributed three intensity summaries (within-mask mean, SD, and
  p90 after within-scan median/IQR standardization), yielding 27 intensity
  features and 45 features in the combined sensitivity family.

## Sensitivity results

- The frozen 3-cluster volume solution was stable under standard scaling
  (bootstrap ARI 0.872) and robust scaling (ARI 0.808); the solutions had
  train ARI 0.606 against one another.
- Volume-only alternatives were moderately similar to the primary solution:
  physical-volume ARI 0.520 and fraction-only ARI 0.761. The combined
  45-feature solution was less similar (ARI 0.270) and had lower silhouette,
  so it should remain secondary rather than replace the volume-led phenotype.
- Removing any one tissue retained moderate-to-high similarity to the primary
  solution (ARI 0.653-0.925). A single-tissue solution did not reproduce the
  multi-tissue solution (ARI 0.036-0.316). This argues against a single tissue
  being sufficient, but does not prove biological independence among tissues.
- For all feature families, training-partition medians were used for missing
  value imputation and the scaler was fitted on training cases only. The
  silhouette was computed on the standardized training matrix; bootstrap ARI
  compared reference labels with K-means labels on resampled training rows,
  and sensitivity ARI compared alternative labels with the primary labels on
  the same training cases.

## Clinical confounding and adjusted association

The primary clusters were associated with age, sex, and smoking index in both
the training and validation partitions. Disease duration was not clearly
different between clusters.

After adjustment for age, sex, smoking index, and disease duration:

- Training-set continuous CAS association remained significant (overall Wald
  p=2.09e-07); the adjusted CAS estimates for clusters 1 and 2 versus cluster
  0 were 0.37 (95% CI 0.08-0.67) and 1.19 (0.77-1.61).
- Training-set CAS >= 3 association remained significant (overall Wald
  p=2.09e-06); adjusted odds ratios were 2.42 (1.20-4.87) and 6.55
  (3.11-13.79).
- Validation-set continuous CAS showed nominal overall support (p=0.0495),
  whereas CAS >= 3 was not supported (p=0.543); confidence intervals were
  wide.
- Ordinal-logistic sensitivity analysis converged in both partitions. The
  common OR for cluster 2 versus cluster 0 was 4.27 (95% CI 2.45-7.44) in
  training and 4.40 (1.42-13.64) in validation; overall Wald p values were
  1.38e-06 and 0.0366, respectively. Cluster 1 estimates were less precise.
  Threshold-specific fits at the highest CAS categories did not converge,
  because those categories were sparse; the proportional-odds assumption is
  therefore not treated as definitively verified.

## Gate decision

**Pass with major caveats for exploratory phenotype characterization. Fail for
promotion as an independently validated activity biomarker or treatment
selection model.**

The defensible paper claim is that a reproducible, volume-led multi-tissue
orbital MRI phenotype can be identified in TOM500 and shows an exploratory,
unadjusted association with CAS. The adjusted association is a training-set
finding that does not replicate in the 100-case validation partition.

## Explicit stop decisions

- Do not add a large texture-radiomics panel at this stage; it would increase
  dimensionality without resolving the validation and confounding problem.
- Do not claim that clusters represent Graves autoimmune mechanisms, treatment
  strata, or clinically actionable activity states.
- Do not describe the 100-case partition as external validation.
- Do not claim an independent CAS association until a larger or independent
  cohort reproduces the adjusted effect.

## Minimum next work

1. Freeze the volume-led phenotype definition and report cluster composition,
   age/sex/smoking imbalance, and CAS association transparently.
2. Add effect-size plots and a prespecified confounder sensitivity table to the
   analysis package.
3. Verify mask-label semantics against the dataset documentation and retain the
   spacing audit in the supplement.
4. If a second cohort or biochemical variables become available, test adjusted
   replication there. Otherwise proceed only with an exploratory brief report.
