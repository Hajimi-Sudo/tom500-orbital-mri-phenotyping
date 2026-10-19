---
status: pass-with-caveats; exploratory-phenotype-only
topic_id: tao-orbital-mri-radiomics-activity
baseline_mode: public-dataset-analysis / replication-access-check
paper_access_status: TOM500 imaging, masks, split, and CAS-linked clinical table verified; TSH/FT4/TRAb/proptosis unavailable
pilot_decision: volume-led multi-tissue phenotype retained; high-dimensional texture expansion deferred
---

# Evaluation Gate Profile

## Problem and discipline

The study is a medicine / thyroid endocrinology / medical-imaging analysis of
thyroid-associated ophthalmopathy. Its target is an exploratory imaging
phenotype and its clinical characterization, not a stand-alone ophthalmic
classifier.

## Current evidence

- `PILOT_AUDIT.md` documents complete image/mask loading, patient-level CAS
  linkage, cluster stability, and the initial CAS association.
- `NEXT_GATE_AUDIT.md` documents spacing/mask audits, feature-family and
  scaling sensitivity, tissue-deletion sensitivity, and covariate-adjusted
  associations.
- `../analysis/server_results/corrected_v2/adjusted_association.json` shows that the adjusted cluster-CAS signal is
  present in training but not statistically supported in validation.

## Fatal flaws and status

- `CRITICAL`: no independent external cohort. Status: unresolved; limits the
  study to exploratory internal validation.
- `CRITICAL`: biochemical thyroid and antibody variables are absent. Status:
  unresolved; TSH, FT4, TRAb, and proptosis claims are prohibited.
- `MAJOR`: clusters are confounded by age, sex, and smoking index. Status:
  documented; adjusted validation does not replicate the association.
- `MAJOR`: spacing is mildly heterogeneous. Status: physical voxel-volume
  normalization is applied and spacing is audited; residual acquisition effects
  remain a limitation.
- `MAJOR`: high-dimensional texture features have not demonstrated incremental
  value. Status: texture expansion deferred.

## Promotion rule

Promote only to an exploratory phenotype manuscript if the manuscript keeps
cluster stability as the primary result, treats CAS association as secondary,
reports covariate imbalance and the null adjusted validation result, and avoids
clinical utility or mechanistic claims. Do not promote to a diagnostic or
treatment-selection model without independent adjusted replication.
