---
profile_id: BIOMEDICAL_WRITING_PROFILE
domain_skill: domain-writing-biomedical
domain_family: biomedical
claim_unit: population_or_model_system_exposure_or_state_outcome
question_frame: PICO-equivalent observational phenotype question
study_design: retrospective cross-sectional public-dataset exploratory analysis
evidence_rule: association-only; no causal, therapeutic, mechanistic, or deployment claims
---

# Biomedical Writing Profile

## Population

Patients with thyroid-associated ophthalmopathy represented in the public
TOM500 orbital MRI dataset. The available clinical table includes CAS, age,
sex, smoking index, and disease duration. TSH, FT4, TRAb, and proptosis are not
available in the verified table.

## Imaging exposure/state

Patient-level orbital MRI tissue-volume features derived from nine annotated
orbital structures. The primary representation is physical volume and volume
fraction; the primary phenotype is a three-cluster solution fitted on the 400-
case training partition.

## Comparator

Alternative feature families, robust versus standard scaling, tissue-deletion
sensitivity, and the held-out 100-case validation partition. These are
internal robustness comparators, not independent external cohorts.

## Outcomes

Primary: cluster stability and reproducibility. Secondary: CAS as a continuous
score and exploratory CAS >= 3 binary threshold. Age, sex, smoking index, and
disease duration are characterization/confounding variables.

## Required language boundary

Use “associated with,” “co-varied with,” “exploratory,” and “hypothesis-
generating.” Avoid “predicts,” “diagnoses,” “determines treatment,” “causes,”
“proves autoimmune mechanism,” and “clinical utility.”

## Required reporting

State the retrospective design, public data source, fixed patient-level split,
mask/image linkage, CAS definition used in the table, missing biochemical
variables, spacing heterogeneity, confounding, and absence of independent
external validation.
