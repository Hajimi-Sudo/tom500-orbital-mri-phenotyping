# Volume-led multi-tissue orbital MRI phenotyping of thyroid-associated ophthalmopathy and exploratory association with CAS

## Article route

Original Research candidate for *Frontiers in Endocrinology*, Thyroid
Endocrinology. This is an actual-result exploratory observational draft. It is
not submission-ready until the reference pool, dataset documentation citation,
ethics/data-use wording, and journal-specific reporting requirements are
completed.

## Abstract

### Background

Thyroid-associated ophthalmopathy (TAO) shows heterogeneous involvement of the
extraocular muscles and other orbital tissues. Clinical Activity Score (CAS) is
useful for clinical characterization, but a compact patient-level description
of coordinated orbital tissue involvement remains underexplored. [CITATION
NEEDED: TAO activity assessment and imaging heterogeneity]

### Objective

To determine whether patient-level orbital MRI tissue-volume features identify
reproducible imaging phenotypes in a public TAO cohort and to characterize their
association with CAS and available clinical covariates.

### Methods

We analyzed 500 cases from the TOM500 public orbital MRI dataset. Nine annotated
orbital structures were converted to physical volume and volume-fraction
features using image-specific voxel spacing. A fixed 400-case training
partition was used to fit a three-cluster K-means phenotype, and the frozen
centroids were assigned to a 100-case validation partition. Stability was
assessed by bootstrap adjusted Rand index (ARI), and sensitivity analyses
examined scaling, feature family, and tissue deletion. CAS was compared across
clusters before and after adjustment for age, sex, smoking index, and disease
duration.

### Results

All 500 image-mask pairs loaded successfully and matched the clinical table.
The volume-led three-cluster solution had a training bootstrap ARI of 0.862 +/-
0.103 from 1,000 bootstrap resamples and showed an unadjusted CAS association in both the training partition
(Kruskal-Wallis p=2.27e-09) and validation partition (p=4.01e-04). Removing any
one tissue retained moderate-to-high similarity to the primary solution (ARI
0.653-0.925), whereas single-tissue solutions did not reproduce it (ARI
0.036-0.316). The clusters were also associated with age, sex, and smoking
index. After covariate adjustment, continuous CAS showed support in training
(p=2.09e-07), but adjusted validation evidence was not consistent across
endpoints: the continuous model showed only nominal overall support (p=0.0495),
whereas the CAS >= 3 endpoint was not supported (p=0.543). An ordinal
sensitivity model was directionally consistent but was limited by sparse
high-CAS thresholds.

### Conclusions

TOM500 supports a reproducible, volume-led multi-tissue orbital MRI phenotype
that provides an exploratory description of TAO imaging heterogeneity and an
unadjusted CAS gradient. The absence of adjusted replication in the validation
partition and the lack of biochemical or external-cohort data preclude claims
of an independently validated activity biomarker, treatment-selection tool, or
autoimmune mechanism.

## Introduction

Thyroid-associated ophthalmopathy is a clinically heterogeneous manifestation
of thyroid-associated orbital disease in which the relative involvement of
extraocular muscles, orbital fat, and other orbital structures varies between
patients. Clinical activity assessment is central to treatment planning, but
the clinical score compresses a spatially distributed orbital process into a
small number of clinical findings. [CITATION NEEDED: endocrine and ophthalmic
background]

Orbital MRI provides quantitative information about tissue morphology and signal
characteristics. Prior imaging studies have examined disease activity,
treatment response, or automated segmentation, but these aims do not directly
answer whether multi-tissue orbital morphology forms stable patient-level
phenotypes. [CITATION NEEDED: TAO MRI/radiomics literature; use verified DOI
records before submission]

An unsupervised phenotype analysis is attractive only if it is evaluated as a
reproducibility problem rather than as a cluster-separation exercise. A useful
analysis should therefore test whether the solution is stable to resampling,
feature representation, scaling, and removal of individual tissues. It should
also distinguish an imaging association with CAS from an independently
validated activity marker, particularly when age, sex, smoking, and acquisition
characteristics may be imbalanced across clusters.

