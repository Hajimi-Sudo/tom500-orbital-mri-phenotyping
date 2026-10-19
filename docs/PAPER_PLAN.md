---
paper_mode: main / actual_result
paper_type: original_research_candidate
target_venue: Frontiers in Endocrinology
target_section: Thyroid Endocrinology
topic_slug: tao-orbital-mri-radiomics-activity
status: plan-ready; exploratory-phenotype-only
rh_status: RH CLI unavailable; local artifact lineage retained
---

# Paper Plan

## Working title

**Volume-led multi-tissue orbital MRI phenotyping of thyroid-associated
ophthalmopathy and exploratory association with CAS**

The title deliberately avoids “activity classification,” “radiomic biomarker,”
and “autoimmune mechanism,” which are stronger than the adjusted validation
evidence supports.

## One-sentence objective

To determine whether patient-level orbital MRI tissue-volume features identify
reproducible imaging phenotypes in TOM500 and to characterize their exploratory
association with CAS while accounting for available clinical covariates.

## Study design

Retrospective public-dataset analysis of 500 TOM500 cases with a fixed 400-case
training partition and 100-case validation partition. Nine annotated orbital
structures are summarized at the patient level using physical volume and volume
fraction features. Three clusters are fitted on training data and assigned to
validation cases by the frozen centroids.

## Endpoint hierarchy

1. Primary: patient-level phenotype reproducibility, including bootstrap
   stability and feature/scaling/tissue sensitivity.
2. Secondary: unadjusted CAS distribution across clusters.
3. Exploratory: covariate-adjusted CAS associations and CAS >= 3 odds.
4. Characterization: age, sex, smoking index, disease duration, mask coverage,
   and spacing heterogeneity.

## Evidence-backed contribution shape

1. A reproducible, volume-led multi-tissue phenotype can be obtained from the
   public TOM500 cohort without treating both eyes as independent observations.
2. The phenotype captures coordinated multi-tissue organization: removing any
   one tissue retains similarity, whereas a single-tissue solution does not
   reproduce the multi-tissue solution.
3. The phenotype shows an exploratory CAS gradient, but adjusted association is
   not supported in the held-out validation partition and therefore is not
   presented as a validated activity biomarker.

## Planned manuscript structure

1. Abstract: clinical problem, data/design, volume-led phenotype, exact
   stability/CAS results, bounded conclusion.
2. Introduction: TAO activity assessment; heterogeneity of orbital tissue
   involvement; gap in patient-level multi-tissue phenotyping; objective.
3. Materials and Methods: dataset, masks, feature construction, split, cluster
   fitting, stability, sensitivity, CAS/covariate models, ethics/data access.
4. Results: cohort/data audit; phenotype stability; tissue sensitivity; CAS and
   covariate characterization; adjusted validation null result.
5. Discussion: endocrine-imaging interpretation, what the phenotype may add,
   why it is not a treatment tool, limitations, and next cohort requirements.
6. Conclusion: exploratory phenotype and evidence boundary in two sentences.

## Required tables and figures

- Table 1: cohort and clinical variables by cluster, with standardized
  differences or effect sizes rather than p values alone.
- Table 2: stability and sensitivity summary.
- Table 3: unadjusted and adjusted CAS associations in training and validation.
- Figure 1: dataset-to-phenotype analysis workflow.
- Figure 2: nine-tissue volume profiles and three-cluster separation.
- Figure 3: training/validation CAS distributions by cluster.
- Figure 4: sensitivity and adjusted-effect forest plot.

## Explicit exclusions

No TSH/FT4/TRAb/proptosis claims; no autoimmune mechanism claim; no treatment
recommendation; no external-validation label for the 100-case partition; no
large texture-radiomics expansion before independent replication.

## Open evidence tasks before submission

- Verify mask-label semantics against the TOM500 documentation and cite the
  data paper.
- Build a screened literature pool with DOI-verified TAO MRI, CAS, endocrine
  imaging, radiomics, and clustering papers.
- Confirm Frontiers article type, word limits, reporting checklist, data/code
  availability language, and ethics wording.
