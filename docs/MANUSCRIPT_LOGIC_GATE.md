---
status: pass-with-caveats
gate_scope: pre-draft logic; no submission-facing prose approved yet
---

# Manuscript Logic Gate

## Reviewer persuasion preflight

- What does the paper do? It identifies and audits a patient-level, volume-led
  multi-tissue orbital MRI phenotype in TOM500, then characterizes its CAS
  association.
- Why does it matter? TAO contains heterogeneous orbital tissue involvement,
  while a compact, reproducible phenotype may organize imaging heterogeneity
  for endocrine-imaging research.
- Why is existing work insufficient? A simple activity classifier does not
  establish whether multi-tissue morphology forms stable patient-level groups;
  this study tests stability before clinical interpretation.
- Why can the approach work? The dataset contains nine tissue masks and a
  patient-level CAS field, enabling tissue coordination to be tested without
  treating eyes as independent samples.
- What would convince a skeptical reader? Stable bootstrap clusters, feature
  and tissue sensitivity, fixed validation assignment, effect sizes with
  uncertainty, and transparent reporting of the null adjusted validation
  association.
- What does the paper not claim? It does not claim a validated activity
  biomarker, treatment-selection tool, thyroid laboratory association, or
  autoimmune mechanism.

## Core claim contract

**One-sentence claim:** In TOM500, patient-level orbital MRI tissue-volume
features yield a reproducible multi-tissue phenotype with an exploratory
association with CAS, but the available evidence is insufficient to establish
an independently validated activity biomarker.

Allowed focus:

1. Patient-level multi-tissue phenotype reproducibility.
2. CAS-linked clinical characterization.
3. Confounding, validation, and evidence boundary.

Forbidden focus: thyroid laboratory biology, antibody mechanisms, treatment
selection, deployment utility, and high-dimensional texture novelty.

## Argument tree

Root: a stable volume-led multi-tissue phenotype is a defensible exploratory
description of TAO imaging heterogeneity.

- Problem 1: orbital involvement is heterogeneous but often summarized as a
  single activity label. Contribution: patient-level nine-tissue phenotype;
  evidence: `../analysis/server_results/bootstrap1000/next_gate_report.json`; sections: Methods 2,
  Results 3.
- Problem 2: cluster separation can be an artifact of a feature family or one
  tissue. Contribution: scaling, feature-family, and tissue-deletion audits;
  evidence: `../analysis/server_results/bootstrap1000/next_gate_report.json`; sections: Methods 2, Results 4.
- Problem 3: phenotype-CAS association may reflect clinical confounding.
  Contribution: covariate characterization and adjusted validation reporting;
  evidence: `../analysis/server_results/corrected_v2/adjusted_association.json`; sections: Results 5, Discussion 6.

## Term registry

| Term | Definition | First use | Allowed aliases | Forbidden aliases |
|---|---|---|---|---|
| TAO/TED | Thyroid-associated ophthalmopathy / thyroid eye disease | Introduction | TAO, TED after definition | Graves orbitopathy as a new endpoint |
| multi-tissue phenotype | Patient-level cluster from nine tissue volume/fraction features | Abstract/Methods | imaging phenotype | autoimmune subtype, treatment subtype |
| CAS | Clinical Activity Score as present in the TOM500 table | Methods | CAS | gold-standard MRI activity |
| volume-led | Primary phenotype driven by physical volume and volume fraction features | Title/Abstract | morphology-led | radiomic biomarker |
| validation partition | Fixed 100-case TOM500 partition used for centroid assignment | Methods | held-out partition | external validation |
| adjusted association | Regression association controlling for available covariates | Results | covariate-adjusted association | independent causal effect |

## Promise-realization matrix

| Promise | Realization | Evidence |
|---|---|---|
| Reproducible phenotype | bootstrap ARI and fixed validation assignment | `../analysis/server_results/bootstrap1000/next_gate_report.json` |
| Multi-tissue rather than single-tissue signal | leave-one-tissue and single-tissue ARI | `../analysis/server_results/bootstrap1000/next_gate_report.json` |
| Endocrine clinical characterization | CAS, age, sex, smoking, disease duration | `../analysis/server_results/bootstrap1000/next_gate_report.json`, `../analysis/server_results/corrected_v2/adjusted_association.json` |
| Independent activity biomarker | explicitly not promised; validation-adjusted null retained | `../analysis/server_results/corrected_v2/adjusted_association.json` |

## Central thread audit

The sole controlling thread is: **reproducible imaging heterogeneity first,
clinical association second, validation limits throughout**.

- Endocrine scope: keep as clinical context and CAS interpretation.
- MRI segmentation: keep as data provenance, not a segmentation-method paper.
- Radiomics: narrow to low-dimensional volume-led features; defer texture.
- Autoimmunity: remove as a mechanistic claim because laboratory fields are
  absent.

## Reader confusion trace

- “Radiomics” in the original topic may imply a texture classifier. Repair:
  define the primary representation as volume/fraction features in the title
  and Methods.
- “Activity” may imply a validated diagnostic endpoint. Repair: use “CAS
  association” and explicitly report the adjusted validation null result.
- “Validation” may be read as external validation. Repair: call the 100 cases
  the fixed validation partition in every section.

## Title-abstract-result alignment

- Title: volume-led multi-tissue phenotype + CAS association.
- Abstract: same two entities, with exploratory and validation boundary.
- Methods: nine masks, physical volume, three clusters, fixed split.
- Results: ARI/stability, CAS distributions, adjusted training/validation
  results.
- Conclusion: phenotype characterization only.

## Gate report

Status: **pass-with-caveats** for outline and result-bound drafting.

Blocking items before submission-facing manuscript: verified literature pool,
mask-label documentation citation, final Frontiers article-type requirements,
ethics/data-use wording, and completed figures/tables.