We performed a patient-level analysis of TOM500, a public orbital MRI dataset
with nine tissue masks and an accompanying clinical table. We prespecified a
volume-led phenotype as the primary representation, used a fixed training and
validation partition, and treated CAS as a secondary clinical-characterization
endpoint. The primary question was whether a reproducible multi-tissue orbital
MRI phenotype could be identified; the secondary question was whether its CAS
association remained supported after accounting for available covariates.

## Materials and Methods

### Study design and data source

This retrospective public-dataset analysis used TOM500, a 500-case orbital MRI
dataset with nine annotated orbital structures. The data source and companion
clinical table were verified before analysis. The verified clinical variables
were age, sex, smoking index, disease duration, and CAS. TSH, FT4, TRAb, and
proptosis were not available in the analyzed clinical table and were therefore
outside the study scope.

The dataset supplied a fixed 400-case training partition and 100-case validation
partition. All analysis units were patients/cases; no bilateral-eye unit was
treated as an independent observation. The two partitions had no overlapping
case IDs.

### Image and mask audit

Each image was paired with the mask sharing its case ID. Image and mask shapes,
affines, finite intensity values, voxel spacing, and mask labels were checked.
All 500 image-mask pairs had shape 512 x 512 x 20. Mask values 0 through 9
occurred in every case, including the nine annotated tissue labels. The modal
voxel spacing was 0.3125 x 0.3125 x 3.85 mm in 467 of 500 cases; the remaining
cases showed small spacing deviations. Volumes were computed using each image's
voxel spacing rather than a single global spacing.

### Feature construction

For each annotated tissue, we calculated physical volume in mm3 and the tissue
fraction as each tissue's physical volume divided by the sum of the nine
annotated tissue volumes. The primary volume-led feature family therefore
contained 18 variables: 9 physical volumes and 9 compositional fractions whose
sum was one for each case.
For each tissue, the sensitivity intensity representation added the within-mask
mean, standard deviation, and 90th percentile of the image after within-scan
median/IQR standardization over finite, nonzero MRI voxels, with image-wide SD
as a fallback when the IQR was non-positive. This yielded 27 intensity
features (9 tissues x 3 summaries), and the combined sensitivity representation
therefore contained 45 features (18 volume-led + 27 intensity). For every
feature family, missing values were filled with column-wise training-partition
medians, and the imputed training matrix was standardized with a scaler fitted
on the training partition; the same values and scaler were applied unchanged
to validation cases.

### Phenotype fitting and validation assignment

Features were imputed using training-set medians and standardized using
training-set parameters. K-means models with 2 through 5 clusters were
evaluated in the exploratory pilot. The primary solution was the three-cluster
volume-led model selected by ranking mean bootstrap ARI first, with silhouette
used only as a secondary criterion for an exact bootstrap-ARI tie.
The model was fitted only in the training partition. Validation cases were
assigned to the nearest frozen training centroid and were not re-clustered.
Silhouette was calculated on the complete standardized training matrix and its
K-means labels. Bootstrap ARI compared reference labels with bootstrap K-means
labels on resampled training rows, while sensitivity ARI compared alternative
labels with the primary labels on the same training cases.

### Stability and sensitivity analyses

Bootstrap stability was summarized with the adjusted Rand index between the
reference labels and labels from 1,000 bootstrap resamples. Sensitivity analyses
compared standard scaling with robust scaling, physical-volume-only features,
fraction-only features, and the combined 45-feature representation. To assess
whether a single tissue drove the phenotype, we repeated clustering after
removing each tissue and separately fitted three-cluster models using each
tissue alone.

### Clinical association analysis

CAS was analyzed as a continuous score and as an exploratory binary endpoint
defined as CAS >= 3. Cluster differences in continuous variables were assessed
with Kruskal-Wallis tests. Sex distributions were compared descriptively and
with a chi-square test. Covariate-adjusted associations were estimated with
heteroskedasticity-robust linear regression for continuous CAS and robust
binomial logistic regression for CAS >= 3. Covariates were age, sex, smoking
index, and disease duration. The validation partition was treated as a fixed
internal validation partition, not as an external cohort.

