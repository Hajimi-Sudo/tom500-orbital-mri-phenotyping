#!/usr/bin/env python3
"""Recompute tissue fractions from the audited nine-tissue volumes.

The legacy feature table used nonzero MRI intensity voxels as denominator.
This correction retains the audited physical volumes and recomputes each
fraction as V_i / sum_j(V_j) for the nine annotated structures.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_ROOT = PROJECT_ROOT / "analysis"
LEGACY = ANALYSIS_ROOT / "legacy_nonzero_image_denominator" / "pilot_features.csv"
OUT = ANALYSIS_ROOT / "pilot_features.csv"
AUDIT = ANALYSIS_ROOT / "fraction_denominator_audit.json"
TISSUES = ["SR", "LR", "MR", "IR", "ON", "FAT", "LG", "SO", "EB"]


def main() -> None:
    frame = pd.read_csv(LEGACY)
    volume_columns = [f"{t}_volume_mm3" for t in TISSUES]
    fraction_columns = [f"{t}_fraction" for t in TISSUES]
    denominator = frame[volume_columns].sum(axis=1)
    if (denominator <= 0).any() or not np.isfinite(denominator).all():
        raise ValueError("Non-positive or non-finite annotated tissue volume detected")

    old_sum = frame[fraction_columns].sum(axis=1)
    for tissue in TISSUES:
        frame[f"{tissue}_fraction"] = frame[f"{tissue}_volume_mm3"] / denominator
    new_sum = frame[fraction_columns].sum(axis=1)
    if not np.allclose(new_sum.to_numpy(), 1.0, atol=1e-12):
        raise AssertionError("Corrected fractions do not sum to one")
    expected = frame[volume_columns].div(denominator, axis=0)
    max_abs_formula_error = float(
        np.max(np.abs(frame[fraction_columns].to_numpy() - expected.to_numpy()))
    )

    frame.to_csv(OUT, index=False)
    report = {
        "formula": "fraction_i = V_i / sum_j(V_j), j in nine annotated tissues",
        "legacy_formula": "fraction_i = tissue_voxels_i / nonzero_MRI_intensity_voxels",
        "legacy_status": "audit_only_not_used_for_final_analysis",
        "corrected_status": "used_for_clustering_sensitivity_and_association_results",
        "source_feature_table": str(LEGACY),
        "output_feature_table": str(OUT),
        "n_cases": int(len(frame)),
        "old_fraction_sum": {
            "min": float(old_sum.min()),
            "median": float(old_sum.median()),
            "max": float(old_sum.max()),
        },
        "new_fraction_sum": {
            "min": float(new_sum.min()),
            "median": float(new_sum.median()),
            "max": float(new_sum.max()),
        },
        "max_abs_formula_error": max_abs_formula_error,
        "physical_volume_columns": volume_columns,
    }
    AUDIT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
