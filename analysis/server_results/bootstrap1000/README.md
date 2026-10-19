# Server evidence: bootstrap1000

The 1,000-resample bootstrap analyses were executed on the remote CPU server
using the audited TOM500 feature table, fixed 400/100 split, seed `20261019`,
and the same feature construction and clustering rules as the prior analysis.

Final bootstrap ARI values from `next_gate_report.json`:

- Standard volume-led features: mean 0.8621388525, SD 0.1026955181
- Robust scaling: mean 0.8065480380, SD 0.1637091068
- Physical volumes only: mean 0.8597217245, SD 0.1145816216
- Fractions only: mean 0.8608864599, SD 0.1098872363
- Combined 45-feature representation: mean 0.8473214337, SD 0.1047193587

The manuscript reports these values rounded to three decimals. This directory
is the canonical manuscript source for primary and sensitivity-family bootstrap
estimates under one 1,000-resample protocol. Patient-level feature tables and
case-level cluster labels are excluded from the public release.

For cluster-number selection, the exploratory implementation ranked the 2--5
cluster candidates by bootstrap ARI mean first and used training silhouette
only as a secondary key for an exact ARI tie. The 2-cluster candidate had
silhouette 0.272 and bootstrap ARI 0.844 (SD 0.118); the selected 3-cluster
candidate had silhouette 0.188 and bootstrap ARI 0.862 (SD 0.103). The 4- and
5-cluster candidates had bootstrap ARI means 0.531 and 0.544, respectively.

SHA256:

```text
073d9e6a9ddb9fb5e4d2b9b26e6e114bde526bc756bf07353d7301e5a44594c9  feature_audit.json
66252ef63b94bdcb89437a330e4c9cdd1505aee2d9b4e2507c4c987f6428ffb7  next_gate_report.json
6f6d17786f086b76308cc672b3b5c8c9ae76f398cf6da50a348956a7eb5a2e44  pilot_report.json
```