As a sensitivity analysis, CAS was also modeled with proportional-odds ordinal
logistic regression using the same covariates and frozen cluster assignments.
Threshold-specific binary logistic fits were inspected descriptively to assess
the proportional-odds assumption. Because the highest CAS thresholds were
sparse, this was treated as a sensitivity check rather than a definitive formal
assumption test.

### Reproducibility and claim boundary

All reported numerical results were generated by server-run analyses archived
locally as evidence files. The analysis was exploratory and did
not evaluate clinical utility, treatment response, prospective deployment, or
causal mechanisms. No multiple-model claim was promoted beyond the prespecified
volume-led phenotype and its sensitivity analyses.

## Results

### Cohort and data integrity

The analyzed cohort contained 500 cases, with 400 cases in training and 100 in
validation. All image-mask pairs passed the loading and shape/affine checks, and
all 500 case IDs matched the clinical table. The CAS distribution was 0:171,
1:128, 2:80, 3:67, 4:33, 5:17, and 6:4. The primary analysis therefore used a
continuous CAS endpoint and the prespecified exploratory CAS >= 3 threshold,
which corresponded to 121/500 cases overall.

### Reproducible volume-led phenotype

The volume-led three-cluster solution had 148, 164, and 88 training cases in
the three clusters, and 38, 35, and 27 validation cases after frozen-centroid
assignment. Its training silhouette was 0.188 and bootstrap ARI was 0.862 +/-
0.103. The two-cluster alternative had a higher silhouette (0.272) and a
slightly lower bootstrap ARI (0.844), but was not selected because its
bootstrap stability was lower under the exploratory stability-first rule.

The solution showed moderate sensitivity to alternative scaling and feature
families. Standard scaling reproduced the primary labels by definition,
whereas robust scaling yielded a train-label ARI of 0.606; their bootstrap ARI
means were 0.872 and 0.808, respectively. Physical-volume-only and
fraction-only representations had ARI values of 0.520 and 0.761 relative to
the primary solution. The combined volume-intensity solution was less similar
(ARI 0.270) and had a lower silhouette, so it was retained only as a
sensitivity analysis.

### Multi-tissue sensitivity

Removing any one tissue retained moderate-to-high similarity to the primary
volume-led solution, with ARI values from 0.653 after removal of fat to 0.925
after removal of lacrimal gland. In contrast, single-tissue solutions had low
similarity to the multi-tissue solution, with ARI values from 0.036 to 0.316.
These results support a coordinated multi-tissue representation, while not
establishing biological independence or a tissue-specific mechanism.

### CAS and clinical characterization

In the training partition, median CAS values were 1, 1, and 2 across the three
clusters, and the unadjusted CAS association was significant (Kruskal-Wallis
p=2.27e-09). In the validation partition, median CAS values were 0, 1, and 2,
with an unadjusted association that remained significant (p=4.01e-04). The
corresponding CAS >= 3 rates were 9.5%, 23.8%, and 48.9% in training and 10.5%,
28.6%, and 40.7% in validation.

The clusters were associated with age in training (p=1.21e-15) and validation
(p=7.72e-06), smoking index in training (p=0.00102) and validation
(p=0.000851), and sex in training (chi-square p=2.24e-09) and validation
(p=0.000139). Disease duration did not differ clearly between clusters in
either partition.

Table 1 reports the smoking index and disease duration medians because both
variables were included in the adjusted models.

### Covariate-adjusted associations

After adjustment for age, sex, smoking index, and disease duration, the overall
training-set association with continuous CAS remained supported (Wald p=2.09e-07).
Relative to cluster 0, adjusted CAS differences were 0.37 (95% CI 0.08-0.67)
for cluster 1 and 1.19 (95% CI 0.77-1.61) for cluster 2. The corresponding
CAS >= 3 odds ratios were 2.42 (95% CI 1.20-4.87) and 6.55 (95% CI 3.11-13.79),
with an overall Wald p=2.09e-06.

The adjusted continuous-CAS association showed only nominal overall support in
the validation partition (p=0.0495), whereas the CAS >= 3 endpoint was not
supported (p=0.543). The validation estimates were directionally positive but
imprecise, and the adjusted findings were not consistent across endpoints.
These results limit the interpretation to exploratory internal evidence.

