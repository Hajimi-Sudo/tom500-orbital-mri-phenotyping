# Data Verification

## Unresolved seed record

- User-supplied name: `Thyroid Eye Disease MRI Dataset`
- User-supplied DOI: `10.6084/m9.figshare.21764519`
- User-supplied cohort: 87 TAO patients
- User-supplied labels: CAS/activity, proptosis, TSH, FT4, TRAb, orbital masks
- Status: `unverified`

## Verification checklist

- [ ] Resolve the DOI or obtain the corrected Figshare URL.
- [ ] Confirm title, authors, release date, version, license, and file sizes.
- [ ] Enumerate image sequences and confirm whether T1/T2 contrast data exist.
- [ ] Enumerate mask labels and confirm whether masks are patient- or eye-level.
- [ ] Locate the clinical table and confirm one row per patient.
- [ ] Confirm CAS scale, activity threshold, timing relative to MRI, and missingness.
- [ ] Confirm TSH, FT4, TRAb units, assay timing, and missingness.
- [ ] Confirm proptosis measurement method and side/visit linkage.
- [ ] Confirm de-identification, reuse permissions, and citation requirements.
- [ ] Compute the final analyzable patient count before any model design.

## Known close match

TOM500 is a verified close match with DOI `10.6084/m9.figshare.27133389`. Its
published data description reports 500 cases of coronal T2WI and segmentations
of nine orbital structures, plus sex, age, disease duration, and smoking
status. It should not be substituted for the proposed activity cohort without
an explicit re-scoping decision.
