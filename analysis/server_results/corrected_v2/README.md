# Server evidence: corrected-v2

All data-dependent analysis in this directory was executed on the remote CPU
server, not on the local workstation.

- Execution: remote CPU server, with machine-specific host and data paths
  intentionally omitted
- Primary feature script: `code/01_feature_extraction/pilot_multitissue.py`
- Secondary scripts: `code/03_analysis/next_gate_analysis.py`,
  `code/03_analysis/adjusted_association.py`, and
  `code/03_analysis/ordinal_cas_sensitivity.py`
- Split: 400 training cases and 100 fixed validation cases
- Bootstrap: the adjusted-association outputs reuse the frozen primary
  phenotype. The canonical 1,000-resample stability results are stored in
  `../bootstrap1000/`.
- Environment: Python 3.10 or newer with dependencies listed in
  `code/requirements.txt`

The primary feature audit found 18 volume-led features (9 physical volumes and
9 compositional fractions), 27 intensity features (9 tissues times mean, SD,
and p90), and 45 combined features. Fractions were computed as
`V_i / sum_j(V_j)` over the nine annotated tissues. The legacy nonzero-MRI
denominator was retained only as an audit reference.

The public release keeps only aggregate JSON reports in this directory. Raw
images, masks, patient-level clinical rows, feature tables, and server logs
are excluded.

The ordinal CAS sensitivity analysis was executed on the remote server from the
same frozen three-cluster solution. The proportional-odds model converged in
the 396 complete training cases and 100 validation cases. Overall Wald p values
were 1.38e-06 and 0.0366; common ORs for cluster 2 versus cluster 0 were 4.27
(95% CI 2.45-7.44) and 4.40 (1.42-13.64). Threshold-specific fits at the
highest CAS categories were non-convergent because of sparse events, so this
analysis is reported as a sensitivity analysis and does not establish the
proportional-odds assumption.
