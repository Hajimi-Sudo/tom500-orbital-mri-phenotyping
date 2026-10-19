# Pilot Audit

## Run

- Dataset: TOM500, 500 cases; train 400, validation 100.
- Image/mask contract: all 500 cases loaded successfully; no case-level errors.
- Features: 18 primary volume-led features (9 physical volumes + 9 fractions),
  27 intensity sensitivity features (9 tissues x mean/SD/p90), and 45 combined
  features. Intensity summaries used within-scan median/IQR standardization.
- Clinical linkage: 500/500 image IDs matched the clinical table; no CAS joins were missing.
- CAS distribution: 0:171, 1:128, 2:80, 3:67, 4:33, 5:17, 6:4.
- Reproducibility: corrected compositional fractions were recomputed from the audited physical volumes; raw images were not modified.

## Signal

- During the exploratory pilot, candidate solutions with 2--5 clusters were ranked first by mean bootstrap ARI and then by silhouette only for an exact bootstrap-ARI tie. The 3-cluster solution had the highest bootstrap ARI (0.862 +/- 0.103); the 2-cluster solution had a higher silhouette (0.272 vs 0.188) but lower bootstrap ARI (0.844 +/- 0.118). CAS Kruskal-Wallis p was 2.27e-09 in train and 4.01e-04 in validation.
- The corrected combined volume plus intensity representation selected 3 clusters. Its bootstrap ARI was 0.847 +/- 0.105; CAS Kruskal-Wallis p was 4.28e-08 in train and 0.00109 in validation.
- Intensity-only clustering selected 2 clusters, but CAS association was not supported in train (p=0.882) or validation (p=0.198).

## Decision

**Go to the next analysis gate, with a narrowed primary phenotype.** The initial signal is strongest for multi-tissue volume organization, with combined features as a sensitivity analysis. Do not promote intensity-only clusters or claim radiomic texture value from this pilot.

## Required next checks

1. Verify the exact mask semantics and voxel-spacing consistency across all cases.
2. Add age, sex, smoking index, and disease duration comparisons with effect sizes and confidence intervals; retain CAS as both continuous and exploratory CAS >= 3 outcomes.
3. Re-run cluster stability under feature-family perturbations, missing-structure handling, and alternative patient-level scaling.
4. Check whether the chosen clusters are driven by one tissue or reflect coordinated multi-tissue organization.
5. Only after these checks, test a restrained texture panel and add an `EVALUATION_GATE_PROFILE` before manuscript promotion.

## Interpretation boundary

This pilot supports an association between low-dimensional orbital tissue morphology and CAS in TOM500. It does not establish Graves autoimmune mechanisms, treatment response, thyroid laboratory associations, or clinical utility.