In the ordinal sensitivity analysis, the proportional-odds model converged in
both partitions. Relative to cluster 0, common odds ratios were 1.51 (95% CI
0.98-2.32; p=0.063) and 4.27 (95% CI 2.45-7.44; p=2.93e-07) for clusters 1
and 2 in training, with an overall Wald p=1.38e-06. In validation, the
corresponding estimates were 2.22 (95% CI 0.84-5.88; p=0.107) and 4.40 (95% CI
1.42-13.64; p=0.010), with an overall Wald p=0.0366. The highest threshold
models were non-convergent because of sparse events, so the proportional-odds
assumption was not considered definitively verified. This sensitivity analysis
does not replace the continuous and binary primary results.

## Discussion

This study identified a stable, volume-led multi-tissue orbital MRI phenotype
in the public TOM500 cohort. The main result is methodological and descriptive:
the patient-level organization of nine orbital tissue volumes was reproducible
under resampling, scaling changes, and tissue deletion, while single-tissue
solutions did not reproduce the multi-tissue organization. This supports the
use of a coordinated tissue representation when describing TAO imaging
heterogeneity.

The unadjusted phenotype-CAS gradient was present in both the training and
validation partitions. However, the clinical interpretation is constrained by
the observed imbalance in age, sex, and smoking index. Covariate adjustment
supported the association in training, but the adjusted validation findings
were not consistent across the continuous and binary endpoints. The ordinal
sensitivity analysis was directionally consistent but was limited by sparse
high-CAS thresholds. The appropriate interpretation is therefore that the
imaging phenotype showed an exploratory association with CAS, not that it is a
consistently replicated or independently validated activity marker.

The result has a narrower endocrine-imaging implication. A quantitative orbital
phenotype may provide a useful research representation for studying how tissue
involvement relates to clinical activity assessment. It does not replace CAS,
does not establish a treatment threshold, and cannot be linked to thyroid
autoantibody levels, hormone levels, or autoimmune mechanisms in the present
dataset because TRAb, TSH, and FT4 were unavailable and no mechanistic
measurements were analyzed.

The negative findings are important. Intensity-only clustering did not show a
CAS association, the combined volume-intensity representation was less similar
to the primary phenotype, and the adjusted validation association was null.
Together, these findings argue against adding a large texture-radiomics panel
without a larger independent cohort and a prespecified incremental-value
question.

## Limitations

First, the analysis used a single public cohort and lacked an independent
external cohort. The 100-case partition was a fixed internal validation
partition, not external validation. Second, the available clinical table did
not contain TSH, FT4, TRAb, proptosis, treatment exposure, or treatment response;
therefore, endocrine biochemical and therapeutic claims were not possible.
Third, age, sex, and smoking index differed across clusters, and adjusted
validation did not replicate the training association. Fourth, voxel spacing
was mildly heterogeneous, although image-specific physical volumes were used.
Fifth, the primary analysis intentionally used a restrained low-dimensional
feature set; the findings do not establish the value of texture radiomics.
Finally, the retrospective design and public-data provenance limit causal and
clinical-utility interpretations.

## Conclusion

Patient-level orbital MRI volume features identified a reproducible,
multi-tissue phenotype in TOM500 and showed an exploratory unadjusted gradient
across CAS. Because adjusted association was not supported in the validation
partition and biochemical/external validation data were unavailable, the
phenotype should be regarded as hypothesis-generating rather than as a
validated activity biomarker or treatment-selection tool.

## Evidence and citation notes

- Dataset identity and linkage: `DATA_VERIFICATION.md`,
  `../analysis/server_results/bootstrap1000/feature_audit.json`.
- Stability and sensitivity: `PILOT_AUDIT.md`,
  `../analysis/server_results/bootstrap1000/next_gate_report.json`,
  `NEXT_GATE_AUDIT.md`.
- Adjusted associations: `../analysis/server_results/corrected_v2/adjusted_association.json`.
- Dataset paper candidate: DOI `10.1038/s41597-025-04427-9`.
- Target-section scope record: `FRONTIER_ATTENTION_EVIDENCE.md`.
- All `[CITATION NEEDED]` markers must be resolved through a DOI-verified
  literature pool before submission-facing drafting.
