---
status: pass-with-caveats
claim_strength_ceiling: D_exploratory / C_empirical_limited
---

# Result-to-Claim Analysis Profile

## Claim matrix

| Claim ID | Proposed claim | Evidence | Strength | Allowed wording |
|---|---|---|---|---|
| C1 | Three volume-led clusters are reproducible in TOM500 | 500/500 cases; corrected-feature train bootstrap ARI 0.862 from 1,000 resamples; scaling and tissue sensitivity | B_empirical_strong | “yielded a reproducible exploratory phenotype” |
| C2 | The signal is multi-tissue rather than single-tissue | leave-one-tissue ARI 0.653-0.925; single-tissue ARI 0.036-0.316 | B_empirical_strong | “was not reproduced by single-tissue solutions” |
| C3 | Clusters differ in unadjusted CAS | corrected-feature train p=2.27e-09; validation p=4.01e-04 | B_empirical_strong | “showed an unadjusted CAS gradient” |
| C4 | Cluster-CAS association is independent of clinical covariates | adjusted train significant; adjusted validation null | F_unsupported_or_blocked | Do not make this claim |
| C5 | The clusters identify active disease | no independent adjusted replication | F_unsupported_or_blocked | Do not make this claim |
| C6 | The clusters reflect autoimmune injury mechanisms | no TRAb/TSH/FT4 and no mechanistic assay | F_unsupported_or_blocked | Do not make this claim |
| C7 | The method can guide treatment selection | no treatment outcome or prospective validation | F_unsupported_or_blocked | Do not make this claim |

## Statistical versus practical significance

The unadjusted CAS p values are statistically strong, but the clinical meaning
of the cluster differences is not established. Age, sex, and smoking imbalance
are substantial; adjusted validation is null. Report effect sizes and confidence
intervals, not p values alone, and frame the result as hypothesis-generating.

## Negative and competing evidence

- Intensity-only clustering did not associate with CAS.
- Combined volume plus intensity features were less similar to the primary
  volume-led solution.
- Adjusted CAS associations did not replicate in validation.
- Mild spacing heterogeneity remains a possible acquisition confounder.

## Required claim repair

Any abstract, contribution, or discussion sentence that uses “predict,”
“diagnose,” “biomarker,” “mechanism,” “treatment,” “independent,” or “external
validation” must be rewritten or removed unless new evidence is added.
