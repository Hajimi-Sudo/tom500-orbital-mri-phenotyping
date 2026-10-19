---
status: plan-ready; deterministic plots first
mode: main / actual_result
figure_generation_route: deterministic_local_for_numeric_figures; RH PaperBanana pending for conceptual workflow figure
---

# Figure Plan

## Figure 1 - Study and analysis workflow

- Role: orient the reader to cohort, masks, patient-level aggregation, train/
  validation boundary, clustering, and CAS characterization.
- Layout: four horizontal evidence lanes: public TOM500 -> nine masks ->
  volume-led patient table -> train-fit/validation-assignment -> clinical
  characterization.
- Allowed labels: “TOM500”, “MRI + masks”, “Patient-level volumes”, “400 train /
  100 validation”, “CAS association”.
- Forbidden labels: “diagnosis”, “treatment selection”, “autoimmune mechanism”,
  “external validation”.
- Route: conceptual figure may use PaperBanana after provider readiness; if not
  available, keep a deterministic local fallback explicitly labeled as such.

## Figure 2 - Multi-tissue phenotype profiles

- Role: show standardized tissue volume/fraction profiles for the three
  clusters and their separation.
- Panels: cluster heatmap of tissue features; nine-tissue profile plot; cluster
  size annotation.
- Data source: the frozen aggregate cluster centers in
  `../analysis/server_results/bootstrap1000/next_gate_report.json`.
- The heatmap uses the 18-feature primary volume-led family (9 volumes + 9
  compositional fractions); the 27 intensity features and 45-feature combined
  sensitivity family are summarized in the sensitivity analysis, not in this
  panel.
- No p-value-only annotation; show cluster sizes and standardized effect sizes.

## Figure 3 - CAS characterization

- Role: show the unadjusted CAS gradient in train and validation partitions.
- Panels: jitter/box or violin plots of CAS by cluster; active CAS >= 3 rates with
  binomial confidence intervals.
- Caption must state that the 100 cases are a fixed validation partition, not an
  external cohort.

## Figure 4 - Robustness and adjusted association

- Role: prevent overinterpretation by showing sensitivity and the validation
  attenuation after covariate adjustment.
- Panels: ARI for scaling/feature-family/tissue deletion; forest plot for
  adjusted CAS OLS and CAS >= 3 logistic effects in train versus validation.
- Data source: `../analysis/server_results/bootstrap1000/next_gate_report.json` and
  `../analysis/server_results/corrected_v2/adjusted_association.json`.
- Use a neutral visual treatment for null validation estimates; do not visually
  imply a confirmed clinical effect.

## Tables

- Table 1: clinical and imaging characteristics by cluster, with missingness,
  median/IQR or count/percentage, and standardized differences.
- Table 2: bootstrap ARI, silhouette, cluster counts, and sensitivity results.
- Table 3: unadjusted and adjusted CAS associations with 95% CIs.

## Figure-quality constraints

- Numeric axes and labels must be generated deterministically from the frozen
  results.
- Use colorblind-safe, print-friendly colors; cluster colors are fixed across
  all figures.
- Do not use decorative MRI imagery, generic neural-network motifs, or
  unsupported mechanistic arrows.
- Every caption must distinguish observed results from interpretation.
