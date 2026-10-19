# Analysis artifacts

This directory contains aggregate audit reports and frozen summary outputs
from the remote server analyses used for the manuscript.

The public release does not include raw MRI files, masks, patient-level
clinical rows, or patient-level feature tables. The expected clinical input
schema is documented in `clinical_characteristics.template.csv`. A local
analysis run must provide the corresponding authorized TOM500 clinical table
and the raw data root separately.

The `server_results/bootstrap1000/` directory contains the canonical aggregate
stability results used in the manuscript. The `server_results/corrected_v2/`
directory contains the aggregate adjusted-association and ordinal CAS
sensitivity outputs.
