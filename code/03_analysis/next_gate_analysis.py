#!/usr/bin/env python3
"""Second-gate audit for the TOM500 multi-tissue phenotype pilot.

The script consumes the frozen low-dimensional pilot features and clinical
table. It keeps the train/validation split fixed, fits transformations on the
train set only, and reports covariate associations plus sensitivity analyses.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, kruskal
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import RobustScaler, StandardScaler


TISSUES = ["SR", "LR", "MR", "IR", "ON", "FAT", "LG", "SO", "EB"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--features", type=Path, required=True)
    p.add_argument("--clinical", type=Path, required=True)
    p.add_argument("--audit", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--bootstrap", type=int, default=200)
    p.add_argument("--seed", type=int, default=20261019)
    return p.parse_args()


def feature_groups(columns: list[str]) -> dict[str, list[str]]:
    return {
        "volume": [c for c in columns if c.endswith("_volume_mm3") or c.endswith("_fraction")],
        "volume_mm3_only": [c for c in columns if c.endswith("_volume_mm3")],
        "fraction_only": [c for c in columns if c.endswith("_fraction")],
        "intensity": [c for c in columns if "_intensity_" in c],
        "combined": [c for c in columns if c.endswith("_volume_mm3") or c.endswith("_fraction") or "_intensity_" in c],
    }


def fit_solution(train: pd.DataFrame, val: pd.DataFrame, columns: list[str], scaler_name: str, seed: int, k: int = 3) -> dict[str, object]:
    x_train = train[columns].astype(float).copy()
    x_val = val[columns].astype(float).copy()
    medians = x_train.median()
    x_train = x_train.fillna(medians)
    x_val = x_val.fillna(medians)
    scaler = StandardScaler() if scaler_name == "standard" else RobustScaler()
    z_train = scaler.fit_transform(x_train)
    z_val = scaler.transform(x_val)
    model = KMeans(n_clusters=k, n_init=50, random_state=seed)
    labels = model.fit_predict(z_train)
    val_labels = model.predict(z_val)
    return {
        "train_labels": labels,
        "val_labels": val_labels,
        "train_centers": model.cluster_centers_.tolist(),
        "train_silhouette": float(silhouette_score(z_train, labels)),
        "train_counts": {str(i): int((labels == i).sum()) for i in range(k)},
        "val_counts": {str(i): int((val_labels == i).sum()) for i in range(k)},
    }


def bootstrap_ari(train: pd.DataFrame, columns: list[str], scaler_name: str, seed: int, n_boot: int) -> dict[str, float]:
    x = train[columns].astype(float).copy()
    x = x.fillna(x.median())
    scaler = StandardScaler() if scaler_name == "standard" else RobustScaler()
    z = scaler.fit_transform(x)
    ref = KMeans(n_clusters=3, n_init=50, random_state=seed).fit_predict(z)
    rng = np.random.default_rng(seed + 1000)
    aris = []
    for b in range(n_boot):
        idx = rng.integers(0, len(z), len(z))
        boot = KMeans(n_clusters=3, n_init=20, random_state=seed + b + 1).fit_predict(z[idx])
        aris.append(adjusted_rand_score(ref[idx], boot))
    return {"mean": float(np.mean(aris)), "sd": float(np.std(aris)), "q025": float(np.quantile(aris, 0.025)), "q975": float(np.quantile(aris, 0.975))}


def cas_summary(frame: pd.DataFrame, labels: np.ndarray, clinical: pd.DataFrame) -> dict[str, object]:
    joined = frame[["case_id"]].copy()
    joined["cluster"] = labels
    merged = joined.merge(clinical, on="case_id", how="left", validate="one_to_one")
    cas_groups = [merged.loc[merged.cluster == c, "CAS"].astype(float).to_numpy() for c in sorted(merged.cluster.unique())]
    stat, p = kruskal(*cas_groups)
    active = merged["CAS"].astype(float) >= 3
    rates = {str(c): float(active[merged.cluster == c].mean()) for c in sorted(merged.cluster.unique())}
    return {"join_missing": int(merged.CAS.isna().sum()), "kruskal": {"statistic": float(stat), "p": float(p)}, "cas_medians": {str(c): float(np.median(g)) for c, g in zip(sorted(merged.cluster.unique()), cas_groups)}, "active_rate_cas_ge_3": rates, "active_count": int(active.sum())}


def bootstrap_median_difference(values: np.ndarray, labels: np.ndarray, a: int, b: int, seed: int, n: int = 2000) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    x = values[labels == a]
    y = values[labels == b]
    observed = float(np.median(x) - np.median(y))
    diffs = []
    for _ in range(n):
        diffs.append(float(np.median(rng.choice(x, len(x), replace=True)) - np.median(rng.choice(y, len(y), replace=True))))
    return {"median_difference_a_minus_b": observed, "ci95_low": float(np.quantile(diffs, 0.025)), "ci95_high": float(np.quantile(diffs, 0.975))}


def clinical_associations(frame: pd.DataFrame, labels: np.ndarray, clinical: pd.DataFrame, seed: int) -> dict[str, object]:
    merged = frame[["case_id"]].copy()
    merged["cluster"] = labels
    merged = merged.merge(clinical, on="case_id", how="left", validate="one_to_one")
    result: dict[str, object] = {"join_missing": int(merged.CAS.isna().sum()), "continuous": {}, "categorical": {}}
    for column in ["CAS", "Age", "SmokingIndex", "DiseaseDuration"]:
        groups = [merged.loc[merged.cluster == c, column].astype(float).dropna().to_numpy() for c in sorted(merged.cluster.unique())]
        stat, p = kruskal(*groups)
        result["continuous"][column] = {"kruskal_statistic": float(stat), "p": float(p), "medians": {str(c): float(np.median(g)) for c, g in zip(sorted(merged.cluster.unique()), groups)}}
        if len(groups) == 2:
            result["continuous"][column]["median_difference_ci95_cluster0_minus_cluster1"] = bootstrap_median_difference(merged[column].astype(float).to_numpy(), merged.cluster.to_numpy(), 0, 1, seed + len(column))
    table = pd.crosstab(merged.cluster, merged["Sex"])
    chi2, p, dof, _ = chi2_contingency(table)
    result["categorical"]["Sex"] = {"chi2": float(chi2), "dof": int(dof), "p": float(p), "table": table.to_dict()}
    return result


def tissue_sensitivity(train: pd.DataFrame, val: pd.DataFrame, base_labels: np.ndarray, groups: dict[str, list[str]], seed: int) -> dict[str, object]:
    result: dict[str, object] = {"leave_one_tissue": {}, "single_tissue": {}}
    for tissue in TISSUES:
        cols = [c for c in groups["volume"] if not c.startswith(tissue + "_")]
        sol = fit_solution(train, val, cols, "standard", seed, 3)
        result["leave_one_tissue"][tissue] = {"ari_to_base": float(adjusted_rand_score(base_labels, sol["train_labels"])), "silhouette": sol["train_silhouette"], "train_counts": sol["train_counts"]}
        single = [c for c in groups["volume"] if c.startswith(tissue + "_")]
        sol_single = fit_solution(train, val, single, "standard", seed, 3)
        result["single_tissue"][tissue] = {"ari_to_base": float(adjusted_rand_score(base_labels, sol_single["train_labels"])), "silhouette": sol_single["train_silhouette"], "train_counts": sol_single["train_counts"]}
    return result


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    features = pd.read_csv(args.features)
    clinical = pd.read_csv(args.clinical)
    features["case_id"] = features["case_id"].astype(str)
    clinical["case_id"] = clinical["Id"].str.split("_").str[0]
    split = {s: set(features.loc[features.split == s, "case_id"]) for s in ["train", "val"]}
    train = features[features.split == "train"].copy()
    val = features[features.split == "val"].copy()
    groups = feature_groups(features.columns.tolist())
    base = fit_solution(train, val, groups["volume"], "standard", args.seed, 3)
    report: dict[str, object] = {"dataset": {"n": len(features), "n_train": len(train), "n_val": len(val), "split_overlap": len(split["train"] & split["val"])}, "feature_counts": {k: len(v) for k, v in groups.items()}, "base_volume_solution": {k: v for k, v in base.items() if k not in ["train_labels", "val_labels"]}, "base_cas": {"train": cas_summary(train, base["train_labels"], clinical), "val": cas_summary(val, base["val_labels"], clinical)}, "base_clinical": {"train": clinical_associations(train, base["train_labels"], clinical, args.seed), "val": clinical_associations(val, base["val_labels"], clinical, args.seed + 1)}, "scaling_sensitivity": {}, "feature_family_sensitivity": {}, "tissue_sensitivity": {}}
    report["feature_schema"] = {
        "primary_volume_led": "9 physical volumes + 9 compositional fractions = 18 features",
        "intensity_sensitivity": "9 tissues x {mean, SD, p90} after within-scan median/IQR standardization = 27 features",
        "combined_sensitivity": "18 volume-led + 27 intensity = 45 features",
        "missing_value_handling": "training-partition column medians",
        "scaling": "StandardScaler or RobustScaler fit on training partition and applied unchanged to validation",
    }
    report["cluster_metric_definitions"] = {
        "train_silhouette": "silhouette_score on the full standardized training matrix and fitted labels",
        "ari_to_primary": "adjusted Rand index between primary and sensitivity labels on the same training cases",
        "bootstrap_ari": "adjusted Rand index between reference labels and bootstrap K-means labels on resampled training rows",
    }
    for scaler in ["standard", "robust"]:
        sol = fit_solution(train, val, groups["volume"], scaler, args.seed, 3)
        report["scaling_sensitivity"][scaler] = {"ari_to_base": float(adjusted_rand_score(base["train_labels"], sol["train_labels"])), "train_silhouette": sol["train_silhouette"], "val_cas": cas_summary(val, sol["val_labels"], clinical), "bootstrap_ari": bootstrap_ari(train, groups["volume"], scaler, args.seed, args.bootstrap)}
    for family in ["volume_mm3_only", "fraction_only", "combined"]:
        sol = fit_solution(train, val, groups[family], "standard", args.seed, 3)
        report["feature_family_sensitivity"][family] = {"ari_to_base": float(adjusted_rand_score(base["train_labels"], sol["train_labels"])), "train_silhouette": sol["train_silhouette"], "val_cas": cas_summary(val, sol["val_labels"], clinical), "bootstrap_ari": bootstrap_ari(train, groups[family], "standard", args.seed, args.bootstrap)}
    report["tissue_sensitivity"] = tissue_sensitivity(train, val, base["train_labels"], groups, args.seed)
    report["audit_metadata"] = json.loads(args.audit.read_text())
    report["interpretation"] = {"primary": "volume-led multi-tissue phenotype", "texture_status": "not tested in this gate", "mechanistic_claim": "not supported", "clinical_utility": "not assessed"}
    (args.out_dir / "next_gate_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
