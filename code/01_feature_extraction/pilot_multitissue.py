#!/usr/bin/env python3
"""Low-dimensional TOM500 multi-tissue phenotype pilot.

This pilot deliberately uses volume, volume fraction, and within-scan
standardized intensity summaries. Texture radiomics are reserved for a later
stage after the image/mask contract and cluster signal are verified.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kruskal, spearmanr
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler


LABELS = {1: "SR", 2: "LR", 3: "MR", 4: "IR", 5: "ON", 6: "FAT", 7: "LG", 8: "SO", 9: "EB"}
INTENSITY_SUMMARIES = ["intensity_mean", "intensity_sd", "intensity_p90"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--data-root", type=Path)
    p.add_argument("--clinical", type=Path, required=True)
    p.add_argument("--split", type=Path)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--features-in", type=Path, help="Reuse a previously audited feature table when raw NIfTI files are unavailable.")
    p.add_argument("--audit-in", type=Path, help="Audit JSON paired with --features-in.")
    p.add_argument("--bootstrap", type=int, default=200)
    p.add_argument("--seed", type=int, default=20261019)
    return p.parse_args()


def load_case(image_path: Path, mask_path: Path) -> tuple[dict[str, float], dict[str, object]]:
    try:
        import nibabel as nib
    except ModuleNotFoundError as exc:
        raise RuntimeError("nibabel is required only when extracting directly from NIfTI files") from exc
    image = nib.load(str(image_path))
    mask = nib.load(str(mask_path))
    image_shape = tuple(int(x) for x in image.shape)
    mask_shape = tuple(int(x) for x in mask.shape)
    if image_shape != mask_shape:
        raise ValueError(f"shape mismatch: {image_path.name} {image_shape} vs {mask_shape}")
    if not np.allclose(image.affine, mask.affine, atol=1e-3):
        raise ValueError(f"affine mismatch: {image_path.name}")

    image_arr = np.asarray(image.get_fdata(dtype=np.float32))
    mask_arr = np.asarray(mask.get_fdata(dtype=np.float32))
    finite = np.isfinite(image_arr)
    nonzero = finite & (image_arr != 0)
    if not nonzero.any():
        raise ValueError(f"empty image: {image_path.name}")
    values = image_arr[nonzero]
    center = float(np.median(values))
    scale = float(np.subtract(*np.percentile(values, [75, 25])))
    if not math.isfinite(scale) or scale <= 1e-6:
        scale = float(np.std(values))
    if not math.isfinite(scale) or scale <= 1e-6:
        raise ValueError(f"constant image: {image_path.name}")
    image_z = (image_arr - center) / scale

    spacing = np.asarray(image.header.get_zooms()[:3], dtype=float)
    if spacing.size != 3 or not np.all(np.isfinite(spacing)) or np.any(spacing <= 0):
        raise ValueError(f"invalid spacing: {image_path.name}: {spacing}")
    voxel_volume = float(np.prod(spacing))
    present = set(int(x) for x in np.unique(mask_arr) if int(x) in LABELS)
    features: dict[str, float] = {}
    # Tissue fractions are compositional: each tissue is divided by the total
    # volume of the nine annotated structures, not by the nonzero MRI field.
    tissue_counts = {
        name: int(((mask_arr == label_id) & finite).sum())
        for label_id, name in LABELS.items()
    }
    total_annotated_voxels = float(sum(tissue_counts.values()))
    for label_id, name in LABELS.items():
        region = (mask_arr == label_id) & finite
        count = tissue_counts[name]
        features[f"{name}_volume_mm3"] = count * voxel_volume
        features[f"{name}_fraction"] = count / total_annotated_voxels if total_annotated_voxels else 0.0
        if count:
            region_values = image_z[region]
            features[f"{name}_intensity_mean"] = float(np.mean(region_values))
            features[f"{name}_intensity_sd"] = float(np.std(region_values))
            features[f"{name}_intensity_p90"] = float(np.percentile(region_values, 90))
        else:
            features[f"{name}_intensity_mean"] = np.nan
            features[f"{name}_intensity_sd"] = np.nan
            features[f"{name}_intensity_p90"] = np.nan
    meta = {
        "image_shape": image_shape,
        "spacing_mm": spacing.tolist(),
        "voxel_volume_mm3": voxel_volume,
        "annotated_tissue_voxels": int(total_annotated_voxels),
        "annotated_tissue_volume_mm3": total_annotated_voxels * voxel_volume,
        "fraction_sum": float(sum(features[f"{name}_fraction"] for name in LABELS.values())),
        "present_labels": sorted(present),
        "mask_unique_values": sorted(int(x) for x in np.unique(mask_arr)),
    }
    return features, meta


def extract_features(args: argparse.Namespace) -> tuple[pd.DataFrame, dict[str, object]]:
    rows: list[dict[str, object]] = []
    audit = {"cases": 0, "errors": [], "shape_counts": {}, "spacing_counts": {}, "mask_value_counts": {}}
    for split in ("train", "val"):
        image_dir = args.data_root / split / "image"
        mask_dir = args.data_root / split / "label"
        image_paths = sorted(image_dir.glob("*.nii.gz"), key=lambda p: int(p.stem.split(".")[0]))
        for image_path in image_paths:
            case_id = image_path.name.removesuffix(".nii.gz")
            mask_path = mask_dir / image_path.name
            row: dict[str, object] = {"case_id": case_id, "split": split}
            try:
                features, meta = load_case(image_path, mask_path)
                row.update(features)
                for key, value in (("shape_counts", str(meta["image_shape"])), ("spacing_counts", str(tuple(round(x, 5) for x in meta["spacing_mm"])))):
                    audit[key][value] = audit[key].get(value, 0) + 1
                for value in meta["mask_unique_values"]:
                    key = str(value)
                    audit["mask_value_counts"][key] = audit["mask_value_counts"].get(key, 0) + 1
            except Exception as exc:  # preserve case-level audit instead of hiding failures
                row["case_error"] = str(exc)
                audit["errors"].append({"case_id": case_id, "split": split, "error": str(exc)})
            rows.append(row)
            audit["cases"] += 1
    return pd.DataFrame(rows), audit


def feature_columns(frame: pd.DataFrame) -> tuple[list[str], list[str], list[str]]:
    volume = [c for c in frame if c.endswith("_volume_mm3") or c.endswith("_fraction")]
    intensity = [c for c in frame if c.endswith("_intensity_mean") or c.endswith("_intensity_sd") or c.endswith("_intensity_p90")]
    return volume, intensity, volume + intensity


def feature_schema() -> dict[str, object]:
    return {
        "tissues": list(LABELS.values()),
        "primary_volume_led": {
            "count": 18,
            "per_tissue": ["volume_mm3", "fraction"],
            "formula": "9 tissue physical volumes + 9 compositional fractions",
        },
        "intensity_sensitivity": {
            "count": 27,
            "per_tissue": INTENSITY_SUMMARIES,
            "formula": "9 tissues x 3 within-mask standardized intensity summaries",
            "normalization": "within-scan median center and IQR scale over finite nonzero MRI voxels; SD fallback when IQR is non-positive",
        },
        "combined_sensitivity": {
            "count": 45,
            "formula": "18 primary volume-led features + 27 intensity features",
        },
        "missing_value_handling": "column-wise training-partition median imputation before scaling",
        "scaling": "StandardScaler fit on training partition and applied unchanged to validation partition",
    }


def fit_clusters(train: pd.DataFrame, val: pd.DataFrame, columns: list[str], bootstrap: int, seed: int) -> dict[str, object]:
    x_train = train[columns].astype(float).copy()
    x_val = val[columns].astype(float).copy()
    medians = x_train.median()
    x_train = x_train.fillna(medians)
    x_val = x_val.fillna(medians)
    scaler = StandardScaler().fit(x_train)
    z_train = scaler.transform(x_train)
    z_val = scaler.transform(x_val)
    out: dict[str, object] = {"feature_count": len(columns), "features": columns, "candidates": {}}
    rng = np.random.default_rng(seed)
    for k in range(2, 6):
        model = KMeans(n_clusters=k, n_init=50, random_state=seed)
        labels = model.fit_predict(z_train)
        val_labels = model.predict(z_val)
        stability: list[float] = []
        for b in range(bootstrap):
            sample_idx = rng.integers(0, len(z_train), len(z_train))
            boot_model = KMeans(n_clusters=k, n_init=20, random_state=seed + b + 1)
            boot_labels = boot_model.fit_predict(z_train[sample_idx])
            stability.append(float(adjusted_rand_score(labels[sample_idx], boot_labels)))
        out["candidates"][str(k)] = {
            "silhouette_train": float(silhouette_score(z_train, labels)),
            "train_cluster_counts": {str(i): int((labels == i).sum()) for i in range(k)},
            "val_cluster_counts": {str(i): int((val_labels == i).sum()) for i in range(k)},
            "bootstrap_ari_mean": float(np.mean(stability)),
            "bootstrap_ari_sd": float(np.std(stability)),
            "train_labels": labels.tolist(),
            "val_labels": val_labels.tolist(),
            "centers": model.cluster_centers_.tolist(),
        }
    return out


def association(frame: pd.DataFrame, labels: np.ndarray, clinical: pd.DataFrame) -> dict[str, object]:
    joined = frame[["case_id"]].copy()
    joined["cluster"] = labels
    merged = joined.merge(clinical, on="case_id", how="left", validate="one_to_one")
    result: dict[str, object] = {"join_rows": int(len(merged)), "join_missing": int(merged["CAS"].isna().sum())}
    if result["join_missing"]:
        return result
    cas = merged["CAS"].astype(float)
    groups = [cas[merged["cluster"] == c].to_numpy() for c in sorted(merged["cluster"].unique())]
    if len(groups) >= 2:
        stat, p_value = kruskal(*groups)
        result["cas_kruskal"] = {"statistic": float(stat), "p": float(p_value), "group_medians": {str(c): float(np.median(g)) for c, g in zip(sorted(merged["cluster"].unique()), groups)}}
    merged["active_cas_ge_3"] = (cas >= 3).astype(int)
    result["active_cas_ge_3_count"] = int(merged["active_cas_ge_3"].sum())
    result["active_rate_by_cluster"] = {str(c): float(merged.loc[merged["cluster"] == c, "active_cas_ge_3"].mean()) for c in sorted(merged["cluster"].unique())}
    return result


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    clinical = pd.read_csv(args.clinical)
    clinical["case_id"] = clinical["Id"].str.split("_").str[0]
    if args.features_in:
        features = pd.read_csv(args.features_in)
        audit = json.loads(args.audit_in.read_text()) if args.audit_in else {"cases": len(features), "errors": []}
    else:
        if not args.data_root or not args.split:
            raise ValueError("--data-root and --split are required when --features-in is not used")
        features, audit = extract_features(args)
    features["case_id"] = features["case_id"].astype(str)
    features.to_csv(args.out_dir / "pilot_features.csv", index=False)
    with args.out_dir.joinpath("feature_audit.json").open("w") as f:
        json.dump(audit, f, indent=2)
    if args.split:
        split = json.loads(args.split.read_text())
    else:
        split = {
            "train": features.loc[features["split"] == "train", "case_id"].astype(str).tolist(),
            "val": features.loc[features["split"] == "val", "case_id"].astype(str).tolist(),
        }
    train = features[features["case_id"].isin(split["train"])].copy()
    val = features[features["case_id"].isin(split["val"])].copy()
    volume, intensity, combined = feature_columns(features)
    report = {
        "dataset": {"n_cases": int(len(features)), "n_train": int(len(train)), "n_val": int(len(val)), "n_errors": int(features.get("case_error", pd.Series(dtype=str)).notna().sum())},
        "feature_families": {"volume": len(volume), "intensity": len(intensity), "combined": len(combined)},
        "feature_schema": feature_schema(),
        "cluster_metric_definitions": {
            "silhouette": "silhouette_score on the full standardized training matrix and its fitted K-means labels",
            "bootstrap_ari": "adjusted Rand index between reference training labels and bootstrap K-means labels on the resampled training rows",
            "sensitivity_ari_to_primary": "adjusted Rand index between primary and sensitivity labels on the same training cases",
        },
        "clinical_fields": list(clinical.columns),
        "cas_distribution": {str(k): int(v) for k, v in clinical["CAS"].value_counts().sort_index().items()},
        "cluster_results": {},
    }
    train_ok = train[train.get("case_error", pd.Series(index=train.index, dtype=object)).isna()].copy()
    val_ok = val[val.get("case_error", pd.Series(index=val.index, dtype=object)).isna()].copy()
    for family, columns in (("volume", volume), ("intensity", intensity), ("combined", combined)):
        if len(train_ok) >= 10 and columns:
            result = fit_clusters(train_ok, val_ok, columns, args.bootstrap, args.seed)
            report["cluster_results"][family] = result
            best_k = max(result["candidates"], key=lambda k: (result["candidates"][k]["bootstrap_ari_mean"], result["candidates"][k]["silhouette_train"]))
            chosen = result["candidates"][best_k]
            report["cluster_results"][family]["chosen_k_by_stability_then_silhouette"] = int(best_k)
            report["cluster_results"][family]["chosen_train_cas_association"] = association(train_ok, np.asarray(chosen["train_labels"]), clinical)
            report["cluster_results"][family]["chosen_val_cas_association"] = association(val_ok, np.asarray(chosen["val_labels"]), clinical)
    with args.out_dir.joinpath("pilot_report.json").open("w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
