#!/usr/bin/env python3
"""Render deterministic result figures and tables from frozen TOM500 outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from scipy.stats import beta


COLORS = {0: "#2F5D7E", 1: "#C76D3A", 2: "#5B8E7D"}
CLUSTER_NAMES = {0: "Cluster 0", 1: "Cluster 1", 2: "Cluster 2"}
TISSUES = ["SR", "LR", "MR", "IR", "ON", "FAT", "LG", "SO", "EB"]
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=PROJECT_ROOT / "analysis")
    p.add_argument("--manuscript-dir", type=Path, default=PROJECT_ROOT / "manuscript" / "frontiers")
    return p.parse_args()


def save(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path.with_suffix(".jpg"), dpi=300, pil_kwargs={"quality": 95}, bbox_inches="tight")
    plt.close(fig)


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(-0.12, 1.04, label, transform=ax.transAxes, fontsize=12, fontweight="bold", va="bottom")


def wilson(success: int, total: int) -> tuple[float, float]:
    if success == 0:
        return 0.0, float(beta.ppf(0.975, 1, total - success + 1))
    if success == total:
        return float(beta.ppf(0.025, success, 1)), 1.0
    return float(beta.ppf(0.025, success, total - success + 1)), float(beta.ppf(0.975, success + 1, total - success))


def load(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict, dict, dict]:
    features = pd.read_csv(root / "pilot_features.csv")
    clinical = pd.read_csv(root / "clinical_characteristics.csv")
    clinical["case_id"] = clinical["Id"].str.split("_").str[0].astype(str)
    features["case_id"] = features["case_id"].astype(str)
    report = json.loads((root / "pilot_report.json").read_text())
    adjusted = json.loads((root / "adjusted_association.json").read_text())
    next_gate = json.loads((root / "next_gate_report.json").read_text())
    return features, clinical, report, adjusted, next_gate


def attach_labels(features: pd.DataFrame, report: dict) -> pd.DataFrame:
    out = features.copy()
    for split in ["train", "val"]:
        labels = np.asarray(report["cluster_results"]["volume"]["candidates"]["3"][f"{split}_labels"])
        idx = out.index[out["split"] == split]
        if len(idx) != len(labels):
            raise ValueError(f"label length mismatch for {split}")
        out.loc[idx, "cluster"] = labels
    out["cluster"] = out["cluster"].astype(int)
    return out


def figure1(root: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set_axis_off()
    labels = [
        ("TOM500", "500 orbital MRI cases"),
        ("MRI + masks", "9 annotated tissues"),
        ("Patient-level volumes", "physical volume + fraction"),
        ("Fixed split", "400 train / 100 validation"),
        ("CAS characterization", "unadjusted + adjusted sensitivity"),
    ]
    xs = np.linspace(0.10, 0.90, len(labels))
    for i, (title, subtitle) in enumerate(labels):
        box = FancyBboxPatch((xs[i] - 0.075, 0.34), 0.15, 0.32, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor="#F5F6F3", edgecolor="#3B4A54", linewidth=1.2)
        ax.add_patch(box)
        ax.text(xs[i], 0.53, title, ha="center", va="center", fontsize=10, fontweight="bold", color="#263238")
        ax.text(xs[i], 0.43, subtitle, ha="center", va="center", fontsize=8, color="#52616B")
        if i < len(labels) - 1:
            arrow = FancyArrowPatch((xs[i] + 0.08, 0.50), (xs[i + 1] - 0.08, 0.50), arrowstyle="-|>", mutation_scale=14, linewidth=1.3, color="#7A8A93")
            ax.add_patch(arrow)
    ax.text(0.5, 0.86, "Patient-level multi-tissue orbital MRI phenotype analysis", ha="center", fontsize=13, fontweight="bold", color="#263238")
    ax.text(0.5, 0.10, "The validation partition is used for frozen-centroid assignment, not external validation.", ha="center", fontsize=8.5, color="#65747C")
    save(fig, root / "Figure1_workflow")


def figure2(root: Path, data: pd.DataFrame) -> None:
    train = data[data["split"] == "train"].copy()
    cols = [f"{t}_volume_mm3" for t in TISSUES] + [f"{t}_fraction" for t in TISSUES]
    z = train[cols].astype(float)
    z = (z - z.mean()) / z.std(ddof=0)
    means = z.assign(cluster=train["cluster"].values).groupby("cluster")[cols].mean().loc[[0, 1, 2]]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), gridspec_kw={"width_ratios": [1.4, 1]})
    im = axes[0].imshow(means.to_numpy(), aspect="auto", cmap="RdBu_r", vmin=-2.0, vmax=2.0)
    axes[0].set_yticks(range(3), [CLUSTER_NAMES[i] for i in range(3)])
    axes[0].set_xticks(range(len(cols)), [t for t in TISSUES] + [f"{t}\nfraction" for t in TISSUES], rotation=70, ha="right", fontsize=7)
    axes[0].axvline(8.5, color="#FFFFFF", linewidth=1.5)
    axes[0].set_title("Cluster feature profiles", fontsize=10)
    axes[0].set_xlabel("Tissue volume and fraction features")
    fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04, label="Train-set standardized mean")
    for c in range(3):
        axes[1].plot(range(len(TISSUES)), means.iloc[c, :9], marker="o", color=COLORS[c], linewidth=2, label=f"{CLUSTER_NAMES[c]} (n={(train.cluster == c).sum()})")
    axes[1].set_xticks(range(len(TISSUES)), TISSUES)
    axes[1].set_ylabel("Standardized physical volume")
    axes[1].set_title("Multi-tissue volume profiles", fontsize=10)
    axes[1].axhline(0, color="#AAB4B8", linewidth=0.8)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", alpha=0.25)
    add_panel_label(axes[0], "A")
    add_panel_label(axes[1], "B")
    fig.suptitle("Volume-led multi-tissue phenotype", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, root / "Figure2_phenotype_profiles")


def figure3(root: Path, data: pd.DataFrame, clinical: pd.DataFrame) -> None:
    merged = data[["case_id", "split", "cluster"]].merge(clinical[["case_id", "CAS"]], on="case_id", validate="one_to_one")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})
    rng = np.random.default_rng(20261019)
    for j, split in enumerate(["train", "val"]):
        subset = merged[merged.split == split]
        for c in range(3):
            vals = subset.loc[subset.cluster == c, "CAS"].to_numpy(float)
            x = np.full(len(vals), c, dtype=float) + rng.uniform(-0.10, 0.10, size=len(vals))
            axes[0].scatter(x, vals, s=12 if split == "train" else 20, alpha=0.25 if split == "train" else 0.55, color=COLORS[c], edgecolors="none", marker="o" if split == "train" else "D")
            axes[0].plot([c - 0.18, c + 0.18], [np.median(vals), np.median(vals)], color="#1D272C", linewidth=2)
        if split == "train":
            axes[0].text(0.02, 0.96, "Train", transform=axes[0].transAxes, fontsize=9, color="#52616B")
        else:
            axes[0].text(0.02, 0.90, "Validation partition", transform=axes[0].transAxes, fontsize=9, color="#52616B")
    axes[0].set_xticks(range(3), [CLUSTER_NAMES[i] for i in range(3)])
    axes[0].set_ylabel("Clinical Activity Score (CAS)")
    axes[0].set_title("CAS distributions by cluster", fontsize=10)
    axes[0].set_ylim(-0.5, 6.5)
    axes[0].grid(axis="y", alpha=0.25)
    for j, split in enumerate(["train", "val"]):
        subset = merged[merged.split == split]
        rates = []
        lows = []
        highs = []
        for c in range(3):
            vals = subset.loc[subset.cluster == c, "CAS"].to_numpy(float)
            success = int((vals >= 3).sum())
            low, high = wilson(success, len(vals))
            rates.append(success / len(vals))
            lows.append(rates[-1] - low)
            highs.append(high - rates[-1])
        x = np.arange(3) + (j - 0.5) * 0.18
        axes[1].errorbar(x, rates, yerr=[lows, highs], fmt="o", capsize=3, linewidth=1.3, markersize=5, color="#334E68" if j == 0 else "#C76D3A", label="Train" if j == 0 else "Validation partition")
    axes[1].set_xticks(range(3), [CLUSTER_NAMES[i] for i in range(3)])
    axes[1].set_ylabel("CAS >= 3 proportion")
    axes[1].set_ylim(0, 0.75)
    axes[1].set_title("Exploratory active-CAS rates", fontsize=10)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", alpha=0.25)
    add_panel_label(axes[0], "A")
    add_panel_label(axes[1], "B")
    fig.suptitle("CAS-linked clinical characterization", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, root / "Figure3_cas_characterization")


def figure4(root: Path, report: dict, adjusted: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={"width_ratios": [1.15, 1]})
    labels = []
    aris = []
    for name in ["standard", "robust"]:
        labels.append(name.capitalize())
        aris.append(report["scaling_sensitivity"][name]["bootstrap_ari"]["mean"])
    for name in ["volume_mm3_only", "fraction_only", "combined"]:
        labels.append(name.replace("_", " ").title())
        aris.append(report["feature_family_sensitivity"][name]["bootstrap_ari"]["mean"])
    x = np.arange(len(labels))
    axes[0].bar(x, aris, color=["#5B8E7D", "#5B8E7D", "#2F5D7E", "#2F5D7E", "#C76D3A"], edgecolor="#263238", linewidth=0.4)
    axes[0].set_xticks(x, labels, rotation=35, ha="right", fontsize=8)
    axes[0].set_ylabel("Bootstrap ARI mean")
    axes[0].set_ylim(0, 1.05)
    axes[0].set_title("Sensitivity of 3-cluster stability", fontsize=10)
    axes[0].grid(axis="y", alpha=0.25)
    names = []
    estimates = []
    lows = []
    highs = []
    for split in ["train", "validation"]:
        block = adjusted[split]["cas_continuous_ols"]["cluster_effects"]
        for cluster in ["cluster_1", "cluster_2"]:
            names.append(f"{split.title()} {cluster[-1]}")
            estimates.append(block[cluster]["estimate"])
            lows.append(block[cluster]["ci95_low"])
            highs.append(block[cluster]["ci95_high"])
    y = np.arange(len(names))
    axes[1].axvline(0, color="#6B7780", linewidth=0.8)
    axes[1].errorbar(estimates, y, xerr=[np.asarray(estimates) - np.asarray(lows), np.asarray(highs) - np.asarray(estimates)], fmt="o", color="#334E68", ecolor="#334E68", capsize=3)
    axes[1].set_yticks(y, names, fontsize=8)
    axes[1].set_xlabel("Adjusted CAS difference vs Cluster 0")
    axes[1].set_title("Covariate-adjusted CAS association\n(age, sex, smoking, disease duration)", fontsize=10)
    axes[1].grid(axis="x", alpha=0.25)
    add_panel_label(axes[0], "A")
    add_panel_label(axes[1], "B")
    fig.suptitle("Robustness and validation boundary", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, root / "Figure4_robustness_adjustment")


def tables(root: Path, data: pd.DataFrame, clinical: pd.DataFrame, report: dict, adjusted: dict) -> None:
    merged = data[["case_id", "split", "cluster"]].merge(clinical, on="case_id", validate="one_to_one")
    for column in ["CAS", "Age", "SmokingIndex", "DiseaseDuration"]:
        merged[column] = pd.to_numeric(merged[column], errors="coerce")
    rows = []
    for split in ["train", "val"]:
        for c in range(3):
            sub = merged[(merged.split == split) & (merged.cluster == c)]
            rows.append({"split": split, "cluster": c, "n": len(sub), "CAS_median": sub.CAS.median(), "CAS_IQR_low": sub.CAS.quantile(0.25), "CAS_IQR_high": sub.CAS.quantile(0.75), "Age_median": sub.Age.median(), "SmokingIndex_median": sub.SmokingIndex.median(), "DiseaseDuration_median": sub.DiseaseDuration.median(), "Male_n": int((sub.Sex == "M").sum()), "Male_pct": float((sub.Sex == "M").mean() * 100), "CAS_ge_3_n": int((sub.CAS >= 3).sum()), "CAS_ge_3_pct": float((sub.CAS >= 3).mean() * 100)})
    pd.DataFrame(rows).to_csv(root / "Table1_clinical_by_cluster.csv", index=False)
    sensitivity = []
    for name, block in report["scaling_sensitivity"].items():
        sensitivity.append({"analysis": f"scaling:{name}", "ARI_to_base": block["ari_to_base"], "bootstrap_ARI_mean": block["bootstrap_ari"]["mean"], "bootstrap_ARI_95_low": block["bootstrap_ari"]["q025"], "bootstrap_ARI_95_high": block["bootstrap_ari"]["q975"], "validation_CAS_p": block["val_cas"]["kruskal"]["p"]})
    for name, block in report["feature_family_sensitivity"].items():
        sensitivity.append({"analysis": f"feature:{name}", "ARI_to_base": block["ari_to_base"], "bootstrap_ARI_mean": block["bootstrap_ari"]["mean"], "bootstrap_ARI_95_low": block["bootstrap_ari"]["q025"], "bootstrap_ARI_95_high": block["bootstrap_ari"]["q975"], "validation_CAS_p": block["val_cas"]["kruskal"]["p"]})
    for tissue, block in report["tissue_sensitivity"]["leave_one_tissue"].items():
        sensitivity.append({"analysis": f"leave_one_tissue:{tissue}", "ARI_to_base": block["ari_to_base"], "bootstrap_ARI_mean": np.nan, "bootstrap_ARI_95_low": np.nan, "bootstrap_ARI_95_high": np.nan, "validation_CAS_p": np.nan})
    pd.DataFrame(sensitivity).to_csv(root / "Table2_sensitivity.csv", index=False)
    rows = []
    for split in ["train", "validation"]:
        for outcome, key, measure in [("CAS continuous", "cas_continuous_ols", "estimate"), ("CAS >= 3", "active_cas_ge_3_logistic", "odds_ratio")]:
            block = adjusted[split][key]
            for cluster, effect in block["cluster_effects"].items():
                rows.append({"split": split, "outcome": outcome, "cluster_vs_0": cluster, "measure": measure, "estimate": effect[measure], "CI95_low": effect["ci95_low"], "CI95_high": effect["ci95_high"], "p": effect["p"], "overall_Wald_p": block["cluster_overall"]["p"]})
    pd.DataFrame(rows).to_csv(root / "Table3_adjusted_associations.csv", index=False)


def main() -> None:
    options = args()
    root = options.root
    manuscript_dir = options.manuscript_dir
    tables_dir = PROJECT_ROOT / "manuscript" / "tables"
    manuscript_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    features, clinical, report, adjusted, next_gate = load(root)
    data = attach_labels(features, report)
    figure1(manuscript_dir)
    figure2(manuscript_dir, data)
    figure3(manuscript_dir, data, clinical)
    figure4(manuscript_dir, next_gate, adjusted)
    tables(tables_dir, data, clinical, next_gate, adjusted)
    print("rendered", len(list(manuscript_dir.glob("Figure*.jpg"))), "JPG figures and", len(list(tables_dir.glob("Table*.csv"))), "CSV tables")


if __name__ == "__main__":
    main()
